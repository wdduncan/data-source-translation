import pandas as pds
from data_mapping.translate_data_source import translate_excel_to_ttl
from .translate_metadata import translate_metadata_excel, translate_data_to_graph_excel
import data_mapping.translation_lib.util.simple_dental_ontology_generated_functions_rdflib as ont
import data_mapping.translation_lib.util.data_source_ontology_generated_functions_rdflib as dso
from data_mapping.translation_lib.util.uri_util import *
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef
from textwrap import dedent

## syntax to import modules in python 3
from src.translation_lib.util import *
from src.translate_metadata import translate_metadata_excel, translate_data_to_graph_excel
from src.translation_lib.util import simple_dental_ontology_generated_functions_rdflib as ont
from src.translation_lib.util import data_source_ontology_generated_functions_rdflib as dso
from src.translation_lib.util.uri_util import *
from uuid import uuid4


def make_record_value_mapper(graph, field_uri_map):
    def return_fn(record, strip_value=True):
        unique_id = rdflib.URIRef("http://ex.com/uuid")  # uris for relations/properties


        r_bnode = rdflib.BNode() ## blank node for record
        graph.add( (r_bnode,rdflib.RDF.type, rdflib.URIRef("http://ex.com/record")))
        graph.add( (r_bnode, unique_id, rdflib.Literal(str(uuid4()))) ) ## uuid for record

        for field_name in field_uri_map:
            uri = rdflib.URIRef(field_uri_map[field_name])
            if strip_value:
                value = str(record[field_name]).strip()
            graph.add( (r_bnode, uri, rdflib.Literal(value)) )
        return graph

    return return_fn


def make_record_datum_mapper(graph, field_uri_map, field_uuid_map=[]):
    has_member = rdflib.URIRef("http://ex.com/has_member") # uris for relations/properties
    literal_value = rdflib.URIRef("http://ex.com/literal_value")
    unique_id = rdflib.URIRef("http://ex.com/uuid")

    for field_name in field_uri_map:
        uri = rdflib.URIRef(field_uri_map[field_name])
        graph.add ( (uri, rdflib.RDF.type, rdflib.URIRef("http://ex.com/field") ) )
        if len(field_uuid_map) < 1: ## uuid for field
            graph.add( (uri, unique_id, rdflib.Literal(str(uuid4()))) )
        else:
            graph.add((uri, unique_id, rdflib.Literal(str(field_uuid_map[field_name]))))


    def return_fn(record, strip_value=True):
        # print("####### fmap: %s" % field_uri_map)
        r_bnode = rdflib.BNode() ## blank node for record
        graph.add( (r_bnode,rdflib.RDF.type, rdflib.URIRef("http://ex.com/record")))
        graph.add( (r_bnode, unique_id, rdflib.Literal(str(uuid4()))) )  ## uuid for record

        for field_name in field_uri_map:
            d_bnode = rdflib.BNode()  ## blank node for datum
            graph.add((d_bnode, rdflib.RDF.type, rdflib.URIRef("http://ex.com/datum")))
            graph.add( (d_bnode, unique_id, rdflib.Literal(str(uuid4()))) )  ## uuid for datum

            field_uri = rdflib.URIRef(field_uri_map[field_name])
            if strip_value:
                value = str(record[field_name]).strip()
            graph.add( (r_bnode, has_member, d_bnode) )
            graph.add( (field_uri, has_member, d_bnode) )
            graph.add( (d_bnode, literal_value, rdflib.Literal(value)) )
        return graph

    return return_fn


def make_data_attribute_mapper(graph, attribute_uri_map, attribute_uuid_map=[]):
    literal_value = rdflib.URIRef("http://ex.com/literal_value") # uris for relations/properties
    uuid_uri = rdflib.URIRef("http://ex.com/uuid")

    graph.add( (literal_value, rdflib.RDF.type,rdflib.OWL.DatatypeProperty) )
    graph.add( (uuid_uri, rdflib.RDF.type,rdflib.OWL.AnnotationProperty) )

    for attribute_name in attribute_uri_map:
        uri = rdflib.URIRef(attribute_uri_map[attribute_name])
        graph.add ( (uri, rdflib.RDF.type, rdflib.OWL.ObjectProperty ) )
        graph.add( (uri, rdflib.RDFS.subPropertyOf, rdflib.URIRef("http://ex.com/data_attribute")))
        # if len(attribute_uuid_map) < 1: ## uuid for attribute
        #     graph.add( (uri, uuid_uri, rdflib.Literal(str(uuid4()))) )
        # else:
        #     graph.add((uri, uuid_uri, rdflib.Literal(str(attribute_uuid_map[attribute_name]))))


    def data_attribute_mapper(record, strip_value=True):
        # record_uri = rdflib.BNode() ## blank node for data record
        # record_uri = rdflib.URIRef("http://ex.com/" + str(uuid4()))
        record_uri = rdflib.URIRef("http://ex.com/record_" + str(record.name))
        graph.add( (record_uri,rdflib.RDF.type, rdflib.URIRef("http://ex.com/data_record")))
        # graph.add( (record_uri, uuid_uri, rdflib.Literal(str(uuid4()))) )  ## uuid for record

        for attribute_name in attribute_uri_map:
            # datum_uri = rdflib.BNode()  ## blank node for datum
            # datum_uri = rdflib.URIRef("http://ex.com/" + str(uuid4()))
            datum_uri = rdflib.URIRef("http://ex.com/" + str(attribute_name) + "_" + str(record.name))
            graph.add((datum_uri, rdflib.RDF.type, rdflib.URIRef("http://ex.com/datum")))
            # graph.add( (datum_uri, uuid_uri, rdflib.Literal(str(uuid4()))) )  ## uuid for datum

            attribute_uri = rdflib.URIRef(attribute_uri_map[attribute_name])
            value = str(record[attribute_name])
            if strip_value:
                value = str(record[attribute_name]).strip()
            graph.add( (record_uri, attribute_uri, datum_uri) )
            graph.add( (datum_uri, literal_value, rdflib.Literal(value)) )
        return graph

    return data_attribute_mapper

