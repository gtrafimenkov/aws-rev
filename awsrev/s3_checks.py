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

import logging
import json

import botocore

from awsrev.results import IssuesCollector


def check_s3_buckets(s3_client, ic: IssuesCollector):
    resp = s3_client.list_buckets()
    buckets = [x["Name"] for x in resp["Buckets"]]
    for b in buckets:
        check_bucket_sse(s3_client, b, ic)
        check_bucket_versioning(s3_client, b, ic)
        check_for_insecure_transport(s3_client, b, ic)


def check_bucket_sse(s3_client, bucket_name, ic: IssuesCollector):
    """Check that the bucket has server-side encryption enabled."""
    try:
        resp = s3_client.get_bucket_encryption(Bucket=bucket_name)
        if not is_recommended_sse_configuration(
            resp["ServerSideEncryptionConfiguration"]
        ):
            ic.add(f"not recommended SSE encryption for S3 bucket {bucket_name}")
    except botocore.exceptions.ClientError as e:
        if "ServerSideEncryptionConfigurationNotFoundError" in str(e):
            ic.add(f"no server-side encryption for S3 bucket {bucket_name}")
        else:
            logging.error("Unexpected error during S3 buckets check: %s", str(e))
            raise e


def is_recommended_sse_configuration(config) -> bool:
    """Check is server side encryption configuration for recommended
    values."""
    try:
        alg = config["Rules"][0]["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"]
        return alg in ["aws:kms", "AES256"]
    except KeyError:
        return False


def check_bucket_versioning(s3_client, bucket_name, ic: IssuesCollector):
    """Check that the bucket has versioning enabled."""
    resp = s3_client.get_bucket_versioning(Bucket=bucket_name)
    if resp.get("Status", "") != "Enabled":
        ic.add(f"no versioning on S3 bucket {bucket_name}")


def check_for_insecure_transport(s3_client, bucket_name, ic: IssuesCollector):
    """Check that insecure transport is not allowed for the bucket."""
    policy = get_bucket_policy(s3_client, bucket_name)
    if not does_policy_disallow_insecure_transport(bucket_name, policy):
        ic.add(f"insecure transport allowed for S3 bucket {bucket_name}")


def get_bucket_policy(s3_client, bucket_name) -> dict:
    """Return bucket's policy or None if there is no policy."""
    try:
        resp = s3_client.get_bucket_policy(Bucket=bucket_name)
        return json.loads(resp["Policy"])
    except botocore.exceptions.ClientError as e:
        if "NoSuchBucketPolicy" in str(e):
            return None
        logging.error("Unexpected error when getting S3 bucket policy: %s", str(e))
        raise e


def does_policy_disallow_insecure_transport(bucket_name, policy) -> bool:
    if policy is None:
        return False
    condition = {"Bool": {"aws:SecureTransport": "false"}}
    resources = [
        f"arn:aws:s3:::{bucket_name}",
        f"arn:aws:s3:::{bucket_name}/*",
    ]
    for statement in policy.get("Statement", []):
        if (
            statement["Effect"] == "Deny"
            and statement["Principal"] == "*"
            and statement["Action"] == "s3:*"
            and sorted(statement["Resource"]) == sorted(resources)
            and statement["Condition"] == condition
        ):
            return True
    return False
