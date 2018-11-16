import pandas as pds
from rdflib import Graph, BNode, RDF, RDFS, OWL, Namespace, BNode, URIRef, Literal, XSD
from rdflib.namespace import NamespaceManager
from pprint import pprint


if __name__ == "__main__":
    g = Graph()
    df = pds.read_excel('patients_1_eav.xlsx')
    for row in df.itertuples():
        ## make triple as it appears in EAV table
        ## note: using blank nodes for each row in df
        eav = \
            """
            {
              "@context":
              {
                "ex": "http://example.com/",
                "rp": "http://purl.roswellpark.org/ontology#",
                "record": "rp:dp_record",
                "field": "rp:dp_field",
                "value": "rp:dp_value",
                "data_record": "rp:DE_000000003"
              },
              "@type": "data_record",
              "record": "%s",
              "field": "%s",
              "value": "%s"
            }
            """ % (row.record, row.field, row.value)
        g.parse(data=eav, format='json-ld')

    # print(g.serialize(format='turtle'))

    ## define context for records
    context = \
        """
          "@context":
          {
            "ex": "http://example.com/",
            "rp": "http://purl.roswellpark.org/ontology#",
            "record": "rp:dp_record",
            "data_record": "rp:DE_000000003",
            "data_record_i": "rp:DE_000000003#",
            "field": "rp:dp_field",
            "field_p": "rp:dp_field#",
            "value": "pr:dp_value",
            "patient_id": "field_p:patient_id",
            "gender": "field_p:gender",
            "birth_date": "field_p:birth_date"
          }
        """

    # for row in df.itertuples():
    #     ## group rows in EAV into 'records' documents
    #     data = \
    #       """
    #         "@id": "data_record_i:%s",
    #         "@type": "data_record",
    #         "%s": "%s"
    #       """ % (row.record, row.field, row.value)
    #     doc = """{%s, \n %s \n}""" % (context, data)
    #     # print(doc, "\n")
    #     g.parse(data=doc, format='json-ld')

    # for s, p, o in g.triples((None, RDF.type, URIRef("http://purl.roswellpark.org/ontology#DE_000000003"))):
    for r in g.subjects(RDF.type, URIRef("http://purl.roswellpark.org/ontology#DE_000000003")):
        for f in g.objects(r, URIRef("http://purl.roswellpark.org/ontology#dp_field")):
            print(f)