def query_prefixes():
    return dedent(
        """
        base <http://purl.example.translation/>
        prefix : <http://purl.example.translation/>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix owl: <http://www.w3.org/2002/07/owl#>
        prefix obo: <http://purl.obolibrary.org/obo/>
        prefix dst: <http://purl.data-source-translation.org/>
        prefix dp: <http://purl.data-source-translation.org/data_property/>
        prefix op: <http://purl.data-source-translation.org/object_property/>
        prefix annotation: <http://purl.data-source-translation.org/annotation/>
        prefix field: <http://purl.data-source-translation.org/data_field>
        prefix record: <http://purl.data-source-translation.org/data_record>
        prefix fv: <http://purl.example.translation/data_property/field_value/>                 
        prefix data: <http://purl.example.translation/>
        prefix meta: <http://purl.example.metadata/>
        prefix ont: <http://purl.obolibrary.org/obo/simple-dental-ontology.owl/>

        """)

def construct_query_for_patients(graph):
    query_str = query_prefixes()
    query_str += \
    """
    ## needs to run in graphdb to work
    ## rdflib can't use CONCAT
    construct {
        ?female_uri rdf:type ont:female_patient .
        ?male_uri rdf:type ont:male_patient .
    } where {
        {
            ?record fv:patient_id|fv:subject_id ?female_id;
                    fv:gender|fv:sex ?female_value .
            values ?female_value {"F" "Female"}
        } union {
            ?record fv:patient_id|fv:subject_id ?male_id;
                    fv:gender|fv:sex ?male_value .
            values ?male_value {"M" "Male"}
        }

        bind(URI(CONCAT(str(?record), "/patient/", str(?female_id))) as ?female_uri)
        bind(URI(CONCAT(str(?record), "/patient/", str(?male_id))) as ?male_uri)
    }
    """
    return query_str

def query_for_patients():
    query_str = query_prefixes()
    query_str += \
        """
        select * where {
            ?record fv:patient_id|fv:subject_id ?id;
                    fv:gender|fv:sex ?gender_value;
                    fv:patient_id|fv:DOB ?dob .
        }
        """
    return query_str

def test_query(graph):
    query_str = query_prefixes()
    query_str += \
    """
    construct {
        ?female_uri a ont:female_patient .
        ?male_uri a ont:male_patient .
    } where {
        {
            ?record fv:patient_id|fv:subject_id ?female_id;
                    fv:gender|fv:sex ?female_value .
            values ?female_value {"F" "Female"}
        } union {
            ?record fv:patient_id|fv:subject_id ?male_id;
                    fv:gender|fv:sex ?male_value .
            values ?male_value {"M" "Male"}
        }
    
        bind(URI(CONCAT(str(?record), "/patient/", str(?female_id))) as ?female_uri)
        bind(URI(CONCAT(str(?record), "/patient/", str(?male_id))) as ?male_uri)
    }
    """


