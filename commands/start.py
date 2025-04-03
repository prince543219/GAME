# commands/start.py
from telethon import Button

command = "start_game_1"

# Command handler function
async def handler(event):
    user = await event.get_sender()
    user_full_name = user.first_name or "there"
    if user.last_name:
        user_full_name += f" {user.last_name}"

    # Generate the profile link for the user
    user_profile_link = f"tg://user?id={user.id}"

    # Fetch bot username dynamically only once per session
    bot_user = await event.client.get_me()
    bot_username = bot_user.username

    # Create greeting message
    greeting_message = (
        f"✨ Hello, [**{user_full_name}**]({user_profile_link})! 👋\n\n"
        "🎮 Welcome to the **Word Game Bot**!\n\n"
        "🕹️ Here, you can:\n"
        "- Play exciting word games.\n"
        "- Track your scores and compete with others.\n\n"
        "📚 Use **/help** to explore all available commands.\n\n"
        "🚀 Ready to have some fun? Let's get started!"
    )

    # If it's a private chat, send the greeting
    if event.is_private:
        buttons = [
            [Button.url("➕ Add Me to a Group", f"https://t.me/{bot_username}?startgroup=true")]
        ]
        await event.reply(greeting_message, buttons=buttons, parse_mode="markdown")
    
    # If it's a group, send the game information
    else:
        group_message = (
            "Hello, 🎮 Here are the available games you can start:\n\n"
        )
        if event.message.raw_text.strip() in ["/start", f"/start@{bot_username}"]:
            await event.reply(group_message)
