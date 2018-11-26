import pandas as pds
from rdflib import Graph, ConjunctiveGraph, BNode, RDF, RDFS, OWL, Namespace, BNode, URIRef, Literal, XSD
from textwrap import dedent
from pprint import pprint
from rdflib.namespace import NamespaceManager
# from pprint import pprint


class jsonld_document:
    def __init__(self, context="", data_template="", document_template="",
                 print_context=False, print_data_template=False, print_document_template=False):
        if len(context) > 0:
            self.set_context(context, print_context)

        if len(data_template) > 0:
            self.data_template = self.set_data_template(data_template, print_data_template)

        if len(document_template) > 0:
            self.document_template = self.set_document_template(document_template, print_document_template)


    def set_context(self, context, print_context=False):
        self.context = jsonld_document.make_context_string(context, print_context)
        return self.context


    def get_context(self):
        return self.context


    @staticmethod
    def make_context_string(context, print_context=False):
        context_string = \
            dedent(""" 
               "@context":
                   %s
               """ % context)

        if print_context: print(context_string)
        return context_string


    def set_data_template(self, data_template, print_data_template=False):
        self.data_template = \
            jsonld_document.make_data_template_string(data_template, print_data_template=print_data_template)
        return self.data_template


    def get_data_template(self):
        return  self.data_template


    @staticmethod
    def make_data_template_string(data_template, print_data_template=False):
        data_template_string = \
            dedent("""
                "@graph": [
                    %s
                ]
                """ % data_template)

        if print_data_template: print(data_template_string)
        return data_template_string


    def set_document_template(self, document_template, print_document_template=False):
        self.document_template = document_template
        return self.document_template


    def get_document_template(self):
        return  self.document_template


    def set_data(self, values_tuple, print_values_tuple=False, print_data=False):
        self.data = \
            self.make_data_string(values_tuple,
                                  print_values_tuple=print_values_tuple,
                                  print_data=print_data)
        return self.data


    def get_data(self):
        return self.data


    def make_data_string(self, values_tuple, print_values_tuple=False, print_data=False):
        if print_values_tuple: print(values_tuple)

        data_string = self.data_template % (values_tuple)

        if print_data: print(data_string)
        return data_string


    def make_context_data_string(self, print_context_data=False):
        context_data_string = \
            dedent("""
              {
                %s,
                %s
              }  
              """ % (self.context, self.data))

        if print_context_data: print(context_data_string)
        return context_data_string


    def set_document(self, values_tuple, print_values_tuple=False, print_document=False):
        self.document = \
            self.make_document_string(values_tuple,
                                      print_values_tuple=print_values_tuple,
                                      print_document=print_document)
        return self.document


    def get_document(self):
        return self.document


    def make_document_string(self, values_tuple, print_values_tuple=False, print_document=False):
        if print_values_tuple: print(values_tuple)

        document_string = self.document_template % (values_tuple)

        if print_document: print(document_string)
        return document_string


