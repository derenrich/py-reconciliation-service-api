Python Reconciliation Service API
=================================

This is a python implementation of the [Reconciliation Service API v0.2](https://w3c.github.io/cg-reports/reconciliation/CG-FINAL-specs-0.2-20230410/). It is [available on pypi](https://pypi.org/project/py-reconciliation-service-api/).

It does not support all methods or utilities of the API including authentication. 


![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-reconciliation-service-api)
![PyPI - Format](https://img.shields.io/pypi/format/py-reconciliation-service-api)
[![PyPI - License](https://img.shields.io/pypi/l/py-reconciliation-service-api.svg)](https://pypi.python.org/pypi/py-reconciliation-service-api/)

Usage
-----

Here is a basic usage example

```python
from py_reconciliation_service_api import build_reconciliation_service

# the standard location of the wikidata implementation of this API
SERVICE_URL = "https://wikidata.reconci.link/en/api"
service = build_reconciliation_service(SERVICE_URL)

# get 6 candidates for the string "sf"
candidates = service.reconcile({"query": "sf", "limit": 6})
assert len(candidates.result) == 6
# the top result should be called San Francisco
assert candidates.result[0].name == "San Francisco"

```