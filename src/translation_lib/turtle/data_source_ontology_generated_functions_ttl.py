################# object properties #################


def data_relation(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/data_relation> %s . \n" % (uri1, uri2) 


def data_relation_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/data_relation/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/data_relation>" 


def defined_by(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/defined_by> %s . \n" % (uri1, uri2) 


def defined_by_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/defined_by/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/defined_by>" 


def defines(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/defines> %s . \n" % (uri1, uri2) 


def defines_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/defines/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/defines>" 


################# data properties #################


def has_int_value(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/has_int_value> %s . \n" % (uri1, uri2) 


def has_int_value_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/has_int_value/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/has_int_value>" 


def has_value(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/has_value> %s . \n" % (uri1, uri2) 


def has_value_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/has_value/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/has_value>" 


def has_string_value(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/has_string_value> %s . \n" % (uri1, uri2) 


def has_string_value_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/has_string_value/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/has_string_value>" 


def has_float_value(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/has_float_value> %s . \n" % (uri1, uri2) 


def has_float_value_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/has_float_value/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/has_float_value>" 


def has_datetime_value(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/has_datetime_value> %s . \n" % (uri1, uri2) 


def has_datetime_value_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/has_datetime_value/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/has_datetime_value>" 


def has_integer_value(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/has_integer_value> %s . \n" % (uri1, uri2) 


def has_integer_value_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/has_integer_value/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/has_integer_value>" 


################# annotation properties #################


def database_name(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/database_name> %s . \n" % (uri1, uri2) 


def database_name_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/database_name/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/database_name>" 


def date(uri1, uri2):
    return "%s <http://purl.org/dc/elements/1.1/date> %s . \n" % (uri1, uri2) 


def date_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.org/dc/elements/1.1/date/%s>" % id
    else:
        return "<http://purl.org/dc/elements/1.1/date>" 


def project_name(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/project_name> %s . \n" % (uri1, uri2) 


def project_name_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/project_name/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/project_name>" 


def table_name(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/table_name> %s . \n" % (uri1, uri2) 


def table_name_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/table_name/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/table_name>" 


def creator(uri1, uri2):
    return "%s <http://purl.org/dc/elements/1.1/creator> %s . \n" % (uri1, uri2) 


def creator_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.org/dc/elements/1.1/creator/%s>" % id
    else:
        return "<http://purl.org/dc/elements/1.1/creator>" 


def file_type(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/file_type> %s . \n" % (uri1, uri2) 


def file_type_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/file_type/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/file_type>" 


def semantic_translation(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/semantic_translation> %s . \n" % (uri1, uri2) 


def semantic_translation_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/semantic_translation/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/semantic_translation>" 


def server_name(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/server_name> %s . \n" % (uri1, uri2) 


def server_name_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/server_name/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/server_name>" 


def file_format(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/file_format> %s . \n" % (uri1, uri2) 


def file_format_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/file_format/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/file_format>" 


def semantic_source(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/semantic_source> %s . \n" % (uri1, uri2) 


def semantic_source_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/semantic_source/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/semantic_source>" 


def datatype_size(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/datatype_size> %s . \n" % (uri1, uri2) 


def datatype_size_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/datatype_size/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/datatype_size>" 


def file_name(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/file_name> %s . \n" % (uri1, uri2) 


def file_name_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/file_name/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/file_name>" 


def semantic_type(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/semantic_type> %s . \n" % (uri1, uri2) 


def semantic_type_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/semantic_type/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/semantic_type>" 


def isruleenabled(uri1, uri2):
    return "%s <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled> %s . \n" % (uri1, uri2) 


def isruleenabled_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled/%s>" % id
    else:
        return "<http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled>" 


def datatype(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/datatype> %s . \n" % (uri1, uri2) 


def datatype_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/datatype/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/datatype>" 


def file_delimiter(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/file_delimiter> %s . \n" % (uri1, uri2) 


def file_delimiter_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/file_delimiter/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/file_delimiter>" 


def database_type(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/database_type> %s . \n" % (uri1, uri2) 


def database_type_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/database_type/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/database_type>" 


def field_name(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/field_name> %s . \n" % (uri1, uri2) 


def field_name_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/field_name/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/field_name>" 


################# classes #################


def data_specification_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/data_specification/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/data_specification>" 


def data_item_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/data_item/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/data_item>" 


def relational_database_schema_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/relational_database_schema/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/relational_database_schema>" 


def data_table_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/data_table/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/data_table>" 


def data_value_domain_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/data_value_domain/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/data_value_domain>" 


def data_field_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/data_field/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/data_field>" 


def data_element_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/data_element/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/data_element>" 


def data_source_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/data_source/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/data_source>" 


def data_schema_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/data_schema/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/data_schema>" 


def data_file_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/data_file/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/data_file>" 


def common_data_element_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/common_data_element/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/common_data_element>" 


def dataset_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/dataset/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/dataset>" 


def spreadsheet_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/spreadsheet/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/spreadsheet>" 


def data_record_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/data_record/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/data_record>" 


def relational_database_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/relational_database/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/relational_database>" 


def database_uri(id=""):
    if len(id.strip()) > 0:
        return "<http://purl.data-source-translation.org/database/%s>" % id
    else:
        return "<http://purl.data-source-translation.org/database>" 

