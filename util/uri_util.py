import os
import rdflib
from rdflib import ConjunctiveGraph, URIRef, RDFS, Literal
from datetime import datetime


def make_uri_map(filename):
    # build graph
    g = rdflib.Graph()
    g.parse(filename)

    # add mapping: lowercase label -> uri
    uri_map = {}
    for uri, p, label in g.triples((None, RDFS.label, None)):
        # use encode('ascii', 'ignore') to ignore unicode characters
        uri_map[str(label.encode('ascii', 'ignore')).lower()] = str(uri.encode('ascii', 'ignore'))

    return uri_map

def write_uri_map(uri_map, filename='uri_map.txt'):
    # save label2uri to file
    with open(filename, 'w') as f:
        f.write(str(uri_map)) # note: label2uri is converted to string


def load_uri_map(force=False, filepath=__file__, filename='uri_map.txt'):
    # create and the lable2uri under the following two coditions:
    # the file does NOT exist OR force is True
    # uri_map_full_name = os.path.join(filepath, filename)
    uri_map_full_name = os.path.join(os.path.abspath('.'), filename)
    if force == True or os.path.exists(uri_map_full_name) == False:
        # print "creating map"
        # make the uri_map map
        uri_map = make_uri_map()

        # write uri_map to file
        write_uri_map(uri_map, uri_map_full_name)

    # otherwise read uri_map from file
    else:
        # print "load from file"
        uri_map = eval(open(uri_map_full_name).read())

    # return uri_map
    return uri_map