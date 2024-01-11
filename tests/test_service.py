from py_reconciliation_service_api import build_reconciliation_service
from pytest import fixture


@fixture(scope="module")
def service():
    return build_reconciliation_service("https://wikidata.reconci.link/en/api")


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
    query = [
        {"query": "trump", "limit": 5},
        {"query": "sf", "limit": 6}
    ]
    candidates = service.reconcile_batch(query)
    assert len(candidates) == 2
    assert len(candidates[0].result) == 5
    assert candidates[0].result[0].id == "Q22686"
    assert len(candidates[1].result) == 6
    assert candidates[1].result[0].id == "Q62"
