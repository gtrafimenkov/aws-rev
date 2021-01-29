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

import sys
import logging

import boto3

import awsrev


def main():
    logging.basicConfig(format="%(asctime)s %(levelname)-10s %(message)s")
    s3_client = boto3.client("s3")
    ic = awsrev.IssuesCollector()
    awsrev.check_s3_buckets(s3_client, ic)
    if ic.issues:
        print(f"Issues found: {len(ic.issues)}", file=sys.stderr)
        for error in ic.issues:
            print(f"- {error}", file=sys.stderr)
        sys.exit(10)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()