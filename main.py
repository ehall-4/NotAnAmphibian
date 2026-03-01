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
BLOCKBOIS_ID = 1315843683811201056

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
    
@bot.command(name="start", description="Starts the game server of the channel you're in.")
async def start(ctx):
    if ctx.channel.id == BLOCKBOIS_ID:
        
        await ctx.send("Starting Minecraft server...")    
        
        subprocess.Popen([
            "sudo", "-u", "minecraft",
            "/opt/minecraft/server/start.sh"
        ])
    
        await ctx.send(f"Minecraft server is running on {os.getenv('IP_ADDRESS')}:{os.getenv('PORT')}!")
        return
    
    await ctx.send("This command can only be used in game channels like #block-bois")

@bot.command(name="stop", description="Stops the game server of the channel you're in.")
async def stop(ctx):
    if ctx.channel.id == BLOCKBOIS_ID:
        await ctx.send("Stopping minecraft server...")
    
        subprocess.Popen([
            "sudo", "-u", "minecraft",
            "/opt/minecraft/server/stop.sh"
        ])
        return
    
    await ctx.send("This command can only be used in game channels like #block-bois")

@bot.command(name="shutdown", hidden=True)
async def shutdown(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("You do not have permission to use this command.")
        return
    
    await ctx.send("Shutting down...")
    
    subprocess.Popen([
        "sudo", "/bin/systemctl", "stop", "discordbot"
    ])

bot.run(token, log_handler=handler, log_level=logging.DEBUG)