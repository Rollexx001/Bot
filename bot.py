import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise SystemExit("Environment variable DISCORD_TOKEN not set. Set it and restart.")

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
    await ctx.send("Hello! my name is john. How can I help you?")

@bot.command()
async def hi(ctx):
    await ctx.send("Hello! How can we render our service to you?")


bot.run(TOKEN)
