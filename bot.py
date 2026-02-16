import os
import discord
from discord.ext import commands, tasks
import logging
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
import random

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise SystemExit("Environment variable DISCORD_TOKEN not set. Set it in .env or environment and restart.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def hello(ctx):
    responses = [
        "Hello! My name is John. How can I help you?",
        "Hey there! I'm John, your friendly bot. What do you need?",
        "Greetings! I'm John. How may I assist you today?",
        "Hi! John here. What can I do for you?",
        "Welcome! I'm John. How can I be of service?",
        "Hey! It's John. What's on your mind?"
    ]
    await ctx.send(random.choice(responses))


@bot.command()
async def hi(ctx):
    await ctx.send("Hello! How can we render our service to you?")


    


bot.run(TOKEN)
