import discord
from discord.embeds import Embed
import utils
from replit import db

# Define the four zones with letters and 'X' for empty spaces
East = [['X' for _ in range(8)] for _ in range(8)]
North = [['X' for _ in range(10)] for _ in range(10)]
South = [['X' for _ in range(8)] for _ in range(8)]
West = [['X' for _ in range(10)] for _ in range(10)]

# List of allowed roles
allowed_roles = [
  "GOLD_UK_HUN",
  "GOLD_STRANGE_DUO",
  "GOLD_GET_GET_AI",
  "GOLD_GIJEONG",
  "GOLD_TARZARIRAY_AMASONANG_KIKAY",
  "GOLD_THE_FRAUDIGAL_SONS",
  "GOLD_VLYUNGANGUHVEOUX",
  "GOLD_KENOUGH",
  "GOLD_WHEN_YOU_BELIEVE",
  "GOLD_BITLY_TARISGOLD_KKMQ_AKTO",
  "GOLD_HOSTS"
]

zone_dict = {"EAST": East, "NORTH": North, "SOUTH": South, "WEST": West}


# Allowed roles only
def get_allowed_role(roles, allowed_roles):
  for role in roles:
    if role.name in allowed_roles:
      return role.name
  return None  # No allowed role found


# Function to claim a letter in a square
def claim_letter(zone, position, role, author):
  if role is None:
    return f"⚠️ **{author} ({role})**, you are not allowed to participate. Contact the hosts."

  claimed_letters = get_claimed_letters(role)

  x, y = convert_coordinates(position)
  letter = get_letter(zone, x, y)

  if letter is None:
    return f"❌ **{author} ({role})**, bobohan mo pa. Invalid coordinates. Try again."
  elif letter == 'X':
    return f"❌ **{author} ({role})**, that area contains nothing. Sad. Try again."
  elif letter == 'T':
    return f"❌ **{author} ({role})**, you checked a tree. Please select coordinates with tents only. Mygahd read the clue."
  elif letter == 'Z':
    return f"⛺️😟 **{author} ({role})**, this is a correct tent, however, someone already took the letter here. Please search other tents."
  elif letter == '?':
    claimed_letters.append(letter)
    set_claimed_letters(role, claimed_letters)
    set_letter(zone, x, y, "Z")
    return f"⛺️✅ **{author} ({role})**, you claimed a **wildcard letter** for your team in the {zone} zone.\nYour team currently has: **{list_letters_by_role(role)}**"
  elif letter in claimed_letters:
    return f"⛺️😟 **{author} ({role})**, you found the letter **{letter}** again. You already have this letter. Wag sugapa. Try again."
  elif letter not in claimed_letters:
    set_letter(zone, x, y, "Z")
    claimed_letters.append(letter)
    return f"⛺️✅ **{author} ({role})**, you claimed the letter **{letter}** for your team in the {zone} zone.\nYour team currently has: **{list_letters_by_role(role)}**"
  else:
    return f"❌ **{author} ({role})**, bobohan mo pa. Invalid coordinates. Try again."


def set_claimed_letters(role, claimed_letters):
  db[f"claimed_letters_{role}"] = claimed_letters


# Function to list letters claimed by a role
def list_letters_by_role(role):
  if role == None:
    return "Invalid role. Choose from the allowed roles."

  return format_claimed_letters(get_claimed_letters(role))


# Function to list all letters claimed by each role (only Admin can use this)
def list_all_letters_by_roles(roles):
  if utils.is_admin(roles):
    embed = Embed(title="🌳⛺️ **TENTS GAME** ⛺️🌳",
                  color=discord.Color.blurple())
    for role in allowed_roles:
      listLetters = format_claimed_letters(get_claimed_letters(role))
      roleName = f"{role}'s Letters'"
      embed.add_field(name=roleName, value=listLetters, inline=False)
    return embed
  else:
    return "Only an Admin can perform this action."


