import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import threading
from server import run_dummy_server
from tictactoe import tic_tac_toe, init_tictactoe
from gif import gif, init_gifs, fetch_gifs

load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot.add_command(tic_tac_toe)
bot.add_command(gif)

init_tictactoe(bot)
init_gifs(bot)

@bot.event
async def on_ready():
    fetch_gifs.start()
    print("Bot is ready and GIF fetching task has started.")

t1 = threading.Thread(target=run_dummy_server)
t1.start()

bot.run(os.getenv('BOT_TOKEN'))
