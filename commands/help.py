# commands/help.py

from telethon import Button

command = "help"  # Command name for dynamic loading

# Command handler function
async def handler(event):
    # Generate help message with available commands
    help_message = (
        "📚 **Help - Word Game Bot**\n\n"
        "Here are the available commands you can use:\n\n"
        "1. /start - Start the bot and get a personalized greeting.\n"
        "2. /help - Get this help message.\n"
        "3. /score - Check your current score.\n"
        "4. /leaderboard - View the leaderboard.\n"
        "5. /game - Start a game (game commands will be added here later).\n\n"
        "✨ You can always type **/start** to get back to the main menu.\n"
    )

    # Send the help message
    await event.reply(help_message, parse_mode="markdown")
