# coding=utf-8
import pandas as pds
from translation_lib.util.uri_util import *
from translation_lib.rdf.translation_operations import *
from rdflib import Graph, RDF, RDFS, OWL, Namespace, BNode, URIRef, Literal, XSD
from rdflib.namespace import NamespaceManager
from translate_data_source import make_data_graph_df

def translate_metadata_excel(data_file, metadata_base_uri, target_namespace_uri):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()
    data_g = make_data_graph_df(df, metadata_base_uri) # build data graph
    meta_g = make_metadata_graph(data_g, metadata_base_uri, target_namespace_uri) # build metadata graph

    return meta_g.serialize(format="turtle")


def translate_data_specification_excel(data_file, metadata_base_uri, target_namespace_uri):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()
    data_g = make_data_graph_df(df, metadata_base_uri)  # build data graph
    meta_g = make_metadata_graph(data_g, metadata_base_uri, target_namespace_uri)  # build metadata graph
    spec_g = make_data_specification_graph(meta_g, metadata_base_uri, target_namespace_uri) # build specification

    return spec_g.serialize(format="turtle")

def translate_data_to_graph_excel(data_file, metadata_base_uri, target_namespace_uri):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()
    data_g = make_data_graph_df(df, metadata_base_uri)  # build data graph
    meta_g = make_metadata_graph(data_g, metadata_base_uri, target_namespace_uri)  # build metadata graph
    # spec_g = make_data_specification_graph(meta_g, metadata_base_uri, target_namespace_uri) # build specification

    merge_g = data_g + meta_g #+ spec_g

    return merge_g.serialize(format="turtle")


def make_metadata_graph(graph, metadata_namespace_uri, target_namespace_uri, data_source="", data_source_base_uri=""):
    """
    Takes as input a rdflib graph with metadata information and returns a graph with metadata relations added.
    :param graph: rdflib data graph containing metadata information
    :return: rdflib graph with metadata relations
    """

    metadata_graph = Graph()

    # namespaces for data source ontology
    dst = Namespace("http://purl.data-source-translation.org/")  # base uri
    dp = Namespace(dst + "data_property/")  # data properties
    op = Namespace(dst + "object_property/")  # object properties
    annotation = Namespace(dst + "annotation/")  # object properties

    # namespaces translated metadata
    metadata = Namespace(parse_base_uri(metadata_namespace_uri))  # base uri
    fv = Namespace(metadata + "data_property/field_value/")  # field values (shortcut)
    fdi = Namespace(metadata + "object_property/field_data_item/")  # field data items (shortcut)

    ## add metadata relations for records
    data_records = graph.subjects(RDF.type, dst.data_record)
    for record in data_records:
        ## add relation that record is about the metadata is about the field (uri)
        field_name = graph.value(record, fv.field_name)
        field_uri = make_uri(target_namespace_uri, field_name)
        metadata_graph.add((record, op.is_about_field, field_uri))
        metadata_graph.add((record, op.specifies, field_uri)) # use 'specifies' relation

        ## add relation that that record is about the data item that has the field's value
        data_item = graph.value(record, fdi.value)
        metadata_graph.add((record, op.is_about_data_item, data_item))

        # add semantic specification information to metadata graph
        sem_type_value = graph.value(record, fv.semantic_type)
        sem_type_uri = URIRef(sem_type_value)
        metadata_graph.add((record, annotation.semantic_type, sem_type_uri)) # add semantic type

        # add semantic specification information to metadata graph
        sem_label_value = graph.value(record, fv.semantic_label)
        metadata_graph.add((record, annotation.semantic_label, sem_label_value)) # add semantic label

        # add semantic specification information to metadata graph
        sem_source_value = graph.value(record, fv.semantic_source)
        sem_source_uri = URIRef(sem_source_value)
        metadata_graph.add((record, annotation.semantic_source, sem_source_uri))

        # get value of data item and add specified value information
        value = graph.value(data_item, dp.data_value)
        metadata_graph.add((record, dp.specified_value, Literal(value)))

    return metadata_graph

def make_data_specification_graph(metadata_graph, metadata_namespace_uri, target_namespace_uri, data_source="", data_source_base_uri=""):

    specification_graph = Graph()

    # namespaces for data source ontology
    dst = Namespace("http://purl.data-source-translation.org/")  # base uri
    dp = Namespace(dst + "data_property/")  # data properties
    op = Namespace(dst + "object_property/")  # object properties

    # namespaces translated metadata
    metadata = Namespace(parse_base_uri(metadata_namespace_uri))  # base uri
    fv = Namespace(metadata + "data_property/field_value/")  # field values (shortcut)
    fdi = Namespace(metadata + "object_property/field_data_item/")  # field data items (shortcut)

    ## add specifications that define fields
    about_field_records = metadata_graph.subject_objects(op.is_about_field)
    for record in about_field_records:
        spec_uri = make_uri(str(record[0]), "specification") # index 0 is the record
        specification_graph.add((spec_uri, RDF.type, OWL.NamedIndividual))
        specification_graph.add((spec_uri, RDF.type, dst.data_specification))
        specification_graph.add((spec_uri, op.defines, record[1])) # index 1 is the field

    ## add specified values for specifications
    about_data_items_records = metadata_graph.subject_objects(op.is_about_data_item)
    for record in about_data_items_records:
        spec_uri = make_uri(str(record[0]), "specification")  # index 0 is the record
        value = metadata_graph.value(record[1], dp.data_value) #index 1 is the data item
        specification_graph.add((spec_uri, dp.specified_value, Literal(value)))

    return specification_graph

# translate_metadata_excel("test_data/simple_dental_data_specification.xlsx", "http://purl.example.metadata/", "http://purl.example.translation/")
# print translate_metadata_excel("test_data/simple_dental_data_specification.xlsx", "http://purl.example.metadata/", "http://purl.example.translation/")

# translate_data_specification_excel("test_data/simple_dental_data_specification.xlsx", "http://purl.example.metadata/", "http://purl.example.translation/")
# print translate_data_specification_excel("test_data/simple_dental_data_specification.xlsx", "http://purl.example.metadata/", "http://purl.example.translation/")

translate_data_to_graph_excel("test_data/simple_dental_data_specification.xlsx", "http://purl.example.metadata/", "http://purl.example.translation/")
# print translate_data_to_graph_excel("test_data/simple_dental_data_specification.xlsx", "http://purl.example.metadata/", "http://purl.example.translation/")