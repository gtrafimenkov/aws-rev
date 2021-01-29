# AWS Revisor

Tool for checking AWS resources for security compliance.

Implemented checks:

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

## License

AGPL v3 or later
