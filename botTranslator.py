#!/usr/bin/env python3

import discord
import os
import re
import asyncio
from dotenv import load_dotenv
from googletrans import Translator

# Load token from .env
load_dotenv()
token = os.getenv('discord_token')

# Initialize translator
translator = Translator()

# Discord intents setup
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def detect_language(text):
    return await asyncio.to_thread(translator.detect, text)

async def translate_text(text, dest):
    return await asyncio.to_thread(translator.translate, text, dest=dest)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Skip messages containing URLs
    if re.search(r'http[s]?://', message.content):
        return

    # Skip empty messages or messages without any alphanumeric characters
    if not message.content.strip() or not any(char.isalnum() for char in message.content):
        return

    try:
        detected = await detect_language(message.content)
        print(f"Detected language: {detected.lang}")

        if detected.lang == 'en':
            translated = await translate_text(message.content, dest='ru')
            await message.channel.send(f"🇬🇧➡️🇷🇺 {translated.text}")

        elif detected.lang == 'ru':
            translated = await translate_text(message.content, dest='en')
            await message.channel.send(f"🇷🇺➡️🇬🇧 {translated.text}")

        else:
            print(f"No translation needed for detected language: {detected.lang}")

    except Exception as e:
        print(f"Translation error: {e}")

client.run(str(token))
