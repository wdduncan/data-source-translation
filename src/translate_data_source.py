from data_translation_operations import *


def translate_data_to_ttl(filepath, base_uri="", ontology_uri="", imports=""):
    # ceate dataframe from demo data
    df = pds.ExcelFile(filepath).parse()

    # just get table and file name part of path
    tablename = get_tablename_from_file(filepath)
    table_uri = get_table_uri()
    filename = get_tablename_from_file(filepath, remove_ext=False)
    field_names = list(df.columns)  # get list of fields

    # specify ontology variables
    if len(base_uri) == 0:
        base_uri = "http://purl.obolibrary.org/obo/data_source_ontology.owl/{0}/".format(tablename)
    if len(ontology_uri) == 0:
        ontology_uri = "http://purl.obolibrary.org/obo/data_source_ontology.owl/{0}".format(filename)

    # add axioms to represent table, fields, field values, records
    axioms = [] # list to hold axioms
    axioms.append(ttl_prefixes(tablename, base_uri, ontology_uri, imports=imports)) # add prefixes
    axioms.append(ttl_table(table_uri, tablename)) # add table
    axioms.append(ttl_fields(table_uri, tablename, field_names)) # add fields
    axioms.append(ttl_field_value_classes(tablename, field_names)) # add field value classes
    axioms.append(ttl_records(df, table_uri, tablename)) # add records and values

    return axioms

### run code
axioms = translate_data_to_ttl("patients_1.xlsx")
print_axioms(axioms)