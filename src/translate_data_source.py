# coding=utf-8
import pandas as pds
from translation_lib.util.uri_util import *
from translation_lib.rdf.translation_operations import *
from rdflib import Graph, RDF, RDFS, OWL, Namespace, BNode, URIRef, Literal, XSD

def translate_excel(data_file, base):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()

    # build data graph
    g = make_graph_df(df, "http://purl.example.translation/")
    test_query(g) # test querying

    # return g.serialize()
    return g.serialize(format="turtle")



def make_graph_df(df, data_namespace):
    # namespaces for data source ontology
    dst = Namespace("http://purl.data-source-translation.org/") # base uri
    dp = Namespace(dst + "data_property/") # data properties
    op = Namespace(dst + "object_property/") # object properties

    # namespaces for data being translated
    data = Namespace(parse_base_uri(data_namespace)) # base uri
    rv = Namespace(data + "data_property/record_value/")  # record values (shortcut)
    fv = Namespace(data + "data_property/field_value/")  # field values (shortcut)

    # declare graph to hold triples
    g = Graph()

    # create a maps of:
    #   field names -> uris
    #   field names -> field value uris
    #   field names -> record value uris
    fmap = make_field_uri_map(data.field, list(df.columns))
    rv_map = make_field_uri_map(rv, list(df.columns))
    fv_map = make_field_uri_map(fv, list(df.columns))

    # declare fields in field map
    for field_uri in fmap.values():
        g.add((field_uri, RDF.type, OWL.NamedIndividual))
        g.add((field_uri, RDF.type, dst.data_field))

    # declare record value and field value data properties (shortcut properties)
    # these properties help make querying easier
    for col_name in list(df.columns):
        rv_uri =  make_uri(rv.field, col_name)
        g.add((rv_uri, RDF.type, OWL.DatatypeProperty))
        g.add((rv_uri, RDFS.subPropertyOf, dp.record_value))

        fv_uri = make_uri(fv.field, col_name)
        g.add((fv_uri, RDF.type, OWL.DatatypeProperty))
        g.add((fv_uri, RDFS.subPropertyOf, dp.record_value))

    # translate data
    for (idx, series) in df.iterrows():
        record_uri = make_uri(data.record, idx)
        g.add((record_uri, RDF.type, OWL.NamedIndividual))
        g.add((record_uri, RDF.type, dst.data_record))

        for (field_name, value) in series.iteritems():
            field_uri = fmap[field_name]
            data_item_uri = make_uri(record_uri, field_name)

            # declare data item (and value)
            g.add((data_item_uri, RDF.type, OWL.NamedIndvidual))
            g.add((data_item_uri, RDF.type, dst.data_item))
            g.add((data_item_uri, dst.has_value, Literal(value)))

            # relate data item to record and field
            g.add((record_uri, dst.has_member, data_item_uri))
            g.add((field_uri, dst.has_member, data_item_uri))

            # relate record and field to value (shortcuts)
            rv_uri = rv_map[field_name]
            fv_uri = fv_map[field_name]
            g.add((record_uri, rv_uri, Literal(value)))
            g.add((fmap[field_name], fv_uri, Literal(value)))

    return g

def test_query(g):
    results = \
        g.query("""
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix field: <http://purl.data-source-translation.org/data_field>
            prefix fv: <http://purl.example.translation/data_property/field_value/> 
            prefix ns2: <http://purl.example.translation/data_property/field_value/> 
            prefix ns3: <http://purl.example.translation/data_property/record_value/> 
            
            select ?field ?v where {
              ?field a field: .
              # ?field a ?type .
              ?field ns2:patient_id ?v .}
            """)
    # for result in results: print result

    results = \
        g.query("""
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix field: <http://purl.data-source-translation.org/data_field>
            prefix fv: <http://purl.example.translation/data_property/field_value/> 
            prefix ns2: <http://purl.example.translation/data_property/field_value/> 
            prefix ns3: <http://purl.example.translation/data_property/record_value/> 
            
            construct {
              ?field rdfs:label ?v
            } where {
              ?field a field: .
              ?field ns2:patient_id ?v .}
            """)

    for result in results: print result

translate_excel("test_data/patients_1.xlsx", "http://purl.example.translation/")
# print translate_excel("test_data/patients_1.xlsx", "http://purl.example.translation/")
