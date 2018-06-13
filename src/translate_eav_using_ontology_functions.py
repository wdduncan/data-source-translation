import pandas as pds
from translation_lib.util.uri_util import *
from translation_lib.rdf.translation_operations import *
from rdflib import Graph, RDF, RDFS, OWL, Namespace, BNode, URIRef, Literal, XSD
import translation_lib.util.data_source_ontology_generated_functions_rdflib as gof

def translate_raw_values(raw_data, eav_metadata):
    df = raw_data
    metadata = eav_metadata

    # create dictionaries for value lookups of multiple choice columns
    dicts = {}
    for row in metadata.itertuples():
        row = row.__dict__

        # no code list for this item so skip it e.g. MRN or any other text field
        if row['element_enum'] == '(null)':
            continue

        project_id = str(row['project_id'])
        field_name = str(row['field_name'])
        codes = str(row['element_enum']).replace(' \\n ', '|')
        code_split = codes.split('|')

        codes_out = {}
        for item in code_split:
            couplet = item.split(',')
            try:
                codes_out[couplet[0]] = str(couplet[1]).strip()
            # typically throws this error for calculated fields and non code lists
            except IndexError:
                continue
        # allows handling of multiple project's data and terms
        if project_id not in dicts:
            dicts[project_id] = {}
        dicts[project_id][field_name] = codes_out

    # do lookups of multiple choice columns to get human readable label
    value_desc = []
    for row in df.itertuples():
        row = row.__dict__
        # codes always cast as floats
        value = str(row['value']).replace('.0', '')
        project_id = str(row['project_id'])
        try:
            value_desc.append(dicts[project_id][str(row['field_name'])][value])
        except:
            value_desc.append('n/a')

    df['value_desc'] = value_desc
    return df

def translate_eav(data_file, meta_data_file, field_semantic_codes_file=""):
    # metadata in this case is only used to get literal value lined up with coded raw value
    raw_data = pds.read_csv(data_file, sep='\t')
    meta_data = pds.read_csv(meta_data_file, sep='\t')

    # pass in a file with project_id, field_name, ncit in order to relate across DBs
    field_semantic_types = {}
    if field_semantic_codes_file != "":
        semantic_codes_df = pds.read_csv(field_semantic_codes_file, sep='\t')
        for row in semantic_codes_df.itertuples():
            row = row.__dict__
            project_id = str(row['project_id'])
            field_name = str(row['field_name'])

            if project_id not in field_semantic_types:
                field_semantic_types[project_id] = {}
            if field_name not in field_semantic_types[project_id]:
                field_semantic_types[project_id][field_name] = str(row['semantic_field_type'])

    df = translate_raw_values(raw_data, meta_data)

    # get unique columns and record:data in dataframe
    records = {}
    columns = []
    for row in df.itertuples():
        # static nature of REDCap EAV columns means we can reference column names in dict format
        row = row.__dict__
        if row['field_name'] not in columns:
            columns.append(row['field_name'])

        instance = str(row['instance']) if str(row['instance']) != '(null)' else '0'
        record = str(row['record']) + '_' + str(row['project_id']) + '_' + str(row['event_id']) + '_' + instance
        if record not in records:
            records[record] = {}

        value = str(row['value_desc']) if row['value_desc'] != 'n/a' else str(row['value'])
        # data randomly gets floated sometimes
        if value[-2:] == '.0':
            value = value.replace('.0', '')

        if row['field_name'] not in records[record]:
            records[record][row['field_name']] = value

        # have to handle multiple value check boxes as concatenated strings
        elif row['field_name'] in records[record]:
            if value not in records[record][row['field_name']]:
                records[record][row['field_name']] += '|| %s' % value

    for record, data in records.items():
        for column in columns:
            if column not in records[record]:
                records[record][column] = '(null)'

    df_transform = pds.DataFrame.from_dict(records, orient='index')

    g = make_data_graph_df(df_transform, "http://purl.example.translation/", "http://foo-bar.com", field_semantic_types=field_semantic_types)
    print g.serialize(format="turtle")

    return g

