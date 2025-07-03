import discord
from discord.ext import commands, tasks
import random
import sys

GIF_CHANNEL_ID = None
gif_urls = None
bot = None


def init_gifs(bot_instance, gif_channel_id):
    global GIF_CHANNEL_ID
    global bot
    GIF_CHANNEL_ID = gif_channel_id
    bot = bot_instance


@tasks.loop(hours=24)
async def fetch_gifs():
    global gif_urls
    channel = bot.get_channel(GIF_CHANNEL_ID)
    if channel:
        print("Channel found, fetching...")
        messages = [msg async for msg in channel.history(limit=sys.maxsize)]
        gif_urls = list(set(msg.content for msg in messages if msg.content.endswith(('.gif'))))
        print("Done fetching")


@commands.command(name='gif')
async def gif(ctx):
    if not gif_urls:
        await ctx.send("No GIFs found or the list hasn't been updated yet.")
        return
    
    for _ in range(10):
        gif_url = random.choice(gif_urls)
        embed = discord.Embed()
        embed.set_image(url=gif_url)
        
        message = await ctx.send(embed=embed)
        if message.embeds and message.embeds[0].image:
            return
        else:
            await message.delete()
    
    await ctx.send("Couldn't find an embeddable GIF.")
