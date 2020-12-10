from enum import Enum

class Sandwich(Enum):
  GUS_SPECIAL = (0, ['Special'])
  WILD_WEST = (1, ['Wild West', 'ww'])
  VALENCIA = (2, ['Valencia', 'v'])
  PANHANDLE = (3, ['Panhandle', 'ph'])
  KEZAR = (4, ['Kezar', 'kz'])
  QUAKE = (5, ['Quake', 'q'])
  FLASHBACK_REUBEN = (6, ['Flasback Reuben', 'fb'])
  MEATBALL = (7, ['Meatball', 'mb'])
  BLT = (8, ['BLT', '710', 'king street'])
  PALL_MALL = (9, ['Pall Mall', 'aids'])

  def __init__(self, i, names):
    self.id = i
    self.names = names

  def get_id(self):
    return self.id

  def get_name(self):
    return self.names[0]

  @staticmethod
  def from_name(name):
    for sandwich in Sandwich:
      for n in sandwich.names:
        if (n.lower().strip() == name.lower().strip()):
          return sandwich
    raise Exception(f"Bruh, this isn't 'Bite Me Sandwiches'! this is Gustavos - '{name}' not found")
