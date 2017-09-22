from simple_data_translation_operations import *

def simple_translation_excel(file_path, base_uri="", ontology_uri="", imports="", with_fields=False):
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
    axioms.append(ttl_field_data_properties_simple(table_name, field_names, terse_label=True, with_fields=with_fields)) # add data properties

    if with_fields:
        # this option includes each field as separate class and instance
        axioms.append(ttl_record_class_simple(table_class_uri, table_name, terse_label=True)) # add record class
        axioms.append(ttl_field_classes_simple(table_class_uri, table_name, field_names, terse_label=True)) # add field classes
        axioms.append(ttl_object_properties_simple()) # add object properties

    axioms.append(ttl_records_simple(df, table_class_uri, table_name, terse_label=True, with_fields=with_fields)) # add records

    return axioms

def main_simple_translate_excel(with_fields=False):
    axioms = simple_translation_excel("patients_1.xlsx", with_fields=with_fields)

    if with_fields:
        save_axioms(axioms, "output/patients-1-simple-with-fields.ttl")
    else:
        save_axioms(axioms, "output/patients-1-simple-no-fields.ttl")

    print_axioms(axioms)

# main_simple_translate_excel()
main_simple_translate_excel(with_fields=True)