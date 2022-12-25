BOOL_CONV = {"yes": True, "no": False, "on": True, "off": False, "true": True, "false": False, "1": True, "0": False}


def conv_bool(v: str) -> bool:
    return BOOL_CONV[v.lower()]
