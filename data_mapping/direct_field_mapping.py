# coding=utf-8
import pandas as pds
from lib.uri_functions import *
from textwrap import dedent
from lib.data_operations import *
from lib.direct_mapping_classes import *
from lib.direct_field_mapping_translation_operations import *


def direct_field_translation(data_source, source_type="spreadsheet"):
    df = pds.ExcelFile(data_source).parse()
    source_name = get_source_name_from_file(data_source)
    table_name = get_table_name_from_file(data_source, remove_ext=False)
    table_uri = get_uri(source_type + "/" + table_name)
    # field_op_map = make_field_to_object_property_map(list(df.columns))
    field_class_map = make_field_to_class_map(list(df.columns))
    axioms = []

    # add prefixes
    ttl = prefix_ttl(source_name, source_type)
    axioms.append(ttl)

    # add field specific object properties
    axioms.append("\n# axioms to create field specific object properties\n")
    ttl = object_properties_ttl(list(df.columns))
    axioms.append(ttl)

    # add data field classes
    axioms.append("\n# axioms to create data field classes\n")
    ttl = data_field_classes_ttl(list(df.columns))
    axioms.append(ttl)

    # add record class
    axioms.append("\n# axioms to create data record class\n")
    record_class_uri = data_record_class_uri(source_name)
    ttl = declare_class(record_class_uri, "ds:data_record")
    axioms.append(ttl)

    # add data records and fields
    axioms.append("\n# axioms to create data records and fields\n")

    for idx, row in enumerate(df.itertuples(), 1):
        record_uri = data_record_uri(idx)
        ttls = \
            dedent("""\
                   # axioms to create {0}
                   {0} 
                        rdf:type owl:NamedIndividual, {1}; 
                        ds:data_record_of {2} .
                   """.format(record_uri, record_class_uri, table_uri))

        ttls += "\n# axioms to create data fields for {0}\n".format(record_uri)
        for field in row._fields[1:]:
            field_uri = data_field_uri(field, idx)
            field_class_uri = field_class_map[field]
            value = getattr(row, field)
            prop_uri = obj_prop_uri(field)
            inv_prop_uri = inv_obj_prop_uri(field)
            ttls += \
                dedent("""\
                       {0} 
                          rdf:type owl:NamedIndividual, {1}; 
                          ds:has_value "{2}";
                          {3} {4} .
                       {4} 
                          {5} {0} .  
                       
                       """.format(field_uri, field_class_uri, value, inv_prop_uri, record_uri, prop_uri))
        axioms.append(ttls)

    return axioms


def main(input_file="", output_file="", print_output=True):
    if len(input_file.strip()) < 1:
        input_file = "patients_1.xlsx"

    axioms = direct_field_translation(input_file)

    if print_output:
        print_axioms(axioms)

    if len(output_file.strip()) > 0:
        # save_axioms(axioms, "output/patients-1-direct-fields.ttl")
        save_axioms(axioms, output_file)


################################
# main()
# main("patients_1.xlsx", "output/patients-1-direct-fields.ttl")
# main("patients_2.xlsx", "output/patients-2-direct-fields.ttl")

# main("services_1.xlsx", "output/services-1-direct-fields.ttl")
# main("services_2.xlsx", "output/services-2-direct-fields.ttl")