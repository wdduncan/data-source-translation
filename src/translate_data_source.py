import pandas as pds

def translate_data_to_ttl(filename):
    # ceate dataframe from demo data
    df = pds.ExcelFile(filename).parse()

    # testing...
    # print df
    axioms = []

    print '# axioms for prefixes'
    ttl = \
"""
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

# imports db mapping ontology
[rdf:type owl:Ontology ;
   owl:imports <http://purl.obolibrary.org/obo/db_mapping.owl> ] .
"""

    axioms.append(ttl)
    print ttl

    print '\n# axioms to create table'

    # create table class
    class_uri = uri('table/' + filename)
    ttl = class_uri + ' rdf:type owl:Class .'
    axioms.append(ttl)
    print ttl

    ttl = class_uri + ' rdfs:subClassOf :table .'
    axioms.append(ttl)
    print ttl

    #  create instance of table
    table_uri = uri('table/' + filename + '_instance')
    ttl = table_uri + ' rdf:type ' + class_uri + ' .'
    axioms.append(ttl)
    print ttl

    print '\n# axioms to create field instances'

    # get list of fields
    fields = list(df.columns)

    for record_idx, field in enumerate(fields, 1):
        # create field classes
        class_uri = uri(filename + '/field/' + field)
        ttl = class_uri + ' rdf:type owl:Class .'
        axioms.append(ttl)
        print ttl

        ttl = class_uri + ' rdfs:subClassOf :field .'
        axioms.append(ttl)
        print ttl

        # create instance of field
        ttl = uri(filename + '/field/' + field + '_' + str(record_idx)) + ' rdf:type ' + class_uri + ' .'
        axioms.append(ttl)
        print ttl

        # field is member of table
        ttl = uri(filename + '/field/' + field + '_' + str(record_idx)) + ' :member_of ' + table_uri + ' .'
        axioms.append(ttl)
        print ttl

        # create data property fields
        prop_uri = uri(filename + '/data_property/' + field + '_data_value')
        ttl = prop_uri + ' rdf:type owl:DatatypeProperty .'
        axioms.append(ttl)
        print ttl

    print '\n# axioms to create records '
    for record_idx, record in enumerate(df.itertuples(), 1):
        # create instance of record
        # print record_id
        record_uri = uri(filename + '/record/record_' + str(record_idx))
        ttl = record_uri  + ' rdf:type :record .'
        axioms.append(ttl)
        print ttl

        ttl = record_uri  + ' :member_of ' + table_uri + ' .'
        axioms.append(ttl)
        print ttl

        for value_idx, value in enumerate(record):
            if value_idx > 0:
                # print record
                # print value_idx, value
                # print value_idx - 1
                # print fields
                # print fields[value_idx - 1]
                value_uri = uri(filename + '/field_value/' + fields[value_idx - 1] + '_value_' + str(record_idx))
                ttl = value_uri + ' rdf:type :field_value .'
                axioms.append(ttl)
                print ttl

                ttl = value_uri + ' :member_of ' + record_uri + ' .'
                axioms.append(ttl)
                print ttl

                # field_uri = uri(filename + '/field/' + field + '_' + str(record_idx))
                # ttl = value_uri + ' :member_of ' + field_uri
                # axioms.append(ttl)
                # print ttl


                # create field values of record
        # for index in range(1, (len(fields)+1)): # note: need to add 1 to length of fields
        #     print # create instance of entity that is represented by the val
        #     entity_uri = uri('entity/' + filename + '/field' + str(index) + '/' + str(record_id))
        #     print entity_uri + ' rdf:type ' + uri('entity') + ' .'
        #
        #     # data that represents the entity
        #     print entity_uri + ' ' + uri('represented_by') + ' ' + "'" + str(record[index]) + "'" + ' .'
        #
        #     # relate entity to record
        #     print record_uri + ' ' + uri('denotes') + ' ' + entity_uri + ' .'
        #
        #     # relate field to record
        #     print uri(filename + '/field' + str(index)) + ' ' + uri('denotes') + ' ' + entity_uri + ' .'


def uri(val):
    return "<http://purl.obolibrary.org/obo/db_mapping.owl/" + val + ">"

translate_data_to_ttl('patients_1.xlsx')