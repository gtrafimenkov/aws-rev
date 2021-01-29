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

import unittest

import awsrev.s3_checks


class InsecureTransportPolicyTests(unittest.TestCase):
    def test_no_policy(self):
        self.assertFalse(
            awsrev.s3_checks.does_policy_disallow_insecure_transport("foo", None)
        )
        self.assertFalse(
            awsrev.s3_checks.does_policy_disallow_insecure_transport("foo", {})
        )

    def test_correct_disallow_policy(self):
        policy = {
            "Version": "2012-10-17",
            "Id": "MyBucketPolicy",
            "Statement": [
                {
                    "Sid": "DenyUnSecureCommunications",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "s3:*",
                    "Resource": [
                        "arn:aws:s3:::test-bucket-2",
                        "arn:aws:s3:::test-bucket-2/*",
                    ],
                    "Condition": {"Bool": {"aws:SecureTransport": "false"}},
                }
            ],
        }
        self.assertTrue(
            awsrev.s3_checks.does_policy_disallow_insecure_transport(
                "test-bucket-2", policy
            )
        )

    def test_misconfigured_disallow_policy(self):
        policy = {
            "Version": "2012-10-17",
            "Id": "MyBucketPolicy",
            "Statement": [
                {
                    "Sid": "DenyUnSecureCommunications",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:*",
                    "Resource": [
                        "arn:aws:s3:::test-bucket-2",
                        "arn:aws:s3:::test-bucket-2/*",
                    ],
                    "Condition": {"Bool": {"aws:SecureTransport": "false"}},
                }
            ],
        }
        self.assertFalse(
            awsrev.s3_checks.does_policy_disallow_insecure_transport(
                "test-bucket-2", policy
            )
        )
