#from telethon import events

#from games.word_scramble import stop_game

#command = "score12"

#async def handler(event):
    #await event.reply("woking on it !will be added soon.")
from telethon import events

from games.word_scramble import display_final_scores
command = "leaderboard"

async def handler(event):
    await  display_final_scores(event)
