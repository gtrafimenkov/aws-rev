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

import boto3

from awsrev.results import IssuesCollector


def check_iam(ic: IssuesCollector):
    """Check IAM settings."""
    client = boto3.client("iam")
    if not check_root_mfa(client):
        ic.add("MFA is not enabled for the root user")


def check_root_mfa(client):
    resp = client.get_account_summary()
    return resp["SummaryMap"].get("AccountMFAEnabled", 0) == 1
