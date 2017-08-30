from data_translation_operations import *


def translate_excel_to_ttl(file_path, base_uri="", ontology_uri="", imports=""):
    # ceate dataframe from demo data
    df = pds.ExcelFile(file_path).parse()

    # just get table and file name part of path
    table_name = get_table_name_from_file(file_path)
    table_uri = get_table_uri(table_name)
    file_name = get_table_name_from_file(file_path, remove_ext=False)
    field_names = list(df.columns)  # get list of fields

    # specify ontology variables
    if len(base_uri) == 0:
        base_uri = "http://purl.obolibrary.org/obo/data_source_ontology.owl/{0}/".format(file_name)
    if len(ontology_uri) == 0:
        ontology_uri = "http://purl.obolibrary.org/obo/data_source_ontology.owl/{0}".format(file_name)

    # add axioms to represent table, fields, field values, records
    axioms = [] # list to hold axioms
    axioms.append(ttl_prefixes(file_name, table_name, base_uri, ontology_uri, imports=imports)) # add prefixes
    axioms.append(ttl_table(table_uri, table_name)) # add table
    axioms.append(ttl_fields(table_uri, table_name, field_names)) # add fields
    axioms.append(ttl_field_datum_classes(table_name, field_names)) # add field datum classes
    axioms.append(ttl_records(df, table_uri, table_name)) # add records and field data

    return axioms

### run code
axioms = translate_excel_to_ttl("patients_1.xlsx")
print_axioms(axioms)
save_axioms(axioms, "output/patients_1.ttl")