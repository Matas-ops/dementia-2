from discord.ext import commands, tasks
from translator import translate_string
import requests
import random

QUOTE_API_KEY = None
BIBLE_API_KEY = None
quote = None
verse = None
crap = None

with open('data/quotes.txt', 'r', encoding='utf-8') as file:
    crap = file.readlines()


def init_quote(quote_api_key, bible_api_key):
    global QUOTE_API_KEY
    global BIBLE_API_KEY
    QUOTE_API_KEY = quote_api_key
    BIBLE_API_KEY = bible_api_key


@tasks.loop(hours=24)
async def fetch_quote_of_day():
    global quote
    url = "https://quotes.rest/qod?language=en"

    headers = {
        "Authorization": f"Bearer {QUOTE_API_KEY}"
    }

    response = requests.get(url, headers=headers)
    print(response.status_code, response.text)

    if response.status_code == 200:
        data = response.json()
        quotes = data.get("contents", {}).get("quotes", [])
        if quotes:
            quote_data = quotes[0]
            quote_text = quote_data.get("quote", "")
            author = quote_data.get("author", "Unknown")
            quote = await translate_string(f"{quote_text} - {author}")


@tasks.loop(hours=24)
async def fetch_verse_of_day():
    global verse
    url = "https://quotes.rest/bible/vod.json"

    headers = {
        "Authorization": f"Bearer {BIBLE_API_KEY}"
    }

    response = requests.get(url, headers=headers)
    print(response.status_code, response.text)

    if response.status_code == 200:
        data = response.json()
        contents = data.get("contents", {})
        testament = contents.get("testament", "Unknown Testament")
        book = contents.get("book", "Unknown Book")
        chapter = contents.get("chapter", "Unknown Chapter")
        verse_text = contents.get("verse", "Unknown Verse")
        verse = await translate_string(f"{testament}, {book} {chapter}: {verse_text}")
        

@commands.command(name='quote')
async def quote(ctx):
    print(f'Received quote command: {ctx.message.content}')
    choice = random.randint(1, 99) % 3
    match choice:
        case 0:
            await ctx.send(random.choice(crap))
        case 1:
            await ctx.send(quote)
        case 2:
            await ctx.send(verse)
