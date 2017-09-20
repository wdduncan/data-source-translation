# coding=utf-8
import pandas as pds
from uri_functions import *
from textwrap import dedent
from data_operations import *


class Ontology:
    data_source_name = ""
    prefix = ""
    ontology_uri = ""
    base_uri = ""
    axioms = []
    df = None
    table_name = ""
    table_uri = ""
    table_class_uri = ""
    field_names = []
    file_name = ""
    reify_fields = False


    def __intit__(self, data_source_name, table_name, base_uri="", ontology_uri="", imports="", reify_fields=False):
        self.data_source_name = data_source_name
        self.table_name = table_name

        if len(base_uri) == 0: self.base_uri = "http://purl.obolibrary.org/data-source/{0}/".format(data_source_name)
        if len(ontology_uri) == 0: self.ontology_uri = "http://purl.obolibrary.org/{0}".format(data_source_name)

        ttl = \
            dedent("""\
                # axioms for prefixes
                @prefix dc: <http://purl.org/dc/elements/1.1/> .
                @prefix owl: <http://www.w3.org/2002/07/owl#> .
                @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
                @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
                @prefix swrl: <http://www.w3.org/2003/11/swrl#> .
                @prefix swrla: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
                @prefix swrlb: <http://www.w3.org/2003/11/swrlb#> .
                @prefix xml: <http://www.w3.org/XML/1998/namespace> .
                @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

                # custom prefixes
                @base <{0}> .
                @prefix : <{0}> .

                # custom class and property prefixes
                @prefix table: <table/> .
                @prefix table_name: <table/{1}> .
                @prefix field: <field/> .
                @prefix record: <record/> .
                @prefix data_property: <data_property/> .
                @prefix dp: <data_property/> .
                @prefix op: <object_property/> .

                # custom instance prefixes
                @prefix record_i: <record/instance/> .
                @prefix fd_i: <field_datum/instance/> .

                # ontology uri
                <{2}> rdf:type owl:Ontology .

                """.format(base_uri, table_name, ontology_uri))

        if len(imports) > 0:
            # check if imports is string or list
            if type(imports) == type(""):  # imports is a list
                ttl += \
                    dedent("""
                                # specified ontology imports
                                <{0}> owl:imports <{1}> .""".format(ontology_uri, imports))
            elif type(imports) == type([]):  # imports is a list
                # use list comprehension ["<" + i + ">" for i in imports] to build list of uris
                # then join with commas
                ttl += \
                    dedent("""
                                # specified ontology imports
                                <{0}> owl:imports {1} .""".format(ontology_uri,
                                                                  ", ".join(["<" + i + ">" for i in imports])))
        # add prefix axioms
        self.axioms.append(ttl)


    def load_data_frame(self, dataframe):
        self.df = dataframe


    def load_dataframe__from_excel(self, file_path):
        self.df = pds.ExcelFile(file_path).parse()


    def set_field_names(self):
        self.field_names = list(self.df.columns)


    def set_table_class_uri(self):
        self.table_class_uri = get_table_class_uri(self.table_name)


    def append_axioms(self, axioms):
        self.axioms.append(axioms)


    def save_axioms(self, output_file):
        with open(output_file, "w") as f:
            for a in self.axioms:
                f.write(a)
        print output_file + " saved"


    def print_axioms(self):
        # for axiom in self.axioms: print axiom
        print "\n".join(self.axioms)

