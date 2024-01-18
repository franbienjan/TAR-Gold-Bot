import discord
from discord.ext import commands, tasks
import json
import random
from replit import db

# Load item data from JSON
with open("items.json", "r") as f:
    items_data = json.load(f)

# Initialize Discord bot
bot = commands.Bot(command_prefix="$")

# Define the list of allowed roles
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

# Allowed roles only
def get_allowed_role(roles, allowed_roles):
  for role in roles:
    if role.name in allowed_roles:
      return role.name
  return None  # No allowed role found

# Initialize variables to keep track of selected items and player inventories
selected_items = []
player_inventories = {}

# Function to select random items every 30 seconds
@tasks.loop(seconds=30)
async def select_items():
    global selected_items
    selected_items = random.sample(db["main_inventory"], 2)
    print(selected_items)

# Event to run when the bot is ready
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    select_items.start()

# Command to allow players to download items
def download(item_choice, role):
    if role is None:
      print("NO ROLE PLEASE TRY AGAIN")
      return ("FAIL", "No item downloaded.")

    global selected_items, player_inventories

    itemCode = 2
    if item_choice.upper() == "A":
      itemCode = 0
    elif item_choice.upper() == "B":
      itemCode = 1
      
    if itemCode in [0, 1]:
        selected_item = selected_items[itemCode]
        playerInventory = db["inv_" + role]

        # Check if the player already has an item with the same leg number in their inventory
        leg_number_matches = any(selected_item["leg_number"] == json_item["leg_number"] for json_item in playerInventory)
        print(leg_number_matches)
      
        if leg_number_matches:
            # Add the dropped items back into circulation
            db["main_inventory"] = db["main_inventory"].append(playerInventory)
            items_data.extend(selected_items)
            selected_items = []
            # Clear the player's inventory
            player_inventories[ctx.author.id] = []
            return ("FAIL", f"You already have an item with leg number {selected_item['leg_number']} in your inventory. Dropping all items...")
        else:
            # Add the selected item to the player's inventory
            if ctx.author.id not in player_inventories:
                player_inventories[ctx.author.id] = []
            player_inventories[ctx.author.id].append(selected_item["leg_number"])

            # Remove the selected items from circulation
            for item in selected_items:
                items_data.remove(item)

            message = f"{ctx.author.mention}, you have successfully downloaded item {item_choice}. Your inventory: {', '.join(player_inventories[ctx.author.id])}"

            # Check if the player has downloaded 9 items without repeating leg numbers
            if len(player_inventories[ctx.author.id]) == 9 and len(set(player_inventories[ctx.author.id])) == 9:
                message = message + "\n" + f"Congratulations {ctx.author.mention}! You have successfully collected 9 unique items."
                return("SUCCESS - ALL", message)

            return("SUCCESS - NEW", message)

    else:
        return ("FAIL", "Invalid item choice. Use $download A or $download B.")

def process_message(command, author):
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
  if command_name == "download":

def initialize():
  db["main_inventory"] = items_data
  for role in allowed_roles:
    db[f"inv_{role}"] = {}

def list_items(role):
  resp = ""
  for item in db[f"inv_{role}"]:
    resp = resp + ", " + item.name
  return resp

# Event to run when an error occurs with the download command
@download.error
async def download_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing item choice. Use $download A or $download B.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid item choice. Use $download A or $download B.")
