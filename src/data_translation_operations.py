# coding=utf-8
import pandas as pds
from uri_functions import *
from textwrap import dedent
from data_operations import *


# @print_function_output()
def ttl_prefixes(data_source_name, table_name, base_uri="", ontology_uri="", imports=""):
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
                @prefix dso: <http://purl.obolibrary.org/obo/data-source-ontology.owl/> .
                @prefix data_source_ontology: <http://purl.obolibrary.org/obo/data-source-ontology.owl/> .
                
                # custom class and property prefixes
                @prefix table: <table/> .
                @prefix table_name: <table/{1}> .
                @prefix field: <field/> .
                @prefix field_datum: <field_datum/> .
                @prefix fd: <field_datum/> .
                @prefix record: <record/> .
                @prefix data_property: <data_property/> .
                @prefix dp: <data_property/> .
                
                # custom instance prefixes
                @prefix table_i: <table/instance/> .
                @prefix field_i: <field/instance/> .
                @prefix field_datum_i: <field_datum/instance/> .
                @prefix fd_i: <field_datum/instance/> .
                @prefix record_i: <record/instance/> .
                
                # ontology uri and default import
                <{2}> rdf:type owl:Ontology;
                      owl:imports <http://purl.obolibrary.org/obo/data-source-ontology.owl> .
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
def ttl_table(table_uri, table_name):
    ttls = ["\n# axioms to create table"]

    # create table class
    label = "{0} table".format(table_name)
    class_uri = get_table_uri(table_name)

    ttl = declare_class(class_uri, "dso:table", label)
    ttls.append(ttl)

    #  create instance of table
    label = "{0} table instance".format(table_name)
    ttl = declare_instance(table_uri, class_uri, label=label)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_fields(table_uri, table_name, fields):
    ttls = ["\n# axioms to create fields"]

    # create field super class for field subclasses
    super_class_uri = get_field_class_uri(table_name)
    label = "{0} field".format(table_name)

    ttl = declare_class(super_class_uri, "dso:field", label)
    ttls.append(ttl)

    for field_name in fields:
        ttl = ttl_field(table_uri, super_class_uri, table_name, field_name)  # create ttl for that field
        ttls.append(ttl)

        ttl = ttl_field_data_property(table_name, field_name)  # create data property field for that field
        ttls.append(ttl + "\n")  # add new line to help visual inspection

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_field(table_uri, super_class_uri, table_name, field_name):
    ttls = []

    # create field class
    class_uri = get_field_class_uri(field_name)
    label = "{0}.{1} field".format(table_name, field_name)

    ttl = declare_class(class_uri, super_class_uri, label)
    ttls.append(ttl)

    # create instance of field class
    field_uri = get_field_uri(field_name)  # uri for instance of field
    label = "{0}.{1} field instance".format(table_name, field_name)

    ttl = declare_instance(field_uri, class_uri, table_uri, label)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_function_output()
def ttl_field_data_properties(table_name, field_names, terse_label=False):
    ttls = []
    for field_name in field_names:
        ttl = ttl_field_data_property(table_name, field_name, terse_label)
        ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_function_output()
def ttl_field_data_property(table_name, field_name, terse_label=False):
    # create data property field
    data_prop_uri = get_data_prop_uri(field_name)

    if terse_label:
        label = field_name
    else:
        label = "{0}.{1} datum value".format(table_name, field_name)

    ttl = declare_data_property(data_prop_uri, label)
    return ttl


# @print_function_output()
def ttl_records(df, table_uri, table_name, terse_label=False):
    ttls = []
    ttls.append("\n# axioms to create record class")

    # create field super class for field subclasses
    record_class_uri = get_record_class_uri(table_name)
    label = "{0} record".format(table_name)

    ttl = declare_class(record_class_uri, "dso:record", label)
    ttls.append(ttl + "\n")  # add new line to help visual inspection

    # create field datum class and subclasses
    field_names = list(df.columns)  # get list of fields
    for record_idx, record in enumerate(df.itertuples(), 1):
        ttls.append("\n# axioms to create record")

        # create instance of record
        record_uri = get_record_uri(table_name, record_idx)
        if terse_label:
            label = "record {0}".format(str(record_idx))
        else:
            label = "{0} record {1}".format(table_name, str(record_idx))

        ttl = declare_instance(record_uri, record_class_uri, table_uri, label)
        ttls.append(ttl)

        ttl = ttl_field_data(table_name, record, record_idx, record_uri, field_names)
        ttls.append(ttl + "\n")  # add new line to help visual inspection

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_field_datum_classes(table_name, field_names):
    ttls = []
    ttls.append('\n# axioms to create field datum classes')

    # create field datum superclass for this table
    super_class_uri = get_field_datum_class_uri(table_name)
    label = "{0} field datum".format(table_name)

    ttl = declare_class(super_class_uri, "dso:field_datum", label)
    ttls.append(ttl + "\n")  # add new line to help visual inspection

    # for every field create a field datum subclass
    for field_name in field_names:
        class_uri = get_field_datum_class_uri(field_name)
        label = "{0}.{1} field datum".format(table_name, field_name)

        ttl = declare_class(class_uri, super_class_uri, label)
        ttls.append(ttl + "\n")  # add new line to help visual inspection

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_field_data(table_name, record, record_idx, record_uri, field_names):
    ttls = ["\n# axioms to create field data"]

    for value_idx, value in enumerate(record):
        # value_idx 0 holds the index of the value tuple, so ignore it
        if value_idx > 0:
            field_name = field_names[value_idx - 1]
            field_uri = get_field_uri(field_name)  # uri for instance of field
            data_prop_uri = get_data_prop_uri(field_name)  # uri for field as data property

            # relate record to data value
            ttl = ttl_record_datum_value(record_uri, data_prop_uri, value)
            ttls.append(ttl)

            # create field datum (fd) instance
            fd_uri = get_field_datum_uri(field_name, record_idx)
            fd_class_uri = get_field_datum_class_uri(field_name)
            label = "{0}.{1} field datum {2}".format(table_name, field_name, str(record_idx))

            ttl = declare_instance(fd_uri, fd_class_uri, [record_uri, field_uri], label)
            ttls.append(ttl)

            # relate fd to datum value
            ttl = ttl_field_value_datum(fd_uri, value)
            ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_field_value_datum(field_datum_uri, value):
    # relate field value to a datum value
    ttl = """{0} dso:has_datum_value "{1}" .""".format(field_datum_uri, value)
    return ttl


# @print_function_output()
def ttl_record_datum_value(record_uri, data_prop_uri, value):
    # relate record to data value
    ttl = """{0} {1} "{2}" .""".format(record_uri, data_prop_uri, value)
    return ttl

