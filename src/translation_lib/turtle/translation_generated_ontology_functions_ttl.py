### object properties ###

def data_relation_ttl(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/data_relation> %s . \n" % (uri1, uri2) 


### data properties ###

def has_string_value_ttl(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/has_string_value> %s . \n" % (uri1, uri2) 

def has_value_ttl(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/has_value> %s . \n" % (uri1, uri2) 

def has_date_time_value_ttl(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/has_date_time_value> %s . \n" % (uri1, uri2) 

def has_int_value_ttl(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/has_int_value> %s . \n" % (uri1, uri2) 

def has_integer_value_ttl(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/has_integer_value> %s . \n" % (uri1, uri2) 

def has_float_value_ttl(uri1, uri2):
    return "%s <http://purl.data-source-translation.org/has_float_value> %s . \n" % (uri1, uri2) 


### classes ###

def data_schema_uri(id):
    return "<http://purl.data-source-translation.org/data_schema/individual/%s>" % id 

def data_field_uri(id):
    return "<http://purl.data-source-translation.org/data_field/individual/%s>" % id 

def data_element_uri(id):
    return "<http://purl.data-source-translation.org/data_element/individual/%s>" % id 

def relational_database_schema_uri(id):
    return "<http://purl.data-source-translation.org/relational_database_schema/individual/%s>" % id 

def dataset_uri(id):
    return "<http://purl.data-source-translation.org/dataset/individual/%s>" % id 

def data_specification_uri(id):
    return "<http://purl.data-source-translation.org/data_specification/individual/%s>" % id 

def spreadsheet_uri(id):
    return "<http://purl.data-source-translation.org/spreadsheet/individual/%s>" % id 

def data_value_domain_uri(id):
    return "<http://purl.data-source-translation.org/data_value_domain/individual/%s>" % id 

def data_file_uri(id):
    return "<http://purl.data-source-translation.org/data_file/individual/%s>" % id 

def database_uri(id):
    return "<http://purl.data-source-translation.org/database/individual/%s>" % id 

def data_record_uri(id):
    return "<http://purl.data-source-translation.org/data_record/individual/%s>" % id 

def data_source_uri(id):
    return "<http://purl.data-source-translation.org/data_source/individual/%s>" % id 

def relational_database_uri(id):
    return "<http://purl.data-source-translation.org/relational_database/individual/%s>" % id 

def data_item_uri(id):
    return "<http://purl.data-source-translation.org/data_item/individual/%s>" % id 

def common_data_element_uri(id):
    return "<http://purl.data-source-translation.org/common_data_element/individual/%s>" % id 

def data_table_uri(id):
    return "<http://purl.data-source-translation.org/data_table/individual/%s>" % id 

