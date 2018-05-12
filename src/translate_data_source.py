# coding=utf-8
import translation_lib.translation_ontology_functons_ttl as txf
import translation_lib.translation_operations_ttl as txo
import pandas as pds

def translate_excel(data_file):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()

    file_name = txo.format_data_source_name(data_file)

    print file_name

translate_excel("test_data/patients_1.xlsx")