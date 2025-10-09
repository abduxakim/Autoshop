from aiogram.types import (ReplyKeyboardMarkup , KeyboardButton , KeyboardButtonPollType,
                            InlineKeyboardMarkup, InlineKeyboardButton)
#from aiogram.types import  KeyboardButtonPollType for enchanced version 
#BUILDER
from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
from database.admin_db.categories_db import get_categories
from database.admin_db.car_brands_db import    get_car_brands
    

# ---- visible-only back button (user sees only "⬅️ Назад") ----
def back_button() -> KeyboardButton:
    """Кнопка Назад (видимая часть) — без технических меток."""
    return KeyboardButton(text="⬅️ Назад")


# Главное меню
def get_admin_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Товары"), KeyboardButton(text="🛒 Заказы")],
            [KeyboardButton(text="📨 Сообщения"), KeyboardButton(text="👥 Пользователи")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="⚙️ Настройки")]
        ],
        resize_keyboard=True
    )









# Кнопки для ответа на feedback
def get_feedback_reply_kb(user_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍ Ответить", callback_data=f"reply_feedback:{user_id}")]
    ])
    return kb


# Кнопки со списком товаров
def get_products_kb(product_list):
    buttons = []
    for p in product_list:
        buttons.append([
            InlineKeyboardButton(
                text=f"✏ {p['name']}",  # имя товара
                callback_data=f"view_product:{p['id']}"  # ID товара
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)



# Кнопки для действий с товаром
def get_product_actions_kb(product_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏ Изменить", callback_data=f"choose_edit_field:{product_id}")],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_product:{product_id}")]
    ])
    return kb


# --- Кнопки для выбора параметра ---
def get_update_fields_kb(product_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📛 Название", callback_data=f"edit_name:{product_id}")],
        [InlineKeyboardButton(text="📝 Описание", callback_data=f"edit_desc:{product_id}")],
        [InlineKeyboardButton(text="💰 Цена", callback_data=f"edit_price:{product_id}")],
        [InlineKeyboardButton(text="📦 Количество", callback_data=f"edit_qty:{product_id}")],
        [InlineKeyboardButton(text="🖼 Фото", callback_data=f"edit_photo:{product_id}")]
    ])
    return kb
