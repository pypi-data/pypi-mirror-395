def concatenate_dict(dict_1, dict_2) -> dict:
    """update dict which has dict as values. And we want concatenate those values to"""
    res = dict_1.copy()
    for key in dict_2:
        if key in dict_1:
            if isinstance(dict_1[key], dict):
                res[key] = concatenate_dict(dict_1=dict_1[key], dict_2=dict_2[key])
            else:
                res.update({key: dict_2[key]})
        else:
            res[key] = dict_2[key]
    return res
