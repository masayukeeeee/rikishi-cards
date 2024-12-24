def transform_banzuke_to_rikishi(banzuke_json):
    """
    extract_profiles()では番付がキーになっているが、力士一人ひとりがキーになるように変換する
    """
    rikishi_dict = {}
    for i, rikishi in enumerate(banzuke_json):
        if rikishi["east"]["name"]:
            rikishi_dict[f"{i+1}-east"] = rikishi["east"]
        if rikishi["west"]["name"]:
            rikishi_dict[f"{i+1}-west"] = rikishi["west"]
    return rikishi_dict

