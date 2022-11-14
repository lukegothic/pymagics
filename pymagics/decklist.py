import re
#import tkinter as tk
#from tkinter import filedialog

reCard = re.compile("(\d)?\s?(.*)")

class Decklist:
    def __init__(self, cards) -> None:
        self.main = {}
        self.sideboard = {}
        self.commander = {}
        for card in cards:
            m = re.match(reCard, card.strip())
            if not m is None:
                quantity = (int)(m.group(1)) if not m.group(1) is None and m.group(1) != "" else 1
                card = m.group(2).strip()
                if card in self.main:
                    self.main[card] += quantity
                else:
                    self.main[card] = quantity

# def from_file(filename=None):
#     if filename is None:
#         root = tk.Tk()
#         root.wm_attributes('-topmost', True)
#         root.withdraw()
#         filename = filedialog.askopenfilename()
#     with open(filename, encoding="utf8") as f:
#         data = f.read()
#     return from_text(data)
    
# def from_text(text):
#     return from_list(text.splitlines())

# def from_list(cardlist):
#     # TODO: distinguir main, sb y commander
#     # TODO: moxfield, etc etc etc
#     deck = {
#         "main": {},
#         "side": {},
#         "commander": {}
#     }
#     for c in cardlist:
#         m = re.match(reCard, c.strip())
#         if not m is None:
#             quantity = (int)(m.group(1)) if not m.group(1) is None and m.group(1) != "" else 1
#             card = m.group(2).strip()
#             if card in deck["main"]:
#                 deck["main"][card] += quantity
#             else:
#                 deck["main"][card] = quantity
#     return deck