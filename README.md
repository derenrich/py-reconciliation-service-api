Python Reconciliation Service API
=================================

This is a python implementation of the [Reconciliation Service API v0.2](https://w3c.github.io/cg-reports/reconciliation/CG-FINAL-specs-0.2-20230410/).

It does not support all methods or utilities of the API including authentication.


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