from translate_data_source import translate_excel
from translate_metadata import translate_metadata_excel, translate_data_to_graph_excel
from rdflib import Graph
from textwrap import dedent


def query_prefixes():
    return dedent(
        """
        base <http://purl.obolibrary.org/obo/simple-dental-ontology.owl/>
        prefix : <http://purl.obolibrary.org/obo/simple-dental-ontology.owl/>
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
