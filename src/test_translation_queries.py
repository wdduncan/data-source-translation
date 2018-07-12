from translate_data_source import translate_excel
from translate_metadata import translate_metadata_excel, translate_data_to_graph_excel
from rdflib import Graph


def test_data_graph_query():
    graph = translate_excel("test_data/patients_1.xlsx", "http://purl.example.translation/")

    results = \
        graph.query("""
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix field: <http://purl.data-source-translation.org/data_field>
            prefix record: <http://purl.data-source-translation.org/data_record>
            prefix fv: <http://purl.example.translation/data_property/field_value/> 

            select ?record ?value where {
              ?record a record:;
                      fv:patient_id ?value .}
            """)

    print("num results: ", len(results))
    print("type: ", type(results))

    for result in results: print (tuple(result))


def test_construct_query():
    graph = translate_excel("test_data/patients_1.xlsx", "http://purl.example.translation/")

    results = \
        graph.query("""
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix field: <http://purl.data-source-translation.org/data_field>
            prefix record: <http://purl.data-source-translation.org/data_record>
            prefix fv: <http://purl.example.translation/data_property/field_value/> 

            construct {
              ?record rdfs:label ?label .
            } where {
              ?record a record:;
                      fv:patient_id ?value .
              bind(concat("record for patient ", str(?value)) as ?label) .
            }
            """)

    print("num results: ", len(results))
    print("type: ", type(results))
    temp_graph = Graph()

    for result in results:
        temp_graph.add(result)
        # print result
    print(temp_graph.serialize(format="turtle"))

def test_metadata_services_1_query():
    data_graph = \
        translate_excel("test_data/services_1.xlsx", "http://purl.example.translation/")
    metadata_graph = \
        translate_data_to_graph_excel("test_data/services_1_specification.xlsx", "http://purl.example.metadata/",
                                      "http://purl.example.translation/")
    dental_graph = \
        Graph(identifier="simple-dental-ontology.owl").parse("translation_lib/ontology/simple-dental-ontology.owl")
    source_graph = \
        Graph(identifier="data-source-translation.owl").parse("translation_lib/ontology/data-source-ontology.owl")

    graph = data_graph + metadata_graph + dental_graph + source_graph  # union all the graphs

    query_str = \
        """
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix owl: <http://www.w3.org/2002/07/owl#>
        prefix obo: <http://purl.obolibrary.org/obo/>
        prefix dst: <http://purl.data-source-translation.org/>
        prefix dp: <http://purl.data-source-translation.org/data_property/>
        prefix op: <http://purl.data-source-translation.org/object_property/>
        prefix annotation: <http://purl.data-source-translation.org/annotation/>
        prefix field: <http://purl.data-source-translation.org/data_field>
        prefix fv: <http://purl.example.translation/data_property/field_value/>                 
        prefix data: <http://purl.example.translation/>
        prefix meta: <http://purl.example.metadata/>
        prefix ont: <http://purl.obolibrary.org/obo/simple-dental-ontology.owl/>

        select ?field ?value ?type 
        where {
          #?type rdfs:subClassOf ont:molar . # needs to be in GraphDB for this to work
          ?type rdfs:subClassOf ont:tooth .
          ?spec op:specifies ?field;
                annotation:semantic_type ?type .
          #optional { ?spec dp:specified_value ?value .}
          ?spec dp:specified_value ?value .

          ?field op:has_member ?data_item .
          ?data_item dp:data_value ?value .  
        } limit 100
        """

    results = graph.query(query_str)
    print("num results: ", len(results))
    for result in results:
        print(result)

    with open("test_data/output_services_1_with_metadata.ttl", "w") as f:
        f.write(graph.serialize(format="turtle"))
        # print graph.serialize(format="turtle")


def test_metadata_patients_query():
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
    graph = pt1_graph + pt2_graph + pt1_metadata_graph + pt2_metadata_graph+ dental_graph + source_graph

    query_str = \
        """
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

        select ?record ?spec ?field ?value ?type 
        where {
          # ?type rdfs:subClassOf ont:patient .
          # ?type rdfs:subClassOf ont:gender .
          ?type rdfs:subClassOf* ont:female_gender . # without a reasoner property path is needed
          ?spec op:specifies ?field;
                annotation:semantic_type ?type .
          # optional { ?spec dp:specified_value ?value .}
          ?spec dp:specified_value ?value .

          ?record a record:;
                  op:has_member ?data_item .
          ?field op:has_member ?data_item .
          ?data_item dp:data_value ?value .  
        } limit 100
        """

    results = graph.query(query_str)
    print("num results: ", len(results))
    for result in results:
        print(result)

    with open("test_data/output_patients_with_metadata.ttl", "w") as f:
        f.write(graph.serialize(format="turtle"))
        # print graph.serialize(format="turtle")


# test_data_graph_query()
test_construct_query()
# test_metadata_services_1_query()
# test_metadata_patients_query()