def translate_eav_1(df, graph=""):
    # if type("") == type(graph): graph = Graph()
    if type("") == type(graph): graph = ConjunctiveGraph() # must use ConjunctiveGraph with "@graph" keyword
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
          "@graph": [
          {
            "@id": "_:b%s",
            "@type": "data_record",
            "project": "%s",
            "record": "%s",
            "field": "%s",
            "value": "%s"
          }]
        }
        """

    eav_doc = jsonld_document(document_template=eav_template)
    # print(repr(('record_1', 'patient_id', 10001)))

    for idx, row in enumerate(df.itertuples()):
        ## put values into tuple
        blank = f"_:b{idx}"
        values = (blank, row.project, row.record, row.field, row.value)

        ## create json-ld document using values tuple
        ## note: using blank nodes for each row in df
        ##       the idx variable is needed to create new blank node ids, in the future, I may experiment with UUIDs
        data = eav_doc.set_document(values)
        # data = eav_doc.set_document(values, print_document=True)

        ## parse data into graphs
        # g.parse(data=eav_doc.data_string, format='json-ld')
        graph.parse(data=data, format='json-ld')

    return graph


def translate_eav_2(df, graph=""):
    if type("") == type(graph): graph = ConjunctiveGraph()

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
              "field_p:%s": "%s",
              "rp:originating_source": {"@id": "%s"}                  
          }]
        }
        """

    eav_doc = jsonld_document(document_template=eav_template)
    # print(repr(('record_1', 'patient_id', 10001)))

    for idx, row in enumerate(df.itertuples()):
        ## put values into tuple
        blank = f"_:b{idx}"
        id = f"project_{row.project}_{row.record}"
        eav_values = (blank, row.project, row.record, row.field, row.value)
        record_values = (id, row.field, row.value, blank)
        values = eav_values + record_values

        ## create json-ld document using values tuple
        ## note: using blank nodes for each row in df
        ##       the idx variable is needed to create new blank node ids, in the future, I may experiment with UUIDs
        data = eav_doc.make_document_string(values)
        # data = eav_doc.make_data_string(values, print_data_string=True)

        ## parse data into graphs
        # g.parse(data=eav_doc.data_string, format='json-ld')
        graph.parse(data=data, format='json-ld')

    return graph


def translate_eav_3(df, graph=""):
    if type("") == type(graph): graph = ConjunctiveGraph()

    # eav_doc = jsonld_doc(context=context)
    context = """
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
      }
      """

    data_template = """
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
              "field_p:%s": "%s",
              "rp:originating_source": {"@id": "%s"}                  
          }
        """

    eav_doc = jsonld_document(context=context, data_template=data_template)

    for idx, row in enumerate(df.itertuples()):
        ## put values into tuple
        blank = f"_:b{idx}"
        id = f"project_{row.project}_{row.record}"
        eav_values = (blank, row.project, row.record, row.field, row.value)
        record_values = (id, row.field, row.value, blank)
        values = eav_values + record_values

        ## bind the tupule values to the data in the eav doc
        eav_doc.set_data(values)

        ## create json-ld document by combining the context with the data
        ## note: using blank nodes for each row in df
        ##       the idx variable is needed to create new blank node ids, in the future, I may experiment with UUIDs
        # data = eav_doc.make_context_data_string(values)
        data = eav_doc.make_context_data_string(print_context_data=True)

        ## parse data into graphs
        # g.parse(data=eav_doc.data_string, format='json-ld')
        graph.parse(data=data, format='json-ld')

    return graph


def translate_eav_4(df, graph=""):
    # if type("") == type(graph): graph = Graph()
    if type("") == type(graph): graph = ConjunctiveGraph() # must use ConjunctiveGraph with "@graph" keyword
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
          "@graph": [
          {
            "@id": "_:b%s",
            "@type": "data_record",
            "project": "%s",
            "record": "%s",
            "field": "%s",
            "value": "%s"
          }]
        }
        """

    eav_doc = jsonld_document(document_template=eav_template)
    # print(repr(('record_1', 'patient_id', 10001)))

    for idx, row in enumerate(df.itertuples()):
        ## put values into tuple
        blank = f"_:b{idx}"
        values = (blank, row.project, row.record, row.field, row.value)

        ## create json-ld document using values tuple
        ## note: using blank nodes for each row in df
        ##       the idx variable is needed to create new blank node ids, in the future, I may experiment with UUIDs
        data = eav_doc.set_document(values)
        # data = eav_doc.set_document(values, print_document=True)

        ## parse data into graphs
        # g.parse(data=eav_doc.data_string, format='json-ld')
        graph.parse(data=data, format='json-ld')

    return graph

if __name__ == "__main__":
    df = pds.read_excel('patients_1_eav.xlsx')

    # g = translate_eav_1(df)
    # g = translate_eav_2(df)
    # g = translate_eav_3(df)
    g = translate_eav_4(df)
    print(str(g.serialize(format='turtle'), 'utf-8'))
    # print(g.serialize(format="turtle").decode('utf-8')) # this also works
