from telethon import events

from games.word_scramble import stop_game

command = "stop"

async def handler(event):
    await stop_game(event)
