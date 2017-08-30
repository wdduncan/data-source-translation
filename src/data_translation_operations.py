# coding=utf-8
import pandas as pds
from uri_functions import *
from textwrap import dedent
from data_operations import *


# @print_function_output()
def ttl_prefixes(tablename, base_uri="", ontology_uri="", imports=""):
    if len(base_uri) == 0: base_uri = "http://purl.obolibrary.org/data_source/{0}/".format(tablename)
    if len(ontology_uri) == 0: ontology_uri = "http://purl.obolibrary.org/{0}".format(tablename)

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
                @prefix dso: <http://purl.obolibrary.org/obo/data_source_ontology.owl/> .
                @prefix data_source_ontology: <http://purl.obolibrary.org/obo/data_source_ontology.owl/> .
                @prefix table: <table/{1}/> .
                @prefix tablename: <table/{1}> .
                @prefix field: <field/{1}/> .
                @prefix field_datum: <field_datum/{1}/> .
                @prefix fd: <field_datum/{1}/> .
                @prefix record: <record/{1}/> .
                @prefix data_property: <data_property/{1}/> .
                @prefix dp: <data_property/{1}/> .

                # ontology uri and default import
                <{2}> rdf:type owl:Ontology;
                      owl:imports <http://purl.obolibrary.org/obo/data_source_ontology.owl> .
                """.format(base_uri, tablename, ontology_uri))

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
def ttl_table(table_uri, tablename):
    ttls = ["\n# axioms to create table"]

    # create table class
    label = "{0} table".format(tablename)
    ttl = declare_class("tablename:", "dso:table", label)
    ttls.append(ttl)

    #  create instance of table
    label = "{0} table instance".format(tablename)
    ttl = declare_instance(table_uri, "tablename:", label=label)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_fields(table_uri, tablename, fields):
    ttls = ["\n# axioms to create fields"]

    for field_name in fields:
        ttl = ttl_field(table_uri, tablename, field_name)  # create ttl for that field
        ttls.append(ttl)

        ttl = ttl_field_data_property(tablename, field_name)  # create data property field for that field
        ttls.append(ttl + "\n")  # add new line to help visual inspection

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_field(table_uri, tablename, field_name):
    ttls = []

    # create field class
    class_uri = "field:{0}".format(field_name)
    label = "{0}.{1} field".format(tablename, field_name)
    ttl = declare_class(class_uri, "dso:field", label)
    ttls.append(ttl)

    # create instance of field class
    field_uri = get_field_uri(field_name)  # uri for instance of field
    label = "{0}.{1} field instance".format(tablename, field_name)
    ttl = declare_instance(field_uri, class_uri, table_uri, label)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_field_data_property(tablename, field_name):
    # create data property field
    data_prop_uri = get_data_prop_uri(field_name)
    label = "{0}.{1} datum value".format(tablename, field_name)
    ttl = declare_data_property(data_prop_uri, label)

    return ttl


# @print_function_output()
def ttl_records(df, table_uri, tablename):
    ttls = []
    ttls.append("\n# axioms to create record class")

    # create record class for this table
    record_class_uri = "record:{0}_record".format(tablename)
    label = "{0} record".format(tablename)
    ttl = declare_class(record_class_uri, "dso:record", label)
    ttls.append(ttl + "\n")  # add new line to help visual inspection

    # create field datum class and subclasses
    field_names = list(df.columns)  # get list of fields
    for record_idx, record in enumerate(df.itertuples(), 1):
        ttls.append("\n# axioms to create record")

        # create instance of record
        record_uri = get_record_uri(tablename, record_idx)
        label = "{0} record {1}".format(tablename, str(record_idx))
        ttl = declare_instance(record_uri, record_class_uri, table_uri, label)
        ttls.append(ttl)

        ttl = ttl_field_data(tablename, record, record_idx, record_uri, field_names)
        ttls.append(ttl + "\n")  # add new line to help visual inspection

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_field_datum_classes(tablename, field_names):
    ttls = []
    ttls.append('\n# axioms to create field datum classes')

    # create field value class for this table
    class_uri = get_field_value_class_uri(tablename)
    label = "{0} field datum".format(tablename)
    ttl = declare_class(class_uri, "dso:field_datum", label)
    ttls.append(ttl + "\n")  # add new line to help visual inspection

    # for every field create a field value value subclass
    for field_name in field_names:
        fv_class_uri = get_field_value_class_uri(tablename, field_name)
        label = "{0}.{1} field datum".format(tablename, field_name)
        ttl = declare_class(fv_class_uri, class_uri, label)
        ttls.append(ttl + "\n")  # add new line to help visual inspection

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_field_data(tablename, record, record_idx, record_uri, field_names):
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
            fd_uri = get_field_value_uri(field_name, record_idx)
            label = "{0}.{1} field datum {2}".format(tablename, field_name, str(record_idx))
            fv_class_uri = get_field_value_class_uri(tablename, field_name)
            ttl = declare_instance(fd_uri, fv_class_uri, label=label)
            ttls.append(ttl)

            # fv is member of field and record
            ttl = ttl_field_datum_membership(fd_uri, record_uri, field_uri)
            ttls.append(ttl)

            # relate fv to datum
            ttl = ttl_field_value_datum(fd_uri, value)
            ttls.append(ttl)

            # ttl = ttl_field_value(tablename, record_idx, value, record_uri, field_uri, field_name, data_prop_uri)
            # ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_field_datum_membership(field_value_uri, record_uri, field_uri):
    ttl = "{0} dso:member_of {1}, {2} .".format(field_value_uri, record_uri, field_uri)
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

