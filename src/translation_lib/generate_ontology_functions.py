# coding=utf-8
import os
import rdflib
from rdflib import ConjunctiveGraph, URIRef, RDFS, Literal, RDF, OWL, BNode
from textwrap import dedent
import re
from datetime import datetime
import pandas as pds


def format_as_python_name(name):
    py_name = name.replace(' ', '_')
    py_name = re.sub(r'[^a-z,A-Z,0-9,_]', '', py_name)
    return py_name


def format_function_property_string(function_name, prop_uri, datatype=""):
    function_string = """\
        def {function_name}_ttl(uri1, uri2):
            return "%s <{prop_uri}> %s . \\n" % (uri1, uri2) 

        """.format(function_name=function_name, prop_uri=prop_uri)
    return function_string


def format_class_uri_function_string(function_name, class_uri):
     function_string = """\
        def {function_name}_uri(id):
            return "<{uri}/individual/%s>" % id 

        """.format(function_name=function_name, uri=class_uri)
     return function_string


def format_uri_as_label(uri, make_lower=True):
    # use the last portion of the uri as label
    # use encode('ascii', 'ignore') to ignore unicode characters

    if '#' in str(uri):  # check if uri uses '#' syntax
        short_uri = str(uri.encode('ascii', 'ignore')).split('#')[-1]
    else:
        short_uri = str(uri.encode('ascii', 'ignore')).split('/')[-1]

    if make_lower:
        return short_uri.lower()
    else:
        return short_uri


def build_ontology_functions(ontology_source,
                             ontology_name,
                             pyfile_name="generated_ontology_functions_ttl.py",
                             print_output=False,
                             save_output=True,
                             make_lower=True):
    def get_label(uri):
        label = str(g.label(uri)) # get rdfs:label for uri

        if len(label.strip()) < 1: # if no label, use last part of uri
            label = format_uri_as_label(uri, make_lower)

        return label

    def output(function_string):
        if save_output: f.write(dedent(function_string))  # write function to file
        if print_output: print(dedent(function_string))  # print function

    # build graph
    g = rdflib.Graph()
    g.parse(ontology_source)

    # specify name of the output file
    if len(ontology_name.strip()) > 0:
        pyfile = "{0}_{1}".format(ontology_name, pyfile_name)
    else:
        pyfile = "my_{0}".format(pyfile_name)

    with open(pyfile, 'w') as f:
        # create a function for each object property
        f.write("### object properties ###\n\n")
        for prop in g.subjects(RDF.type, OWL.ObjectProperty):
            fname = format_as_python_name(get_label(prop)) # create function name
            function_string = format_function_property_string(fname, prop) # create python function string
            output(function_string)


        # create a function for each data property
        f.write("\n### data properties ###\n\n")
        for prop in g.subjects(RDF.type, OWL.DatatypeProperty):
            fname = format_as_python_name(get_label(prop))  # create function name
            function_string = format_function_property_string(fname, prop)  # create python function string
            output(function_string)

        # create a function for each class that returns a uri for an individual / instance
        f.write("\n### classes ###\n\n")
        for class_uri in g.subjects(RDF.type, OWL.Class):
            if type(class_uri) != rdflib.term.BNode:
                fname = format_as_python_name(get_label(class_uri))
                function_string = format_class_uri_function_string(fname, class_uri)
                output(function_string)

# build_ontology_functions('simple-dental-ontology.owl', "simple_dental_ontology", print_output=True)
build_ontology_functions('data-source-ontology.owl', 'translation', print_output=True)