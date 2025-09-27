import discord
from discord.ext import commands
import json
import os
import time
from dotenv import load_dotenv

# ---------------- GLOBAL SETTINGS ----------------
COINS_PER_MINUTE = 10  # Global coin reward rate

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")  # remove default help to avoid conflict

# ---------------- FILE PATHS ----------------
COINS_FILE = "coins.json"
IMAGES_FOLDER = "images"

# In-memory tracker for join times
join_times = {}

# Load or initialize coin data safely
if os.path.exists(COINS_FILE):
    try:
        with open(COINS_FILE, "r") as f:
            content = f.read().strip()
            coins = json.loads(content) if content else {}
    except json.JSONDecodeError:
        coins = {}
else:
    coins = {}

# ---------------- SHOP ----------------
# Using your image filenames
shop_items = {
    "friend1": "niran1.png",
    "friend2": "raja2.png",
    "friend3": "raja3.png",
}

# ---------------- HELPERS ----------------
def save_coins():
    with open(COINS_FILE, "w") as f:
        json.dump(coins, f, indent=4)

def award_coins(user_id, seconds):
    minutes = int(seconds // 60)
    if minutes > 0:
        earned = minutes * COINS_PER_MINUTE
        coins[str(user_id)] = coins.get(str(user_id), 0) + earned
        save_coins()
        return earned
    return 0

# ---------------- EVENTS ----------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
@bot.event
async def on_voice_state_update(member, before, after):
    # Member joins voice
    if after.channel and (before.channel is None):
        join_times[member.id] = time.time()
        
        # Give 20 coins on join
        coins[str(member.id)] = coins.get(str(member.id), 0) + 20
        save_coins()
        
        text_channel = discord.utils.get(member.guild.text_channels, name="general")
        if text_channel:
            await text_channel.send(f"👋 Welcome {member.mention}! You got **20 coins** for joining the VC!")

    # Member leaves voice
    elif before.channel and (after.channel is None):
        if member.id in join_times:
            joined_at = join_times.pop(member.id)
            duration = time.time() - joined_at
            earned = award_coins(member.id, duration)
            text_channel = discord.utils.get(member.guild.text_channels, name="general")
            if text_channel:
                await text_channel.send(
                    f"👋 Goodbye {member.mention}! You earned **{earned} coins** for watching."
                )

# ---------------- COMMANDS ----------------
@bot.command()
async def balance(ctx):
    user_id = str(ctx.author.id)
    bal = coins.get(user_id, 0)
    await ctx.send(f"💰 {ctx.author.mention}, you have **{bal} coins**.")

@bot.command(name="shop")
async def shop_cmd(ctx):
    items = "\n".join([f"🛒 {name} ({file})" for name, file in shop_items.items()])
    await ctx.send(f"**Shop Items:**\n{items}\n\nUse `!buy item_name` to purchase.")

@bot.command()
async def buy(ctx, item_name: str):
    user_id = str(ctx.author.id)
    bal = coins.get(user_id, 0)

    if item_name not in shop_items:
        await ctx.send("❌ That item does not exist in the shop.")
        return

    cost = 10  # fixed cost
    if bal < cost:
        await ctx.send(f"❌ You need at least {cost} coins to buy {item_name}.")
        return

    # Deduct coins
    coins[user_id] = bal - cost
    save_coins()

    # Build file path
    file_path = os.path.join(IMAGES_FOLDER, shop_items[item_name])
    if os.path.exists(file_path):
        await ctx.send(
            f"✅ {ctx.author.mention} purchased **{item_name}**!",
            file=discord.File(file_path)
        )
    else:
        # Debug print for missing file
        print(f"DEBUG: File not found: {os.path.abspath(file_path)}")
        await ctx.send(f"⚠️ Sorry, the file for this item is missing.\nExpected at: `{os.path.abspath(file_path)}`")

@bot.command(name="commands")
async def list_commands(ctx):
    cmds = [cmd.name for cmd in bot.commands]
    await ctx.send("Available Commands:\n" + "\n".join([f"🔹 {c}" for c in cmds]))

# Custom help command
@bot.command(name="help")
async def help_cmd(ctx, command_name: str = None):
    if command_name is None:
        cmds = [cmd.name for cmd in bot.commands]
        await ctx.send("📖 Use `!help <command>` to see details.\nCommands:\n" +
                       "\n".join([f"🔹 {c}" for c in cmds]))
    else:
        command_name = command_name.lower()
        help_text = {
            "balance": "💡 `!balance` → Shows your current coin balance.",
            "shop": "💡 `!shop` → Lists all available shop items.",
            "buy": "💡 `!buy <item_name>` → Purchase an item from the shop (cost: 10 coins).",
            "commands": "💡 `!commands` → Shows a list of all commands.",
            "help": "💡 `!help [command]` → Shows help for commands."
        }
        await ctx.send(help_text.get(command_name, "❌ Command not found. Use `!commands` to see all commands."))

# ---------------- ERROR HANDLER ----------------
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Invalid command. Use `!commands` to see the list of commands.")
    else:
        raise error

# ---------------- RUN ----------------
bot.run(TOKEN)
