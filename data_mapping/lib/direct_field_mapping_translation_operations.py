# coding=utf-8
import pandas as pds
from uri_functions import *
from textwrap import dedent
from data_operations import *
from direct_mapping_classes import *

# @print_function_output()
def prefix_ttl(source_name, source_type, source_uri="", base="", ontology_uri=""):
    # specify the base uri
    if base.strip() == "":
        base = "http://purl.obolibrary.org/obo/data-source/{0}".format(source_name)

    # specify uri for the data source
    if source_uri.strip() == "":
        source_uri = "<{0}/{1}/{2}>".format(base, source_type, source_name)

    # create uri for ontology
    if ontology_uri.strip() == "":
        ontology_uri = "<{0}/{1}.owl>".format(base, source_name)

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
                @prefix : <http://purl.obolibrary.org/obo/data-source/{2}/> .
                @prefix ds: <http://purl.obolibrary.org/obo/data-source-ontology.owl/> .
                @prefix op: <object_property/> .
                @prefix dp: <data_property/> .
                @prefix df: <data_field/> .
                @prefix dr: <data_record/> .
                
                @prefix data_field: <http://purl.obolibrary.org/obo/data-source-ontology.owl/data_field> .
                @prefix data_record: <http://purl.obolibrary.org/obo/data-source-ontology.owl/data_record> .
                @prefix has_value: <http://purl.obolibrary.org/obo/data-source-ontology.owl/has_value> .
                @prefix has_member: <http://purl.obolibrary.org/obo/data-source-ontology.owl/has_member> .
                @prefix has_data_field: <http://purl.obolibrary.org/obo/data-source-ontology.owl/has_data_field> .
                @prefix has_data_record: <http://purl.obolibrary.org/obo/data-source-ontology.owl/has_data_record> .
                @prefix member_of: <http://purl.obolibrary.org/obo/data-source-ontology.owl/member_of> .
                @prefix data_field_of: <http://purl.obolibrary.org/obo/data-source-ontology.owl/data_field_of> .
                @prefix data_record_of: <http://purl.obolibrary.org/obo/data-source-ontology.owl/data_record_of> .
                
                # ontology uri
                {1} rdf:type owl:Ontology .
    
                # specified ontology imports
                {1} owl:imports <http://purl.obolibrary.org/obo/data-source-ontology.owl> . 
    
                ## specify data source
                {3} rdf:type owl:NamedIndividual, ds:{4} .
    
              """.format(base, ontology_uri, source_name, source_uri, source_type))
    return ttl

# @print_function_output()
def object_properties_ttl(data_fields):
    ttls = ["\n# axioms to create object properties"]

    for field in data_fields:
        # create membership relations needed to related records to data fields
        field_uri = obj_prop_uri(field)
        ttl = declare_object_property(field_uri, super_property_uri="ds:has_data_field")
        ttls.append(ttl)

        # create inverse relations
        field_uri = inv_obj_prop_uri(field)
        ttl = declare_object_property(field_uri, super_property_uri="ds:data_field_of")
        ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")

def data_field_classes_ttl(data_fields):
    ttls = ["\n# axioms to data field classes"]

    for field in data_fields:
        # create data field class
        class_uri = data_field_class_uri(field)
        ttl = declare_class(class_uri, "ds:data_field")
        ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")


# @print_function_output()
def data_field_class_ttl(table_class_uri, table_name, field_name, terse_label=False):
    if terse_label:
        label = field_name
    else:
        label = "{0}.{1} field".format(table_name, field_name)

    class_uri = get_field_class_uri(table_name)

    # create field class
    ttl = declare_class(class_uri, table_class_uri, label)
    return ttl


def make_field_to_class_map(field_list):
    map = {}
    for field_name in field_list:
        map[field_name] = data_field_class_uri(field_name)

    return map


def make_field_to_object_property_map(field_list):
    map = {}
    for field_name in field_list:
        map[field_name] = obj_prop_uri(field_name)

    return map


def make_field_to_inv_object_property_map(field_list):
    map = {}
    for field_name in field_list:
        map[field_name] = inv_obj_prop_uri(field_name)

    return map

def make_field_to_data_property_map(field_list):
    map = {}
    for field_name in field_list:
        map[field_name] = data_prop_uri(field_name)

    return map