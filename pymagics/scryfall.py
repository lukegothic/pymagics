from requests_cache import CachedSession

def get_bulk_cards(t="oracle"):
    session = CachedSession()
    bulk_info = session.get("https://api.scryfall.com/bulk-data/{}-cards".format(t)).json()
    bulk_data = session.get(bulk_info["download_uri"])
    return bulk_data.json()

def decklist_to_scryfall(decklist):
    data = get_bulk_cards()
    data = [c | c["card_faces"][0] if "card_faces" in c else c for c in data]
    # TODO: lib util toDict(array, key) (INTENTAR RECUPERAR CODIGO)
    data_dict = {}
    for c in data:
      data_dict[c["name"]] = c
    return [data_dict[c.split(" // ")[0]] for c in decklist]