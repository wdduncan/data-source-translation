def get_uri(val, base=''):
    if base:
        return "<" + base + val + ">"
    else:
        return "<" + val + ">"

def get_table_uri(tablename='', base=''):
    if tablename:
        return get_uri(tablename + '_i', base)
    else:
        return 'tablename:_i'

def get_field_uri(field_name, tablename='', base=''):
    if tablename:
        return get_uri(tablename + '/field/' + field_name + '_i', base)
    else:
        return 'field:' + field_name + '_i'

def get_data_prop_uri(field_name, tablename='', base=''):
    if tablename:
        return get_uri(tablename + '/data_property/' + field_name + '_data_value', base)
    else:
        return 'data_property:' + field_name + '_data_value'

def get_record_uri(tablename, record_idx, record_name='', base=''):
    if record_name:
        return get_uri(tablename + '/record/' + record_name + str(record_idx) + '_i', base)
    else:
        return 'record:' + tablename + '_record_' + str(record_idx) + '_i'

def get_field_value_uri(field_name, record_idx, tablename='', base=''):
    if tablename:
        return get_uri(tablename + '/field_value/' + field_name + '_value_' + str(record_idx) + '_i', base)
    else:
        return 'field_value:' + field_name + '_value_' + str(record_idx) + '_i'
