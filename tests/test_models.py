from py_reconciliation_service_api.models.manifest import Manifest
from py_reconciliation_service_api.models.reconciliation import BatchReconciliationQuery, BatchReconciliationResult


# from https://wikidata.reconci.link/en/api
EXAMPLE_MANIFEST = """
{"defaultTypes":[{"id":"Q35120","name":"entity"}],"extend":{"property_settings":[{"default":0,"help_text":"Maximum number of values to return per row (0 for no limit)","label":"Limit","name":"limit","type":"number"},{"choices":[{"name":"Any rank","value":"any"},{"name":"Only the best rank","value":"best"},{"name":"Preferred and normal ranks","value":"no_deprecated"}],"default":"best","help_text":"Filter statements by rank","label":"Ranks","name":"rank","type":"select"},{"choices":[{"name":"Any statement","value":"any"},{"name":"At least one reference","value":"referenced"},{"name":"At least one non-wiki reference","value":"no_wiki"}],"default":"any","help_text":"Filter statements by their references","label":"References","name":"references","type":"select"},{"default":false,"help_text":"The number of values will be returned.","label":"Return counts instead of values","name":"count","type":"checkbox"}],"propose_properties":{"service_path":"/en/propose_properties","service_url":"https://wikidata.reconci.link"}},"identifierSpace":"http://www.wikidata.org/entity/","name":"Wikidata reconci.link (en)","preview":{"height":100,"url":"https://wikidata.reconci.link/en/preview?id={{id}}","width":400},"schemaSpace":"http://www.wikidata.org/prop/direct/","suggest":{"entity":{"service_path":"/en/suggest/entity","service_url":"https://wikidata.reconci.link"},"property":{"service_path":"/en/suggest/property","service_url":"https://wikidata.reconci.link"},"type":{"service_path":"/en/suggest/type","service_url":"https://wikidata.reconci.link"}},"versions":["0.1","0.2"],"view":{"url":"https://www.wikidata.org/wiki/{{id}}"}}
"""


def test_manifest():
    manifest = Manifest.model_validate_json(EXAMPLE_MANIFEST)
    assert manifest.name == "Wikidata reconci.link (en)"
    assert '0.2' in manifest.versions


SIMPLE_EXAMPLE_QUERY = """
{
  "q1": {
    "query": "Hans-Eberhard Urbaniak"
  },
  "q2": {
    "query": "Ernst Schwanhold"
  }
}
"""


def test_simple_query():
    query = BatchReconciliationQuery.model_validate_json(SIMPLE_EXAMPLE_QUERY)
    assert len(query.root) == 2
    assert query.root['q1'].query == "Hans-Eberhard Urbaniak"
    assert query.root['q2'].query == "Ernst Schwanhold"


EXAMPLE_QUERY = """
{"q0": {"query": "Christel Hanewinckel", "type": "DifferentiatedPerson", "limit": 5, "properties": [{"pid": "professionOrOccupation", "v": ["Politik*",{"id": "wissenschaftler","name": "Wissenschaftler(in)"}]}],"type_strict": "should"}}
"""


def test_array_property_value_query():
    query = BatchReconciliationQuery.model_validate_json(EXAMPLE_QUERY)
    assert len(query.root) == 1
    assert query.root['q0'].type == "DifferentiatedPerson"
    assert query.root['q0'].limit == 5
    assert query.root['q0'].query == "Christel Hanewinckel"
    assert query.root['q0'].properties[0].v[0] == "Politik*"
    assert query.root['q0'].properties[0].v[1].name == "Wissenschaftler(in)"


COMPLEX_EXAMPLE_QUERY = """
{
  "q0": {
    "query": "Christel Hanewinckel",
    "type": "DifferentiatedPerson",
    "limit": 5,
    "properties": [
      {
        "pid": "professionOrOccupation",
        "v": "Politik*"
      },
      {
        "pid": "affiliation",
        "v": "http://d-nb.info/gnd/2022139-3"
      }
    ],
    "type_strict": "should"
  },
  "q1": {
    "query": "Franz Thönnes",
    "type": "DifferentiatedPerson",
    "limit": 5,
    "properties": [
      {
        "pid": "professionOrOccupation",
        "v": "Politik*"
      },
      {
        "pid": "affiliation",
        "v": "http://d-nb.info/gnd/2022139-3"
      }
    ],
    "type_strict": "any"
  }
}
"""


def test_complex_query():
    query = BatchReconciliationQuery.model_validate_json(COMPLEX_EXAMPLE_QUERY)
    assert len(query.root) == 2
    assert query.root['q0'].type == "DifferentiatedPerson"
    assert query.root['q0'].limit == 5
    assert query.root['q0'].query == "Christel Hanewinckel"
    assert query.root['q0'].properties[0].v == "Politik*"
    assert query.root['q0'].properties[1].v == "http://d-nb.info/gnd/2022139-3"
    assert query.root['q1'].type == "DifferentiatedPerson"
    assert query.root['q1'].limit == 5
    assert query.root['q1'].query == "Franz Thönnes"
    assert query.root['q1'].properties[0].v == "Politik*"
    assert query.root['q1'].properties[1].v == "http://d-nb.info/gnd/2022139-3"
    assert query.root['q0'].type_strict == "should"
    assert query.root['q1'].type_strict == "any"


def test_batch_reconciliation_result():
    json = open("tests/batch_reconciliation_result.json", "r").read()
    result = BatchReconciliationResult.model_validate_json(json)
    assert len(result.root) == 2
    assert len(result.root['q1'].result) == 2
    assert len(result.root['q2'].result) == 2

    assert len(result.root['q2'].result[1].type) == 2
    assert result.root['q2'].result[1].match is False
    assert result.root['q2'].result[1].name == "Schwanhold, Nadine"
