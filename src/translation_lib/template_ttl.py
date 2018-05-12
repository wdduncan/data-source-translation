# coding=utf-8
from textwrap import dedent


################# funcitons from template_ttl.py #################


def prefixes(base="", ontology_uri=""):
    # specify the base uri
    if base.strip() == "":
        base = "http://purl.data-source-translation.org/"

    # create uri for ontology
    if ontology_uri.strip() == "":
        ontology_uri = "http://purl.obolibrary.org/obo/my_translated-data-source.owl"

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
        @prefix sesame: <http://www.openrdf.org/schema/sesame#> .
        
        # custom prefixes
        @base <{0}> .
        @prefix dst: <http://purl.data-source-translation.org/>
        
        # ontology uri
        <{1}> rdf:type owl:Ontology .
        
        """.format(base, ontology_uri))
    return ttl


def triple(subj, pred, obj):
    return """{0} {1} {2} .\n""".format(subj, pred, obj)


def declare_individual(uri, class_uri, label=""):
    ttl = dedent("""{0} rdf:type owl:NamedInvidual, {1} .\n""".format(uri, class_uri))
    if len(label.strip()) > 0:
        ttl += """{0} rdfs:label "{1}" .\n""".format(uri, label)
    return ttl


def declare_class(class_uri, label=""):
    ttl = """{0} rdf:type owl:Class .\n""".format(class_uri)
    if len(label.strip()) > 0:
        ttl += """{0} rdfs:label "{1}" .\n""".format(class_uri, label)

    return ttl



def declare_object_property(prop_uri, label=""):
    ttl = """{0} rdf:type owl:ObjectProperty .\n""".format(prop_uri)
    if len(label.strip()) > 0:
        ttl += """{0} rdfs:label "{1}" .\n""".format(prop_uri, label)

    return ttl


def declare_data_property(prop_uri, label=""):
    ttl = """{0} rdf:type owl:DataProperty .\n""".format(prop_uri)
    if len(label.strip()) > 0:
        ttl += """{0} rdfs:label "{1}" .\n""".format(prop_uri, label)

    return ttl
