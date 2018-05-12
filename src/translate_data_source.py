# coding=utf-8
from translation_lib.translation_ontology_functons_ttl import *
import pandas as pds

def translate_excel(data_file):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()

