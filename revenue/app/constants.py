
BRAND_NAMES_TO_IDS = {
    "Nory Sushi": "352h67i328fh",
    "Nory Pizza": "345hngydkgs",
    "Nory Taco": "2hg8j32gw8g"
}

BRAND_IDS = set(BRAND_NAMES_TO_IDS.values())


def get_brand_id(brand_name: str):
    """
    Idealy this would come from the DB

    :param brand_name: as appears on the csv data dump
    :return: brand id as it would appear in the DB
    """
    return BRAND_NAMES_TO_IDS.get(brand_name)