# Get claimed letters PER ROLE
def get_claimed_letters(role):
  return db["claimed_letters_" + role]


# Function to reset all zones with provided letters and 'X' for empty spaces (only Admin can use this)
def reset_all_zones(roles):
  if utils.is_admin(roles):
    populate_zones()
    for role in allowed_roles:
      db["claimed_letters_" + role] = []
    db["tent_zone_NORTH"] = North
    db["tent_zone_EAST"] = East
    db["tent_zone_SOUTH"] = South
    db["tent_zone_WEST"] = West
    return "All zones have been reset by Admin."
  else:
    return "Only Admin can reset all zones."


# Function to display the letters in a selected area (only Admin can use this)
def display_selected_area(zone, roles):
  if utils.is_admin(roles):
    letters = get_zone(zone)
    newline = '\n'
    if letters:
      return f"Letters in the {zone} zone:{newline}{'{newline}'.join([' '.join(row) for row in letters])}"
    else:
      return f"No letters found in the {zone} zone."
  else:
    return "Only Admin can display the letters in a selected area."


# Function to convert letter + number coordinates to list indices
def convert_coordinates(coord):
  coord = coord.upper()
  letter_part, number_part = '', ''

  for char in coord:
    if char.isalpha():
      letter_part += char
    elif char.isnumeric():
      number_part += char

  if letter_part and number_part:
    letter = letter_part
    number = int(number_part) - 1  # Convert to zero-based index
    if len(letter) == 1:
      return ord(letter) - ord('A'), number
    elif len(letter) == 2 and letter[0].isalpha() and letter[1].isalpha():
      column_index = (ord(letter[0]) - ord('A') + 1) * 26 + (ord(letter[1]) -
                                                             ord('A'))
      return column_index - 1, number
  return None, None


# Function to get the letter at a specific position in a zone
def get_letter(zone, x, y):
  if zone == "EAST":
    if 0 <= x < 8 and 0 <= y < 8:
      return db["tent_zone_EAST"][x][y]
  elif zone == "NORTH":
    if 0 <= x < 10 and 0 <= y < 10:
      return db["tent_zone_NORTH"][x][y]
  elif zone == "SOUTH":
    if 0 <= x < 8 and 0 <= y < 8:
      return db["tent_zone_SOUTH"][x][y]
  elif zone == "WEST":
    if 0 <= x < 10 and 0 <= y < 10:
      return db["tent_zone_WEST"][x][y]
  return None


# Function to set a letter at a specific position in a zone
def set_letter(zone, x, y, letter):
  if zone == "EAST":
    if 0 <= x < 8 and 0 <= y < 8:
      db["tent_zone_EAST"][x][y] = letter
  elif zone == "NORTH":
    if 0 <= x < 10 and 0 <= y < 10:
      db["tent_zone_NORTH"][x][y] = letter
  elif zone == "SOUTH":
    if 0 <= x < 8 and 0 <= y < 8:
      db["tent_zone_SOUTH"][x][y] = letter
  elif zone == "WEST":
    if 0 <= x < 10 and 0 <= y < 10:
      db["tent_zone_WEST"][x][y] = letter


# Function to get the entire zone
def get_zone(zone):
  return db[f"tent_zone_{zone}"]


# Function to format claimed letters as a string
def format_claimed_letters(letters):
  if len(letters) == 0:
    return 'None'
  return ', '.join(letters)


# Function to check whether a role has five unique letters
def has_five_unique_letters(role):
  claimed_letters = get_claimed_letters(role)
  return len(claimed_letters) >= 5


