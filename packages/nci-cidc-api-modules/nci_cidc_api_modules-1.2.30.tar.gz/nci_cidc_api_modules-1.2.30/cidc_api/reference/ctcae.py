# Stubbed to accept any string
def is_ctcae_event_term(v):
    if not isinstance(v, str):
        raise TypeError("Value must be a string")
    return v


# Stubbed to accept any string
def is_ctcae_event_code(v):
    if not isinstance(v, str):
        raise TypeError("Value must be a string")
    return v


# Stubbed to accept any string
def is_ctcae_severity_grade(v):
    if not isinstance(v, str):
        raise TypeError("Value must be a string")
    return v


# Stubbed to accept any string
def is_ctcae_system_organ_class(v):
    if not isinstance(v, str):
        raise TypeError("Value must be a string")
    return v


# Determines if the CTCAE term is one of the "Other, specify" types of terms for which we include
# additional data about the AE.
def is_ctcae_other_term(v):
    if isinstance(v, str):
        return "Other, specify" in v
    return False
