import discord
import os
import google.generativeai as genai
import json
from datetime import datetime
from dotenv import load_dotenv

def PersonaLoadFull():
    with open("PersonaYuna.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    PromptLine = [f"{key} :  {value}" for key, value in data.items()]
    FullPrompt = "\n".join(PromptLine)
    return FullPrompt

def LogFullConversation(user_id, role, content):
    os.makedirs("chat_history", exist_ok=True)
    filename = f"chat_history/{user_id}.jsonl"

    log_entry = {
        "timestamp" : datetime.utcnow().isoformat(),
        "role" : role,
        "content" : content
    }

    with open(filename, "a", encoding="utf-8") as f:
        json.dump(log_entry, f, ensure_ascii=False)
        f.write("\n")

# ------------------------memory
MEMORY_FILE = "memory.json"

def LoadMemory(): #LoadLastMemory
    try:
        with open(MEMORY_FILE, "r",encoding="utf-8") as f:
          return json.load(f)
    except FileNotFoundError:
        return{}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def CountTokens(text):
    return len(text.split())

def update_memory(user_id, role, content): #add content and limit 5120 token
    memory = LoadMemory()
    uid = str(user_id)
    if uid not in memory:
        memory[uid] = []
    
    memory[uid].append({"role": role, "content" : content})


    while True: #list context 
        combined = "\n".join([f"{m['role']}: {m['content']}" for m in memory[uid]])
        if CountTokens(combined) < 5120:
            break
        memory[uid].pop(3)
    
    save_memory(memory)

def get_context(user_id):
    memory = LoadMemory()
    uid = str(user_id)
    return "\n".join([f"{m['role']}: {m['content']}" for m in memory.get(uid, [])]) 

# ------------------------------

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
        user_prompt = message.content[5:].strip()
        user_id = message.author.id
        
        persona_data = PersonaLoadFull()
        memory_context = get_context(user_id)

        full_prompt =f"{persona_data} \n\n {memory_context}\nuser :  {user_prompt} \nYuna : "

        response = model.generate_content(full_prompt)
        reply = response.text

        update_memory(user_id, "user", user_prompt)
        update_memory(user_id, "Yuna", reply)

        LogFullConversation(user_id, "user", user_prompt)
        LogFullConversation(user_id, "Yuna", reply)




        await message.channel.send(response.text)

client.run(DISCORD_TOKEN)
