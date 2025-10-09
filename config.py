import os
from dotenv import load_dotenv

# === Загружаем переменные окружения ===
load_dotenv()

# === Telegram Bot Configuration ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# === Безопасность: проверяем важные переменные ===
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Добавьте его в файл .env")

if not ADMIN_IDS:
    print("⚠️ ADMIN_IDS не заданы. Рекомендуется указать хотя бы одного администратора.")

# === Необязательный красивый вывод при запуске ===
def print_config_summary():
    """Вывод краткой информации при старте (без токена)."""
    print("✅ Config loaded successfully!")
    print(f"Admins: {ADMIN_IDS}")
    print(f"Bot token: {'***' + BOT_TOKEN[-5:] if BOT_TOKEN else 'MISSING'}")

# Вызываем при импорте
print_config_summary()
