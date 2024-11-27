from dotenv import dotenv_values
import discord
from discord.ext import commands
from io import BytesIO

from modules.openai import openai_init
from modules.json import load_json, save_json
from modules.imgur import imgur_upload
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

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")
    activity = discord.Activity(type=discord.ActivityType.playing, name="!help")

    await bot.change_presence(activity=activity)

@bot.command(name="help")
async def help(ctx):
    await ctx.send(
"""
# prefix: !
```
!tokenhistory: 현재 채널에 저장된 히스토리 토큰 사용량
!checktoken [text]: [text] 토큰 측정
!clearhistory: 현재 채널 대화 히스토리 초기화
!jsonhistory: 현재 채널 대화 히스토리 JSON 파일로 다운로드
```
# [Github Repository](https://github.com/Y0rFa1se/discord_gpt)
"""
    )

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
            if attachment.content_type and attachment.content_type.startswith("image/"):
                file_data = await attachment.read()

                image_url = imgur_upload(("image.png", BytesIO(file_data), attachment.content_type), ENV_DICT["IMGUR_CLIENT_ID"])
                history = load_json(f"{message.guild}/{message.channel.category}", message.channel)
                history = render_image(history, image_url)
                history = cut_message(history)
                save_json(f"{message.guild}/{message.channel.category}", message.channel, history)

                await message.channel.send("Image uploaded.")

    if message.content:
        requests = message.content
        history = load_json(f"{message.guild}/{message.channel.category}", message.channel)
        history = render_requests(history, requests)
        history = cut_message(history)
        responses = gpt_request(history, MODEL)

        msg = await message.channel.send("Typing...")
        collected = ""

        async for chunk in responses:
            collected += chunk.choices[0].message.content

            await msg.edit(content=collected)

        history = render_responses(history, collected)
        save_json(f"{message.guild}/{message.channel.category}", message.channel, history)

    await bot.process_commands(message)

bot.run(ENV_DICT["DISCORD_TOKEN"])
