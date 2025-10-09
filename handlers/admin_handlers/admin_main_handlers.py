import os
from aiogram import  F
from aiogram.filters import Command 
from aiogram.types import Message, CallbackQuery
from config import ADMIN_IDS

from aiogram.fsm.context import FSMContext 

from collections import defaultdict

from keyboards.admin_kb.categories_kb import *
from keyboards.admin_kb.car_brands_kb import *
from keyboards.admin_kb.admin_kb import *

from loader import bot  # нужно, чтобы скачать фото
from aiogram import Router
from locales.help_texts import *

# Пер-юзер "стек возврата".
# В продакшне можно хранить в redis/DB, но для простоты — в памяти:
BACK_STACKS = defaultdict(list)

BACK_ROUTES = {
    "categories": build_categories_kb,
    "brands": lambda: get_car_brands_kb("name"),
    "main": get_admin_main_menu,
    "action_categories": get_category_action_kb,
}

admin_main_router = Router()



# --- 1. /help ---
@admin_main_router.message(Command("help"))
async def cmd_help(message: Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer(HELP_ADMIN)
    else:
        await message.answer(HELP_CLIENT)

# Админ выбрал "📦 Товары" -> показываем действия с категориями
@admin_main_router.message(F.text == "📦 Товары")
async def show_products_menu(message: Message):
    user = message.from_user.id
    # при входе в меню действий: родитель = main
    BACK_STACKS[user].append("main")
    await message.answer("Что хотите сделать с категориями?", reply_markup=get_category_action_kb())



# Универсальный обработчик "Назад" (видит пользователь только "⬅️ Назад")
@admin_main_router.message(F.text == "⬅️ Назад")
async def go_back(message: Message, state: FSMContext):
    user = message.from_user.id

    # очищаем FSM (если есть активное состояние)
    if await state.get_state() is not None:
        await state.clear()

    # получаем целевой маршрут из стека (pop). Если стека нет — main
    if BACK_STACKS[user]:
        target = BACK_STACKS[user].pop()
    else:
        target = "main"

    # если стек стал слишком большим (на худой конец) — можно обрезать, но не обязательно
    # DEBUG: можно логировать BACK_STACKS[user]

    # берем функцию-генератор клавиатуры (по умолчанию — главное меню)
    kb_func = BACK_ROUTES.get(target, BACK_ROUTES["main"])
    await message.answer("Возврат назад", reply_markup=kb_func())

@admin_main_router.callback_query(F.data.startswith("back:"))
async def go_back_inline(callback: CallbackQuery, state: FSMContext):
    user = callback.from_user.id
    target = callback.data.split(":")[1]

    # очищаем FSM
    if await state.get_state() is not None:
        await state.clear()

    kb_func = BACK_ROUTES.get(target, BACK_ROUTES["main"])

    try:
        await callback.message.delete() # удаляем старое сообщение тоесть InlineKeyboardMarkup
        await callback.message.answer(
            f"↩️ Возврат в {target}",
            reply_markup=get_category_action_kb()
        )
    except Exception as e:
        # если "message is not modified"
        if "message is not modified" in str(e):
            # удаляем сообщение и отправляем новое
            await callback.message.delete()
            await callback.message.answer(
                f"↩️ Возврат в {target}",
                reply_markup=kb_func()
            )
        else:
            raise
    await callback.answer()








"""adding_products = {}

# Папка для фото
IMAGE_DIR = "product_images"
os.makedirs(IMAGE_DIR, exist_ok=True)


# --- Временное "хранилище" (имитация БД) ---
products = {}  # id: {"name": str, "desc": str, "photo": str, "price": float, "qty": int}
orders = []  # список заказов
feedbacks = {}
users = set()
"""

'''
# --- 3. Добавление товара ---
@router.message(Command("add_product"))
async def cmd_add_product(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(
        "📸 Отправьте фото товара с подписью в формате:\n"
        "`название;описание;цена;количество`\n\n"
        "Пример:\n`Monster Energy;Энергетический напиток;123.45;10`",
        parse_mode="Markdown"
    )


# ---  Обработка шагов и отправка фото ---
@router.message(F.photo, F.from_user.id.in_(ADMIN_IDS))
async def handle_product_photo(message: Message):
     # 1. Проверка на фото
    if not message.photo:
        await message.answer("❌ Нужно отправить фото товара с подписью!")
        return

    # Проверяем наличие подписи
    if not message.caption:
        await message.answer(
            "❌ Добавьте подпись в формате:\n"
            "`название;описание;цена;количество`",
            parse_mode="Markdown"
        )
        return

    # Разбираем данные
    try:
        name, description, price, quantity = message.caption.split(";")
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        await message.answer(
            "❌ Неверный формат!\nПример:\n"
            "`Monster Energy;Энергетический напиток;123.45;10`",
            parse_mode="Markdown"
        )
        return

    # Скачиваем фото
    file_id = message.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    filename = f"{name.strip().replace(' ', '_')}.jpg"
    local_path = os.path.join(IMAGE_DIR, filename)
    await bot.download_file(file_info.file_path, local_path)

    # Сохраняем в базу
    add_product(name.strip(), description.strip(), price, quantity, local_path)

    await message.answer(f"✅ Товар *{name.strip()}* успешно добавлен!", parse_mode="Markdown")



# --- 7. Просмотр заказов ---
@router.message(Command("orders"))
async def show_orders(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    if not orders:
        await message.answer("📭 Заказов пока нет.")
        return

    text = "📦 Заказы:\n\n"
    for o in orders:
        text += f"👤 {o['user']} | 📦 {o['product']} x{o['qty']} | 📞 {o['phone']}\n"
    await message.answer(text)

# --- 8. Рассылка ---
@router.message(Command("broadcast"))
async def start_broadcast(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    products["_broadcast"] = True
    await message.answer("Введите текст для рассылки:")

@router.message(F.from_user.id.in_(ADMIN_IDS))
async def process_broadcast(message: Message):
    if products.get("_broadcast"):
        for uid in users:
            await message.bot.send_message(uid, message.text)
        products.pop("_broadcast", None)
        await message.answer("✅ Рассылка завершена.")

# --- 9. Статистика ---
@router.message(Command("stats"))
async def show_stats(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    total_sales = sum(o.get("total", 0) for o in orders)
    await message.answer(
        f"📊 Статистика:\n"
        f"👥 Пользователей: {len(users)}\n"
        f"📦 Заказов: {len(orders)}\n"
        f"💰 Общая сумма продаж: {total_sales} ₽"
    )

# --- 10. Feedback (как раньше) ---
@router.message(F.text.startswith("/feedback_from_user"))
async def receive_feedback(message: Message):
    try:
        parts = message.text.split(" ", 3)
        user_id = int(parts[1])
        username = parts[2]
        feedback_text = parts[3]

        feedbacks[user_id] = {"username": username, "text": feedback_text}

        await message.answer(
            f"📩 Новый отзыв от @{username} (ID: {user_id}):\n\n"
            f"{feedback_text}",
            reply_markup=get_feedback_reply_kb(user_id)
        )
    except Exception as e:
        await message.answer(f"⚠ Ошибка обработки отзыва: {e}")


@router.callback_query(F.data.startswith("reply_feedback:"))
async def process_reply_button(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    feedbacks["_reply_to"] = user_id
    await callback.message.answer(f"✏ Введите ответ для пользователя ID: {user_id}")
    await callback.answer()

@router.message(F.from_user.id.in_(ADMIN_IDS))
async def send_admin_reply(message: Message):
    if "_reply_to" in feedbacks:
        user_id = feedbacks["_reply_to"]
        reply_text = message.text
        await message.bot.send_message(user_id, f"📬 Ответ от администратора:\n{reply_text}")
        await message.answer("✅ Ответ отправлен.")
        del feedbacks["_reply_to"]

'''

