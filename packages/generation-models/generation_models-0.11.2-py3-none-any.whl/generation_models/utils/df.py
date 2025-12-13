def reform_for_multiindex_df(d: dict):
    r"""Helper function to reform a nested dictionary of arrays so it can be easily converted into a multi-index
    columned pandas dataframe
    """
    reformed_model_dict = dict()
    for outer_key, inner_dict in d.items():
        for inner_key, values in inner_dict.items():
            reformed_model_dict[(outer_key, inner_key)] = values
    return reformed_model_dict
