import os
import re
import rdflib
from rdflib import URIRef


def make_uri(base_uri, entity_uri="", base_end_char="/"):
    """:returns a URIRef based on the base uri and entity uri"""

    base_uri = parse_base_uri(base_uri, base_end_char)
    if len(str(entity_uri).strip()) > 0:
        uri = "%s%s%s" % (str(base_uri), str(base_end_char).strip(), str(entity_uri).strip())
        return URIRef(uri.strip())
    else:
        return URIRef(str(base_uri).strip())


def parse_base_uri(base_uri, base_end_char="/"):
    """formats the base uri so that it ends with a '/','#', or the end_char"""
    if str(base_uri).endswith("/") or str(base_uri).endswith("#"):
        return base_uri
    else:
        return "{0}{1}".format(str(base_uri).strip(), str(base_end_char).strip())


def strip_extension(name):
    """character's after the first '.' in name"""
    return  name.split('.') [0]


def parse_python_name(name):
    """parses name into valid python syntax"""
    py_name = name.replace(' ', '_')
    py_name = py_name.replace('.', '_')
    py_name = py_name.replace('-', '_')
    py_name = py_name.replace('+', '_')
    py_name = py_name.replace('=', '_')
    py_name = py_name.replace('!', '_')
    py_name = py_name.replace(',', '_')
    py_name = py_name.replace('*', '_')
    py_name = py_name.replace('@', '_')
    py_name = py_name.replace('&', '_')
    py_name = py_name.replace('$', '_')
    py_name = py_name.replace('~', '_')
    py_name = py_name.replace('?', '_')
    py_name = py_name.replace(':', '_')
    py_name = py_name.replace('%20', '_')
    py_name = re.sub(r'[^a-z,A-Z,0-9,_]', '', py_name)
    return py_name


def parse_uri_as_label(uri, make_lower=True, make_upper=False, replace_underscore=False):
    """
    for uris that have label like ending (e.g., http://example.com/foo_bar)
    return the last portion (e.g., foo_bar)
    if replace_underscore is true, the underscrores are replaced with sapces (e.g., foo bar)
    """
    # use the last portion of the uri as label
    # use encode('ascii', 'ignore') to ignore unicode characters
    if '#' in str(uri):  # check if uri uses '#' syntax
        short_uri = str(uri.encode('ascii', 'ignore')).split('#')[-1]
    else:
        short_uri = str(uri.encode('ascii', 'ignore')).split('/')[-1]

    # determine underscore usage
    if replace_underscore:
        short_uri = short_uri.replace("_", " ")

    # determine case
    if make_lower:
        short_uri = parse_python_name(short_uri.lower())
    elif make_upper:
        short_uri = parse_python_name(short_uri.upper())

    return short_uri


def parse_file_name(data_file, remove_extension=False):
    """
    returns the last part of a file name (e.g., /user/data/foo.xml -> foo.xml)
    if remove_extension is True, the characters after the last period are removed
    """
    file_name = str(data_file.encode('ascii', 'ignore')).strip().split('/')[-1]
    if remove_extension:
        file_name = strip_extension(file_name)

    return file_name



