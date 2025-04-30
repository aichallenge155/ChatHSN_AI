import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Bot Token (loaded from .env)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Gemini API Key (loaded from .env)
AI_API_KEY = os.getenv("AI_API_KEY")


# Database Configuration
DB_PATH = 'database/users.db'  # Fayl yolunun müvafiq olaraq düzəldildiyinə əmin olun

# Bot Configuration
COMMAND_PREFIX = '!'
BOT_DESCRIPTION = "AI-powered Discord Bot for the IT Olympiad"

# Response Styles
RESPONSE_STYLES = {
    "default": "Respond in a helpful, concise manner.",
    "kid": "Respond like a curious 8-year-old child who uses simple language.",
    "physics_teacher": "Respond like a knowledgeable physics teacher who explains concepts clearly and uses relevant examples.",
    "poet": "Respond in a poetic style with metaphors and vivid language.",
    "historian": "Respond as a historian who provides context and historical references."
}

# Optional: Check all required variables at startup
def check_env_vars():
    if not DISCORD_TOKEN:
        raise ValueError("❌ Discord Token tapılmadı! .env faylını yoxlayın.")
    if not AI_API_KEY:
        raise ValueError("❌ AI API Key tapılmadı! .env faylını yoxlayın.")
    
    
    print("✅ Config faylı uğurla yükləndi.")
    print(f"DISCORD_TOKEN (ilk 5 simvol): {DISCORD_TOKEN[:5]}*****")
    print(f"AI_API_KEY (ilk 5 simvol): {AI_API_KEY[:5]}*****")