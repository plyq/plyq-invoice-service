# plyq-invoice-service
Create the invoice based on the config
![pytest](https://github.com/plyq/plyq-invoice-service/actions/workflows/python-app.yml/badge.svg)
[![codecov](https://codecov.io/gh/plyq/plyq-invoice-service/branch/main/graph/badge.svg?token=2OK4NKDNZG)](https://codecov.io/gh/plyq/plyq-invoice-service)
![Changelog CI](https://github.com/plyq/plyq-invoice-service/actions/workflows/changelog-ci.yml/badge.svg)


## How to run

```bash
pipenv run python ./run.py config/company-a.json
```

It will create a new invoice under the `invoices` dir
