import pandas as pds
from translation_lib.util.uri_util import *
from translation_lib.rdf.translation_operations import *
from rdflib import Graph, RDF, RDFS, OWL, Namespace, BNode, URIRef, Literal, XSD
from translation_lib.util.ontology_class.data_source_ontology_generated_class_rdflib import data_source_ontology


def translate_excel(data_file, base):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()

    # build data graph
    g = make_data_graph_df(df, "http://purl.example.translation/", "http://foo.com")
    # test_query(g) # test querying

    print g.serialize(format="turtle")
    return g


def make_data_graph_df(df, data_namespace_uri, data_source="", data_source_base_uri=""):
    # namespaces for data being translated
    data = Namespace(parse_base_uri(data_namespace_uri))  # base uri
    fv = Namespace(data + "data_property/field_value/")  # field values (shortcut)
    fdi = Namespace(data + "object_property/field_data_item/")  # field data items (shortcut)

    dst = data_source_ontology()

    # create datasource uri
    data_source_uri = None
    if len(data_source.strip()) > 0:
        data_source = parse_python_name(data_source)
        if (data_source_base_uri.strip()) > 0:
            data_source_uri = make_uri(data_source_base_uri, data_source)
        else:
            data_source_uri = make_uri(data, data_source)

    # declare graph to hold triples
    graph = Graph(identifier=data_namespace_uri)

    # add data source to ontology
    if data_source_uri:
        dst.declare_individual(graph, data_source_uri, dst.data_source_uri)

    # create a maps of:
    #   field names -> uris
    #   field names -> field value uris (data properties)
    #   field names -> field data item uris (object properties)
    field_map = make_field_uri_map(data.data_field, list(df.columns))
    fv_map = make_field_uri_map(fv, list(df.columns))
    fdi_map = make_field_uri_map(fdi, list(df.columns))

    # declare fields in field map
    for field_uri in field_map.values():
        dst.declare_individual(graph, field_uri, dst.data_field_uri)

    # declare field value data and field data item properties (shortcut properties)
    # these properties help make querying easier
    for col_name in list(df.columns):
        fv_uri = make_uri(fv, col_name)
        dst.declare_data_property(graph, fv_uri, dst.field_value_uri)

        fdi_uri = make_uri(fdi, col_name)
        dst.declare_object_property(graph, fdi_uri, dst.has_member_uri)

    # translate data
    for (idx, series) in df.iterrows():
        record_uri = make_uri(data.data_record, idx)
        dst.declare_individual(graph, record_uri, dst.data_record_uri)

        # link reord to data source (if given)
        if data_source_uri:
            dst.has_member(graph, data_source_uri, record_uri)

        for (field_name, value) in series.iteritems():
            field_uri = field_map[field_name]
            data_item_uri = make_uri(record_uri, field_name)

            # declare data item (and value)
            dst.declare_individual(graph, data_item_uri, dst.data_item_uri)
            dst.data_value(graph, data_item_uri, value)

            # relate data item to record and field
            dst.has_member(graph, record_uri, data_item_uri)
            dst.has_member(graph, field_uri, data_item_uri)

            # relate record to value (i.e., field value) (shortcut)
            fv_uri = fv_map[field_name]
            graph.add((record_uri, fv_uri, Literal(value)))

            # relate record to data item (field data item) (shortcut)
            fdi_uri = fdi_map[field_name]
            graph.add((record_uri, fdi_uri, data_item_uri))

    return graph

translate_excel("test_data/patients_1.xlsx", "http://purl.example.translation/")