def make_data_graph_df(df, data_namespace_uri, data_source="", data_source_base_uri="", field_semantic_types={}):
    # namespaces for data being translated
    data = Namespace(parse_base_uri(data_namespace_uri))  # base uri
    fv = Namespace(data + "data_property/field_value/")  # field values (shortcut)
    fdi = Namespace(data + "object_property/field_data_item/")  # field data items (shortcut)

    # create datasource uri
    data_source_uri = None
    if len(data_source.strip()) > 0:
        data_source = parse_python_name(data_source)
        if (data_source_base_uri.strip()) > 0:
            data_source_uri = make_uri(data_source_base_uri, data_source)
        else:
            data_source_uri = make_uri(data, data_source)

    # declare graph to hold triples
    graph = Graph(identifier=data_namespace_uri)

    # add data source to ontology
    if data_source_uri:
        gof.declare_individual(graph, data_source_uri, gof.data_source_uri)

    # create a maps of:
    #   field names -> uris
    #   field names -> field value uris (data properties)
    #   field names -> field data item uris (object properties)
    field_map = make_field_uri_map(data.data_field, list(df.columns))
    fv_map = make_field_uri_map(fv, list(df.columns))
    fdi_map = make_field_uri_map(fdi, list(df.columns))

    # declare fields in field map
    for field_uri in field_map.values():
        gof.declare_individual(graph, field_uri, gof.data_field_uri)

    # assign semantic types to fields
    if field_semantic_types:
        for project, fields in field_semantic_types.items():
            for field, code in fields.items():
                gof.semantic_type(graph, field_map[field], uri2='http://purl.obolibrary.org/obo/%s' % code)

    # declare field value data and field data item properties (shortcut properties)
    # these properties help make querying easier
    for col_name in list(df.columns):
        fv_uri = make_uri(fv, col_name)
        gof.declare_data_property(graph, fv_uri, gof.field_value_uri)

        fdi_uri = make_uri(fdi, col_name)
        gof.declare_object_property(graph, fdi_uri, gof.has_member_uri)

    # translate data
    for (idx, series) in df.iterrows():
        record_uri = make_uri(data.data_record, idx)
        gof.declare_individual(graph, record_uri, gof.data_record_uri)

        # link reord to data source (if given)
        if data_source_uri:
            gof.has_member(graph, data_source_uri, record_uri)

        # filter out (null) values
        processed_series = []
        for (field_name, value) in series.iteritems():
            if value != '(null)':
                # split out multiple values to overload checkbox field_names
                if str(value).split('||') > 1:
                    values = str(value).split('||')
                    for val in values:
                        processed_series.append((field_name, str(val).strip()))
                else:
                    processed_series.append((field_name, value))

        for (field_name, value) in processed_series:

            field_uri = field_map[field_name]
            data_item_uri = make_uri(record_uri, field_name)

            # declare data item (and value)
            gof.declare_individual(graph, data_item_uri, gof.data_item_uri)
            gof.data_value(graph, data_item_uri, value)

            # relate data item to record and field
            gof.has_member(graph, record_uri, data_item_uri)
            gof.has_member(graph, field_uri, data_item_uri)

            # relate record to value (i.e., field value) (shortcut)
            fv_uri = fv_map[field_name]
            graph.add((record_uri, fv_uri, Literal(value)))

            # relate record to data item (field data item) (shortcut)
            fdi_uri = fdi_map[field_name]
            graph.add((record_uri, fdi_uri, data_item_uri))

    return graph

if __name__ == "__main__":
    translate_eav(
        data_file=r'test_data/EAV_sample_raw_data.txt',
        meta_data_file=r'test_data/EAV_sample_meta_data.txt',
        field_semantic_codes_file=r'test_data/EAV_sample_field_semantic_data.txt'
    )