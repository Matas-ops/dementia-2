import random
from discord.ext import commands, tasks
from TikTokApi import TikTokApi
import os

USERNAME_55 = "alexandrioss2"
USERNAME_GEDIPLIUSAS = "gedipliusas.ok"

tiktok_tokens = []
tiktok_videos = []
tiktok_videos_55 = []
tiktok_videos_gedipliusas = []


def init_tiktok_tokens(tokens):
    global tiktok_tokens
    tiktok_tokens = tokens

@tasks.loop(hours=24)
async def get_tiktok_videos():
    global tiktok_videos, tiktok_videos_55, tiktok_videos_gedipliusas
    try:
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=tiktok_tokens,
                num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "chromium"))

            async for video in api.user(username=USERNAME_55).videos(count=50):
                tiktok_videos_55.append(f"https://www.tiktok.com/@{USERNAME_55}/video/{video.id}")
            async for video in api.user(username=USERNAME_GEDIPLIUSAS).videos(count=50):
                tiktok_videos_gedipliusas.append(f"https://www.tiktok.com/@{USERNAME_GEDIPLIUSAS}/video/{video.id}")

        tiktok_videos = tiktok_videos_55 + tiktok_videos_gedipliusas

    except Exception as e:
        print(f"get_tiktok_videos error: {e}")

@commands.command(name='55', aliases=['5.5'])
async def tiktok_55(ctx):
    if not tiktok_videos_55:
        await ctx.send('Error :(')
        return

    await ctx.send(random.choice(tiktok_videos_55))

@commands.command(name='gedipliusas')
async def tiktok_gedipliusas(ctx):
    if not tiktok_videos_gedipliusas:
        await ctx.send('Error :(')
        return
    await ctx.send(random.choice(tiktok_videos_gedipliusas))

@commands.command(name='tiktok')
async def tiktok_all(ctx):
    if not tiktok_videos:
        await ctx.send('Error :(')
        return
    await ctx.send(random.choice(tiktok_videos))
