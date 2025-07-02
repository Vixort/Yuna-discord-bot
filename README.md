# Yuna-Bot

Yuna-Bot is a Discord AI chatbot powered by Google's Gemini API.  
She responds to `!ask` messages using your custom persona defined in a `persona.json` file.

---

## Features

- Chat with Gemini AI using natural language
- Custom personality via `persona.json`
- Supports environment variables with `.env`
- Lightweight, no database required

### Persistent Chat Log
- Saves every single message (user + bot) to chat_history/{user_id}.jsonl
- Useful for auditing, training data, or personal review
- Separated per user and stored in JSON Lines format


---

## ⚙️ Installation (Windows)

### 1. Install Python 3.8 or higher  
[Download Python](https://www.python.org/downloads/windows/)  
Make sure to check “Add Python to PATH” during installation

### 2. Install Git  
[Download Git](https://git-scm.com/download/win)  
You can use Git Bash, Command Prompt, or PowerShell

### 3. Clone this repository

```bash
git clone https://github.com/Vixort/Yuna-discord-bot.git
cd Yuna-discord-bot
```

### 4. (Optional) Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 5. Install dependencies
```bash
pip install discord.py google-generativeai python-dotenv

```
### 6. Configure environment variables
```.env
DISCORD_TOKEN=your_discord_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

### 7. Run the bot
```bash
python Yuna.py
```

---


