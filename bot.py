from telethon import TelegramClient, events
import importlib
import os

# Import your bot credentials
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the client
client = TelegramClient("client", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Function to dynamically load command handlers
def load_handlers():
    commands_dir = "commands"
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"{commands_dir}.{filename[:-3]}"
            try:
                # Dynamically import the handler module
                module = importlib.import_module(module_name)
                if hasattr(module, "command") and hasattr(module, "handler"):
                    command = module.command
                    handler = module.handler
                    # Register the command handler
                    client.add_event_handler(handler, events.NewMessage(pattern=f"/{command}"))
            except Exception as e:
                print(f"Failed to load handler {module_name}: {e}")

# Load all handlers
load_handlers()

# Add a handler for button clicks
@client.on(events.CallbackQuery)
async def callback(event):
    from commands.game import button_handler
    await button_handler(event)

# Start the client
print("Client is running...")
client.run_until_disconnected()
