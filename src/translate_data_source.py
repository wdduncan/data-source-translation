# coding=utf-8
import translation_lib.translation_ontology_functions_ttl as txf
import translation_lib.translation_operations_ttl as txo
import pandas as pds
import datetime as dtm
from rdflib import Graph, RDF, RDFS, OWL, Namespace, BNode, URIRef, Literal, XSD
import rdflib.extras.infixowl as rowl

def translate_excel(data_file, base):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()

    # create uris
    base = txo.format_base_uri(base) # base uri
    file_name = txo.format_data_file_name(data_file)  # file name
    file_uri = "<spreadsheet/{0}>".format(file_name) # file uri
    ontology_uri = "{0}/{1}.data.owl".format(base, file_name) # ontology uri

    # prefixes
    axioms = [txo.prefixes(base, ontology_uri)]

    axioms.append("# declare data file")
    axioms.append(txf.declare_individual(file_uri, txf.spreadsheet_uri(), file_name))

    # declare fields as data relations
    axioms.append(txo.declare_df_fields(df))

    # declare data records
    axioms.append(txo.translate_df_records(df))

    return '\n'.join(axioms)

def test_rdf():
    df = pds.ExcelFile("test_data/patients_1.xlsx").parse()
    dfg = make_data_df(df)
    print dfg.serialize(format="turtle")


def make_data_df(df):
    def make_uri(base_uri, entity_uri="", base_end_char="/"):
        if base_uri.endswith("/") or base_uri.endswith("#"):
            uri = "%s%s" % (str(base_uri), entity_uri)
            return URIRef(uri.strip())
        elif len(str(entity_uri)) > 0:
            uri = "%s%s%s" % (str(base_uri), base_end_char, str(entity_uri).strip())
            return URIRef(uri.strip())
        else:
            return URIRef(str(base_uri).strip())

    n = Namespace("http://example.org/people/")
    dst = Namespace("http://purl.data-source-translation.org/")
    record = Namespace("http://purl.data-source-translation.org/data_record/")
    data = Namespace("http://purl.example.translation/")

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

# print translate_excel("test_data/patients_1.xlsx", "http://purl.example.translation/")
test_rdf()
