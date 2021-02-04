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

from awsrev import s3_checks


class SSERecommendedConfigTest(unittest.TestCase):
    def test_few_cases(self):
        cases = [
            (
                {
                    "Rules": [
                        {
                            "ApplyServerSideEncryptionByDefault": {
                                "SSEAlgorithm": "aws:kms",
                                "KMSMasterKeyID": "42ebfeb5-be96-4456-b794-123456789012",
                            },
                            "BucketKeyEnabled": False,
                        }
                    ]
                },
                True,
            ),
            (
                {
                    "Rules": [
                        {
                            "ApplyServerSideEncryptionByDefault": {
                                "SSEAlgorithm": "AES256"
                            },
                            "BucketKeyEnabled": False,
                        }
                    ]
                },
                True,
            ),
        ]

        for num, case in enumerate(cases):
            config, expected_result = case
            self.assertEqual(
                s3_checks.is_recommended_sse_configuration(config),
                expected_result,
                msg=f"case {num}",
            )


class InsecureTransportPolicyTests(unittest.TestCase):
    def test_no_policy(self):
        self.assertFalse(s3_checks.does_policy_disallow_insecure_transport("foo", None))
        self.assertFalse(s3_checks.does_policy_disallow_insecure_transport("foo", {}))

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
            s3_checks.does_policy_disallow_insecure_transport("test-bucket-2", policy)
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
            s3_checks.does_policy_disallow_insecure_transport("test-bucket-2", policy)
        )
