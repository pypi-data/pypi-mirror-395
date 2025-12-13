def flatten(d,sep):
    out = {}
    for key, val in d.items():
        if isinstance(val, dict):
            val = [val]
        if isinstance(val, list):
            for subdict in val:
                deeper = flatten(subdict,sep).items()
                out.update({key + sep + key2: val2 for key2, val2 in deeper})
        else:
            out[key] = val
    return out