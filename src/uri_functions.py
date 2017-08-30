from data_operations import parse_parameter


def get_uri(val, base=""):
    if len(base) > 0:
        return "<" + base + val + ">"
    else:
        return "<" + val + ">"


def get_uri_label(uri, label):
    if len(label) > 0:
        return """\n{0} rdfs:label "{1}" .""".format(uri, label)
    else:
        return ""


def get_table_class_uri(class_name):
    return "table:{0}".format(class_name)


def get_table_uri(table_name):
    return "table_i:{0}_i".format(table_name)


def get_field_class_uri(class_name):
    return "field:{0}_field".format(class_name)


def get_field_uri(field_name):
    return "field_i:{0}_field_i".format(field_name)


def get_data_prop_uri(property_name):
    return "data_property:{0}_datum_value".format(property_name)


def get_record_class_uri(class_name):
    return "record_i:{0}_record".format(class_name)


def get_record_uri(class_name, record_idx):
    return "record_i:{0}_record_{1}_i".format(class_name, str(record_idx))


def get_field_datum_class_uri(class_name):
    return "field_value:{0}_field_datum".format(class_name)


def get_field_datum_uri(field_name, record_idx):
    return "field_datum_i:{0}_field_datum_{1}_i".format(field_name, str(record_idx))


def declare_instance(insance_uri ,class_uri, member_uri="", label=""):
    ttl = "{0} rdf:type owl:NamedIndividual, {1} .".format(insance_uri, parse_parameter(class_uri))
    if len(member_uri) > 0:
        ttl += "\n{0} dso:member_of {1} .".format(insance_uri, parse_parameter(member_uri))
    if len(label) > 0:
        ttl += get_uri_label(insance_uri, label)
    return ttl


def declare_class(class_uri, super_class_uri="", label=""):
    ttl = ttl = "{0} rdf:type owl:Class .".format(class_uri)
    if len(super_class_uri) > 0:
        ttl += "\n{0} rdfs:subClassOf {1} .".format(class_uri, parse_parameter(super_class_uri))
    if len(label) > 0:
        ttl += get_uri_label(class_uri, label)
    return ttl


def declare_data_property(data_property_uri, label=""):
    ttl = "{0} rdf:type owl:DatatypeProperty .".format(data_property_uri)
    if len(label) > 0:
        ttl += get_uri_label(data_property_uri, label)
    return ttl

