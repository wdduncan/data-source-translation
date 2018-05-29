# coding=utf-8
import pandas as pds
from translation_lib.util.uri_util import *
from translation_lib.rdf.translation_operations import *
from rdflib import Graph, RDF, RDFS, OWL, Namespace, BNode, URIRef, Literal, XSD
from rdflib.namespace import NamespaceManager


def translate_metadata_excel(data_file, base):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()

    # build data graph
    data_g = make_graph_df(df, base)
    # print(data_g.serialize(format="turtle"))

    meta_g = make_metadata_graph(data_g, base)
    # return g.serialize()
    # return meta_g.serialize(format="turtle")


def make_graph_df(df, data_namespace_uri, data_source="", data_source_base_uri=""):
    """
    :param df: Pandas dataframe to be trasformed in rdflib graph
    :param data_namespace_uri: Base URI of the graph containing the translated data
    :param data_source: Name of the data source containing the data
    :param data_source_base_uri: Base URI of the data source if you wish it to be different than the data URI
    :return: Rdflib graph of triples representing the data

    This function transforms a Pandas dataframe into a Rdflib graph. The translation scheme is based on the data source
    translation ontology found at https://github.com/wdduncan/data-source-translation.
    """
    # namespaces for data source ontology
    dst = Namespace("http://purl.data-source-translation.org/")  # base uri
    dp = Namespace(dst + "data_property/")  # data properties
    op = Namespace(dst + "object_property/")  # object properties

    # namespaces for data being translated
    data = Namespace(parse_base_uri(data_namespace_uri))  # base uri
    # rv = Namespace(data + "data_property/record_value/")  # record values (shortcut) BD: Not using record value (5/18/2018)
    fv = Namespace(data + "data_property/field_value/")  # field values (shortcut)

    # create datasource uri
    data_source_uri = None
    if len(data_source.strip()) > 0:
        data_source = parse_python_name(data_source)
        if (data_source_base_uri.strip()) > 0:
            data_source_uri = make_uri(data_source_base_uri, data_source)
        else:
            data_source_uri = make_uri(data, data_source)

    # declare graph to hold triples
    g = Graph(identifier=data_namespace_uri)

    # add data source to ontology
    if data_source_uri:
        g.add((data_source_uri, RDF.type, OWL.NamedIndividual))

    # create a maps of:
    #   field names -> uris
    #   field names -> field value uris
    #   field names -> record value uris
    # rv_map = make_field_uri_map(rv, list(df.columns)) # BD: Not using record value (5/18/2018)
    fmap = make_field_uri_map(data.data_field, list(df.columns))
    fv_map = make_field_uri_map(fv, list(df.columns))

    # declare fields in field map
    for field_uri in fmap.values():
        g.add((field_uri, RDF.type, OWL.NamedIndividual))
        g.add((field_uri, RDF.type, dst.data_field))

    # declare record value and field value data properties (shortcut properties)
    # these properties help make querying easier
    for col_name in list(df.columns):
        # BD: Not using record value (5/18/2018)
        # rv_uri =  make_uri(rv.field, col_name)
        # g.add((rv_uri, RDF.type, OWL.DatatypeProperty))
        # g.add((rv_uri, RDFS.subPropertyOf, dp.record_value))

        fv_uri = make_uri(fv, col_name)
        g.add((fv_uri, RDF.type, OWL.DatatypeProperty))
        g.add((fv_uri, RDFS.subPropertyOf, dp.field_value))

    # translate data
    for (idx, series) in df.iterrows():
        record_uri = make_uri(data.data_record, idx)
        g.add((record_uri, RDF.type, OWL.NamedIndividual))
        g.add((record_uri, RDF.type, dst.data_record))

        # link reord to data source (if given)
        if data_source_uri:
            g.add(data_source_uri, dst.has_member, record_uri)

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
            # rv_uri = rv_map[field_name] # BD: Not using record value (5/18/2018)
            # g.add((record_uri, rv_uri, Literal(value))) # BD: Not using record value (5/18/2018)

            # relate record to value in field (shortcut)
            fv_uri = fv_map[field_name]
            g.add((fmap[field_name], fv_uri, Literal(value)))
            g.add((record_uri, fv_uri, Literal(value)))

    return g


def make_metadata_graph(graph, data_namespace_uri, data_source="", data_source_base_uri=""):
    """

    :param graph: rdflib data graph
    :return: rdflib graph with metadata relations
    """
    # print(graph.identifier)
    # for n in graph.namespace_manager.namespaces(): print(n)

    meta_graph = Graph()

    # namespaces for data source ontology
    dst = Namespace("http://purl.data-source-translation.org/")  # base uri
    dp = Namespace(dst + "data_property/")  # data properties
    op = Namespace(dst + "object_property/")  # object properties

    # namespaces translated data
    data = Namespace(parse_base_uri(data_namespace_uri))  # base uri
    data_field = Namespace(data + "data_field/")
    fv = Namespace(data + "data_property/field_value/")  # field values (shortcut)

    # values = graph.subjects(RDFS.subPropertyOf, dp.field_value)
    # for v in values: print v

    print graph.serialize(format="turtle")
    # for data_item in graph.objects(dst.data_record, dp.has_member): print data_item
    data_fields = graph.subjects(RDF.type, dst.data_field)
    field_data_items = graph.objects(data_field.field, dst.has_member) # find field daga items

    # print(field_data_items)
    # for f in field_data_items: print f

    # field_data_items = None
    # for data_field in data_fields:
    #     short_uri = str(data_field).split("/")[-1]
    #     if short_uri == "field":
    #         field_data_items = graph.objects(data_field, dst.has_member)
    #         break

    data_records = graph.subjects(RDF.type, dst.data_record)
    # for record in data_records:
    #     # items = graph.objects(record, dst.has_member)
    #     # for i in items: print graph.value(i, dst.has_value)
    #     for s, p, o in graph.triples((record, None, None)):
    #         print s, p, o

    # data_item = graph.value(data_field, dst.has_member)
    # print data_item
    # value = graph.value(data_item, dst.has_value)
    # print value

translate_metadata_excel("test_data/simple_dental_data_specification.xlsx", "http://purl.example.metadata/")
# print translate_metadata_excel("test_data/simple_dental_data_specification.xlsx", "http://purl.example.metadata/")
