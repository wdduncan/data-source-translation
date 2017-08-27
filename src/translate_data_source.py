import pandas as pds
from uri_functions import *
from textwrap import dedent
from data_operations import *


@print_output()
def ttl_prefixes(filname):
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
                @prefix filename: <table/{0}> .
                @prefix field: <field/{0}/> .
                @prefix field_value: <field_value/{0}/> .
                @prefix fv: <field_value/{0}/> .
                @prefix record: <record/{0}/> .
                @prefix data_property: <data_property/{0}/> .

                # imports db mapping ontology
                [rdf:type owl:Ontology ;
                   owl:imports <http://purl.obolibrary.org/obo/db_mapping.owl> ] .
                """.format(filname))

    return ttl

@print_output()
def ttl_table(table_uri, filename):
    ttls = []
    ttls.append('# axioms to create table')

    # create table class
    ttl = 'filename: rdf:type owl:Class; rdfs:subClassOf :table .'
    ttls.append(ttl)

    #  create instance of table
    ttl = table_uri + ' rdf:type filename: .'
    ttls.append(ttl)

    # join all ttl statements
    ttl = '\n'.join(ttls)
    return ttl

@print_output()
def ttl_fields(table_uri, fields):
    ttls = []
    ttls.append('\n# axioms to create fields')

    for field in fields:
        ttl = ttl_field(table_uri, field) # create ttl for that field
        ttls.append(ttl)

        ttl = ttl_field_data_property(field) # create data property field for that field
        ttls.append(ttl)

    # join all ttl statements
    ttl = '\n'.join(ttls)
    return ttl

@print_output()
def ttl_field(table_uri, field):
    ttls = []

    # create field class
    class_uri = 'field:' + field
    ttl = class_uri + ' rdf:type owl:Class; rdfs:subClassOf :field .'
    ttls.append(ttl)

    # create instance of field class
    field_uri = 'field:' + field + '_i'  # uri for instance of field
    ttl = field_uri + ' rdf:type ' + class_uri + ' .'
    ttls.append(ttl)

    # field is member of table
    ttl = field_uri + ' :member_of ' + table_uri + ' .'
    ttls.append(ttl)


    # join all ttl statements
    ttl = '\n'.join(ttls)
    return ttl

@print_output()
def ttl_field_data_property(field):
    # create data property field
    prop_uri = 'data_property:' + field + '_data_value'
    ttl = prop_uri + ' rdf:type owl:DatatypeProperty .'

    return ttl

@print_output()
def ttl_records(df, table_uri, filename):
    ttls = []
    ttls.append('\n# axioms to create records')

    fields = list(df.columns)  # get list of fields
    for record_idx, record in enumerate(df.itertuples(), 1):
        # create instance of record
        record_uri = 'record:' + filename + '_record_' + str(record_idx)
        ttl = record_uri  + ' rdf:type :record .'
        ttls.append(ttl)

        ttl = record_uri  + ' :member_of ' + table_uri + ' .'
        ttls.append(ttl)


    # join all ttl statements
    ttl = '\n'.join(ttls)
    return ttl

@print_output()
def ttl_field_values(record, record_uri, fields):
    ttls = []

    for value_idx, value in enumerate(record):
        if value_idx > 0:
            field_name = fields[value_idx - 1]
            field_uri = 'field:' + field_name + '_i'  # uri for instance of field
            prop_uri = 'data_property:' + field_name + '_data_value'

            ttl = ttl_field_value(record, value, record_uri, field_uri, field_name, prop_uri)
            ttls.append(ttl)

    # join all ttl statements
    ttl = '\n'.join(ttls)
    return ttl

@print_output()
def ttl_field_value(record_idx, value, record_uri, field_uri, field_name, prop_uri):
    ttls = []

    # print record
    # print value_idx, value
    # print value_idx - 1
    # print fields
    # print fields[value_idx - 1]
    value_uri = 'field_value:' + field_name + '_value_' + str(record_idx)

    ttl = value_uri + ' rdf:type :field_value .'
    ttls.append(ttl)

    ttl = value_uri + ' :member_of ' + record_uri + ' .'
    ttls.append(ttl)

    ttl = value_uri + ' :member_of ' + field_uri + ' .'
    ttls.append(ttl)

    # field_uri = get_uri(filename + '/field/' + field + '_' + str(record_idx))
    # ttl = value_uri + ' :member_of ' + field_uri
    # axioms.append(ttl)
    # print ttl

    # join all ttl statements
    ttl = '\n'.join(ttls)
    return ttl


def translate_data_to_ttl(filepath):
    # ceate dataframe from demo data
    df = pds.ExcelFile(filepath).parse()

    # just get the file name part of path
    filename = get_filename(filepath)

    # list to hold axioms
    axioms = []

    # add prefixes
    axioms.append(ttl_prefixes(filename))

    # add table
    table_uri = get_table_uri()
    axioms.append(ttl_table(table_uri, filename))

    # add fields
    fields = list(df.columns) # get list of fields
    axioms.append(ttl_fields(table_uri, fields))

    # add records
    axioms.append(ttl_records(df, table_uri,filename))


        # for value_idx, value in enumerate(record):
        #     if value_idx > 0:
        #         # print record
        #         # print value_idx, value
        #         # print value_idx - 1
        #         # print fields
        #         # print fields[value_idx - 1]
        #         value_uri = get_uri(filename + '/field_value/' + fields[value_idx - 1] + '_value_' + str(record_idx))
        #         ttl = value_uri + ' rdf:type :field_value .'
        #         axioms.append(ttl)
        #         print ttl
        #
        #         ttl = value_uri + ' :member_of ' + record_uri + ' .'
        #         axioms.append(ttl)
        #         print ttl
        #
        #         # field_uri = get_uri(filename + '/field/' + field + '_' + str(record_idx))
        #         # ttl = value_uri + ' :member_of ' + field_uri
        #         # axioms.append(ttl)
        #         # print ttl


        # create field values of record
        # for index in range(1, (len(fields)+1)): # note: need to add 1 to length of fields
        #     print # create instance of entity that is represented by the val
        #     entity_uri = get_uri('entity/' + filename + '/field' + str(index) + '/' + str(record_id))
        #     print entity_uri + ' rdf:type ' + get_uri('entity') + ' .'
        #
        #     # data that represents the entity
        #     print entity_uri + ' ' + get_uri('represented_by') + ' ' + "'" + str(record[index]) + "'" + ' .'
        #
        #     # relate entity to record
        #     print record_uri + ' ' + get_uri('denotes') + ' ' + entity_uri + ' .'
        #
        #     # relate field to record
        #     print get_uri(filename + '/field' + str(index)) + ' ' + get_uri('denotes') + ' ' + entity_uri + ' .'



translate_data_to_ttl('patients_1.xlsx')
