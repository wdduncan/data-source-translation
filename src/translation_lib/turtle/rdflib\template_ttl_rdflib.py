from textwrap import dedent
from rdflib import Graph,URIRef,RDF,OWL,RDFS
import re

#Declare graph
g = Graph()

#Function to declare individual
def declare_individual(uri, class_uri,label=""):

    uri =  URIRef(uri)
    class_uri = URIRef(class_uri)

    #Create graph of URI
    g.add((uri,RDF.type,OWL.NamedIndividual))

    #Declaring a Class URI
    g.add((class_uri, RDF.type, OWL.NamedIndividual))

    if len(label.strip()) > 0:
        g.add((uri,RDFS.label,URIRef(label)))

    return g.serialize(format="turtle")

#Function to generate a triple
def triple(subj,pred,obj):

    subj = URIRef(subj)
    pred = URIRef(pred)
    obj = URIRef(obj)

    #Create a graph of a triple with subject, predicate and object
    g.add((subj,pred,obj))

    return g.serialize(format="turtle")

#Function to declare a class
def declare_class(class_uri,parent_uri,label=""):

    class_uri = URIRef(class_uri)
    parent_uri = URIRef(parent_uri)

    #Declaring an OWL Class
    g.add((class_uri,RDF.type,OWL.Class))

    if len(parent_uri.strip()) > 0:
        g.add((class_uri,RDFS.subClassOf,parent_uri))

    if len(label.strip()) > 0:
        g.add((class_uri,RDFS.label,URIRef(label)))


    return g.serialize(format="turtle")

#Function to declare Object property
def declare_object_property(prop_uri,parent_uri,label=""):

    prop_uri = URIRef(prop_uri)

    #Declaring an object property
    g.add((prop_uri,RDF.type,OWL.ObjectProperty))

    if len(parent_uri.strip()) > 0:
        g.add((prop_uri, RDFS.subPropertyOf, parent_uri))

    if len(label.strip()) > 0:
        g.add((prop_uri, RDFS.label, URIRef(label)))

    return g.serialize(format="turtle")


# Function to declare Data property
def declare_data_property(prop_uri,parent_uri,label=""):
    prop_uri = URIRef(prop_uri)

    # Declaring an data property
    g.add((prop_uri, RDF.type, OWL.DataProperty))

    if len(parent_uri.strip()) > 0:
        g.add((prop_uri, RDFS.subPropertyOf, parent_uri))

    if len(label.strip()) > 0:
        g.add((prop_uri, RDFS.label, URIRef(label)))

    return g.serialize(format="turtle")

def format_uri_name(name):
    uri_name = name.replace(' ', '_')
    uri_name = uri_name.replace('.', '_')
    uri_name = uri_name.replace('-', '_')
    uri_name = uri_name.replace('+', '_')
    uri_name = uri_name.replace('=', '_')
    uri_name = uri_name.replace('!', '_')
    uri_name = uri_name.replace(',', '_')
    uri_name = uri_name.replace('*', '_')
    uri_name = uri_name.replace('@', '_')
    uri_name = uri_name.replace('&', '_')
    uri_name = uri_name.replace('$', '_')
    uri_name = uri_name.replace('~', '_')
    uri_name = uri_name.replace('?', '_')
    uri_name = uri_name.replace(':', '_')
    uri_name = uri_name.replace('%20', '_')
    uri_name = re.sub(r'[^a-z,A-Z,0-9,_]', '', uri_name)
    return uri_name








