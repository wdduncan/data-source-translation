import pandas as pds
from lib.ttl_template import *


def make_patient_df(data_file):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()

    # add column of patient uris
    temp = map(ttl_patient_uri, df['patient_id'])
    df['patient_uri'] = temp

    # add column of gender uris
    temp = map(ttl_gender_uri, df['patient_id'], df['gender'])
    df['gender_uri'] = temp

    # add column of gender class uris
    temp = map(ttl_gender_class_uri, df['gender'])
    df['gender_class_uri'] = temp

    return df


def translate_patients(data_file='lib/patients_1.xlsx',
                       output_file='output/patients_1.ttl',
                       print_ttl=True,
                       save_ttl=False):
    # create patient dataframe with uris
    df = make_patient_df(data_file)

    with open(output_file, 'w') as f:
        # local function for printing and saving turtle output
        def output(value_str, print_ttl=print_ttl, save_ttl=save_ttl):
            if print_ttl == True: print value_str
            if save_ttl == True: f.write(value_str)

        # output prefixes
        output(ttl_prefixes())

        slice = df[['patient_id', 'patient_uri', 'gender_uri', 'gender_class_uri', 'birth_date']]
        for (idx, patient_id, puri, guri, gclass, dob) in slice.itertuples():
            # create patient triples
            label = """patient {0}""".format(str(patient_id))
            output(ttl_declare_individual(puri, ":patient", label))
            output(ttl_birth_date(puri, dob) + "\n") # patient's birth date

            # create gender triples
            label = """patient {0} gender""".format(str(patient_id))
            output(ttl_declare_individual(guri, gclass, label))
            output(ttl_has_quality(puri, guri) + "\n") # relate gender to patient


def make_services_df(data_file):
    # load Excel file into dataframe
    df = pds.ExcelFile(data_file).parse()

    # add column of patient uris
    temp = map(ttl_patient_uri, df['patient_id'])
    df['patient_uri'] = temp

    # add column of provider uris
    temp = map(ttl_provider_uri, df['provider_id'])
    df['provider_uri'] = temp

    # add column of tooth uris
    temp = map(ttl_tooth_uri, df['patient_id'], df['tooth'])
    df['tooth_uri'] = temp

    # add column of tooth class uris
    temp = map(ttl_tooth_class_uri, df['tooth'])
    df['tooth_class_uri'] = temp

    # add column of procedure uris
    temp = map(ttl_procedure_uri, df['service_id'])
    df['procedure_uri'] = temp

    # add column of service code uris
    temp = map(ttl_service_code_uri, df['service_id'], df['service_code'])
    df['service_code_uri'] = temp

    # add column of service code class uris
    temp = map(ttl_service_code_class_uri, df['service_code'])
    df['service_code_class_uri'] = temp

    # add column of material uris
    temp = map(ttl_material_uri, df['service_code'], df['service_id'])
    df['material_uri'] = temp

    # add column of material class uris
    temp = map(ttl_material_class_uri, df['service_code'])
    df['material_class_uri'] = temp

    # add column of material names
    temp = map(ttl_material_name, df['service_code'])
    df['material_name'] = temp

    return df


def translate_services(data_file='lib/services_1.xlsx',
                       output_file='output/services_1.ttl',
                       print_ttl=True,
                       save_ttl=False):
    # create services dataframe with uris
    df = make_services_df(data_file)

    with open(output_file, 'w') as f:
        # local function for printing and saving turtle output
        def output(value_str, print_ttl=print_ttl, save_ttl=save_ttl):
            if print_ttl == True: print value_str
            if save_ttl == True: f.write(value_str)

        # output prefixes
        output(ttl_prefixes())


        slice = \
            df[['patient_id','provider_id', 'tooth',
                'surface', 'service_code', 'service_date',
                'patient_uri', 'provider_uri','tooth_uri',
                'tooth_class_uri','service_code_uri', 'service_code_class_uri',
                'procedure_uri','material_uri', 'material_class_uri', 'material_name']]

        for (idx, pt_id, prov_id, tooth,
             surface, code, srv_date,
             pt_uri, prov_uri, tth_uri,
             tth_class_uri, code_uri, code_class_uri,
             proc_uri, mat_uri, mat_class_uri, mat_name) in slice.itertuples():

            # create triples for individuals
            output(ttl_declare_individual(prov_uri, ":provider", "provider " + str(prov_id)))
            output(ttl_declare_individual(proc_uri, ":procedure", "provider " + str(prov_id)))
            output(ttl_declare_individual(code_uri, code_class_uri, code))
            output(ttl_declare_individual
                   (tth_uri, tth_class_uri,
                    "tooth " + str(tooth) + " of patient " + str(pt_id)))

            # since the surface field contains multiple value (e.g., "mod") loop over each surface letter
            for s in list(surface):
                surface_uri = ttl_surface_uri(pt_id, tooth, s)
                surface_class_uri = ttl_surface_class_uri(s)
                surface_name = ttl_surface_name(s)
                output(ttl_declare_individual
                            (surface_uri, surface_class_uri,
                             surface_name + " of tooth " + str(tooth) + " in patient " + str(pt_id)))

            output(ttl_declare_individual
                   (mat_uri, mat_class_uri,
                    mat_name + " placed in tooth " + str(tooth) + " of patient " + str(pt_id)) + "\n")


            # relate individuals/data properteis

            # date of service
            output(ttl_service_date(proc_uri, srv_date))

            # procedure participants
            output(ttl_has_participant(proc_uri, pt_uri))
            output(ttl_has_participant(proc_uri, prov_uri))
            output(ttl_has_participant(proc_uri, tth_uri))
            output(ttl_has_participant(proc_uri, mat_uri) + "\n")

            # parthood relations
            for s in list(surface):
                surface_uri = ttl_surface_uri(pt_id, tooth, s)
                output(ttl_part_of(mat_uri, surface_uri)) # material part of surface
                output(ttl_part_of(surface_uri, tth_uri)) # surface part of tooth
            output(ttl_part_of(tth_uri, pt_uri) + "\n") # tooth part of patient

            # service code about procedure
            output(ttl_is_about(code_uri, proc_uri) + "\n")

    return df

translate_patients(data_file='lib/patients_1.xlsx', output_file='output/patients_1.ttl',save_ttl=True)
translate_services(data_file='lib/services_1.xlsx', output_file='output/services_1.ttl',save_ttl=True)