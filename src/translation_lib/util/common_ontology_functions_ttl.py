# coding=utf-8
from textwrap import dedent
from rdflib import Graph,URIRef,RDF,OWL,RDFS, Literal
import re


################# funcitons from common_ontology_functions_ttl.py ###################


def triple(subj, pred, obj):
    return """{0} {1} {2} .\n""".format(subj, pred, obj)


def declare_individual(uri, class_uri, label=""):
    ttl = dedent("""{0} rdf:type owl:NamedInvidual, {1} .\n""".format(uri, class_uri))
    if len(label.strip()) > 0:
        ttl += """{0} rdfs:label "{1}" .\n""".format(uri, label)
    return ttl


def declare_class(class_uri, label="", parent_uri=""):
    ttl = """{0} rdf:type owl:Class .\n""".format(class_uri)

    if len(parent_uri.strip()) > 0:
        ttl += """{0} rdfs:subCalssOf {1} .\n""".format(class_uri, parent_uri)

    if len(label.strip()) > 0:
        ttl += """{0} rdfs:label "{1}" .\n""".format(class_uri, label)

    return ttl



def declare_object_property(prop_uri, label="", parent_uri=""):
    ttl = """{0} rdf:type owl:ObjectProperty .\n""".format(prop_uri)

    if len(parent_uri.strip()) > 0:
        ttl += """{0} rdfs:subPropertyOf {1} .\n""".format(prop_uri, parent_uri)

    if len(label.strip()) > 0:
        ttl += """{0} rdfs:label "{1}" .\n""".format(prop_uri, label)

    return ttl


def declare_data_property(prop_uri, label="", parent_uri=""):
    ttl = """{0} rdf:type owl:DatatypeProperty .\n""".format(prop_uri)

    if len(parent_uri.strip()) > 0:
        ttl += """{0} rdfs:subPropertyOf {1} .\n""".format(prop_uri, parent_uri)

    if len(label.strip()) > 0:
        ttl += """{0} rdfs:label "{1}" .\n""".format(prop_uri, label)

    return ttl