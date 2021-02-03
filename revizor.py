#!/usr/bin/env python3

###############################################################################
# Copyright (c) 2021 Gennady Trafimenkov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################

import argparse
import logging
import sys

import boto3

import awsrev
import awsrev.kms


def main():

    parser = argparse.ArgumentParser(description="AWS Revizor")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--regions",
        help="Comma separated list of AWS regions to check. "
        "Checking all regions by default.",
    )

    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)-10s %(message)s",
        level=logging.INFO if args.verbose else logging.WARNING,
    )
    s3_client = boto3.client("s3")
    ec2_client = boto3.client("ec2")
    regions = awsrev.get_enabled_regions(ec2_client)
    if args.regions is not None:
        only_regions = [x.strip() for x in args.regions.split(",")]
        regions = sorted(list(set(regions) & set(only_regions)))

    ic = awsrev.IssuesCollector()

    awsrev.kms.check_cmk(regions, ic)

    awsrev.check_s3_buckets(s3_client, ic)
    if ic.issues:
        print(f"Issues found: {len(ic.issues)}")
        for error in ic.issues:
            print(f"- {error}")
        sys.exit(10)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
