# Stubbed to accept any string
def is_ICD10CM_code(v):
    if not isinstance(v, str):
        raise TypeError("Value must be a string")
    return v


# Stubbed to accept any string
def is_ICD10CM_term(v):
    if not isinstance(v, str):
        raise TypeError("Value must be a string")
    return v
