# coding=utf-8
import translation_lib.translation_ontology_functions_ttl as txf
import translation_lib.translation_operations_ttl as txo
import pandas as pds
import datetime as dtm
from translation_lib.uri_util import *
from rdflib import Graph, RDF, RDFS, OWL, Namespace, BNode, URIRef, Literal, XSD
import rdflib.extras.infixowl as rowl

def translate_excel(data_file, base):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()

    g = make_graph_df(df, "http://purl.example.translation/")
    return g.serialize(format="turtle")



def make_graph_df(df, data_namespace):
    dst = Namespace("http://purl.data-source-translation.org/")
    data = Namespace(data_namespace)

    g = Graph()

    # declare fields
    for field_name in list(df.columns):
        field_uri =  make_uri(data.field, field_name)
        g.add((field_uri, RDF.type, OWL.NamedIndividual))
        g.add((field_uri, RDF.type, dst.data_field))

    for (idx, series) in df.iterrows():
        record_uri = make_uri(data.record, idx)
        g.add((record_uri, RDF.type, OWL.NamedIndividual))
        g.add((record_uri, RDF.type, dst.data_record))

        for (field, value) in series.iteritems():
            field_uri = make_uri(data.field, field_name)
            data_uri = make_uri(record_uri, field)

            g.add((record_uri, dst.has_member, data_uri))
            g.add((record_uri, dst.has_member, data_uri))
            g.add((data_uri, dst.has_value, Literal(value)))

    return g


print translate_excel("test_data/patients_1.xlsx", "http://purl.example.translation/")
