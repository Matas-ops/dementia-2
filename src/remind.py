import discord
from discord.ext import commands
import asyncio
import re

bot = None

def init_remind(bot_instance):
    global bot
    bot = bot_instance

# Helper to parse flexible time inputs
def parse_time(time_str):
    pattern = r'(\d+)([smhd])'
    matches = re.findall(pattern, time_str.lower())
    if not matches:
        return None

    total_seconds = 0
    unit_multipliers = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400
    }

    for value, unit in matches:
        try:
            total_seconds += int(value) * unit_multipliers[unit]
        except (ValueError, KeyError):
            return None

    return total_seconds if total_seconds > 0 else None

@commands.command(name='remind')
async def remind(ctx, time: str, *, reminder: str):
    """
    Usage examples:
    !remind 10m Drink water
    !remind 1h30m Meeting with team
    !remind 2d15m10s Take a break
    !remind 3d Go grocery shopping
    """

    print(f'Received remind command: {ctx.message.content}')
    delay = parse_time(time)

    if delay is None:
        await ctx.send("⛔ Invalid time format. Use `10m`, `1h30m`, `2d15m10s`, etc.")
        return

    await ctx.send(f"⏰ Got it! I’ll remind you in `{time}` to: **{reminder}**")
    await asyncio.sleep(delay)

    try:
        await ctx.send(f"🔔 Hey {ctx.author.mention}, here's your reminder: **{reminder}**")
    except discord.HTTPException:
        print("Failed to send reminder.")
