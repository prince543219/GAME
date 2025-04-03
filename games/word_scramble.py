import random
import asyncio
import json
from telethon import events, Button

# File path for wordlist JSON
WORDLIST_FILE = "data/wordlist.json"  # Path to your wordlist JSON file

# Store user games (track active games)
active_games = {}

# Store player scores
player_scores = {}

# Store players who participated in the current game session
active_players_in_game = {}

# File to save player scores persistently
SCORES_FILE = "player_scores.json"

# Helper function to save scores to a file
def save_scores():
    with open(SCORES_FILE, "w") as file:
        json.dump(player_scores, file)

# Helper function to load scores from a file
def load_scores():
    global player_scores
    try:
        with open(SCORES_FILE, "r") as file:
            player_scores = json.load(file)
    except FileNotFoundError:
        player_scores = {}

# Load scores at the start
load_scores()

async def start_word_scramble(event):
    """
    Start the Word Scramble game.
    Users first choose the game mode (Word Scramble), then choose their difficulty level.
    """
    user_id = event.sender_id

    # Check if the user is already playing a game
    if user_id in active_games:
        await event.respond("❌ You are already playing a game. Type /stop to end the current game.")
        return

    # Handle game mode selection
    @event.client.on(events.CallbackQuery)
    async def handle_game_mode_choice(callback_event):
        if callback_event.sender_id != user_id:
            return  # Ignore other users' inputs

        # If the user selects "Word Scramble", show the difficulty options
        if callback_event.data.decode("utf-8") == "word_scramble":
            # Send difficulty level selection
            buttons = [
                [Button.inline("Easy 😊", b"easy"), Button.inline("Medium 😉", b"medium")],
                [Button.inline("Hard ☠️", b"hard")]
            ]
            await callback_event.respond("🎮 Choose your difficulty level:", buttons=buttons)

            # Delete the game mode selection message immediately after responding
            await callback_event.delete()

        # Remove the current game mode selection handler
        event.client.remove_event_handler(handle_game_mode_choice)

        # Handle difficulty choice
        @event.client.on(events.CallbackQuery)
        async def handle_difficulty_choice(callback_event):
            if callback_event.sender_id != user_id:
                return  # Ignore other users' inputs

            difficulty = callback_event.data.decode("utf-8")

            # Load the word list based on difficulty (No need for word list for "word_scramble")
            wordlist = await load_wordlist_from_file(difficulty)
            
            active_games[user_id] = event.chat_id
            await callback_event.respond(f"✅ You chose {difficulty.capitalize()} difficulty. Let's start the game!", buttons=None)

            # Delete the difficulty selection message
            await callback_event.delete()

            # Start the game loop
            await play_game(event, wordlist)

            # Clean up the handler after the game starts
            event.client.remove_event_handler(handle_difficulty_choice)
            await event.delete()


async def play_game(event, wordlist):
    """
    Play the Word Scramble game.
    Words are scrambled, and players have a limited time to guess the correct answer.
    """
    user_id = event.sender_id
    active_games[user_id] = event.chat_id
    chat_id = event.chat_id
    # Inside play_game function
    active_players = []

    # Add participants to active players list
    participants = await event.client.get_participants(chat_id)
    for participant in participants:
        active_players.append(participant.id)
        if participant.id not in player_scores:
            player_scores[participant.id] = 0

    # Store the active players list in the active_players_in_game dictionary
    active_players_in_game[chat_id] = active_players

    # Loop through the word list
    for word in wordlist:
        if user_id not in active_games:
            break  # Game stopped by user
        
        word = random.choice(wordlist)
        scrambled_word = ''.join(random.sample(word, len(word)))
        await event.respond(f"🧩 Word Scramble\n\nUnscramble this word: {scrambled_word}\nYou have 30 seconds to guess!")

        correct_guess = None
        timer_task = asyncio.create_task(asyncio.sleep(30))

        def check_message(guess_event):
            return (
                guess_event.chat_id == chat_id 
                and guess_event.text.strip().lower() != "/stop" 
                and guess_event.sender_id in active_players
            )

        @event.client.on(events.NewMessage(func=check_message))
        async def handle_guess(guess_event):
            nonlocal correct_guess

            if guess_event.text.strip().lower() == word.lower() and correct_guess is None:
                correct_guess = guess_event.sender_id
                first_name = guess_event.sender.first_name or "Anonymous"
                await event.respond(f"✅ {first_name} guessed the word correctly: {word}!")
                
                # Update score only if it's the highest
                player_scores[correct_guess] = max(player_scores[correct_guess], len(word))
                active_players_in_game[correct_guess] = True
                save_scores()  # Save updated scores
                timer_task.cancel()

        try:
            await timer_task
            if correct_guess is None:
                await event.respond(f"❌ Time's up! The correct word was: {word}")
        except asyncio.CancelledError:
            pass

        event.client.remove_event_handler(handle_guess)

        if user_id not in active_games:
            await event.respond("❌ The game has been stopped.")
            return

    active_games.pop(user_id, None)

    # Display final scores
    await display_final_scores(event, active_players)

async def display_final_scores(event, active_players):
    """
    Display the final scores of the game.
    """
    # Ensure player_scores is accessed correctly for each player
    final_scores = {player_id: player_scores.get(player_id, 0) for player_id in active_players}
    sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:10]

    leaderboard = "🏅 Top 10 Scores:\n"
    for idx, (player_id, score) in enumerate(sorted_scores):
        participant = await event.client.get_entity(player_id)
        first_name = participant.first_name or "Anonymous"
        profile_link = f"tg://user?id={player_id}"
        leaderboard += f"{idx + 1}. [**{first_name}**]({profile_link}): {score} points\n"

    await event.respond(leaderboard, parse_mode="md")
    active_players_in_game.clear()  # Optionally clear active players


async def stop_game(event):
    """
    Stop the current game, notify the user, and display the final scores.
    """
    user_id = event.sender_id
    chat_id = event.chat_id

    if user_id not in active_games:
        await event.respond("❌ You are not currently playing any game.")
        return

    # Remove the game from active_games
    active_games.pop(user_id, None)

    # Notify the user
    await event.respond("🛑 Your game has been stopped. Displaying final scores...")

    # Debugging: Print active_players_in_game to verify the data
    print("active_players_in_game:", active_players_in_game)

    # Retrieve the list of active players from active_players_in_game
    active_players = active_players_in_game.get(chat_id, [])

    # Debugging: Print active_players to verify the data
    print("Retrieved active players for chat_id", chat_id, ":", active_players)

    # If active_players is not a list, handle the error
    if not isinstance(active_players, list):
        await event.respond("❌ There was an error retrieving the active players list.")
        return

    if not active_players:
        await event.respond("❌ No active players in this game session.")
    else:
        await display_final_scores(event, active_players)




async def load_wordlist_from_file(difficulty):
    """
    Load the word list based on the chosen difficulty from the JSON file.
    """
    try:
        with open(WORDLIST_FILE, "r") as file:
            data = json.load(file)
        print(f"Loaded data: {data}")  # Debugging line
        # Return the word list for the given difficulty level
        return data.get(difficulty, [])
    except FileNotFoundError:
        print(f"File {WORDLIST_FILE} not found.")  # Debugging line
        return []
