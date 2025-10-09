from aiogram.types import (ReplyKeyboardMarkup , KeyboardButton , KeyboardButtonPollType,
                            InlineKeyboardMarkup, InlineKeyboardButton)
#from aiogram.types import  KeyboardButtonPollType for enchanced version 
#BUILDER
from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
from database.admin_db.categories_db import get_categories
from database.admin_db.car_brands_db import    get_car_brands
from keyboards.admin_kb.admin_kb import back_button  


# Меню действий с категориями (отсюда — в список категорий или добавить)
def get_category_action_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
             [
                KeyboardButton(text="📂 Показать категории товаров"),
                KeyboardButton(text="➕ Добавить категорию"),
            ],
            [back_button()]  # видимая кнопка Назад
        ],
        resize_keyboard=True
    )


# Список категорий через inline
# Универсальный список категорий (choose | delete | update)
def build_categories_kb(action="choose", lang="ru"):
    """
    action: choose | delete | update | manage
    choose  -> просто список категорий (для выбора)
    manage  -> список категорий + кнопки ✏ и 🗑 справа от каждой
    delete  -> список категорий (по клику удаляем)
    update  -> список категорий (по клику обновляем)
    """
    categories = get_categories()
    if not categories:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Нет категорий", callback_data="noop")]]
        )

    keyboard = []

    if action == "manage":
        # 📂 Категория + ✏ и 🗑 в одной строке
        for cat in categories:
            text = cat.get(f"name_{lang}", cat["name_ru"])
            keyboard.append([
                InlineKeyboardButton(text=f"📂 {text}", callback_data="noop"),
                InlineKeyboardButton(text="✏", callback_data=f"update_cat:{cat['id']}"),
                InlineKeyboardButton(text="🗑", callback_data=f"delete_cat:{cat['id']}")
            ])
    else:
        # Остальные режимы — компактно по 2 в ряд
        row = []
        for i, cat in enumerate(categories, start=1):
            text = cat.get(f"name_{lang}", cat["name_ru"])

            if action == "choose":
                row.append(InlineKeyboardButton(text=text, callback_data=f"choose_cat:{cat['id']}"))
            elif action == "delete":
                row.append(InlineKeyboardButton(text=text, callback_data=f"delete_cat:{cat['id']}"))
            elif action == "update":
                row.append(InlineKeyboardButton(text=text, callback_data=f"update_cat:{cat['id']}"))

            if i % 2 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)

    # Добавляем "Назад" или "Отмена"
    if action == "choose":
        keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back:categories")])
    else:
        keyboard.append([InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel_{action}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_post_delete_kb(lang="ru"):
    """
    Клавиатура после удаления категории:
    показывает оставшиеся категории без кнопки 'Отмена',
    добавляет 'Назад', если список не пуст.
    """
    categories = get_categories()
    if not categories:
        return None

    keyboard = []
    for cat in categories:
        text = cat.get(f"name_{lang}", cat["name_ru"])
        keyboard.append([InlineKeyboardButton(text=text, callback_data=f"delete_cat:{cat['id']}")])

    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back:categories")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_confirm_delete_kb(cat_id: int, lang="ru"):
    """Клавиатура подтверждения удаления категории"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete:{cat_id}"),
                InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_delete")
            ]
        ]
    )






#Выбор языка обновления категории
def update_category_choose_lang_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="update_lang:ru"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="update_lang:en"),
                InlineKeyboardButton(text="🇺🇿 O‘zbek", callback_data="update_lang:uz"),
            ],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_update")]
        ]
    )