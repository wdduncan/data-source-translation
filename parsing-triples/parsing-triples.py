import pandas as pds
from collections import namedtuple
from pprint import pprint
from string import Formatter

# schema = {patients:
#               {"name": "patients",
#                "fields": [{patient_id: {"values": "all", "proxy": person},
#                           gender: {"values": [{"M": "male", "proxy": male_gender_role},
#                                               {"F": "female", "proxy": female_gender_role}]},
#                           birth_date: {"values": "all"}}]}}

# Table_Shema = namedtuple("Table_Schema", "name fields")
# Field_Schema = namedtuple("Field_Schema", "name values")
# Value_Schema = namedtuple("Value_Schema", "value proxy")
#
# patients = Table_Shema(name="patients",
#                        fields=[
#                         Field_Schema(name="patient_id", values=Value_Schema(value="all", proxy="person")),
#                         Field_Schema(name="gender", values=[Value_Schema(value="M", proxy="male_patient"),
#                                                             Value_Schema(value="F", proxy="female_patient")]),
#                         Field_Schema(name="birth_date", values=[Value_Schema(value="all", proxy=None)])])




patients = {"name": "patients",
            "fields": [{"patient_id": {"values": "all", "proxy": "person"},
                        "gender": {"values": [{"M": "male", "proxy": "male_patient"},
                                              {"F": "female", "proxy": "female_patient"}]},
                        "birth_date": {"values": "all"}}]}


df = pds.ExcelFile("data/patients_1.xlsx").parse()

for results in df.itertuples(index=False):
    values = list(results) # this also works results[:]
    fields = results._fields
    # triplify("""\
    #                 <!patient_id>> a <<patient>> .
    #                 <!gender>> a <<male>>
    #                 """, patient_id='123', gender="m")

    print triplify("""\
                        <!patient_id>> a <<patient>> .
                        <!gender>> a <<male>>
                        """, **results._asdict())

    # for field in results._fields:
    #     # make_uri(field, getattr(results, field))
    #     print triplify("""\
    #             patient_id a <@patient>> .
    #             """)

# print df.to_string()
# print schema
# print and_p((type(gender) is Field), True)
# pprint(patients)