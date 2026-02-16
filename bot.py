import os
import discord
from discord.ext import commands, tasks
import logging
from datetime import datetime
from typing import Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise SystemExit("Environment variable DISCORD_TOKEN not set. Set it and restart.")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = False

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=commands.DefaultHelpCommand(),
    case_insensitive=True
)

# In-memory data store
user_data = {}


# Events
@bot.event
async def on_ready():
    logger.info(f"✓ Bot logged in as {bot.user} ({bot.user.id})")
    logger.info(f"✓ Connected to {len(bot.guilds)} guild(s)")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="!help for commands"
        )
    )


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors gracefully"""
    logger.error(f"Command error in {ctx.command}: {error}")
    
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: {error.param.name}")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help` to see available commands.")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")


@bot.event
async def on_member_join(member):
    """Log when a member joins"""
    logger.info(f"Member joined: {member} ({member.id})")
    user_data[member.id] = {
        "name": member.name,
        "joined": datetime.now(),
        "messages": 0
    }


# Commands - Greeting Group
greeting_group = commands.Group(name="greet", help="Greeting commands")


@greeting_group.command(name="hello", help="Say hello")
async def greet_hello(ctx):
    """Send a friendly greeting"""
    await ctx.send(f"Hello {ctx.author.mention}! I'm a Discord bot. How can I help you?")


@greeting_group.command(name="hi", help="Send a brief greeting")
async def greet_hi(ctx):
    """Send a brief greeting"""
    await ctx.send(f"Hi {ctx.author.mention}! 👋 How can I assist you today?")


bot.add_command(greeting_group)


# Commands - Utility Group
utility_group = commands.Group(name="util", help="Utility commands")


@utility_group.command(name="ping", help="Check bot latency")
async def util_ping(ctx):
    """Check bot latency/response time"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: {latency}ms")


@utility_group.command(name="userinfo", help="Get user information")
async def util_userinfo(ctx, member: Optional[discord.Member] = None):
    """Get information about a user"""
    member = member or ctx.author
    
    embed = discord.Embed(
        title=f"User Info - {member}",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Status", value=member.status, inline=False)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=False)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    await ctx.send(embed=embed)


@utility_group.command(name="serverinfo", help="Get server information")
async def util_serverinfo(ctx):
    """Get information about the server"""
    guild = ctx.guild
    
    embed = discord.Embed(
        title=f"Server Info - {guild.name}",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Guild ID", value=guild.id, inline=False)
    embed.add_field(name="Members", value=guild.member_count, inline=False)
    embed.add_field(name="Channels", value=len(guild.channels), inline=False)
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)
    embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=False)
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    await ctx.send(embed=embed)


bot.add_command(utility_group)


# Commands - Developer/Admin
@bot.command(name="stats", help="Show bot statistics")
async def stats(ctx):
    """Display bot statistics"""
    embed = discord.Embed(
        title="Bot Statistics",
        color=discord.Color.purple(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Guilds", value=len(bot.guilds), inline=True)
    embed.add_field(name="Users", value=len(list(bot.get_all_members())), inline=True)
    embed.add_field(name="Commands", value=len(bot.commands), inline=True)
    embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
    
    await ctx.send(embed=embed)


@bot.command(name="echo", help="Echo your message")
async def echo(ctx, *, message: str):
    """Repeat a message back to you"""
    await ctx.send(f"🔊 {message}")


@bot.command(name="about", help="About this bot")
async def about(ctx):
    """Show information about the bot"""
    embed = discord.Embed(
        title="About Me",
        description="A feature-rich Discord bot built with discord.py",
        color=discord.Color.gold(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Version", value="1.0.0", inline=False)
    embed.add_field(name="Developer", value="Your Name", inline=False)
    embed.add_field(name="Prefix", value="!", inline=False)
    
    await ctx.send(embed=embed)


# Background tasks
@tasks.loop(minutes=30)
async def update_status():
    """Update bot status periodically"""
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} servers | !help"
        )
    )


@update_status.before_loop
async def before_update_status():
    await bot.wait_until_ready()


update_status.start()


# Run the bot
if __name__ == "__main__":
    logger.info("Starting bot...")
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        raise
