import discord

items_data = {
    "chess": 236,
    "bowl": 456,
    "adidas": 2968,
    "tawas": 68,
    "mop": 169,
    "remote": 350,
    "sickle": 65,
    "microphone": 1995,
    "pechay": 12,
    "ribeye": 7392,
    "hammer": 53,
    "shirt": 551,
    "boxer": 183,
    "soju": 325,
    "airbed": 510,
    "watch": 95,
    "lube": 118,
    "microfiber": 34,
    "tape": 40,
    "racket": 109
}

#Returns 1 if higher
#Returns 0 if lower
#Returns 2 if equal
#Returns 3 if unknown input
def item_guess(command):

  try:
    command_parts = command.split()
    item = command_parts[1].lower()
    guess = command_parts[2]

    result = 3
    if command_parts[0].lower() == "guess" and item and guess and item.lower() in items_data:
      
      guess = float(guess)
      item_value = items_data[item.lower()]

      if guess > item_value:
          result = 0
      elif guess < item_value:
          result = 1
      else:
          result = 2
  except (ValueError, IndexError):
    result = 3
    
  return result

def get_message(input_value):
  if input_value == 1:
      return ", taasan mo pa! Higher! <:higher_up:1171787382559887430>"
  elif input_value == 0:
      return ", sumobra! Lower! <:lower_down:1171787648474550372>"
  elif input_value == 2:
      return ", mismo! Sakto! ✅"
  else:
      return ", huh? Ansabe mo? Follow the syntax `$guess <item_name> <value>`!"