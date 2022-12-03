from pyluke.venn import VennDistribution2, VennDistribution3, VennDistribution4, VennDistribution
from pyluke import array
from lxml import etree
from . import mappers

class MCPOrder:
  def __init__(self, bracket=612, stock="(S30) Standard Smooth", foil=False, cardback="1LrVX0pUcye9n_0RtaDNVl2xPrQgn7CYf", optimized=True, lists=[]):
    self.quantity = None
    self.bracket = bracket
    self.stock = stock
    self.foil = "true" if foil else "false"
    self.order = []
    self.optimized = optimized
    if len(lists) > 0:
      self.fill(lists)
    self.cardback = cardback

  # TODO: metodo fill con parametro optimize dentro que coja 1, 2, 3 o 4 listas y las optimize o no
  def fill(self, lists):
    match len(lists):
      case 0:
        raise Exception("At least one list must be provided")
      case 1:
        self.order = [[c, None] for c in lists[0]]
      case 2:
        self.fill_fromVennDistribution(VennDistribution2(set(lists[0]), set(lists[1])))
      case 3:
        self.fill_fromVennDistribution(VennDistribution3(set(lists[0]), set(lists[1]), set(lists[2])))
      case 4:
        self.fill_fromVennDistribution(VennDistribution4(set(lists[0]), set(lists[1]), set(lists[2]), set(lists[3])))
      case _:
        raise Exception("Unexpected number of lists provided")

  #in: VennDistribution
  #out: array of arrays [[front, back], [front, back], [front, back]...]
  #     front will always have value, back can be None
  def fill_fromVennDistribution(self, venn: VennDistribution):
    # 2 sets
    # ab  -> None
    # a   -> None
    # b   -> None
    if isinstance(venn, VennDistribution2):
      # union
      for i in venn.union:
        self.order.append([i, None])
      # x sets
      for i in venn.sets.a:
        self.order.append([i, None])
      for i in venn.sets.b:
        self.order.append([i, None])

    # 3 sets
    # abc -> empty
    # ab  -> c
    # ac  -> b
    # bc  -> a
    # a   -> bc | b | c
    # b   -> ac | a | c
    # c   -> ab | a | b
    elif isinstance(venn, VennDistribution3):
      # union
      for i in venn.union:
        self.order.append([i, None])
      # xy intersections
      for i in venn.intersections.ab:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.c)])
      for i in venn.intersections.ac:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.b)])
      for i in venn.intersections.bc:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.a)])
      # x sets
      for i in venn.sets.a:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.b, venn.sets.c, venn.intersections.bc)])
      for i in venn.sets.b:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.c, venn.intersections.ac)])
      for i in venn.sets.c:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.b, venn.intersections.ab)])

    # 4 sets
    # abcd  -> empty
    # abc   -> d
    # abd   -> c
    # acd   -> b
    # bcd   -> a
    # ab    -> cd | c | d
    # cd    -> ab | c | d
    # ac    -> bd | b | d
    # bd    -> ac | a | c
    # ad    -> bc | b | c
    # bc    -> ad | a | d
    # a     -> bcd | bc | bd | cd | b | c | d
    # b     -> acd | ac | ad | cd | a | c | d
    # c     -> abd | ab | ad | bd | a | b | d
    # d     -> abc | ab | ac | bc | a | b | c
    elif isinstance(venn, VennDistribution4):
      # union
      for i in venn.union:
        self.order.append([i, None])
      # xyz intersections
      for i in venn.intersections.abc:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.d)])
      for i in venn.intersections.abd:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.c)])
      for i in venn.intersections.acd:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.b)])
      for i in venn.intersections.bcd:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.a)])
      # xy intersections
      for i in venn.intersections.ab:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.c, venn.sets.d, venn.intersections.cd)])
      for i in venn.intersections.cd:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.b, venn.intersections.ab)])
      for i in venn.intersections.ac:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.b, venn.sets.d, venn.intersections.bd)])
      for i in venn.intersections.bd:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.c, venn.intersections.ac)])
      for i in venn.intersections.ad:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.b, venn.sets.c, venn.intersections.bc)])
      for i in venn.intersections.bc:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.d, venn.intersections.ad)])
      # x sets
      for i in venn.sets.a:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.b, venn.sets.c, venn.sets.d, venn.intersections.bc, venn.intersections.bd, venn.intersections.cd, venn.intersections.bcd)])
      for i in venn.sets.b:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.c, venn.sets.d, venn.intersections.ac, venn.intersections.ad, venn.intersections.cd, venn.intersections.acd)])
      for i in venn.sets.c:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.b, venn.sets.d, venn.intersections.ab, venn.intersections.ad, venn.intersections.bd, venn.intersections.abd)])
      for i in venn.sets.d:
        self.order.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.b, venn.sets.c, venn.intersections.ab, venn.intersections.ac, venn.intersections.bc, venn.intersections.abc)])
    else:
      raise Exception("Invalid object or VennDistribution supplied")

  def generate_xml_order(self, cards, local_path, suffix):
    if len(cards) == 0:
      return None
    order = etree.Element("order")
    details = self.generate_xml_details(cards)
    order.append(details)
    (fronts, backs) = self.generate_xml_cards(cards, local_path, suffix)
    if not fronts is None:
      order.append(fronts)
    if not backs is None:
      order.append(backs)
    cardback = self.generate_xml_cardback()
    order.append(cardback)
    return order

  def generate_xml_details(self, cards):
    details = etree.Element("details")
    quantity = etree.Element("quantity")
    quantity.text = str(len(cards))
    details.append(quantity)
    bracket = etree.Element("bracket")
    bracket.text = str(self.bracket)
    details.append(bracket)
    stock = etree.Element("stock")
    stock.text = self.stock
    details.append(stock)
    foil = etree.Element("foil")
    foil.text = self.foil
    details.append(foil)
    return details
  
  def generate_xml_cards(self, cards, local_path, suffix):
    fronts = etree.Element("fronts")
    backs = etree.Element("backs")
    for slot, card in enumerate(cards):
      front = self.generate_xml_card(card[0], slot, local_path, suffix)
      if not front is None:
        fronts.append(front)
      back = self.generate_xml_card(card[1], slot, local_path, suffix)
      if not back is None:
        backs.append(back)
    return (fronts if len(fronts) > 0 else None, backs if len(backs) > 0 else None)
    
  def generate_xml_card(self, card, slot, local_path, suffix):
    if card is None:
      return None
    xcard = etree.Element("card")
    id = etree.Element("id")
    if local_path is None:
      id.text = card
    else:
      full_local_path = local_path / "{}{}".format(mappers.cardname_to_filename(card), suffix)
      id.text = str(full_local_path)
    xcard.append(id)
    slots = etree.Element("slots")
    slots.text = str(slot)
    xcard.append(slots)
    return xcard
  
  def generate_xml_cardback(self):
    cardback = etree.Element("cardback")
    cardback.text = self.cardback
    return cardback

  # standalonefrontonlyorder: genera order aparte para las que solo tienen front
  def generate_xml(self, local_path=None, suffix=None, standalonefrontsonly=False):
    if standalonefrontsonly:
      cards_with_front_and_back = [c for c in self.order if not c[1] is None]
      cards_with_front = [c for c in self.order if c[1] is None]
      order_front_and_back = self.generate_xml_order(cards_with_front_and_back, local_path, suffix)
      order_front = self.generate_xml_order(cards_with_front, local_path, suffix)
      return (
        etree.tostring(order_front_and_back, encoding=str) if not order_front_and_back is None else None,
        etree.tostring(order_front, encoding=str) if not order_front is None else None
      )
    else:
      return etree.tostring(self.generate_xml_order(self.order, local_path, suffix), encoding=str)
