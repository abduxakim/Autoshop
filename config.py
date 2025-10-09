import os
from dotenv import load_dotenv


# Загружаем переменные окружения
load_dotenv()

# Значения по умолчанию (если нет .env)
DEFAULT_BOT_TOKEN = "8331610433:AAH2mZIMnT5sb_Fkt8_MusS4KAYdjzuqycI"
#DEFAULT_ADMIN_IDS = [7053160]
DEFAULT_ADMIN_IDS = [767183120,7053160]

# Пытаемся получить из .env, иначе берём дефолт
BOT_TOKEN = os.getenv("BOT_TOKEN", DEFAULT_BOT_TOKEN)

admin_env = os.getenv("ADMIN_IDS", "")
if admin_env.strip():
    ADMIN_IDS = [int(x.strip()) for x in admin_env.split(",") if x.strip()]
else:
    ADMIN_IDS = DEFAULT_ADMIN_IDS


