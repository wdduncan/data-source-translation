# coding=utf-8
from textwrap import dedent
import uuid
import translation_ontology_functions_ttl as txf


def prefixes(base="", ontology_uri=""):
    # specify the base uri
    if base.strip() == "":
        base = "http://purl.data-source-translation.org/"

    # create uri for ontology
    if ontology_uri.strip() == "":
        ontology_uri = "http://purl.obolibrary.org/obo/my_translated-data-source.owl"

    ttl = dedent("""\
        # axioms for prefixes
        @prefix dc: <http://purl.org/dc/elements/1.1/> .
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix swrl: <http://www.w3.org/2003/11/swrl#> .
        @prefix swrla: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
        @prefix swrlb: <http://www.w3.org/2003/11/swrlb#> .
        @prefix xml: <http://www.w3.org/XML/1998/namespace> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        @prefix sesame: <http://www.openrdf.org/schema/sesame#> .

        # custom prefixes
        @base <{0}> .
        @prefix dst: <http://purl.data-source-translation.org/>

        # ontology uri
        <{1}> rdf:type owl:Ontology .

        """.format(base, ontology_uri))
    return ttl


def format_base_uri(base, end_char="/"):
    if base.endswith("/") or base.endswith("#"):
        return base
    else:
        return "{0}{1}".format(base, end_char)


def format_data_file_name(data_file):
    name = str(data_file.encode('ascii', 'ignore')).split('/')[-1]
    return name.strip()


def translate_df(df, ontology_uri, base):
    axioms = [prefixes(base, ontology_uri)] # inialize axioms with prefixes

    # declare field names as object properties
    axioms.append(translate_df_fields(df))

    return axioms


def translate_df_fields(df):
    ttls = ["\n# declare object properties"]

    field_names = list(df.columns)
    for field_name in field_names:
        uri = "<data_relation/{0}>".format(txf.format_uri_name(field_name))
        ttl = txf.declare_object_property(uri, field_name, txf.data_relation_uri())
        ttls.append(ttl)

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl


def translate_df_records(df):
    def set_field_uris(x):
        return "<data_relation/{0}>".format(txf.format_uri_name(x))

    def set_data_item_uris(x):
        return "<data_item/{0}>".format(uuid.uuid4())

    ttls = ["\n# declare records"]

    field_uris = map(set_field_uris, list(df.columns)) # get list field name uris

    for record in df.itertuples():
        record_uri = "<data_record/{0}>".format(uuid.uuid4()) # create record uri
        ttls.append(txf.declare_individual(record_uri, txf.data_record_uri()))

        values = record[1:] # get list of values in record, NB: start with 1; 0 is the index
        data_item_uris = map(set_data_item_uris, values) # create list of uris for each data item

        for idx, data_item_uri in enumerate(data_item_uris):
            # create individual data items with values
            ttls.append(txf.declare_individual(data_item_uri, txf.data_item_uri()))
            ttls.append(txf.has_value(data_item_uri, values[idx]))

            # relate data item to record
            ttls.append(txf.triple(record_uri, field_uris[idx], data_item_uri))

    # join all ttl statements
    ttl = "\n".join(ttls)
    return ttl
