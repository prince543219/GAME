from telethon import Button
from telethon import events
from games.word_scramble import start_word_scramble

# Define the command for this handler
command = "game"

# Command to handle /game
async def handler(event):
    """Handles the /game command and displays inline buttons."""
    game_buttons = [
        [Button.inline("Word Scramble", b"word_scramble"),],
    ]
    
    await event.respond(
        "🎮 Click on game to start:",
        buttons=game_buttons
    )

# Command to handle button clicks
async def button_handler(event):
    """Handles the game selection button clicks."""
    game_choice = event.data.decode('utf-8')
    
    if game_choice == "word_scramble":
        await start_word_scramble(event)
    elif game_choice == "word_chain":
        await event.respond("🧩 Starting Word Chain...")  # Example message
    elif game_choice == "hangman":
        await event.respond("🧩 Starting Hangman...")  # Example message
    elif game_choice == "word_guess":
        await event.respond("🧩 Starting Word Guess...")  # Example message
    else:
        await event.respond("❌ Invalid game selection.")
