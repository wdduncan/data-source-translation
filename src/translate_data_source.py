import pandas as pd

def translate_data_to_ttl(filename):
    # get data from RI-demo-data
    df = pd.ExcelFile(filename).parse()

    # testing...
    # print df

    #  create instance of table
    print uri('table/' + filename) + ' rdf:type ' + uri('table') + ' .'

    # get list of fields
    fields = list(df)
    for field in fields:
        # create instance of field
        print uri(filename + '/field/' + field) + ' rdf:type ' + uri('field') + ' .'

    for record in df.itertuples():
        # create instance of record
        record_id = record[0]
        # print record_id
        record_uri = uri('table/record/' + str(record_id))
        print record_uri  + ' rdf:type ' + uri('record') + ' .'

        for index in range(1, (len(fields)+1)): # note: need to add 1 to length of fields
            print # create instance of entity that is represented by the val
            entity_uri = uri('entity/' + filename + '/field' + str(index) + '/' + str(record_id))
            print entity_uri + ' rdf:type ' + uri('entity') + ' .'

            # data that represents the entity
            print entity_uri + ' ' + uri('represented_by') + ' ' + "'" + str(record[index]) + "'" + ' .'

            # relate entity to record
            print record_uri + ' ' + uri('denotes') + ' ' + entity_uri + ' .'

            # relate field to record
            print uri(filename + '/field' + str(index)) + ' ' + uri('denotes') + ' ' + entity_uri + ' .'


def uri(val):
    return "http://purl.obolibrary.org/obo/db_mapping.owl/" + val

translate_data_to_ttl('patients.xlsx')