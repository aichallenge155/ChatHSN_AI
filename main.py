import discord
import asyncio
from discord.ext import commands
import os
import sys
from config import DISCORD_TOKEN, COMMAND_PREFIX, BOT_DESCRIPTION
from database import init_db

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for v2 of discord.py


# Create bot instance
bot = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    description=BOT_DESCRIPTION,
    intents=intents,
    help_command=None  # Disable default help command
)

    
async def load_extensions():
    """Load all command extensions."""
    # Initialize database
    init_db()
    
    # Load command extensions
    from commands import base_commands, special_commands
    
    await base_commands.setup(bot)
    await special_commands.setup(bot)
    
    print("Extensions loaded successfully.")

@bot.event
async def on_ready():
    """Called when the bot is ready."""
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print(f"Using discord.py version: {discord.__version__}")
    print("------")

    # Set the bot's status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{COMMAND_PREFIX}help"
        ),
        status=discord.Status.online
    )
    
    print("Presence updated!")

@bot.event
async def on_command_error(ctx, error):
    """Global error handler for bot commands."""
    from utils import handle_command_error
    await handle_command_error(ctx, error)

async def main():
    """Main function to start the bot."""
    try:
        # Load extensions
        await load_extensions()
        
        # Start the bot
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        # Make sure we clean up properly
        await bot.close()

if __name__ == "__main__":
    # Run the bot
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot shutting down...")
        sys.exit(0)