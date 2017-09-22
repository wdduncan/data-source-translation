# coding=utf-8
import pandas as pds
from uri_functions import *
from textwrap import dedent
from data_operations import *
from direct_mapping_classes import *


# @print_function_output()
def ttl_table_direct(ont, super_class_uri="owl:Thing", terse_label=False):
    ttls = ["\n# axioms to create table"]

    # create table class
    if terse_label:
        label = ont.table_name
    else:
        label = "{0} table".format(ont.table_name)

    class_uri = get_table_class_uri(ont.table_name)

    # create class
    ttl = declare_class(class_uri, super_class_uri, label)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_function_output()
def ttl_data_properties_direct(ont, terse_label=False):
    ttls = ["\n# axioms to create data properties"]

    if ont.reify_fields:
        # when using fields we need a data property to relate field datum to value
        ttl = declare_data_property("dp:has_value", "has value")
        ttls.append(ttl)

    for field_name in ont.field_names:
        ttl = ttl_data_property_direct(ont, field_name, terse_label)
        ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")

# @print_function_output()
def ttl_data_property_direct(ont, field_name, terse_label=False):
    # create data property field
    data_prop_uri = get_data_prop_uri(field_name)

    if terse_label:
        label = field_name
    else:
        label = "{0}.{1} value".format(ont.table_name, field_name)

    ttl = declare_data_property(data_prop_uri, label)
    return ttl

# @print_function_output()
def ttl_record_class_direct(ont, terse_label=False):
    ttls = ["\n# axioms to create record class"]

    if terse_label:
        label = "record"
    else:
        label = "{0} record".format(ont.table_name)

    class_uri = get_record_class_uri(ont.table_name)

    # create class
    ttl = declare_class(class_uri, ont.table_class_uri, label)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_records_direct(ont, terse_label=False):
    ttls = ["\n# axioms to create records"]

    # create records as instance of table class
    for record_idx, record in enumerate(ont.df.itertuples(), 1):
        # make instance of record
        record_uri = get_record_uri(ont.table_name, record_idx)
        ttl = ttl_record_direct(ont, record_uri, record_idx, terse_label)
        ttls.append(ttl)

        # relate record to values
        ttl = ttl_record_data_values_direct(record, record_uri, ont.field_names)
        ttls.append(ttl)

        if ont.reify_fields:
            ttl = ttl_field_datum_direct(record, record_uri, record_idx, ont.field_names)
            ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl

# @print_function_output()
def ttl_record_direct(ont, record_uri, record_idx, terse_label=False):
    ttls = ["\n# axioms to create record"]

    # create label
    if terse_label:
        label = "record {0}".format(str(record_idx))
    else:
        label = "{0} record {1}".format(ont.table_name, str(record_idx))

    # declare instance
    ttl = declare_instance(record_uri, ont.table_class_uri, label=label)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


# @print_function_output()
def ttl_record_data_values_direct(record, record_uri, field_names):
    ttls = ["\n# axioms to relate record to values"]

    for value_idx, value in enumerate(record):
        # value_idx 0 holds the index of the value tuple, so ignore it
        if value_idx > 0:
            field_name = field_names[value_idx - 1]
            data_prop_uri = get_data_prop_uri(field_name)  # uri for field as data property

            # relate record to data value
            ttl = """{0} {1} "{2}" .""".format(record_uri, data_prop_uri, value)
            ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")


def ttl_field_datum_direct(record, record_uri, record_idx, field_names):
    ttls = ["\n# axioms to create field datum instances and relate to record"]

    for value_idx, value in enumerate(list(record)):
        # value_idx 0 holds the index of the value tuple, so ignore it
        if value_idx > 0:
            field_name = field_names[value_idx - 1]
            fd_uri = get_field_datum_uri(field_name, record_idx) # get uri for instance of field datum

            # relate record to field datum
            ttl = "{0} op:has_member {1} .".format(record_uri, fd_uri)
            ttls.append(ttl)

            ttl = "{0} op:member_of {1} .".format(fd_uri, record_uri)
            ttls.append(ttl)

            # relate field datum to value
            ttl = """{0} dp:has_value "{1}" .""".format(fd_uri, value)
            ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")


# @print_function_output()
def ttl_field_data_properties_direct(ont, terse_label=False):
    ttls = ["\n# axioms to create data properties"]

    if ont.reify_fields:
        # when using fields we need a data property to relate field datum to value
        ttl = declare_data_property("dp:has_value", "has value")
        ttls.append(ttl)

    for field_name in ont.field_names:
        ttl = ttl_field_data_property_direct(ont, field_name, terse_label)
        ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")


# @print_function_output()
def ttl_properties_direct(table_name, field_names, terse_label=False):
    ttls = ["\n# axioms to create object and data properties"]

    # create member of relation needed to related records to field datum instances
    ttl = ttl_object_properties_direct()
    ttls.append(ttl)

    # create data properties
    ttl = ttl_field_data_properties_direct(table_name, field_names, terse_label)
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")


# @print_function_output()
def ttl_field_data_property_direct(ont, field_name, terse_label=False):
    # create data property field
    data_prop_uri = get_data_prop_uri(field_name)

    if terse_label:
        label = field_name
    else:
        label = "{0}.{1} datum value".format(ont.table_name, field_name)

    ttl = declare_data_property(data_prop_uri, label)
    return ttl


# @print_function_output()
def ttl_object_properties_direct():
    ttls = ["\n# axioms to create object properties"]

    # create membership relations needed to related records to field datum instances
    ttl = declare_object_property("op:member_of", "member of")
    ttls.append(ttl)

    ttl = declare_object_property("op:has_member", "has member")
    ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")


# @print_function_output()
def ttl_field_classes_direct(table_class_uri, table_name, field_names, terse_label=False):
    ttls = ["\n# axioms to create field classes"]

    for field_name in field_names:
        ttl = ttl_field_class_direct(table_class_uri, table_name, field_name, terse_label)
        ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return (ttl + "\n")


# @print_function_output()
def ttl_field_class_direct(table_class_uri, table_name, field_name, terse_label=False):
    if terse_label:
        label = field_name
    else:
        label = "{0}.{1} field".format(table_name, field_name)

    class_uri = get_field_class_uri(table_name)

    # create field class
    ttl = declare_class(class_uri, table_class_uri, label)
    return ttl