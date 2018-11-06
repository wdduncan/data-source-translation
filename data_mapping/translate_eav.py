import pandas as pds
from rdflib import Graph, BNode, RDF, RDFS, OWL, Namespace, BNode, URIRef, Literal, XSD
from rdflib.namespace import NamespaceManager
from pprint import pprint


def make_iri_map_fn(iri_map):
    def fn(key):
        if key in iri_map:
            return URIRef(iri_map[key])
        else:
            return None
    return fn

if __name__ == "__main__":
    iri_map =\
        {
            'base': 'http://ex.com/',
            'entity_base': 'http://ex.com/entity/',
            'record': 'http://ex.com/dp_record',
            'field': 'http://ex.com/dp_field',
            'value': 'http://ex.com/dp_value'
         }
    miri = make_iri_map_fn(iri_map)
    # print(miri('record'))
    df = pds.read_excel('patients_1_eav.xlsx')

    g = Graph()
    for r in df.itertuples():
        # print(r.record)
        # if "record_1" == str(r.record):
        b = BNode()        # create record as blank node
        g.add((b, miri('record'), Literal(r.record)))
        g.add((b, miri('field'), Literal(r.field)))
        g.add((b, miri('value'), Literal(r.value)))

    for (s, _, record) in g.triples((None, miri('record'), None)):
        doc = """
            {
              "@context":
              {
                 "@vocab": "http://foo.com/"
                 "rp": "http://purl.roswellpark.org/ontology#"
                 "data_record": "rp:DE_000000003"
                 "data_field": "rp:DE_000000007"
                 "dp": "rp:DE_000000007#db_"
                 "data_record_i":  "rp:DE_000000003#"
              },
              "@id": "data_record_i:%s"
              "@type": "data_record"
            }""" % record

        # for (s, _, field) in g.triples((s, miri('field'), None)):
        for field in g[s:miri('field')]:
            print(field)

        # print(doc)

    # pprint(str(g.serialize(format='turtle')))

    # qry = """
    #     construct {
    #         ?record a <http://example.com/data_record>;
    #                 ?field ?v .
    #     } where {
    #        ?b <http://ex.com/dp_record> ?r;
    #           <http://ex.com/dp_field> ?f;
    #           <http://ex.com/dp_value> ?v .
    #
    #         bind(iri(concat("http://example.com/record#", ?r)) as ?record)
    #         bind(iri(concat("http://example.com/field#", ?f)) as ?field)
    #     }
    # """
    #
    # results = g.query(qry)
    # for r in results:
    #     print(r)
    # # create instance of record
