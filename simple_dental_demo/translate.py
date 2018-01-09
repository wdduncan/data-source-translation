import pandas as pds
from lib.ttl_template import *

def translate_patients(data_file='lib/patients_1.xlsx', output_file='output/patients_1.ttl'):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()

    # add column of patient uris
    temp = map(patient_uri, df['patient_id'])
    df['patient_uri'] = temp

    # add column of gender uris
    temp = map(gender_uri, df['patient_id'], df['gender'])
    df['gender_uri'] = temp

    # add column of gender class uris
    temp = map(gender_class_uri, df['gender'])
    df['gender_class_uri'] = temp

    slice = df[['patient_id', 'patient_uri', 'gender_uri', 'gender_class_uri', 'birth_date']]
    for (idx, patient_id, puri, guri, gclass, dob) in slice.itertuples():
        # create patient triples
        label = """ "patient {0}" """.format(str(patient_id))
        print declare_individual(puri, ":patient", label)
        print birth_date(puri, dob) + "\n" # patient's birth date

        # create gender triples
        label = """ "patient {0} gender" """.format(str(patient_id))
        print declare_individual(guri, gclass, label)
        print has_quality(puri, guri) + "\n" # relate gender to patient



def translate_services(data_file='lib/services_1.xlsx', output_file='output/services_1.ttl'):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()

    # add column of patient uris
    temp = map(patient_uri, df['patient_id'])
    df['patient_uri'] = temp

    # add column of provider uris
    temp = map(provider_uri, df['provider_id'])
    df['provider_uri'] = temp

    # add column of tooth uris
    temp = map(tooth_uri, df['patient_id'], df['tooth'])
    df['tooth_uri'] = temp

    # add column of tooth class uris
    temp = map(tooth_class_uri, df['tooth'])
    df['tooth_class_uri'] = temp

    # add column of procedure uris
    temp = map(procedure_uri, df['service_id'])
    df['procedure_uri'] = temp

    # add column of material uris
    temp = map(material_uri, df['service_code'], df['service_id'])
    df['material_uri'] = temp

    #add column of material class uris
    temp = map(material_class_uri, df['service_code'])
    df['material_class_uri'] = temp

    slice = df[['patient_id','provider_id', 'tooth', 'service_code', 'service_date',
                'patient_uri', 'provider_uri','tooth_uri', 'tooth_class_uri',
                'procedure_uri', 'material_uri', 'material_class_uri']]
    for (idx, pt_id, prov_id, tooth, code, date, pt_uri, prov_uri,
         tth_uri, tth_class_uri, proc_uri, mat_uri, mat_class_uri) in slice.itertuples():
        print pt_uri

    print df

translate_services()