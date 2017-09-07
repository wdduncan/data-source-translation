class OWL_Class(object):
    pass


class Field(object):
    pass


class Table(object):
    pass

def is_owl_class(a):
    return type(a) is OWL_Class

def is_field(a):
    return type(a) is Field


def is_table(a):
    return type(a) is Table

# patients = Table()
# patient_id = Field()
# gender = Field()
# birth_date = ()
