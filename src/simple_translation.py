from simple_data_translation_operations import *

def simple_translation_excel(file_path, base_uri="", ontology_uri="", imports=""):
    # ceate dataframe from demo data
    df = pds.ExcelFile(file_path).parse()

    table_name = get_table_name_from_file(file_path)
    table_class_uri = get_table_class_uri(table_name)
    file_name = get_table_name_from_file(file_path, remove_ext=False)
    field_names = list(df.columns)  # get list of fields

    # specify ontology variables
    if len(base_uri) == 0:
        base_uri = "http://purl.obolibrary.org/obo/data-source-ontology.owl/{0}/".format(file_name)
    if len(ontology_uri) == 0:
        ontology_uri = "http://purl.obolibrary.org/obo/data-source-ontology.owl/{0}".format(file_name)

    # add axioms to represent table, fields, field values, records
    axioms = []  # list to hold axioms
    axioms.append(ttl_prefixes_simple(file_name, table_name, base_uri, ontology_uri, imports=imports))  # add prefixes
    axioms.append(ttl_table_simple(table_name, terse_label=True)) # add table
    axioms.append(ttl_field_data_properties_simple(table_name, field_names, terse_label=True)) # add data properties
    axioms.append(ttl_records_simple(df, table_class_uri, table_name, terse_label=True)) # add records

    return axioms

def main_simple_translate_excel():
    axioms = simple_translation_excel("patients_1.xlsx")
    save_axioms(axioms, "output/patients-1-simple.ttl")
    print_axioms(axioms)

main_simple_translate_excel()