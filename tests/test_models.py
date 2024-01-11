from py_reconciliation_service_api.models.manifest import Manifest


# from https://wikidata.reconci.link/en/api
EXAMPLE_MANIFEST = """
{"defaultTypes":[{"id":"Q35120","name":"entity"}],"extend":{"property_settings":[{"default":0,"help_text":"Maximum number of values to return per row (0 for no limit)","label":"Limit","name":"limit","type":"number"},{"choices":[{"name":"Any rank","value":"any"},{"name":"Only the best rank","value":"best"},{"name":"Preferred and normal ranks","value":"no_deprecated"}],"default":"best","help_text":"Filter statements by rank","label":"Ranks","name":"rank","type":"select"},{"choices":[{"name":"Any statement","value":"any"},{"name":"At least one reference","value":"referenced"},{"name":"At least one non-wiki reference","value":"no_wiki"}],"default":"any","help_text":"Filter statements by their references","label":"References","name":"references","type":"select"},{"default":false,"help_text":"The number of values will be returned.","label":"Return counts instead of values","name":"count","type":"checkbox"}],"propose_properties":{"service_path":"/en/propose_properties","service_url":"https://wikidata.reconci.link"}},"identifierSpace":"http://www.wikidata.org/entity/","name":"Wikidata reconci.link (en)","preview":{"height":100,"url":"https://wikidata.reconci.link/en/preview?id={{id}}","width":400},"schemaSpace":"http://www.wikidata.org/prop/direct/","suggest":{"entity":{"service_path":"/en/suggest/entity","service_url":"https://wikidata.reconci.link"},"property":{"service_path":"/en/suggest/property","service_url":"https://wikidata.reconci.link"},"type":{"service_path":"/en/suggest/type","service_url":"https://wikidata.reconci.link"}},"versions":["0.1","0.2"],"view":{"url":"https://www.wikidata.org/wiki/{{id}}"}}
"""


def test_manifest():
    manifest = Manifest.model_validate_json(EXAMPLE_MANIFEST)
    assert manifest.name == "Wikidata reconci.link (en)"
    assert '0.2' in manifest.versions
