from telethon import events
from games.word_scramble import active_games  # Import active games

# Command definition
command = "revoke"

async def handler(event):
    """Handles the /revoke command to remove a user from all active games."""
    user_id = event.sender_id

    if user_id in active_games:
        del active_games[user_id]
        await event.respond("✅ You have been removed from all active games.")
    else:
        await event.respond("❌ You are not part of any active games.")
