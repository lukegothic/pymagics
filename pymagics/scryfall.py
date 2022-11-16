from requests_cache import CachedSession

def get_bulk_cards(t="oracle"):
    session = CachedSession()
    bulk_info = session.get("https://api.scryfall.com/bulk-data/{}-cards".format(t)).json()
    bulk_data = session.get(bulk_info["download_uri"])
    return bulk_data.json()