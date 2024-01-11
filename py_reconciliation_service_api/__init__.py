from typing import Any, Dict, List, Optional

import httpx

from .models.manifest import Manifest
from .models.reconciliation import (
    BatchReconciliationQuery,
    BatchReconciliationResult,
    ReconciliationQuery,
    ReconciliationResult,
)


class ReconciliationService:
    _base_url: str
    _manifest: Manifest
    _async_client: Optional[httpx.AsyncClient] = None
    _sync_client: Optional[httpx.Client] = None
    _httpx_args: Dict[str, Any]

    def __init__(self, base_url: str, manifest: Manifest, httpx_args: Dict[str, Any] = {}):
        self._base_url = base_url
        self._manifest = manifest
        self._httpx_args = httpx_args

    def _get_sync_client(self) -> httpx.Client:
        if self._sync_client is None:
            self._sync_client = httpx.Client(**self._httpx_args)
        return self._sync_client

    async def _get_async_client(self) -> httpx.AsyncClient:
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(**self._httpx_args)
        return self._async_client

    def reconcile(self, query: ReconciliationQuery) -> ReconciliationResult:
        return self.reconcile_batch([query])[0]

    def reconcile_batch(self, query: List[ReconciliationQuery]) -> List[ReconciliationResult]:
        queries = {f"q{i}": q for i, q in enumerate(query)}
        client = self._get_sync_client()
        batch_query = BatchReconciliationQuery.model_validate(queries)
        batch_query_json = batch_query.model_dump_json(exclude_none=True)
        resp = client.post(self._base_url, data={"queries": batch_query_json})
        if resp.status_code != 200:
            raise Exception(f"Could not reconcile batch: {resp.status_code} {resp.text}")
        batch_result = BatchReconciliationResult.model_validate(resp.json())
        out = []
        for i in range(len(query)):
            if f"q{i}" not in batch_result.root:
                raise Exception(f"Missing result for query q{i}")
            out.append(batch_result.root[f"q{i}"])
        return out


def build_reconciliation_service(base_url: str, *, httpx_args: Dict[str, Any] = {}) -> "ReconciliationService":
    client = httpx.Client(**httpx_args)

    manifest_resp = client.get(base_url)
    if manifest_resp.status_code != 200:
        raise Exception(f"Could not fetch manifest from {base_url}: {manifest_resp.status_code} {manifest_resp.text}")

    if manifest_resp.headers.get("content-type") != "application/json":
        raise Exception(
            f"Manifest from {base_url} has unexpected content type: {manifest_resp.headers.get('content-type')}"
        )

    manifest = Manifest.model_validate(manifest_resp.json())

    if "0.2" not in manifest.versions:
        raise Exception(f"Manifest from {base_url} has no version 0.2. Only supports versions {manifest.versions}")

    return ReconciliationService(base_url, manifest)
