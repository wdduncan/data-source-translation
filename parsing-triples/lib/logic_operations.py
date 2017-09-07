

def and_p(a, b):
    return a and b


def or_p(a, b):
    return a or b


def if_p(a, b):
    return not a or b


def iff_p(a, b):
    return if_p(a, b) and if_p(b, a)
