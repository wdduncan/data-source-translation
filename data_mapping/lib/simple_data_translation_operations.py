# coding=utf-8
import pandas as pds
from uri_functions import *
from textwrap import dedent
from data_operations import *


# @print_function_output()
def ttl_prefixes_simple(data_source_name, table_name, base_uri="", ontology_uri="", imports=""):
    if len(base_uri) == 0: base_uri = "http://purl.obolibrary.org/data-source/{0}/".format(data_source_name)
    if len(ontology_uri) == 0: ontology_uri = "http://purl.obolibrary.org/{0}".format(data_source_name)

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
                @base <{0}> .
                @prefix : <{0}> .
                
                # custom class and property prefixes
                @prefix table: <table/> .
                @prefix table_name: <table/{1}> .
                @prefix field: <field/> .
                @prefix record: <record/> .
                @prefix data_property: <data_property/> .
                @prefix dp: <data_property/> .
                @prefix op: <object_property/> .

                # custom instance prefixes
                @prefix record_i: <record/instance/> .
                @prefix fd_i: <field_datum/instance/> .
                
                # ontology uri
                <{2}> rdf:type owl:Ontology .
                      
                """.format(base_uri, table_name, ontology_uri))

    if len(imports) > 0:
        # check if imports is string or list
        if type(imports) == type(""):  # imports is a list
            ttl += \
                dedent("""
                        # specified ontology imports
                        <{0}> owl:imports <{1}> .""".format(ontology_uri, imports))
        elif type(imports) == type([]):  # imports is a list
            # use list comprehension ["<" + i + ">" for i in imports] to build list of uris
            # then join with commas
            ttl += \
                dedent("""
                        # specified ontology imports
                        <{0}> owl:imports {1} .""".format(ontology_uri,
                                                          ", ".join(["<" + i + ">" for i in imports])))

    return ttl

# @print_function_output()
def ttl_table_simple(table_name, super_class_uri="owl:Thing", terse_label=False):
    ttls = ["\n# axioms to create table"]

    # create table class
    if terse_label:
        label = table_name
    else:
        label = "{0} table".format(table_name)

    class_uri = get_table_class_uri(table_name)

    # create class
    ttl = declare_class(class_uri, super_class_uri, label)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_record_class_simple(super_class_uri, table_name, terse_label=False):
    ttls = ["\n# axioms to create record class"]

    if terse_label:
        label = "record"
    else:
        label = "{0} record".format(table_name)

    class_uri = get_record_class_uri(table_name)

    # create class
    ttl = declare_class(class_uri, super_class_uri, label)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_records_simple(df, class_uri, table_name, terse_label=False, with_fields=False):
    ttls = ["\n# axioms to create records"]

    # create field datum class and subclasses
    field_names = list(df.columns)  # get list of fields
    for record_idx, record in enumerate(df.itertuples(), 1):
        # make instance of record
        record_uri = get_record_uri(class_uri, record_idx)
        ttl = ttl_record_simple(record_uri, class_uri, record_idx, table_name, terse_label)
        ttls.append(ttl)

        # relate record to values
        ttl = ttl_record_data_values_simple(record, record_uri, field_names)
        ttls.append(ttl)

        if with_fields:
            ttl = ttl_field_datum_simple(record, record_uri, record_idx, field_names)
            ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


def ttl_record_simple(record_uri, class_uri, record_idx, table_name, terse_label=False):
    ttls = ["\n# axioms to create record"]

    # create label
    if terse_label:
        label = "record {0}".format(str(record_idx))
    else:
        label = "{0} record {1}".format(table_name, str(record_idx))

    # declare instance
    ttl = declare_instance(record_uri, class_uri, label=label)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_record_data_values_simple(record, record_uri, field_names):
    ttls = ["\n# axioms to relate record to values"]

    for value_idx, value in enumerate(record):
        # value_idx 0 holds the index of the value tuple, so ignore it
        if value_idx > 0:
            field_name = field_names[value_idx - 1]
            data_prop_uri = get_data_prop_uri(field_name)  # uri for field as data property

            # relate record to data value
            ttl = """{0} {1} "{2}" .""".format(record_uri, data_prop_uri, value)
            ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")


def ttl_field_datum_simple(record, record_uri, record_idx, field_names):
    ttls = ["\n# axioms to create field datum instances and relate to record"]

    for value_idx, value in enumerate(list(record)):
        # value_idx 0 holds the index of the value tuple, so ignore it
        if value_idx > 0:
            field_name = field_names[value_idx - 1]
            fd_uri = get_field_datum_uri(field_name, record_idx) # get uri for instance of field datum

            # relate record to field datum
            ttl = "{0} op:has_member {1} .".format(record_uri, fd_uri)
            ttls.append(ttl)

            ttl = "{0} op:member_of {1} .".format(fd_uri, record_uri)
            ttls.append(ttl)

            # relate field datum to value
            ttl = """{0} dp:has_value "{1}" .""".format(fd_uri, value)
            ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")


# @print_function_output()
def ttl_field_data_properties_simple(table_name, field_names, terse_label=False, with_fields=False):
    ttls = ["\n# axioms to create data properties"]

    if with_fields:
        # when using fields we need a data property to relate field datum to value
        ttl = declare_data_property("dp:has_value", "has value")
        ttls.append(ttl)

    for field_name in field_names:
        ttl = ttl_field_data_property_simple(table_name, field_name, terse_label)
        ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")


# @print_function_output()
def ttl_properties_simple(table_name, field_names, terse_label=False):
    ttls = ["\n# axioms to create object and data properties"]

    # create member of relation needed to related records to field datum instances
    ttl = ttl_object_properties_simple()
    ttls.append(ttl)

    # create data properties
    ttl = ttl_field_data_properties_simple(table_name, field_names, terse_label)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")



# @print_function_output()
def ttl_object_properties_simple():
    ttls = ["\n# axioms to create object properties"]

    # create membership relations needed to related records to field datum instances
    ttl = declare_object_property("op:member_of", "member of")
    ttls.append(ttl)

    ttl = declare_object_property("op:has_member", "has member")
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")


# @print_function_output()
def ttl_field_data_property_simple(table_name, field_name, terse_label=False):
    # create data property field
    data_prop_uri = get_data_prop_uri(field_name)

    if terse_label:
        label = field_name
    else:
        label = "{0}.{1} datum value".format(table_name, field_name)

    ttl = declare_data_property(data_prop_uri, label)
    return ttl


# @print_function_output()
def ttl_field_classes_simple(table_class_uri, table_name, field_names, terse_label=False):
    ttls = ["\n# axioms to create field classes"]

    for field_name in field_names:
        ttl = ttl_field_class_simple(table_class_uri, table_name, field_name, terse_label)
        ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")


# @print_function_output()
def ttl_field_class_simple(table_class_uri, table_name, field_name, terse_label=False):
    if terse_label:
        label = field_name
    else:
        label = "{0}.{1} field".format(table_name, field_name)

    class_uri = get_field_class_uri(table_name)

    # create field class
    ttl = declare_class(class_uri, table_class_uri, label)
    return ttl