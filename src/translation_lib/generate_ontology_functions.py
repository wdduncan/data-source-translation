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
    py_name = py_name.replace('.owl', '')
    py_name = py_name.replace('.rdf', '')
    py_name = py_name.replace('.ttl', '')
    py_name = py_name.replace('.trig', '')
    py_name = py_name.replace('.xml', '')
    py_name = py_name.replace('.', '_')
    py_name = py_name.replace('-', '_')
    py_name = py_name.replace('+', '_')
    py_name = py_name.replace('=', '_')
    py_name = py_name.replace('!', '_')
    py_name = py_name.replace(',', '_')
    py_name = py_name.replace('*', '_')
    py_name = py_name.replace('@', '_')
    py_name = py_name.replace('&', '_')
    py_name = py_name.replace('$', '_')
    py_name = py_name.replace('~', '_')
    py_name = py_name.replace('?', '_')
    py_name = py_name.replace(':', '_')
    py_name = py_name.replace('%20', '_')
    py_name = re.sub(r'[^a-z,A-Z,0-9,_]', '', py_name)
    return py_name


def format_function_property_string(function_name, prop_uri, datatype=""):
    function_string = """
        def {function_name}(uri1, uri2):
            return "%s <{prop_uri}> %s . \\n" % (uri1, uri2) 

        """.format(function_name=function_name, prop_uri=prop_uri)
    return function_string


def format_uri_function_string(function_name, uri):
     function_string = """
        def {function_name}_uri(id=""):
            if len(id.strip()) > 0:
                return "<{uri}/%s>" % id
            else:
                return "<{uri}>" 

        """.format(function_name=function_name, uri=uri)
     return function_string


def format_uri_as_label(uri, make_lower=True):
    # use the last portion of the uri as label
    # use encode('ascii', 'ignore') to ignore unicode characters
    if '#' in str(uri):  # check if uri uses '#' syntax
        short_uri = str(uri.encode('ascii', 'ignore')).split('#')[-1]
    else:
        short_uri = str(uri.encode('ascii', 'ignore')).split('/')[-1]

    if make_lower:
        return format_as_python_name(short_uri.lower())
    else:
        return format_as_python_name(short_uri)


def format_generated_functions_file_name(ontology_source, pyfile_name="", make_lower=True):
    # specify name of the python file name for generated functions
    pyfile_name = pyfile_name.strip()
    if len(pyfile_name) > 0:
        pyfile = pyfile_name
    else:
        ontology = format_uri_as_label(ontology_source.strip(), make_lower=make_lower)
        pyfile = "{0}_generated_functions_ttl.py".format(format_as_python_name(ontology))

    return pyfile

def build_ontology_functions(ontology_source,
                             pyfile_name="",
                             print_output=False,
                             save_output=True,
                             make_lower=True):
    def get_label(uri):
        label = str(g.label(uri)) # get rdfs:label for uri
        if len(label.strip()) < 1: # if no label, use last part of uri
            label = format_uri_as_label(uri, make_lower)
        return label

    def output(output_string):
        if save_output: f.write(dedent(output_string))  # write output to file
        if print_output: print(dedent(output_string))  # print output

    # specify name of the output file
    pyfile = \
        format_generated_functions_file_name(ontology_source, pyfile_name=pyfile_name, make_lower=make_lower)

    # build graph
    g = rdflib.Graph()
    g.parse(ontology_source)

    with open(pyfile, 'w') as f:
        # create a function for each object property
        output("################# object properties #################\n\n")
        for prop in g.subjects(RDF.type, OWL.ObjectProperty): # query for object properteis
            fname = format_as_python_name(get_label(prop)) # create function name
            function_string = format_function_property_string(fname, prop) # create python function string
            uri_string = format_uri_function_string(fname, prop)
            output(function_string)
            output(uri_string)


        # create a function for each data property
        output("\n################# data properties #################\n\n")
        for prop in g.subjects(RDF.type, OWL.DatatypeProperty): # query for data properties
            fname = format_as_python_name(get_label(prop))  # create function name
            function_string = format_function_property_string(fname, prop)  # create python function string
            uri_string = format_uri_function_string(fname, prop)
            output(function_string)
            output(uri_string)

        # create a function for each annotation property
        output("\n################# annotation properties #################\n\n")
        for prop in g.subjects(RDF.type, OWL.AnnotationProperty):  # query for data properties
            fname = format_as_python_name(get_label(prop))  # create function name
            function_string = format_function_property_string(fname, prop)  # create python function string
            uri_string = format_uri_function_string(fname, prop)
            output(function_string)
            output(uri_string)

        # create a function for each class that returns a uri for an individual / instance
        output("\n################# classes #################\n\n")
        for class_uri in g.subjects(RDF.type, OWL.Class): # query for classes
            if type(class_uri) != rdflib.term.BNode:
                class_name = format_as_python_name(get_label(class_uri))  # create class name
                uri_string = format_uri_function_string(class_name, class_uri)
                output(uri_string)

# build_ontology_functions('simple-dental-ontology.owl', "simple_dental_ontology_ttl.py", print_output=True)
build_ontology_functions('data-source-ontology.owl', print_output=True)