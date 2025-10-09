from aiogram.types import (ReplyKeyboardMarkup , KeyboardButton , KeyboardButtonPollType,
                            InlineKeyboardMarkup, InlineKeyboardButton)
#from aiogram.types import  KeyboardButtonPollType for enchanced version 
#BUILDER
from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
from database.admin_db.categories_db import get_categories
from database.admin_db.car_brands_db import    get_car_brands
from keyboards.admin_kb.admin_kb import back_button 


# Список car brands
def get_car_brands_kb(name_field="name"):
    brands = get_car_brands()

    keyboard = []
    row = []
    for i, brand in enumerate(brands, start=1):
        text = brand.get(name_field, brand.get("name"))
        row.append(KeyboardButton(text=text))
        if i % 2 == 0:
            keyboard.append(row); row = []
    if row:
        keyboard.append(row)

    keyboard.append([back_button()])  # вернёмся в categories (логика в handler)
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# 🚘 Меню действий с брендами авто (отсюда — в список брендов или добавить)
def get_car_brands_action_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📂 Показать бренды авто", callback_data="show_brands")],
            [InlineKeyboardButton(text="➕ Добавить бренд авто", callback_data="add_brand")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back:categories")]
        ]
    )

