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
                @prefix : <http://purl.obolibrary.org/obo/db_mapping.owl/> .
                @prefix table: <table/{1}/> .
                @prefix tablename: <table/{1}> .
                @prefix field: <field/{1}/> .
                @prefix field_value: <field_value/{1}/> .
                @prefix fv: <field_value/{1}/> .
                @prefix record: <record/{1}/> .
                @prefix data_property: <data_property/{1}/> .
                @prefix dv: <data_property/{1}/> .

                # ontology uri
                <{2}> rdf:type owl:Ontology .
                """.format(base_uri, tablename, ontology_uri))

    if len(imports) > 0:
        # check if imports is string or list
        if type(imports) == type(""): # imports is a list
            ttl += \
                dedent("""
                        # ontology imports
                        <{0}> owl:imports <{1}> .""".format(ontology_uri, imports))
        elif type(imports) == type([]): # imports is a list
            # use list comprehension ["<" + i + ">" for i in imports] to build list of uris
            # then join with commas
            ttl += \
                dedent("""
                        # ontology imports
                        <{0}> owl:imports {1} .""".format(ontology_uri,
                                                          ", ".join(["<" + i + ">" for i in imports])))

    return ttl

# @print_function_output()
def ttl_table(table_uri):
    ttls = ["\n# axioms to create table"]
    
    # create table class
    ttl = declare_class("tablename:", ":table")
    ttls.append(ttl)

    #  create instance of table
    ttl = declare_instance(table_uri, "tablename:")
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_function_output()
def ttl_fields(table_uri, fields):
    ttls = ["\n# axioms to create fields"]

    for field_name in fields:
        ttl = ttl_field(table_uri, field_name) # create ttl for that field
        ttls.append(ttl)

        ttl = ttl_field_data_property(field_name) # create data property field for that field
        ttls.append(ttl + "\n") # add new line to help visual inspection

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_function_output()
def ttl_field(table_uri, field_name):
    ttls = []

    # create field class
    class_uri = "field:{0}".format(field_name)
    ttl = declare_class(class_uri, ":field")
    ttls.append(ttl)

    # create instance of field class
    field_uri = get_field_uri(field_name)  # uri for instance of field
    ttl = declare_instance(field_uri, class_uri, table_uri)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_function_output()
def ttl_field_data_property(field_name):
    # create data property field
    data_prop_uri = get_data_prop_uri(field_name)
    ttl = declare_data_property(data_prop_uri)

    return ttl

# @print_function_output()
def ttl_records(df, table_uri, tablename):
    ttls = []
    ttls.append('\n# axioms to create records and values')

    # create record class for this table
    record_class_uri = "record:{0}_record".format(tablename)
    ttl = declare_class(record_class_uri, ":record")
    ttls.append(ttl + "\n")  # add new line to help visual inspection

    # create field value class and subclasses
    field_names = list(df.columns)  # get list of fields
    ttl = ttl_field_value_classes(tablename, field_names)
    ttls.append(ttl + "\n")  # add new line to help visual inspection

    for record_idx, record in enumerate(df.itertuples(), 1):
        # create instance of record
        record_uri = get_record_uri(tablename, record_idx)
        ttl = declare_instance(record_uri, record_class_uri, table_uri)
        ttls.append(ttl)

        ttl = ttl_field_values(tablename, record, record_idx, record_uri, field_names)
        ttls.append(ttl + "\n") # add new line to help visual inspection

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_function_output()
def ttl_field_value_classes(tablename, field_names):
    ttls = []
    ttls.append('\n# axioms to create field value classes')

    # create field value class for this table
    class_uri = get_field_value_class_uri(tablename)
    ttl = declare_class(class_uri, ":field_value")
    ttls.append(ttl)

    # for every field create a field value value subclass
    for field_name in field_names:
        fv_class_uri = get_field_value_class_uri(tablename, field_name)
        ttl = declare_class(fv_class_uri, class_uri)
        ttls.append(ttl)  # add new line to help visual inspection

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

#  @print_function_output()
def ttl_field_values(tablename, record, record_idx, record_uri, field_names):
    ttls = []

    for value_idx, value in enumerate(record):
        if value_idx > 0:
            field_name = field_names[value_idx - 1]
            field_uri = get_field_uri(field_name)  # uri for instance of field
            data_prop_uri = get_data_prop_uri(field_name) # uri for field as data property

            ttl = ttl_field_value(tablename, record_idx, value, record_uri, field_uri, field_name, data_prop_uri)
            ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_function_output()
def ttl_field_value(tablename, record_idx, value, record_uri, field_uri, field_name, data_prop_uri):
    ttls = []

    # create uri for field value (fv) instance and class
    fv_uri = get_field_value_uri(field_name, record_idx)
    fv_class_uri = get_field_value_class_uri(tablename, field_name)

    # create instance
    ttl = "{0} rdf:type {1} .".format(fv_uri, fv_class_uri)
    ttls.append(ttl)

    # relate fv to record and field
    ttl = "{0} :member_of {1}, {2} .".format(fv_uri, record_uri, field_uri)
    ttls.append(ttl)

    # relate fv to value
    ttl = """{0} :has_data_value "{1}" .""".format(fv_uri, value)
    ttls.append(ttl)

    # relate record to value
    ttl = """{0} {1} "{2}" .""".format(record_uri, data_prop_uri, value)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


def translate_data_to_ttl(filepath, base_uri="", ontology_uri="", imports=""):
    # ceate dataframe from demo data
    df = pds.ExcelFile(filepath).parse()

    # just get table and file name part of path
    tablename = get_tablename_from_file(filepath)
    filename = get_tablename_from_file(filepath, remove_ext=False)

    # specify ontology variables
    if len(base_uri) == 0:
        base_uri = "http://purl.obolibrary.org/obo/db_mapping.owl/{0}/".format(tablename)
    if len(ontology_uri) == 0:
        ontology_uri = "http://purl.obolibrary.org/obo/db_mapping.owl/{0}".format(filename)
    if len(imports) == 0:
        imports = "http://purl.obolibrary.org/obo/db_mapping.owl"

    # list to hold axioms
    axioms = []

    # add prefixes
    axioms.append(ttl_prefixes(tablename, base_uri, ontology_uri, imports=imports))

    # add table
    table_uri = get_table_uri()
    axioms.append(ttl_table(table_uri))

    # add fields
    fields = list(df.columns) # get list of fields
    axioms.append(ttl_fields(table_uri, fields))

    # add records and values
    axioms.append(ttl_records(df, table_uri, tablename))

    return axioms

### run code
axioms = translate_data_to_ttl("patients_1.xlsx")
print_axioms(axioms)