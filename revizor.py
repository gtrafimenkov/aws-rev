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
import awsrev.iam
import awsrev.kms
import awsrev.regions
import awsrev.results
import awsrev.s3


def main():

    check_groups = sorted(["iam", "kms", "s3"])

    parser = argparse.ArgumentParser(description="AWS Revizor")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--regions",
        help="Comma separated list of AWS regions to check. "
        "Checking all regions by default.",
    )
    parser.add_argument(
        "--groups",
        help="Comma separated list of checks to perform. "
        "By default doing all checks. "
        f"Possible values: {','.join(check_groups)}",
    )

    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)-10s %(message)s",
        level=logging.INFO if args.verbose else logging.WARNING,
    )
    ec2_client = boto3.client("ec2")
    regions = awsrev.regions.get_enabled_regions(ec2_client)
    if args.regions is not None:
        only_regions = [x.strip() for x in args.regions.split(",")]
        regions = sorted(list(set(regions) & set(only_regions)))

    allowed_groups = check_groups
    if args.groups is not None:
        supplied = [x.strip() for x in args.groups.split(",")]
        for group in supplied:
            if group not in check_groups:
                logging.error("Unknown check group '%s'", group)
                sys.exit(1)
        allowed_groups = sorted(list(set(allowed_groups) & set(supplied)))
        logging.info(
            "checking %d group(s): %s", len(allowed_groups), ",".join(allowed_groups)
        )

    ic = awsrev.results.IssuesCollector()

    checks = [
        ("iam", lambda: awsrev.iam.check_iam(ic)),
        ("kms", lambda: awsrev.kms.check_cmk(regions, ic)),
        ("s3", lambda: awsrev.s3.check_buckets(ic)),
    ]

    for group, checker in checks:
        if group in allowed_groups:
            checker()

    if ic.issues:
        print(f"Issues found: {len(ic.issues)}")
        for error in sorted(ic.issues):
            print(f"- {error}")
        sys.exit(10)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
