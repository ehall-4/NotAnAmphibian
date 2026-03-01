import subprocess
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os


# ------------------------------------------------
# Load environment variables and my user ID
# ------------------------------------------------
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

OWNER_ID = 127634987854987264

# ------------------------------------------------
# Initialize bot, logging and intents
# ------------------------------------------------

handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content= True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ------------------------------------------------
# Events
# ------------------------------------------------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event 
async def on_message(message):
    if message.author == bot.user:
        return
    if "frog" in message.content.lower():
        await message.reply(f"What *are* frogs? :frog:")
        
    await bot.process_commands(message)

# ------------------------------------------------
# '!' Commands
# ------------------------------------------------

@bot.command()
async def hello(ctx):
    await ctx.reply(f"Hello {ctx.author.mention}!")
    
@bot.command()
async def startserver(ctx):
    await ctx.send("Starting Minecraft server...")
    
    subprocess.Popen([
        "sudo", "-u", "minecraft",
        "/opt/minecraft/server/start.sh"
        ])
    
    await ctx.send("Minecraft server is running!")
   
@bot.command()
async def shutdown(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("You do not have permission to use this command.")
        return
    
    await ctx.send("Shutting down...")
    
    subprocess.Popen([
        "sudo", "/bin/systemctl", "stop", "discordbot"
    ])

bot.run(token, log_handler=handler, log_level=logging.DEBUG)