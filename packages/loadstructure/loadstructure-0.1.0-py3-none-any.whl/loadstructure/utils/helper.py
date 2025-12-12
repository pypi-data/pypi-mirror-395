def _merge_dicts(a: dict, b: dict) -> dict:
    """
    Recursively merge dict b into dict a.
    Later values override earlier ones.
    """
    result = a.copy()
    for k, v in b.items():
        if (
            k in result 
            and isinstance(result[k], dict) 
            and isinstance(v, dict)
        ):
            result[k] = _merge_dicts(result[k], v)
        else:
            result[k] = v
    return result
