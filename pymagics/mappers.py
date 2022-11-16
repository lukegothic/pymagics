# windows invalid
  # < (less than)
  # > (greater than)
  # : (colon - sometimes works, but is actually NTFS Alternate Data Streams)
  # " (double quote)
  # / (forward slash)
  # \ (backslash)
  # | (vertical bar or pipe)
  # ? (question mark)
  # * (asterisk)
# MTG chars
#  !"&'()+,-./012346789:?ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz®àáâãéíñöúûüŠ

char = "\"/:?®àáâãéíñöúûüŠ"
repl =  "'___raaaaeinouuuS"
tran = str.maketrans(char, repl)

def cardname_to_filename(name):
  return name.translate(tran)