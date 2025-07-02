import discord
import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

def PersonaLoad():
    with open("PersonaYuna.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["persona"]


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17-thinking") # Setting you model api
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

    if message.content.startswith("!ask"):
        user_prompt = message.content[5:]
        persona = PersonaLoad()
        full_prompt =f"{persona} \n\n User :  {user_prompt} \nYuna : "
        response = model.generate_content(full_prompt)
        await message.channel.send(response.text)

client.run(DISCORD_TOKEN)
