def get_uri(val, base=''):
    if base:
        return "<" + base + val + ">"
    else:
        return "<" + val + ">"

def get_table_uri(filename='', base=''):
    if filename:
        return get_uri(filename + '_i', base)
    else:
        return 'filename:_i'

def get_field_uri(field_name, filename='', base=''):
    if filename:
        return get_uri(filename + '/field/' + field_name + '_i', base)
    else:
        return 'field:' + field_name + '_i'

def get_prop_uri(field_name, filename='', base=''):
    if filename:
        return get_uri(filename + '/field/' + field_name + '_i', base)
    else:
        return 'field:' + field_name + '_i'

def get_record_uri():
    pass

def get_field_value_uri():
    pass