# Function to populate the zones with provided letters and 'X' for empty spaces
def populate_zones():
  East_letters = [
      "T R X X X X K T",
      "X X X A T X X X",
      "E X X X X X X X",
      "T X X X A T X X",
      "X ? T X X X T O",
      "X X X E T X X X",
      "X X X X T E X X",
      "X R T A T X T R",
  ]
  for i, row in enumerate(East):
    row[:] = East_letters[i].split()

  North_letters = [
      "X X X X ? X K X T R",
      "? X X X T X T X X T",
      "T X R X X X X X X ?",
      "A X T X E X T O X X",
      "T X X X T X X X X X",
      "X T R X X X X E T ?",
      "X X X T X R T T X X",
      "O T X O X X X X X R",
      "T X T X X X X K X T",
      "E X A X X X X T T ?",
  ]
  for i, row in enumerate(North):
    row[:] = North_letters[i].split()

  South_letters = [
      "X X X T R T K X",
      "R X X X X X X X",
      "T X X R T K X X",
      "X X X T X X T A",
      "T E X X A X X X",
      "X X X X T X X O",
      "O X X X X X X T",
      "T X A T X A T X",
  ]
  for i, row in enumerate(South):
    row[:] = South_letters[i].split()

  West_letters = [
      "X ? T T X K X T X K",
      "X X X ? X T X A X T",
      "X O T X X X X X T K",
      "X X X X X E X X X X",
      "? X O X X T X X E T",
      "T X T X T X O X X X",
      "O T E X A X T X X X",
      "X X T X X X X X X X",
      "K T K T O X X T X K",
      "X X T X X X X E X T",
  ]
  for i, row in enumerate(West):
    row[:] = West_letters[i].split()

# Function to check if coordinates are valid
def is_valid_coordinates(coordinates):
    if len(coordinates) == 2 or len(coordinates) == 3:
        letter, number = coordinates[0], coordinates[1]
        if letter.isalpha() and letter.isupper() and number.isdigit() and 1 <= int(number) <= 10:
            return True
    return False

# Function to process user messages and return results as an embed message
def process_message(command, member):

  # Author Name and Roles
  author = member.display_name
  roles = member.roles

  # Parse command details
  command_parts = command.split()
  command_name = command_parts[0].lower()
  command_args = command_parts[1:]

  # Relevant Tent Role
  role = get_allowed_role(roles, allowed_roles)

  ## ?claim ZONE POSITION
  if command_name == "claim":
    if has_five_unique_letters(role):
      return f"🏁 **{author}**, your team **{role}** already found all letters!"
      
    if len(command_args) != 2:
      return f"❌ **{author} ({role})**, you posted an invalid command. Use: ```$claim [ZONE] [COORDINATES]```"
    else:
      zone, coordinates = command_args[0].upper(), command_args[1].upper()
      if zone in ["EAST", "WEST", "SOUTH", "NORTH"
                  ] and is_valid_coordinates(coordinates):
        resp = claim_letter(zone, coordinates, role, author)
        if has_five_unique_letters(role):
          resp = resp + "\n" + f"🎉🎈 {coordinates} **{author}**, your team **{role}** found all letters! You may now check-in here: https://drive.google.com/file/d/1XxUhWY3zOG5OhYNEXFaNCCtR5VXBoLEw/view?usp=sharing"
        return resp
      else:
        return f"❌ {coordinates} **{author} ({role})**, invalid zone or coordinates. Use a valid zone (EAST, WEST, SOUTH, NORTH) and valid coordinates (e.g., A1, A2). Wag tanga, okay?"

  ## ?list letters
  ## ?list letters all
  elif command_name == "list":
    if len(command_args) == 1 and command_args[0] == "letters":
      role = get_allowed_role(roles, allowed_roles)
      return list_letters_by_role(role)
    elif len(command_args) == 2 and command_args[
        0] == "letters" and command_args[1] == "all":
      return list_all_letters_by_roles(roles)
    else:
      return "Invalid command format. Use: $list letters [all]"

  elif command_name == "reset":
    if len(command_args) == 1 and command_args[0] == "tents":
      return reset_all_zones(roles)
    else:
      return "Invalid command format. Use: $reset tents"

  elif command_name == "display":
    if len(command_args) == 1:
      zone = command_args[0].upper()
      return display_selected_area(zone, roles)
    else:
      return "Invalid command format. Use: $display [ZONE]"

  else:
    return None
