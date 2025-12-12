# Stubbed to accept any string
def is_uberon_term(v):
    if not isinstance(v, str):
        raise TypeError("Value must be a string")
    return v
