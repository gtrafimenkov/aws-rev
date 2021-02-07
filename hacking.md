# Hacking

## How to setup dev environment

```
python3 -m venv venv-dev
. venv-dev/bin/activate
pip install -r requirements-dev.txt
```

## Before pushing changes or making a pull request

- perform `make check`
- if you added new or modified existing checks, make sure that
  the [minimal IAM policy](./extras/terraform/ro-iam-policy)
  is up to date
