#!/usr/bin/env python3

import discord
import os
import re
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

    # Skip empty or emoji-only messages
    if not message.content.strip() or message.content.strip().isascii() == False:
        return

    try:
        detected = translator.detect(message.content)
        print(f"Detected language: {detected.lang}")

        if detected.lang == 'en':
            translated = translator.translate(message.content, dest='ru')
            await message.channel.send(f"🇬🇧➡️🇷🇺 {translated.text}")

        elif detected.lang == 'ru':
            translated = translator.translate(message.content, dest='en')
            await message.channel.send(f"🇷🇺➡️🇬🇧 {translated.text}")

        else:
            print("Message language is neither English nor Russian — skipping.")

    except Exception as e:
        print(f"Translation error: {e}")

client.run(str(token))
