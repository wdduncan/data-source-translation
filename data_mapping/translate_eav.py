import pandas as pds
from rdflib import Graph, ConjunctiveGraph, BNode, RDF, RDFS, OWL, Namespace, BNode, URIRef, Literal, XSD
from textwrap import dedent
from pprint import pprint
from rdflib.namespace import NamespaceManager
# from pprint import pprint


class jsonld_doc:
    def __init__(self, context="", data_template="", doc_template=""):
        self.context = \
                dedent(""" 
                    "@context":
                    { 
                        %s
                    }
                    """ % context)

        self.data_template = dedent(data_template)
        self.doc_template = dedent(doc_template)

    def get_doc_template(self):
        if len(self.doc_template):
            return self.doc_template
        else:
            return \
                dedent(
                """
                {
                    %s,
                    %s
                }
                """ % (self.context, self.data_template))

    def set_data_string(self, values_tuple, print_values_tuple=False, print_data_string=False):
        self.data_string = \
            self.make_data_string(values_tuple,
                                  print_values_tuple=print_values_tuple,
                                  print_data_string=print_data_string)
        return self.data_string


    def make_data_string(self, values_tuple, print_values_tuple=False, print_data_string=False):
        if print_values_tuple: print(values_tuple)

        if len(self.doc_template) > 0:
            data_string = self.doc_template % (values_tuple)
        else:
            data_string = self.data_template % (values_tuple)

        if print_data_string: print(data_string)
        return data_string


def translate_eav_1(df, graph=""):
    if type("") == type(graph): graph = Graph()
    eav_template = \
        """
        {
          "@context":
          {
            "ex": "http://example.com/",
            "rp": "http://purl.roswellpark.org/ontology#",
            "project": "rp:dp_project",
            "record": "rp:dp_record",
            "field": "rp:dp_field",
            "value": "rp:dp_value",
            "data_record": "rp:DE_000000003"
          },
          "@id": "_:b%s",
          "@type": "data_record",
          "project": "%s",
          "record": "%s",
          "field": "%s",
          "value": "%s"
        }
        """

    eav_doc = jsonld_doc(doc_template=eav_template)
    # print(repr(('record_1', 'patient_id', 10001)))

    for idx, row in enumerate(df.itertuples()):
        ## put values into tuple
        blank = f"_:b{idx}"
        values = (blank, row.project, row.record, row.field, row.value)

        ## create json-ld document using values tuple
        ## note: using blank nodes for each row in df
        ##       the idx variable is needed to create new blank node ids
        ##       in the future, I may experiment with UUIDs
        # data = eav_doc.make_data_string(values)
        data = eav_doc.make_data_string(values, print_data_string=True)

        ## parse data into graphs
        # g.parse(data=eav_doc.data_string, format='json-ld')
        graph.parse(data=data, format='json-ld')

    return graph


def translate_eav_2(df, graph=""):
    if type("") == type(graph): graph = ConjunctiveGraph()
    # context = \
    #     """
    #       "@context":
    #       {
    #         "ex": "http://example.com/",
    #         "rp": "http://purl.roswellpark.org/ontology#",
    #         "record": "rp:dp_record",
    #         "data_record": "rp:DE_000000003",
    #         "data_record_i": "rp:DE_000000003#",
    #         "field": "rp:dp_field",
    #         "field_p": "rp:dp_field#",
    #         "value": "pr:dp_value",
    #         "patient_id": "field_p:patient_id",
    #         "gender": "field_p:gender",
    #         "birth_date": "field_p:birth_date"
    #       }
    #     """

    # eav_doc = jsonld_doc(context=context)
    eav_template = \
        """
        {
          "@context":
          {
            "ex": "http://example.com/",
            "rp": "http://purl.roswellpark.org/ontology#",
            "project": "rp:dp_project",
            "record": "rp:dp_record",
            "field": "rp:dp_field",
            "field_p": "rp:dp_field#",
            "value": "rp:dp_value",
            "data_record": "rp:DE_000000003",
            "data_record_i": "rp:DE_000000003#"
          },
          "@graph": [
          {
              "@id": "%s",
              "@type": "data_record",
              "project": "%s",
              "record": "%s",
              "field": "%s",
              "value": "%s"
          },
          {
              "@id": "data_record_i:%s",
              "@type": "data_record",
              "field_p:%s": "%s"                     
          }]
        }
        """

    eav_doc = jsonld_doc(doc_template=eav_template)
    # print(repr(('record_1', 'patient_id', 10001)))

    for idx, row in enumerate(df.itertuples()):
        ## put values into tuple
        blank = f"_:b{idx}"
        id = f"project_{row.project}_{row.record}"
        eav_values = (blank, row.project, row.record, row.field, row.value)
        record_values = (id, row.field, row.value)
        values = eav_values + record_values

        ## create json-ld document using values tuple
        ## note: using blank nodes for each row in df
        ##       the idx variable is needed to create new blank node ids
        ##       in the future, I may experiment with UUIDs
        data = eav_doc.make_data_string(values)
        # data = eav_doc.make_data_string(values, print_data_string=True)

        ## parse data into graphs
        # g.parse(data=eav_doc.data_string, format='json-ld')
        graph.parse(data=data, format='json-ld')

    return graph


if __name__ == "__main__":
    df = pds.read_excel('patients_1_eav.xlsx')

    # g = translate_eav_1(df)
    g = translate_eav_2(df)
    print(str(g.serialize(format='turtle'), 'utf-8'))
    # print(g.serialize(format="turtle").decode('utf-8')) # this also works
