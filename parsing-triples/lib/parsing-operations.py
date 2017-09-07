import re
from textwrap import dedent

def find_ontology_uri(label, **kwargs):
    URI = {"patient": "<http://patient>",
            "male": "<http://male_gender>",
            "female": "<http://female_gender>",
            "birth_date": "<http://birth_date>"}

    # print URI[label]
    if label in URI.keys():
        return URI[label]



def find_entity_uri(entity, **kwargs):
    if len(str(entity).strip()) < 1: return

    uri = ""
    templates = {
        "patient_id": "<patient/{patient_id}>",
        "gender": "<patient/{patient_id}/gender/{gender}>"}

    if entity in templates.keys():
        uri = templates[entity]
        uri = uri.format(**kwargs)
        # for f in uri._formatter_field_name_split(): print f
        # for f in uri._formatter_field_name_split(): print f

    return uri


def make_triple(field):
    triples = {"patient_id": "<<patient_id>>",
               "gender": "<gender>",
               "birth_date": "<birth_date>"}

    triples = {"patient_id": "<<patient_id>>",
               "gender": "<gender>",
               "birth_date": "<birth_date>"}



def parse_uri(string, **kwargs):
    matches = re.findall(r"<<.*?>>", string)
    if matches:
        for m in matches:
            label = str(m).replace("<<", "").replace(">>", "")
            uri = find_ontology_uri(label, **kwargs)
            string = re.sub(m, uri, string)

    matches = re.findall(r"<!.*?>>", string)
    if matches:
        for m in matches:
            entity = str(m).replace("<!", "").replace(">>", "")
            uri = find_entity_uri(entity, **kwargs)
            string = re.sub(m, uri, string)

    return string


def triplify(string, **kwargs):
    string = parse_uri(string, **kwargs)
    return dedent(string)
