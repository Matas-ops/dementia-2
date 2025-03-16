import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import threading
from server import run_dummy_server
from tictactoe import tic_tac_toe, init_tictactoe
from gif import gif, init_gifs, fetch_gifs
from quote import quote, init_quote, fetch_quote_of_day, fetch_verse_of_day

load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot.add_command(tic_tac_toe)
bot.add_command(gif)
bot.add_command(quote)

init_tictactoe(bot)
init_gifs(bot, int(os.getenv("GIF_CHANNEL_ID")))
init_quote(os.getenv("QUOTE_API_KEY"), os.getenv("BIBLE_API_KEY"))

@bot.event
async def on_ready():
    print("Bot is ready.")
    fetch_gifs.start()
    fetch_quote_of_day.start()
    fetch_verse_of_day.start()

t1 = threading.Thread(target=run_dummy_server)
t1.start()

bot.run(os.getenv('BOT_TOKEN'))
