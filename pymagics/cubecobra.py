import requests
from .decklist import Decklist

#TODO: exceptcions en base

class ParamException(Exception):
  pass

class NotFoundException(Exception):
  pass

def get_list(cube_name=None):
  if cube_name is None:
    raise ParamException("cubename param is required")
  url = "https://cubecobra.com/cube/download/plaintext/{}".format(cube_name)
  r = requests.get(url)
  if r.url == url:
    cards = r.text.splitlines()
    deck = Decklist(cards)
    return deck
  else:
    raise NotFoundException("cubename '{}' not found".format(cube_name))
