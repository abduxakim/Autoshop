translations = {
    # ---------- START ----------
    "welcome": {
        "ru": "Здравствуйте! Добро пожаловать в службу доставки Les Ailes 🚀",
        "en": "Hello! Welcome to Les Ailes delivery service 🚀",
        "uz": "Assalomu alaykum! Les Ailes yetkazib berish xizmatiga xush kelibsiz 🚀"
    },
    "choose_lang": {
        "ru": "🌐 Пожалуйста, выберите язык:",
        "en": "🌐 Please select a language:",
        "uz": "🌐 Iltimos, tilni tanlang:"
    },
    "share_phone": {
        "ru": "📱 Пожалуйста, поделитесь номером телефона",
        "en": "📱 Please share your phone number",
        "uz": "📱 Iltimos, telefon raqamingizni ulashing"
    },
    "reg_success": {
        "ru": "✅ Регистрация завершена!",
        "en": "✅ Registration completed!",
        "uz": "✅ Roʻyxatdan oʻtish tugallandi!"
    },

    # ---------- HELP ----------
    "help": {
        "ru": "📌 Доступные команды:\n/products — Товары\n/order — Сделать заказ\n/feedback — Отзыв\n/help — Помощь",
        "en": "📌 Available commands:\n/products — Products\n/order — Place order\n/feedback — Feedback\n/help — Help",
        "uz": "📌 Mavjud buyruqlar:\n/products — Mahsulotlar\n/order — Buyurtma berish\n/feedback — Fikr bildirish\n/help — Yordam"
    },

    # ---------- PRODUCTS ----------
    "no_products": {
        "ru": "❌ Товары отсутствуют.",
        "en": "❌ No products available.",
        "uz": "❌ Mahsulotlar mavjud emas."
    },
    "product_in_cart": {
        "ru": "✅ Добавлено в корзину!",
        "en": "✅ Added to cart!",
        "uz": "✅ Savatga qo‘shildi!"
    },
    "product_not_found": {
        "ru": "❌ Товар не найден.",
        "en": "❌ Product not found.",
        "uz": "❌ Mahsulot topilmadi."
    },

    # ---------- CART ----------
    "cart_empty": {
        "ru": "🛒 Ваша корзина пуста.",
        "en": "🛒 Your cart is empty.",
        "uz": "🛒 Savatingiz bo‘sh."
    },
    "cart_title": {
        "ru": "🛍 Ваша корзина:\n\n",
        "en": "🛍 Your cart:\n\n",
        "uz": "🛍 Savatingiz:\n\n"
    },
    "cart_total": {
        "ru": "\n💰 Итого: {total} сум.",
        "en": "\n💰 Total: {total} UZS.",
        "uz": "\n💰 Jami: {total} so‘m."
    },

    # ---------- ORDERS ----------
    "no_orders": {
        "ru": "📭 У вас ещё нет заказов.",
        "en": "📭 You don’t have any orders yet.",
        "uz": "📭 Sizda hali buyurtmalar yo‘q."
    },
    "orders_title": {
        "ru": "📜 История заказов:\n\n",
        "en": "📜 Order history:\n\n",
        "uz": "📜 Buyurtmalar tarixi:\n\n"
    },
    "order_item": {
        "ru": "🆔 Заказ {id} | 💰 {price} сум. | Статус: {status}\n",
        "en": "🆔 Order {id} | 💰 {price} UZS | Status: {status}\n",
        "uz": "🆔 Buyurtma {id} | 💰 {price} so‘m | Status: {status}\n"
    },

    # ---------- FEEDBACK ----------
    "feedback_start": {
        "ru": "💬 Напишите свой вопрос или отзыв:",
        "en": "💬 Write your question or review:",
        "uz": "💬 Savolingiz yoki sharhingizni yozing:"
    },
    "feedback_success": {
        "ru": "✅ Ваше сообщение отправлено администратору!",
        "en": "✅ Your message has been sent to the administrator!",
        "uz": "✅ Xabaringiz administratorga yuborildi!"
    }
}


def t(key: str, lang: str = "ru", **kwargs) -> str:
    """
    Получает перевод строки по ключу и языку.
    Подставляет переменные вида {var}.
    Если перевода нет — вернёт русский вариант или сам ключ.
    """
    text = translations.get(key, {}).get(lang, translations.get(key, {}).get("ru", key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
