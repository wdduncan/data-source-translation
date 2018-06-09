from translate_data_source import translate_excel
from translate_metadata import translate_metadata_excel, translate_data_to_graph_excel
from rdflib import Graph
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

    # create dental ontology and source translation graphs
    dental_graph = \
        Graph(identifier="simple-dental-ontology.owl").parse("translation_lib/ontology/simple-dental-ontology.owl")
    source_graph = \
        Graph(identifier="data-source-translation.owl").parse("translation_lib/ontology/data-source-ontology.owl")

    # union all the graphs
    graph = pt1_graph + pt2_graph + pt1_metadata_graph + pt2_metadata_graph + dental_graph + source_graph

    return graph

def instantiate_patients(graph):
    query_str = query_prefixes()
    query_strx = \
    """
    ## needs to run in graphdb to work
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
    query_str += \
        """
        ## needs to run in graphdb to work
        select * where {
            ?record fv:patient_id|fv:subject_id ?id;
                    fv:gender|fv:sex ?gender_value .
        }
        """

    results = graph.query(query_str)
    for result in results:
        # graph.add(result)
        print result
    # print graph.serialize(format="turtle")



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
def instantiate_entities():
    graph = make_data_graph()
    instantiate_patients(graph)

instantiate_entities()

