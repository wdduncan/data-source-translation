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


def get_table_uri(tablename="", base=""):
    return "tablename:_table_i"


def get_field_uri(field_name, tablename="", base=""):
    return "field:" + field_name + "_field_i"


def get_data_prop_uri(field_name, tablename="", base=""):
    return "data_property:" + field_name + "_datum_value"


def get_record_uri(tablename, record_idx, record_name='', base=""):
    return "record:" + tablename + "_record_" + str(record_idx) + "_i"


def get_field_value_uri(field_name, record_idx, tablename="", base=""):
    return "field_value:" + field_name + "_field_datum_" + str(record_idx) + "_i"


def get_field_value_class_uri(tablename, field_name=""):
    if len(field_name) > 0:
        return "field_value:{0}.{1}_field_value".format(tablename, field_name)
    else:
        return "field_value:{0}_field_value".format(tablename)


def declare_instance(insance_uri ,class_uri, member_uri="", label=""):
    ttl = "{0} rdf:type owl:NamedIndividual, {1} .".format(insance_uri, class_uri)
    if len(member_uri) > 0:
        ttl += "\n{0} dso:member_of {1} .".format(insance_uri, member_uri)
    if len(label) > 0:
        ttl += get_uri_label(insance_uri, label)
    return ttl


def declare_class(class_uri, super_uri="", label=""):
    ttl = ttl = "{0} rdf:type owl:Class .".format(class_uri)
    if len(super_uri) > 0:
        ttl += "\n{0} rdfs:subClassOf {1} .".format(class_uri, super_uri)
    if len(label) > 0:
        ttl += get_uri_label(class_uri, label)
    return ttl


def declare_data_property(data_property_uri, label=""):
    ttl = "{0} rdf:type owl:DatatypeProperty .".format(data_property_uri)
    if len(label) > 0:
        ttl += get_uri_label(data_property_uri, label)
    return ttl

