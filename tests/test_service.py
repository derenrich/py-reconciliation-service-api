import pytest
from pytest import fixture

from py_reconciliation_service_api import build_reconciliation_service


# API endpoints taken from https://reconciliation-api.github.io/testbench/#/
@fixture(scope="module")
def service():
    return build_reconciliation_service("https://wikidata.reconci.link/en/api")


@fixture(scope="module")
def geonames_service():
    return build_reconciliation_service("https://fornpunkt.se/apis/reconciliation/geonames")


@fixture(scope="module")
def globalnames_service():
    return build_reconciliation_service("https://verifier.globalnames.org/api/v1/reconcile")


@fixture(scope="module")
def knolbase_service():
    return build_reconciliation_service("https://ringgaard.com/reconcile/")


@fixture(scope="module")
def eukg_service():
    return build_reconciliation_service("https://openrefine-reconciliation.linkedopendata.eu/en/api")


@fixture(scope="module")
def eol_service():
    return build_reconciliation_service("https://eol.org/api/reconciliation")


@fixture(scope="module")
def binomia_service():
    return build_reconciliation_service("https://api.bionomia.net/reconcile")


def test_trump(service):
    candidates = service.reconcile({"query": "trump", "limit": 5})
    assert len(candidates.result) == 5
    assert candidates.result[0].id == "Q22686"
    assert candidates.result[0].name == "Donald Trump"
    assert candidates.result[0].score == 100.0
    assert candidates.result[0].match is False
    assert candidates.result[0].type[0].id == "Q5"
    assert candidates.result[0].type[0].name == "human"


def test_sf(service):
    candidates = service.reconcile({"query": "sf", "limit": 6})
    assert len(candidates.result) == 6
    assert candidates.result[0].id == "Q62"
    assert candidates.result[0].name == "San Francisco"
    assert candidates.result[0].score == 100.0

    assert candidates.result[1].id == "Q24925"
    assert candidates.result[1].name == "science fiction"

    assert candidates.result[2].id == "Q146682"
    assert candidates.result[2].name == "spontaneous fission"


def test_multiple(service):
    query = [{"query": "trump", "limit": 5}, {"query": "sf", "limit": 6}]
    candidates = service.reconcile_batch(query)
    assert len(candidates) == 2
    assert len(candidates[0].result) == 5
    assert candidates[0].result[0].id == "Q22686"
    assert len(candidates[1].result) == 6
    assert candidates[1].result[0].id == "Q62"


@pytest.mark.asyncio
async def test_async_multiple(service):
    query = [{"query": "trump", "limit": 5}, {"query": "sf", "limit": 6}]
    candidates = await service.reconcile_batch_async(query)
    assert len(candidates) == 2
    assert len(candidates[0].result) == 5
    assert len(candidates[0].result[0].features) == 1
    assert candidates[0].result[0].features[0] is not None
    assert candidates[0].result[0].features[0].id == "all_labels"

    assert candidates[0].result[0].id == "Q22686"
    assert len(candidates[1].result) == 6
    assert candidates[1].result[0].id == "Q62"


def test_geonames(geonames_service):
    candidates = geonames_service.reconcile({"query": "berlin", "limit": 5})
    assert len(candidates.result) == 5
    # geonames returns an int instead of a string? this isn't in spec?
    assert candidates.result[0].id == 2950159
    assert candidates.result[0].name == "Berlin"
    assert candidates.result[0].score == 50.0
    assert candidates.result[0].match is False
    assert candidates.result[0].type[0].id == "Concept"


def test_globalnames(globalnames_service):
    candidates = globalnames_service.reconcile({"query": "Homo sapiens", "limit": 5})
    assert len(candidates.result) == 3
    assert candidates.result[0].id == "7db4f8a2-aafe-56b6-8838-89522c67d9f0"
    assert candidates.result[0].name.startswith("Homo sapiens Linnaeus")


def test_knolbase(knolbase_service):
    candidates = knolbase_service.reconcile({"query": "Battle of inchon", "limit": 1})
    assert len(candidates.result) == 1
    assert candidates.result[0].id == "Q483039"


def test_eukg(eukg_service):
    candidates = eukg_service.reconcile({"query": "Google Canada", "limit": 1})
    assert len(candidates.result) == 1
    assert candidates.result[0].id == "Q4549434"


def test_eol(eol_service):
    candidates = eol_service.reconcile({"query": "Homo sapiens", "limit": 5})
    # Encyclopedia of Life endpoint just ignores the limit query? Returns way more
    # assert len(candidates.result) == 5
    assert candidates.result[0].id == "pages/327955"
    assert candidates.result[0].name == "Homo sapiens Linnaeus 1758"


def test_binomia(binomia_service):
    candidates = binomia_service.reconcile({"query": "Mickley", "limit": 1})
    assert len(candidates.result) == 1
    assert candidates.result[0].id == "0000-0002-5988-5275"
    assert candidates.result[0].name == "James Mickley"
