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

import collections
import logging
import typing

import boto3

from awsrev.results import IssuesCollector

UserInfo = collections.namedtuple("UserInfo", ["name", "id", "arn"])


def check_iam(ic: IssuesCollector):
    """Check IAM settings."""
    client = boto3.client("iam")
    if not check_root_mfa(client):
        ic.add("MFA is not enabled for the root user")

    users = get_users(client)
    for user in users:
        logging.info("checking user %s", user.name)
        login_profile = get_user_login_profile(client, user.name)
        if login_profile:
            # the user has a console password
            # checking that he/she has an MFA device enabled
            if not does_user_have_mfa(client, user.name):
                ic.add(f"MFA is not enabled for user {user.arn}")


def check_root_mfa(client):
    resp = client.get_account_summary()
    return resp["SummaryMap"].get("AccountMFAEnabled", 0) == 1


def get_users(client) -> typing.List[UserInfo]:
    """Return list of users."""
    users = []
    args = {}
    while True:
        resp = client.list_users(**args)
        users += [UserInfo(x["UserName"], x["UserId"], x["Arn"]) for x in resp["Users"]]
        if resp.get("Truncated", False):
            args["Marker"] = resp["NextMarker"]
        else:
            break
    return users


def get_user_login_profile(client, user_name):
    """Return's user login profile or None if there is none."""
    try:
        resp = client.get_login_profile(UserName=user_name)
        return resp["LoginProfile"]
    except client.exceptions.NoSuchEntityException:
        return None


def does_user_have_mfa(client, user_name) -> bool:
    """Check if the user has an MFA device enabled."""
    # If list_mfa_devices returns anything, then the user has enabled MFA.
    return len(get_user_mfa_devices(client, user_name)) > 0


def get_user_mfa_devices(client, user_name):
    """Get list of MFA devices of the given user.  There might be maximum of 1 device."""
    devices = []
    args = {}
    while True:
        resp = client.list_mfa_devices(UserName=user_name, **args)
        devices += resp["MFADevices"]
        if resp.get("Truncated", False):
            args["Marker"] = resp["NextMarker"]
        else:
            break
    return devices
