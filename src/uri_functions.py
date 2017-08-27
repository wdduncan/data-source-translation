def get_uri(val, base=""):
    if len(base) > 0:
        return "<" + base + val + ">"
    else:
        return "<" + val + ">"

def get_table_uri(tablename='', base=""):
    if len(tablename) > 0:
        return get_uri(tablename + "_table_i", base)
    else:
        return "tablename:_table_i"

def get_field_uri(field_name, tablename='', base=""):
    if len(tablename) > 0:
        return get_uri(tablename + "/field/" + field_name + "_field_i", base)
    else:
        return "field:" + field_name + "_field_i"

def get_data_prop_uri(field_name, tablename='', base=""):
    if len(tablename) > 0:
        return get_uri(tablename + "/data_property/" + field_name + "_data_value", base)
    else:
        return "data_property:" + field_name + "_data_value"

def get_record_uri(tablename, record_idx, record_name='', base=""):
    if len(record_name) > 0:
        return get_uri(tablename + "/record/" + record_name + str(record_idx) + "_i", base)
    else:
        return "record:" + tablename + "_record_" + str(record_idx) + "_i"

def get_field_value_uri(field_name, record_idx, tablename='', base=""):
    if len(tablename) > 0:
        return get_uri(tablename + "/field_value/" + field_name + "_field_value_" + str(record_idx) + "_i", base)
    else:
        return "field_value:" + field_name + "_field_value_" + str(record_idx) + "_i"


def declare_instance(insance_uri ,class_uri, member_uri=""):
    if len(member_uri) > 0:
        return "{0} rdf:type owl:NamedIndividual, {1}; :member_of {2} .".format(insance_uri, class_uri, member_uri)
    else:
        return "{0} rdf:type {1} .".format(insance_uri, class_uri)
    pass

def declare_class(class_uri, super_uri=""):
    if len(super_uri) > 0:
        return "{0} rdf:type owl:Class; rdfs:subClassOf {1} .".format(class_uri, super_uri)
    else:
        return "{0} rdf:type owl:Class .".format(class_uri)

def declare_data_property(data_property_uri):
    return "{0} rdf:type owl:DatatypeProperty .".format(data_property_uri)