def make_data_graph():
    # translate patient data
    pt1_graph = \
        translate_excel_to_ttl("test_data/patients_1.xlsx", "http://purl.example.translation/")
    pt2_graph = \
        translate_excel_to_ttl("test_data/patients_2.xlsx", "http://purl.example.translation/")

    # translate patient metadata
    pt1_metadata_graph = \
        translate_data_to_graph_excel("test_data/patients_1_specification.xlsx", "http://purl.example.metadata/",
                                      "http://purl.example.translation/")
    pt2_metadata_graph = \
        translate_data_to_graph_excel("test_data/patients_2_specification.xlsx", "http://purl.example.metadata/",
                                      "http://purl.example.translation/")

    # translate services performed data
    srv1_graph = \
        translate_excel_to_ttl("test_data/services_1.xlsx", "http://purl.example.translation/")
    srv2_graph = \
        translate_excel_to_ttl("test_data/services_2.xlsx", "http://purl.example.translation/")

    # translate services metadata
    srv1_metadata_graph = \
        translate_data_to_graph_excel("test_data/services_1_specification.xlsx", "http://purl.example.metadata/",
                                      "http://purl.example.translation/")
    srv2_metadata_graph = \
        translate_data_to_graph_excel("test_data/services_2_specification.xlsx", "http://purl.example.metadata/",
                                      "http://purl.example.translation/")

    # union all the graphs
    graph = \
        pt1_graph + pt2_graph + \
        srv1_graph + srv2_graph
        # pt1_metadata_graph + pt2_metadata_graph + \
        # srv1_metadata_graph + srv2_metadata_graph

    return graph


def instantiate_entities():
    def instantiate_patients():
        results = graph.query(query_for_patients())
        for result in results:
            id = str(result[3])
            gender = str(result[2])
            uri = make_uri(str(data), "patient/%s" % id)

            print(result[1])
            # if "Female" == gender or "F" == gender:
            #     dso.declare_individual(graph, uri, ont.female_patient_uri)
            # else:
            #     dso.declare_individual(graph, uri, ont.male_patient_uri)



    graph = make_data_graph() ## create graph

    # set up namespaces
    data = Namespace("http://purl.example.translation/")
    fv = Namespace(data + "data_property/field_value/")  # field values (shortcut)
    fdi = Namespace(data + "object_property/field_data_item/")  # field data items (shortcut)


    instantiate_patients()

def make_uri_map(df):
    uri_map = {}
    for c in df.columns:
        uri_map[c] = "http://ex.com/" + str(c)

    return uri_map

# instantiate_entities()

## test record/value mapping (direct mapping)
g = rdflib.Graph()
df = pds.ExcelFile("test_data/patients_1.xlsx").parse()

# mapper = make_record_value_mapper(g, make_uri_map(df))
# df.apply(rvm, axis = 1)
# for stmt in g: print(stmt)


## test record/attribute mapping
g = rdflib.Graph()
g.add( (rdflib.URIRef("http://ex.com/data_record"), rdflib.RDF.type, rdflib.OWL.Class))
g.add( (rdflib.URIRef("http://ex.com/datum"), rdflib.RDF.type, rdflib.OWL.Class))
g.add( (rdflib.URIRef("http://ex.com/entity"), rdflib.RDF.type, rdflib.OWL.Class))
g.add( (rdflib.URIRef("http://ex.com/person"), rdflib.RDF.type, rdflib.OWL.Class))
g.add( (rdflib.URIRef("http://ex.com/person"), rdflib.RDFS.subClassOf, rdflib.URIRef("http://ex.com/entity")))
g.add( (rdflib.URIRef("http://ex.com/person_gender"), rdflib.RDF.type, rdflib.OWL.Class))
g.add( (rdflib.URIRef("http://ex.com/person_gender"), rdflib.RDFS.subClassOf, rdflib.URIRef("http://ex.com/entity")))
g.add( (rdflib.URIRef("http://ex.com/male"), rdflib.RDF.type, rdflib.OWL.Class))
g.add( (rdflib.URIRef("http://ex.com/male"), rdflib.RDFS.subClassOf, rdflib.URIRef("http://ex.com/person")))
g.add( (rdflib.URIRef("http://ex.com/male_gender"), rdflib.RDF.type, rdflib.OWL.Class))
g.add( (rdflib.URIRef("http://ex.com/male_gender"), rdflib.RDFS.subClassOf, rdflib.URIRef("http://ex.com/person_gender")))
g.add( (rdflib.URIRef("http://ex.com/female"), rdflib.RDF.type, rdflib.OWL.Class))
g.add( (rdflib.URIRef("http://ex.com/female"), rdflib.RDFS.subClassOf, rdflib.URIRef("http://ex.com/person")))
g.add( (rdflib.URIRef("http://ex.com/female_gender"), rdflib.RDF.type, rdflib.OWL.Class))
g.add( (rdflib.URIRef("http://ex.com/female_gender"), rdflib.RDFS.subClassOf, rdflib.URIRef("http://ex.com/person_gender")))
g.add( (rdflib.URIRef("http://ex.com/is_about"), rdflib.RDF.type, rdflib.OWL.ObjectProperty))
g.add( (rdflib.URIRef("http://ex.com/data_attribute"), rdflib.RDF.type, rdflib.OWL.ObjectProperty))

mapper = make_data_attribute_mapper(g, make_uri_map(df))

df.apply(mapper, axis = 1)
for stmt in g: print(stmt)
g.serialize(destination='output.owl')
# print(df)
