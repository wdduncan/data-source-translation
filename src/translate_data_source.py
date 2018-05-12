# coding=utf-8
import translation_lib.translation_ontology_functions_ttl as txf
import translation_lib.translation_operations_ttl as txo
import pandas as pds
import datetime as dtm

def translate_excel(data_file, base):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()

    # create uris
    base = txo.format_base_uri(base) # base uri
    file_name = txo.format_data_file_name(data_file)  # file name
    file_uri = "<spreadsheet/{0}>".format(file_name) # file uri
    ontology_uri = "{0}/{1}.data.owl".format(base, file_name) # ontology uri

    # prefixes
    axioms = [txo.prefixes(base, ontology_uri)]

    axioms.append("# declare data file")
    axioms.append(txf.declare_individual(file_uri, txf.spreadsheet_uri(), file_name))

    # declare data relations
    axioms.append(txo.translate_df_fields(df))

    # declare data records
    axioms.append(txo.translate_df_records(df))

    return '\n'.join(axioms)

translate_excel("test_data/patients_1.xlsx", "http://purl.example.translation/")