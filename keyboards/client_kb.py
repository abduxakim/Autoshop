from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database.common_db import *

# Тексты для разных языков
MENU_TEXTS = {
    "ru": {
        "order": "🛍 Заказать",
        "my_orders": "📖 Мои заказы",
        "settings": "⚙️ Настройки",
        "info": "ℹ️ Информация",
        "feedback": "☎️ Обратная связь",
        "back": "⬅️ Назад",
        "send_phone": "📲 Отправить номер",
        "change_name": "✏️ Сменить имя",
        "change_lang": "🇷🇺 Изменить язык",
        "change_phone": "📱 Сменить номер",

        # Категории
        "category_paints": "🎨 Моральные изделия",
        "category_bumpers": "🚗 Бамперы",

        # Бренды
        "brand_chevrolet": "Chevrolet",
        "brand_daewoo": "Daewoo"
    },
    "en": {
        "order": "🛍 Order",
        "my_orders": "📖 My Orders",
        "settings": "⚙️ Settings",
        "info": "ℹ️ Info",
        "feedback": "☎️ Feedback",
        "back": "⬅️ Back",
        "send_phone": "📲 Send phone number",
        "change_name": "✏️ Change name",
        "change_lang": "🇬🇧 Change language",
        "change_phone": "📱 Change phone",

        # Categories
        "category_paints": "🎨 Paint Materials",
        "category_bumpers": "🚗 Bumpers",

        # Brands
        "brand_chevrolet": "Chevrolet",
        "brand_daewoo": "Daewoo"
    },
    "uz": {
        "order": "🛍 Buyurtma berish",
        "my_orders": "📖 Mening buyurtmalarim",
        "settings": "⚙️ Sozlamalar",
        "info": "ℹ️ Ma’lumot",
        "feedback": "☎️ Fikr bildirish",
        "back": "⬅️ Orqaga",
        "send_phone": "📲 Telefon raqam yuborish",
        "change_name": "✏️ Ismni o‘zgartirish",
        "change_lang": "🇺🇿 Tilni o‘zgartirish",
        "change_phone": "📱 Raqamni o‘zgartirish",

        # Kategoriyalar
        "category_paints": "🎨 Bo‘yoq materiallari",
        "category_bumpers": "🚗 Bamperlar",

        # Brendlar
        "brand_chevrolet": "Chevrolet",
        "brand_daewoo": "Daewoo"
    }
}


# Главное меню (в зависимости от языка)
def get_main_menu_kb(lang="ru"):
    t = MENU_TEXTS[lang]
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["order"]), KeyboardButton(text=t["my_orders"])],
            [KeyboardButton(text=t["settings"]), KeyboardButton(text=t["info"])],
            [KeyboardButton(text=t["feedback"])]
        ],
        resize_keyboard=True
    )
    return kb


# Меню настроек
def get_setting_menu(lang="ru"):
    t = MENU_TEXTS[lang]
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["change_name"]), KeyboardButton(text=t["change_lang"])],
            [KeyboardButton(text=t["change_phone"]), KeyboardButton(text=t["back"])]
        ],
        resize_keyboard=True
    )
    return kb


# Выбор языка
def get_lang_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Русский 🇷🇺")],
            [KeyboardButton(text="English 🇬🇧")],
            [KeyboardButton(text="O‘zbekcha 🇺🇿")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return kb


# Запрос телефона
def get_contact_kb(lang="ru"):
    t = MENU_TEXTS[lang]
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["back"])],
            [KeyboardButton(text=t["send_phone"], request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return kb


# Ввод имени
def get_name_kb(lang="ru"):
    t = MENU_TEXTS[lang]
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t["back"])]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return kb

#Зделать заказ
def get_product_order(lang="ru"):
    t = MENU_TEXTS[lang]
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("")),KeyboardButton(text=t(""))],
            [KeyboardButton(text=t("back"))]
                
        ],
        resize_keyboard=True,
        one_time_keyboard=True          
    )
    return kb

# Выбор категории товаров
def get_category_menu(lang="ru"):
    category = get_categories()

    keyboard = []
    row = []

    for i,category in enumerate(category,start=1):
        text=category[f"name_{lang}"]
        row.append(KeyboardButton(text=text))

        if i%2==0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([KeyboardButton(text="⬅️ Назад")])

    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
    



# Выбор бренда (например, для бамперов)
def get_brand_menu(lang="ru"):
    brands = get_brands()

    keyboard = []
    row = []
    for i, brand in enumerate(brands, start=1):
        # Динамический выбор названия в зависимости от языка
        text = brand[f"name_{lang}"] # берем название бренда на нужном языке и Создаём кнопку с этим текстом 
        row.append(KeyboardButton(text=text)) # Добавляем кнопку в текущую строку row

        # каждые 2 кнопки → новая строка
        if i % 2 == 0:
            keyboard.append(row)
            row = []

    if row:  # если осталась "лишняя" кнопка
        keyboard.append(row)

    # кнопка Назад
    keyboard.append([KeyboardButton(text="⬅️ Назад")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
