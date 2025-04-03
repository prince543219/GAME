# commands/help.py

from telethon import Button

command = "help_game"  # Command name for dynamic loading

# Command handler function
async def handler(event):
    # Generate help message with available commands
    help_message = (
        "📚 **Help - Word Game Bot**\n\n"
        "Here are the available commands you can use:\n\n"
        "1. /help_game - Get this help message.\n"
        "2. /leaderboard - View the leaderboard.\n"
        "3. /game - Start a game (game commands will be added here later).\n\n"
        "4. /stop_game - to stop the game (commands only for admins).\n"
    )

    # Send the help message
    await event.reply(help_message, parse_mode="markdown")
