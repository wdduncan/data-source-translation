from translate_data_source import translate_excel
from translate_metadata import translate_metadata_excel, translate_data_to_graph_excel
import translation_lib.util.simple_dental_ontology_generated_functions_rdflib as ont
import translation_lib.util.data_source_ontology_generated_functions_rdflib as dso
from translation_lib.util.uri_util import *
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef
from textwrap import dedent


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
        translate_excel("test_data/patients_1.xlsx", "http://purl.example.translation/")
    pt2_graph = \
        translate_excel("test_data/patients_2.xlsx", "http://purl.example.translation/")

    # translate patient metadata
    pt1_metadata_graph = \
        translate_data_to_graph_excel("test_data/patients_1_specification.xlsx", "http://purl.example.metadata/",
                                      "http://purl.example.translation/")
    pt2_metadata_graph = \
        translate_data_to_graph_excel("test_data/patients_2_specification.xlsx", "http://purl.example.metadata/",
                                      "http://purl.example.translation/")

    # translate services performed data
    srv1_graph = \
        translate_excel("test_data/services_1.xlsx", "http://purl.example.translation/")
    srv2_graph = \
        translate_excel("test_data/services_2.xlsx", "http://purl.example.translation/")

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

            print result[1]
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

instantiate_entities()

