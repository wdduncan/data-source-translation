# coding=utf-8
from textwrap import dedent
import re


################# funcitons from template_ttl.py #################


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
    ttl = """{0} rdf:type owl:DataProperty .\n""".format(prop_uri)

    if len(parent_uri.strip()) > 0:
        ttl += """{0} rdfs:subPropertyOf {1} .\n""".format(prop_uri, parent_uri)

    if len(label.strip()) > 0:
        ttl += """{0} rdfs:label "{1}" .\n""".format(prop_uri, label)

    return ttl


def format_uri_name(name):
    uri_name = name.replace(' ', '_')
    uri_name = uri_name.replace('.', '_')
    uri_name = uri_name.replace('-', '_')
    uri_name = uri_name.replace('+', '_')
    uri_name = uri_name.replace('=', '_')
    uri_name = uri_name.replace('!', '_')
    uri_name = uri_name.replace(',', '_')
    uri_name = uri_name.replace('*', '_')
    uri_name = uri_name.replace('@', '_')
    uri_name = uri_name.replace('&', '_')
    uri_name = uri_name.replace('$', '_')
    uri_name = uri_name.replace('~', '_')
    uri_name = uri_name.replace('?', '_')
    uri_name = uri_name.replace(':', '_')
    uri_name = uri_name.replace('%20', '_')
    uri_name = re.sub(r'[^a-z,A-Z,0-9,_]', '', uri_name)
    return uri_name
