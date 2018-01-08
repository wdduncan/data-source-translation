# coding=utf-8
import pandas as pds
from uri_functions import *
from textwrap import dedent
from data_operations import *
from direct_mapping_classes import *

def ttl_prefixes(base="", ontology_uri=""):
    # specify the base uri
    if base.strip() == "":
        base = "http://purl.obolibrary.org/obo/simple-dental-ontology.owl"

    # create uri for ontology
    if ontology_uri.strip() == "":
        ontology_uri = "http://purl.obolibrary.org/obo/simple-dental-ontology.owl/translate"

    ttl = \
        dedent("""\
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
                @prefix : <http://purl.obolibrary.org/obo/simple-dental-ontology.owl/>
                
                
                # ontology uri
                <{1}> rdf:type owl:Ontology .
    
              """.format(base, ontology_uri))
    return ttl


def declare_individual(uri, class_uri, label=""):
	ttl = """
	{0} rdf:type owl:NamedInvidual .
	{0} rdf:type {1} .
	""".format(uri, class_uri)
	
	if len(label.strip(O)) > 0:
		ttl += """
		{0} rdfs:label {1} .
		""".format(uri, label)
	
	return ttl

def declare_class(class_uri, label=""):
	ttl = """
	{0} rdf:type owl:Class .
	""".format(class_uri)
	
	if len(label.strip(O)) > 0:
		ttl += """
		{0} rdfs:label {1} .
		""".format(class_uri, label)
	
	return ttl

def ttl_triple(subj pred obj):
	return """{0} {1} {2} .""".format(subj pred obj)