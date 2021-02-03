# AWS Revisor

Tool for checking AWS resources for security compliance.

Implemented checks:

- KSM
  - rotation is enabled for user managed customer master keys (CMK)
- S3
  - bucket encryption is enabled
  - bucket versioning is enabled
  - insecure transport is disabled

## Usage

```
python-pip3 install -r requirements.txt
export AWS_PROFILE=xxx
./revizor.py
```

It is possible to limit checks to one or more regions:

```
./revizor.py --regions us-west-1,eu-west-1
```

Global resources are always checked.

The application doesn't create any AWS resources and uses
only read-only API calls.  Minimal IAM policy can be found in
[extras/terraform/ro-iam-policy/](./extras/terraform/ro-iam-policy/).

## License

AGPL v3 or later
