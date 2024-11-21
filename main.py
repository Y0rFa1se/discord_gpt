from dotenv import dotenv_values
import discord
from discord.ext import commands

from modules.gpt import openai_init, count_token, cut_message, render_requests, render_image, render_responses, openai_request
from modules.json import load_json, save_json

ENV_DICT = dotenv_values(".env")

openai_init(ENV_DICT["GPT_API"])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")

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
    save_json(ctx.channel, [])
    await ctx.send("History cleared.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return
    
    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("image/"):
                image_url = attachment.url
                history = load_json(message.channel)
                history = render_image(history, image_url)
                history = cut_message(history)
                save_json(message.channel, history)

    if message.content:
        requests = message.content
        history = load_json(message.channel)
        history = render_requests(history, requests)
        responses = openai_request(history, model=ENV_DICT["MODEL"])
        history = render_responses(history, responses)
        save_json(message.channel, history)
        await message.channel.send(responses)

    await bot.process_commands(message)

bot.run(ENV_DICT["DISCORD_TOKEN"])