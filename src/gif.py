import discord
from discord.ext import commands, tasks
import random
import os
import sys

GIF_CHANNEL_ID = int(os.getenv("GIF_CHANNEL_ID"))
gif_urls = []
bot = None

def init_gifs(bot_instance):
    global bot
    bot = bot_instance

@tasks.loop(hours=24)
async def fetch_gifs():
    #Fetches and stores GIFs from the specific channel every 24 hours.
    global gif_urls
    channel = bot.get_channel(GIF_CHANNEL_ID)
    if channel:
        print("Channel found, fetching...")
        messages = [msg async for msg in channel.history(limit=sys.maxsize)]
        gif_urls = [msg.content for msg in messages if msg.content.endswith(('.gif'))]
        print("Done fetching")

@commands.command(name='gif')
async def gif(ctx):
    #Fetches a random available GIF from the stored list.
    if not gif_urls:
        await ctx.send("No GIFs found or the list hasn't been updated yet.")
        return
    
    # Try finding an embeddable GIF 10 times
    for _ in range(10):
        gif_url = random.choice(gif_urls)
        embed = discord.Embed()
        embed.set_image(url=gif_url)
        
        # Send the embed but delete if it doesn't properly display
        message = await ctx.send(embed=embed)
        if message.embeds and message.embeds[0].image:
            return  # GIF successfully embedded, exit the loop
        else:
            await message.delete()  # Delete if no valid GIF preview
    
    await ctx.send("Couldn't find an embeddable GIF.")
