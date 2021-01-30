# Read-only IAM policy for AWS Revizor

It contains minimal set of permissions.

## Usage example

This terraform code snippet creates the role, an IAM user,
and attaches the role to the user:

```
resource "aws_iam_user" "aws-rev-ro" {
  name = "aws-rev-ro"
}

resource "aws_iam_access_key" "aws-rev-ro" {
  user = aws_iam_user.aws-rev-ro.name
}

module "ro-iam-policy" {
  source = "./ro-iam-policy"
}

resource "aws_iam_user_policy_attachment" "aws-rev-ro" {
  user       = aws_iam_user.aws-rev-ro.name
  policy_arn = module.ro-iam-policy.arn
}

output "aws-rev-ro-access-key-id" {
  value = aws_iam_access_key.aws-rev-ro.id
}

output "aws-rev-ro-access-key-secret" {
  value = aws_iam_access_key.aws-rev-ro.secret
}
```

## License

AGPL v3 or later
