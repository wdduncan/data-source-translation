# coding=utf-8
import pandas as pds
from lib.uri_functions import *
from textwrap import dedent
from lib.data_operations import *
from lib.direct_mapping_classes import *
from lib.direct_mapping_translation_operations import *


def direct_translation_excel(file_path, base_uri="", ontology_uri="", imports="", reify_fields=False):
    # ceate dataframe from demo data
    df = pds.ExcelFile(file_path).parse()
    table_name = get_table_name_from_file(file_path)
    file_name = get_table_name_from_file(file_path, remove_ext=False)

    # specify ontology variables
    if len(base_uri) == 0:
        base_uri = "http://purl.obolibrary.org/obo/data-source-ontology.owl/{0}/".format(file_name)
    if len(ontology_uri) == 0:
        ontology_uri = "http://purl.obolibrary.org/obo/data-source-ontology.owl/{0}".format(file_name)

    # set up ontology object to hold info
    ont = Ontology(file_path, table_name, base_uri, ontology_uri, imports=imports)
    ont.df = df
    ont.table_class_uri = get_table_class_uri(table_name)
    ont.file_name = file_name
    ont.field_names = list(df.columns)
    ont.reify_fields = reify_fields

    # print_axioms(ont.axioms)
    # return

    # add axioms
    ont.append_axioms(ttl_table_direct(ont, terse_label=True)) # add table
    ont.append_axioms(ttl_data_properties_direct(ont, terse_label=True)) # add data properties
    ont.append_axioms(ttl_records_direct(ont, terse_label=True)) # add records

    return ont.axioms


def main_direct_translate_excel(reify_fields=False):
    axioms = direct_translation_excel("patients_1.xlsx", reify_fields=reify_fields)

    if reify_fields:
        save_axioms(axioms, "output/patients-1-direct-reify-fields.ttl")
    else:
        save_axioms(axioms, "output/patients-1-direct.ttl")

    print_axioms(axioms)

    # axioms = []
    # axioms = direct_translation_excel("patients_2.xlsx", reify_fields=reify_fields)
    #
    # if reify_fields:
    #     save_axioms(axioms, "output/patients-2-direct-reify-fields.ttl")
    # else:
    #     save_axioms(axioms, "output/patients-2-direct.ttl")
    #
    # print_axioms(axioms)

main_direct_translate_excel()
# axioms = direct_translation_excel("patients_2.xlsx", reify_fields=False)