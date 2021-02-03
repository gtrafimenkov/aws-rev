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

KeyInfo = collections.namedtuple("KeyInfo", ["id", "arn"])


def check_cmk(aws_regions, ic: IssuesCollector):
    """Check customer managed CMK for issues."""
    for region in aws_regions:
        logging.info("checking KMS CMK in %s", region)
        client = boto3.client("kms", region_name=region)
        keys = get_all_cmk(client)
        for key in keys:
            if is_customer_managed_key(client, key.id):
                if not is_key_rotation_enabled(client, key.id):
                    ic.add(f"key rotation is not enabled for {key.arn}")


def is_customer_managed_key(client, key_id) -> bool:
    """Check if this key customer managed."""
    resp = client.describe_key(KeyId=key_id)
    return resp["KeyMetadata"]["KeyManager"] == "CUSTOMER"


def is_key_rotation_enabled(client, key_id) -> bool:
    """Check if rotation is enabled for a key."""
    resp = client.get_key_rotation_status(KeyId=key_id)
    return resp["KeyRotationEnabled"]


def get_all_cmk(client) -> typing.List[KeyInfo]:
    """Return list of all customer managed keys."""
    keys = []
    args = {}
    while True:
        resp = client.list_keys(**args)
        keys += [KeyInfo(x["KeyId"], x["KeyArn"]) for x in resp["Keys"]]
        if resp.get("Truncated", False):
            args["Marker"] = resp["NextMarker"]
        else:
            break
    return keys
