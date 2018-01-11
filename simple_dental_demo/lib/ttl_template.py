# coding=utf-8
from textwrap import dedent

def ttl_prefixes(base="", ontology_uri=""):
    # specify the base uri
    if base.strip() == "":
        base = "http://purl.obolibrary.org/obo/simple-dental-ontology.owl"

    # create uri for ontology
    if ontology_uri.strip() == "":
        ontology_uri = "http://purl.obolibrary.org/obo/simple-dental-ontology.owl/translate.owl"

    ttl = dedent("""\
        # axioms for prefixes
        @prefix dc: <http://purl.org/dc/elements/1.1/> .
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix swrl: <http://www.w3.org/2003/11/swrl#> .
        @prefix swrla: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
        @prefix swrlb: <http://www.w3.org/2003/11/swrlb#> .
        @prefix xml: <http://www.w3.org/XML/1998/namespace> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        
        # custom prefixes
        @base <{0}/> .
        @prefix : <http://purl.obolibrary.org/obo/simple-dental-ontology.owl/> . 
        
        # ontology uri
        <{1}> rdf:type owl:Ontology .
        
        """.format(base, ontology_uri))
    return ttl


def ttl_declare_individual(uri, class_uri, label=""):
    ttl = dedent("""{0} rdf:type owl:NamedInvidual, {1} .\n""".format(uri, class_uri))
    if len(label.strip()) > 0:
        ttl += """{0} rdfs:label "{1}" .\n""".format(uri, label)
    return ttl


def ttl_declare_class(class_uri, label=""):
    ttl = """{0} rdf:type owl:Class .\n""".format(class_uri)
    if len(label.strip()) > 0:
        ttl += """{0} rdfs:label "{1}" .\n""".format(class_uri, label)

    return ttl


def ttl_triple(subj, pred, obj):
    return """{0} {1} {2} .\n""".format(subj, pred, obj)


def ttl_part_of(uri1, uri2):
    return ttl_triple(uri1, ":part_of", uri2)


def ttl_has_part(uri1, uri2):
    return ttl_triple(uri1, ":has_part", uri2)


def ttl_has_quality(uri1, uri2):
    return ttl_triple(uri1, ":has_quality", uri2)


def ttl_quality_of(uri1, uri2):
    return ttl_triple(uri1, ":quality_of", uri2)


def ttl_has_participant(uri1, uri2):
    return ttl_triple(uri1, ":has_participant", uri2)


def ttl_participates_in(uri1, uri2):
    return ttl_triple(uri1, ":participates_in", uri2)


def ttl_is_about(uri1, uri2):
    return ttl_triple(uri1, ":is_about", uri2)


def ttl_birth_date(patient_uri, dob):
    dob = """"{0}"^^xsd:date""".format(str(dob))
    return ttl_triple(patient_uri, ":birth_date", dob)


def ttl_service_date(procedure_uri, srv_date):
    srv_date = """"{0}"^^xsd:date""".format(str(srv_date))
    return ttl_triple(procedure_uri, ":service_date", srv_date)


def ttl_patient_uri(patient_id):
    return """<patient/{0}>""".format(str(patient_id))


def ttl_provider_uri(provider_id):
    return """<provider/{0}>""".format(str(provider_id))


def ttl_procedure_uri(service_id):
    return """<procedure/{0}>""".format(str(service_id))


def ttl_material_uri(service_code, service_id):
    return """<material/{0}/{1}>""".format(service_code, str(service_id))


def ttl_material_class_uri(service_code):
    service_code = service_code.lower()

    # amalgam procedures: d2140, d2150, d2160, d2161
    if service_code[0:3] == "d21":
        return ":amalagam"
    #resin procedures: d2330, d2331, d2332, d2335
    elif service_code[0:3] == "d23":
        return ":resin"
    else:
        return ":restoration_material"


def ttl_material_name(service_code):
    service_code = service_code.lower()

    # amalgam procedures: d2140, d2150, d2160, d2161
    if service_code[0:3] == "d21":
        return "amalagam"
    #resin procedures: d2330, d2331, d2332, d2335
    elif service_code[0:3] == "d23":
        return "resin"
    else:
        return "restoration_material"


def ttl_service_code_uri(service_id, service_code):
    return """<procedure/{0}/service_code/{1}>""".format(str(service_id), service_code)


def ttl_service_code_class_uri(service_code):
    return """:{0}""".format(service_code.upper())


def ttl_tooth_uri(patient_id, tooth):
    return """<patient/{0}/tooth/{1}>""".format(str(patient_id), str(tooth))


def ttl_tooth_class_uri(tooth):
    return """:tooth_{0}""".format(str(tooth))


def ttl_surface_uri(patient_id, tooth, surface):
    return """<patient/{0}/tooth/{1}/surface/{2}>""".format(str(patient_id), str(tooth), str(surface))


def ttl_surface_class_uri(surface):
    if surface.lower() == "m":
        return ":mesial"
    elif surface.lower() == "o":
        return ":occlusal"
    elif surface.lower() == "d":
        return ":distal"
    elif surface.lower() == "f":
        return ":facial"
    elif surface.lower() == "l":
        return ":lingual"
    elif surface.lower() == "b":
        return ":buccal"
    elif surface.lower() == "i":
        return ":incisal"
    else:
        return ":tooth_surface"


def ttl_surface_name(surface):
    if surface.lower() == "m":
        return "mesial surface"
    elif surface.lower() == "o":
        return "occlusal surface"
    elif surface.lower() == "d":
        return "distal surface"
    elif surface.lower() == "f":
        return "facial surface"
    elif surface.lower() == "l":
        return "lingual surface"
    elif surface.lower() == "b":
        return "buccal surface"
    elif surface.lower() == "i":
        return "incisal surface"
    else:
        return "tooth surface"


def ttl_gender_uri(patient_id, gender):
    return """<patient/{0}/gender/{1}>""".format(patient_id, gender)


def ttl_gender_class_uri(gender):
    if gender.lower() == "m" or gender.lower() == "male":
        return ":male_gender"
    elif gender.lower() == "f" or gender.lower() == "female":
        return ":female_gender"
    else:
        return ":gender"
