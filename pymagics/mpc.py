from pyluke.venn import VennDistribution3, VennDistribution4, VennDistribution
from pyluke import array
from lxml import etree

class MCPOrder:
  def __init__(self, bracket=612, stock="(S30) Standard Smooth", foil=False, cardback="1LrVX0pUcye9n_0RtaDNVl2xPrQgn7CYf", optimized=True, lists=[]):
    self.quantity = None
    self.bracket = bracket
    self.stock = stock
    self.foil = "true" if foil else "false"
    self.fronts = []
    self.backs = []
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
        # simple put on front
        pass
      case 2:
        # simple intersection + a b sets
        pass
      case 3:
        # venn
        self.fill_fromVennDistribution(VennDistribution3(set(lists[0]), set(lists[1]), set(lists[2])))
      case 4:
        self.fill_fromVennDistribution(VennDistribution4(set(lists[0]), set(lists[1]), set(lists[2]), set(lists[3])))
      case _:
        raise Exception("Unexpected number of lists provided")
  
  #in: VennDistribution
  #out: array of arrays [[front, back], [front, back], [front, back]...]
  #     front will always have value, back can be None
  def fill_fromVennDistribution(self, venn: VennDistribution):
    # 3 sets
    # abc -> empty
    # ab  -> c
    # ac  -> b
    # bc  -> a
    # a   -> bc | b | c
    # b   -> ac | a | c
    # c   -> ab | a | b
    out = []
    if isinstance(venn, VennDistribution3):
      # union
      for i in venn.union:
        out.append([i, None])
      # xy intersections
      for i in venn.intersections.ab:
        out.append([i, array.pop_AnyOrNone(venn.sets.c)])
      for i in venn.intersections.ac:
        out.append([i, array.pop_AnyOrNone(venn.sets.b)])
      for i in venn.intersections.bc:
        out.append([i, array.pop_AnyOrNone(venn.sets.a)])
      # x sets
      for i in venn.sets.a:
        out.append([i, array.pop_AnyOrNone(venn.sets.b, venn.sets.c, venn.intersections.bc)])
      for i in venn.sets.b:
        out.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.c, venn.intersections.ac)])
      for i in venn.sets.c:
        out.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.b, venn.intersections.ab)])

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
        out.append([i, None])
      # xyz intersections
      for i in venn.intersections.abc:
        out.append([i, array.pop_AnyOrNone(venn.sets.d)])
      for i in venn.intersections.abd:
        out.append([i, array.pop_AnyOrNone(venn.sets.c)])
      for i in venn.intersections.acd:
        out.append([i, array.pop_AnyOrNone(venn.sets.b)])
      for i in venn.intersections.bcd:
        out.append([i, array.pop_AnyOrNone(venn.sets.a)])
      # xy intersections
      for i in venn.intersections.ab:
        out.append([i, array.pop_AnyOrNone(venn.sets.c, venn.sets.d, venn.intersections.cd)])
      for i in venn.intersections.cd:
        out.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.b, venn.intersections.ab)])
      for i in venn.intersections.ac:
        out.append([i, array.pop_AnyOrNone(venn.sets.b, venn.sets.d, venn.intersections.bd)])
      for i in venn.intersections.bd:
        out.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.c, venn.intersections.ac)])
      for i in venn.intersections.ad:
        out.append([i, array.pop_AnyOrNone(venn.sets.b, venn.sets.c, venn.intersections.bc)])
      for i in venn.intersections.bc:
        out.append([i, array.pop_AnyOrNone(venn.sets.a, venn.sets.d, venn.intersections.ad)])
      # x sets
      for i in venn.sets.a:
        out.append([i, array.pop_AnyOrNone(venn.sets.b, venn.sets.c, venn.sets.d, venn.intersections.bc, venn.intersections.bd, venn.intersections.cd, venn.intersections.bcd)])
      for i in venn.sets.b:
        out.append([i, array.pop_AnyOrNone(venn.sets.b, venn.sets.c, venn.sets.d, venn.intersections.ac, venn.intersections.ad, venn.intersections.cd, venn.intersections.acd)])
      for i in venn.sets.c:
        out.append([i, array.pop_AnyOrNone(venn.sets.b, venn.sets.c, venn.sets.d, venn.intersections.ab, venn.intersections.ad, venn.intersections.bd, venn.intersections.abd)])
      for i in venn.sets.d:
        out.append([i, array.pop_AnyOrNone(venn.sets.b, venn.sets.c, venn.sets.d, venn.intersections.ab, venn.intersections.ac, venn.intersections.bc, venn.intersections.abc)])
    else:
      raise Exception("Invalid object or VennDistribution supplied")
    self.fronts = [o[0] for o in out]
    self.backs = [o[1] for o in out]

  def generate(self):
    root = etree.Element("order")
    # details
    details = etree.Element("details")
    quantity = etree.Element("quantity")
    quantity.text = str(len(self.fronts))
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
    root.append(details)
    # fronts
    # TODO: si no optimizado puede que haya una carta en varias posiciones, controlar!
    fronts = etree.Element("fronts")
    for i, front in enumerate(self.fronts):
      if not front is None:
        card = etree.Element("card")
        id = etree.Element("id")
        id.text = front
        card.append(id)
        slots = etree.Element("slots")
        slots.text = str(i)
        card.append(slots)
        fronts.append(card)
    root.append(fronts)
    # backs
    backs = etree.Element("backs")
    for i, back in enumerate(self.backs):
      if not back is None:
        card = etree.Element("card")
        id = etree.Element("id")
        id.text = front
        card.append(id)
        slots = etree.Element("slots")
        slots.text = str(i)
        card.append(slots)
        backs.append(card)
    root.append(backs)
    # cardback
    cardback = etree.Element("cardback")
    cardback.text = self.cardback
    root.append(cardback)
    return etree.tostring(root)