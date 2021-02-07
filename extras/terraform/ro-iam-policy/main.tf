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

resource "aws_iam_policy" "aws-rev-ro" {
  name        = "aws-rev-ro"
  path        = "/"
  description = "Read only access for AWS Revizor"

  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3Access",
            "Effect": "Allow",
            "Action": [
                "s3:GetBucketPolicy",
                "s3:GetBucketVersioning",
                "s3:GetEncryptionConfiguration",
                "s3:ListAllMyBuckets"
            ],
            "Resource": "*"
        },
        {
            "Sid": "EC2Access",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeRegions"
            ],
            "Resource": "*"
        },
        {
            "Sid": "IAMAccess",
            "Effect": "Allow",
            "Action": [
                "iam:GetAccountSummary",
                "iam:GetLoginProfile",
                "iam:ListMFADevices",
                "iam:ListUsers"
            ],
            "Resource": "*"
        },
        {
            "Sid": "KMSAccess",
            "Effect": "Allow",
            "Action": [
                "kms:DescribeKey",
                "kms:GetKeyRotationStatus",
                "kms:ListKeys"
            ],
            "Resource": "*"
        }
    ]
}
POLICY
}
