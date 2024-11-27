from dotenv import dotenv_values
import discord
from discord.ext import commands
from io import BytesIO
import asyncio
import aiohttp

from modules.openai import openai_init
from modules.json import load_json, save_json
from modules.imgur import imgur_upload
from modules.wolfram import get_wolfram
from modules.langchain import process_pdf
from modules.gpt import (
    count_token,
    cut_message,
    render_requests,
    render_image,
    render_responses,
    gpt_request
)

ENV_DICT = dotenv_values(".env")

openai_init(ENV_DICT["GPT_API"])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

streaming_chunk = dict()

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")
    activity = discord.Activity(type=discord.ActivityType.playing, name="!help")

    await bot.change_presence(activity=activity)

@bot.command(name="help")
async def help(ctx):
    with open("templates/help.md", "r") as f:
        help_text = f.read()
        await ctx.send(help_text)

@bot.command(name="tokenhistory")
async def check_token(ctx):
    tokens = count_token(load_json(ctx.channel), model=ENV_DICT["MODEL"])
    await ctx.send(tokens)

@bot.command(name="checktoken")
async def check_token(ctx, *args):
    tokens = count_token([{"content": arg} for arg in args], model=ENV_DICT["MODEL"])
    await ctx.send(tokens)

@bot.command(name="clearhistory")
async def clear_history(ctx):
    save_json(f"{ctx.guild}/{ctx.channel.category}", ctx.channel, [])
    await ctx.send("History cleared.")

@bot.command(name="jsonhistory")
async def json_history(ctx):
    file = discord.File(f"chat_history/{ctx.guild}/{ctx.channel.category}/{ctx.channel}.json", filename="history.json")
    await ctx.send(file=file)

    with open(f"chat_history/{ctx.guild}/{ctx.channel.category}/{ctx.channel}.json", "r") as f:
        unicode_encoded = f.read().encode("utf-8")

        decoded = unicode_encoded.decode("unicode_escape")

        with open(f"chat_history/{ctx.guild}/{ctx.channel.category}/{ctx.channel}_decoded.json", "w", encoding="utf-8") as f:
            f.write(decoded)

    file = discord.File(f"chat_history/{ctx.guild}/{ctx.channel.category}/{ctx.channel}_decoded.json", filename="history_decoded.json")
    await ctx.send(file=file)

@bot.command(name="streamchunk")
async def stream_chunk(ctx, number: int):
    streaming_chunk[ctx.channel] = number
    await ctx.send(f"Streaming chunk set to {number}.")

@bot.command(name="wa")
async def wolfram_alpha(ctx, *args):
    query = " ".join(args)
    response = await get_wolfram(query, ENV_DICT["WOLFRAM_APP_ID"])

    if response:
        await ctx.send(response)
        
    else:
        await ctx.send("No results found.")

@bot.event
async def on_message(message):
    MODEL = str(message.channel.category)

    if message.author.bot:
        return
    
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return
    
    if str(message.channel).startswith("bot_off"):
        return
    
    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type:
                if attachment.content_type.startswith("image/"):
                    file_data = await attachment.read()

                    image_url = imgur_upload(("image.png", BytesIO(file_data), attachment.content_type), ENV_DICT["IMGUR_CLIENT_ID"])
                    history = load_json(f"{message.guild}/{message.channel.category}", message.channel)
                    history = render_image(history, image_url)
                    history = cut_message(history)
                    save_json(f"{message.guild}/{message.channel.category}", message.channel, history)

                    await message.channel.send("Image uploaded.")

                elif attachment.content_type and attachment.content_type.startswith("pdf"):
                    print("pdf")
                    url = attachment.url

                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            pdf_binary = await response.read()

                            with open("files/pdf.pdf", "wb") as f:
                                f.write(pdf_binary)

                    text = "pdf content: " + process_pdf(pdf_binary)
                    history = load_json(f"{message.guild}/{message.channel.category}", message.channel)
                    history = render_requests(history, text)
                    history = cut_message(history)
                    save_json(f"{message.guild}/{message.channel.category}", message.channel, history)

                    await message.channel.send("PDF uploaded.")

    if message.content:
        requests = message.content
        history = load_json(f"{message.guild}/{message.channel.category}", message.channel)
        history = render_requests(history, requests)
        history = cut_message(history)
        responses = gpt_request(history, MODEL)

        msg = await message.channel.send("Typing...")
        collected = ""

        for idx, chunk in enumerate(responses):
            if chunk.choices[0].delta.content:
                collected += chunk.choices[0].delta.content

                chunk_size = streaming_chunk.get(message.channel, 10)
                if idx % chunk_size == 0:
                    try:
                        await asyncio.wait_for(msg.edit(content=collected), timeout=0.2)

                    except asyncio.TimeoutError:
                        pass

        await msg.edit(content=collected)

        history = render_responses(history, collected)
        save_json(f"{message.guild}/{message.channel.category}", message.channel, history)

    await bot.process_commands(message)

bot.run(ENV_DICT["DISCORD_TOKEN"])
