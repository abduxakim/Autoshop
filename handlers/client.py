from aiogram import Router, F
from aiogram.types import Message, CallbackQuery , FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter,Command

from keyboards.client_kb import *
from database.client_db import *
from database.common_db import *
from loader import bot  # нужно, чтобы скачать фото
from config import ADMIN_IDS
from locales.translations import t

router = Router()


# Определяем состояния
class RegState(StatesGroup):
    phone = State()
    lang = State()
    feedback = State()

# ---------- REGISTRATION (LANG) ----------
@router.message(StateFilter(RegState.lang))
async def reg_lang(message: Message, state: FSMContext):
    lang_map = {
        "Русский 🇷🇺": "ru",
        "English 🇬🇧": "en",
        "O‘zbekcha 🇺🇿": "uz"
    }
    lang = lang_map.get(message.text)
    if not lang:
        await message.answer(
            "❌ Quyidagi tugmalardan tilni tanlang.\n\n"
            "❌ Пожалуйста, выберите язык с кнопок ниже.\n\n"
            "❌ Please select a language from the buttons below.\n"
        )
        return

    await state.update_data(lang=lang)

    # Запрос телефона
    await message.answer(
        t("share_phone", lang),
        reply_markup=get_contact_kb(lang)
    )
    await state.set_state(RegState.phone)


# ---------- REGISTRATION (PHONE) ----------
@router.message(F.contact, StateFilter(RegState.phone))
async def reg_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    phone = message.contact.phone_number

    save_user(message.from_user, phone, lang)

    await message.answer(
        t("reg_success", lang),
        reply_markup=get_main_menu_kb(lang)
    )
    await state.clear()


# ---------- PRODUCTS ----------
@router.message(F.text == "🛍 Заказать")
async def show_products(message: Message):
    user = get_user_by_id(message.from_user.id)
    lang = user.get("lang", "ru") if user else "ru"

    products = get_all_products()
    if not products:
        await message.answer(t("no_products", lang))
        return

    #TODO после нажатие Заказать сделать список товаров используя ReplyKeyboardMarkup and KeyboardButton
    for p in products:
        text = f"📦 {p['name']}\n💰 {p['price']} сум.\n{p['description']}"
        kb = InlineKeyboardBuilder()
        kb.button(text="🛒 В корзину", callback_data=f"add_cart:{p['id']}")
        await message.answer_photo(
            photo=open(p["photo_path"], "rb"),
            caption=text,
            reply_markup=kb.as_markup()
        )


# ---------- ADD TO CART ----------
@router.callback_query(F.data.startswith("add_cart"))
async def add_to_cart_handler(callback: CallbackQuery):
    user = get_user_by_id(callback.from_user.id)
    user_id = callback.from_user.id
    lang = user.get("lang", "ru") if user else "ru"

    product_id = int(callback.data.split(":")[1])
    product = next((p for p in get_all_products() if p["id"] == product_id), None)

    if not product:
        await callback.answer(t("product_not_found", lang), show_alert=True)
        return

    order = get_pending_order(user_id)
    order_id = order["id"] if order else create_order(user_id)

    add_to_cart(order_id, product_id, 1, product["price"])
    await callback.answer(t("product_in_cart", lang))


# ---------- CART ----------
@router.message(F.text == "/order")
async def show_cart(message: Message):
    user = get_user_by_id(message.from_user.id)
    lang = user.get("lang", "ru") if user else "ru"

    order = get_pending_order(message.from_user.id)
    if not order:
        await message.answer(t("cart_empty", lang))
        return

    items = get_cart(order["id"])
    if not items:
        await message.answer(t("cart_empty", lang))
        return

    text = t("cart_title", lang)
    total = 0
    for item in items:
        text += f"📦 {item['name']} — {item['quantity']} × {item['price']} = {item['subtotal']} сум.\n"
        total += item["subtotal"]

    text += t("cart_total", lang, total=total)
    await message.answer(text)


# ---------- MY ORDERS ----------
@router.message(F.text == "📖 Мои заказы")
async def my_orders(message: Message):
    user = get_user_by_id(message.from_user.id)
    lang = user.get("lang", "ru") if user else "ru"

    orders = get_user_orders(message.from_user.id)
    if not orders:
        await message.answer(t("no_orders", lang))
        return

    text = t("orders_title", lang)
    for order in orders:
        text += t("order_item", lang, id=order['id'], price=order['total_price'], status=order['status'])
    await message.answer(text)


# ---------- FEEDBACK ----------
@router.message(F.text == "☎️ Обратная связь")
async def feedback_start(message: Message, state: FSMContext):
    user = get_user_by_id(message.from_user.id)
    lang = user.get("lang", "ru") if user else "ru"

    await message.answer(t("feedback_start", lang))
    await state.set_state(RegState.feedback)


@router.message(StateFilter(RegState.feedback))
async def feedback_save(message: Message, state: FSMContext):
    user = get_user_by_id(message.from_user.id)
    lang = user.get("lang", "ru") if user else "ru"

    save_feedback(message.from_user.id, message.text)
    await message.answer(t("feedback_success", lang))
    await state.clear()


