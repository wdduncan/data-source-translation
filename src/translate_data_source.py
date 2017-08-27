import pandas as pds
from uri_functions import *
from textwrap import dedent
from data_operations import *


# @print_output()()
def ttl_prefixes(tablename, ontology_uri):
    ttl = dedent("""\
                # axioms for prefixes'
                @base <http://purl.obolibrary.org/obo/db_mapping.owl/> .
                @prefix : <http://purl.obolibrary.org/obo/db_mapping.owl/> .
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
                @prefix table: <table/{0}/> .
                @prefix tablename: <table/{0}> .
                @prefix field: <field/{0}/> .
                @prefix field_value: <field_value/{0}/> .
                @prefix fv: <field_value/{0}/> .
                @prefix record: <record/{0}/> .
                @prefix data_property: <data_property/{0}/> .
                @prefix dv: <data_property/{0}/> .

                # set ontology uri and import db mapping ontology
                <{1}> rdf:type owl:Ontology ;
                      owl:imports <http://purl.obolibrary.org/obo/db_mapping.owl> .
                """.format(tablename, ontology_uri))

    return ttl

# @print_output()
def ttl_table(table_uri):
    ttls = ["# axioms to create table"]
    
    # create table class
    ttl = declare_class("tablename:", ":table")
    ttls.append(ttl)

    #  create instance of table
    ttl = declare_instance(table_uri, "tablename:")
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_output()
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

# @print_output()
def ttl_field(table_uri, field_name):
    ttls = []

    # create field class
    class_uri = "field:{0}".format(field_name)
    ttl = declare_class(class_uri, ":field")
    ttls.append(ttl)

    # create instance of field class
    field_uri = "field:{0}_i".format(field_name)  # uri for instance of field
    ttl = declare_instance(field_uri, class_uri, table_uri)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_output()
def ttl_field_data_property(field_name):
    # create data property field
    data_prop_uri = get_data_prop_uri(field_name)
    ttl = declare_data_property(data_prop_uri)

    return ttl

@print_output()
def ttl_records(df, table_uri, tablename):
    ttls = []
    ttls.append('\n# axioms to create records and values')

    # create record class for this table
    class_uri = "record:{0}_record".format(tablename)
    ttl = declare_class(class_uri, ":record")
    ttls.append(ttl + "\n")  # add new line to help visual inspection

    fields = list(df.columns)  # get list of fields
    for record_idx, record in enumerate(df.itertuples(), 1):
        # create instance of record
        record_uri = get_record_uri(tablename, record_idx)
        ttl = declare_instance(record_uri, class_uri, table_uri)
        ttls.append(ttl)

        ttl = ttl_field_values(record, record_idx, record_uri, fields)
        ttls.append(ttl + "\n") # add new line to help visual inspection

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_output()
def ttl_field_values(record, record_idx, record_uri, fields):
    ttls = []

    for value_idx, value in enumerate(record):
        if value_idx > 0:
            field_name = fields[value_idx - 1]
            field_uri = get_field_uri(field_name)  # uri for instance of field
            data_prop_uri = get_data_prop_uri(field_name) # uri for field as data property

            ttl = ttl_field_value(record_idx, value, record_uri, field_uri, field_name, data_prop_uri)
            ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_output()
def ttl_field_value(record_idx, value, record_uri, field_uri, field_name, data_prop_uri):
    ttls = []

    field_value_uri = get_field_value_uri(field_name, record_idx)
    ttl = "{0} rdf:type :field_value .".format(field_value_uri)
    ttls.append(ttl)

    ttl = "{0} :member_of {1}, {2} .".format(field_value_uri, record_uri, field_uri)
    ttls.append(ttl)

    ttl = """{0} :has_data_value "{1}" .""".format(field_value_uri, value)
    ttls.append(ttl)

    ttl = record_uri + ' ' + data_prop_uri + ' ' + str(value) + ' .'
    ttl = """{0} {1} "{2}" .""".format(record_uri, data_prop_uri, value)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


def translate_data_to_ttl(filepath):
    # ceate dataframe from demo data
    df = pds.ExcelFile(filepath).parse()

    # just get the file name part of path
    tablename = get_tablename_from_file(filepath)

    # list to hold axioms
    axioms = []

    # add prefixes
    filename = get_tablename_from_file(filepath, remove_ext=False)
    axioms.append(ttl_prefixes(tablename, "http://purl.obolibrary.org/obo/db_mapping.owl/" + filename))

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
# print_axioms(axioms)