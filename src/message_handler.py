import discord
from url_sanitizer import sanitize_url

async def handle_message(bot, message):
    if message.author.bot:
        return

    prefix = bot.command_prefix if isinstance(bot.command_prefix, str) else "!"
    if message.content and message.content.startswith(prefix):
        await bot.process_commands(message)
        return

    sanitized = sanitize_url(message.content)
    if sanitized == message.content:
        return
    message.content = sanitized

    content = message.content or ""
    embed = discord.Embed(color=discord.Color.blurple())
    try:
        avatar_url = message.author.display_avatar.url
    except Exception as e:
        print(e)
        avatar_url = None
    embed.set_author(name=str(message.author), icon_url=avatar_url)
    embed.set_footer(text=f"User ID: {message.author.id}")

    files = []
    if message.attachments:
        for att in message.attachments:
            try:
                f = await att.to_file()
                files.append(f)
            except Exception as e:
                print(e)

    try:
        await message.channel.send(embed=embed)
        send_kwargs = {}
        if content:
            send_kwargs["content"] = content
        if files:
            send_kwargs["files"] = files
        if send_kwargs:
            await message.channel.send(**send_kwargs)
            await message.delete()
    except Exception as e:
        print(e)
