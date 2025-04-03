from telethon import events

from games.word_scramble import stop_game

command = "stop_game"

async def handler(event):
    await stop_game(event)
