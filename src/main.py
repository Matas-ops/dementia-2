import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import threading
from server import run_dummy_server
from tictactoe import tic_tac_toe, init_tictactoe
from gif import gif, init_gifs, fetch_gifs, daily_gif
from remind import remind, init_remind
from message_handler import handle_message

load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot.add_command(tic_tac_toe)
bot.add_command(gif)
bot.add_command(remind)

init_tictactoe(bot)
init_gifs(bot, int(os.getenv("GIF_CHANNEL_ID")), int(os.getenv("BOT_CHANNEL_ID")))
init_remind(bot)

@bot.event
async def on_ready():
    print("Bot is ready.")
    fetch_gifs.start()
    daily_gif.start()

@bot.event
async def on_message(message):
    await handle_message(bot, message)

t1 = threading.Thread(target=run_dummy_server)
t1.start()

bot.run(os.getenv('BOT_TOKEN'))
