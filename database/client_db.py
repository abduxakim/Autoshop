import mysql.connector


# Функция подключения к базе
# TODO: вынести параметры в .env и создать отдельного пользователя вместо root
# TODO: позже вынести эти данные в .env (через python-dotenv)
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,  
        user="root",
        password="Loki200528MySQL!",
        database="shop_db",
        charset='utf8mb4'
    )



# -----------------------------
# Работа с пользователями
# -----------------------------

def save_user(user, phone, language):
    """
    Сохранить или обновить пользователя.
    Если такой id уже есть → обновляем phone и language.
    """
    conn = get_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO users (id, username, phone, language)
             VALUES (%s, %s, %s, %s)
             ON DUPLICATE KEY UPDATE phone=%s, language=%s"""
    cursor.execute(sql, (user.id, user.username, phone, language, phone, language))
    conn.commit()
    cursor.close()
    conn.close()


def get_user_by_id(user_id):
    """ Получить данные пользователя по ID. """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


# -----------------------------
# Работа с заказами и корзиной
# -----------------------------

def get_pending_order(user_id):
    """ Получить активный (неоформленный) заказ пользователя. """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE user_id=%s AND status='pending'", (user_id,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()
    return order


def create_order(user_id):
    """ Создать новый заказ со статусом pending. """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (user_id, total_price, status) VALUES (%s, 0.00, 'pending')",
        (user_id,)
    )
    order_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return order_id


def add_to_cart(order_id, product_id, quantity, price):
    """
    Добавить товар в корзину.
    subtotal = quantity * price.
    Также обновляем total_price заказа.
    """
    subtotal = quantity * price
    conn = get_connection()
    cursor = conn.cursor()

    # Добавляем позицию в корзину
    sql = """INSERT INTO order_items (order_id, product_id, quantity, price, subtotal)
             VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(sql, (order_id, product_id, quantity, price, subtotal))

    # Обновляем total_price в заказе
    cursor.execute("UPDATE orders SET total_price = total_price + %s WHERE id=%s", (subtotal, order_id))

    conn.commit()
    cursor.close()
    conn.close()


def get_cart(order_id):
    """
    Получить все товары в корзине по order_id.
    Возвращает список словарей: id, name, quantity, price, subtotal.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT oi.id, p.name, oi.quantity, oi.price, oi.subtotal
             FROM order_items oi
             JOIN products p ON oi.product_id = p.id
             WHERE oi.order_id=%s"""
    cursor.execute(sql, (order_id,))
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items


def clear_cart(order_id):
    """
    Очистить корзину (удалить товары).
    Также сбросить total_price в заказе.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM order_items WHERE order_id=%s", (order_id,))
    cursor.execute("UPDATE orders SET total_price = 0 WHERE id=%s", (order_id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_user_orders(user_id):
    """
    Получить историю заказов пользователя (кроме pending).
    Возвращает список заказов с товарами внутри.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Получаем заказы
    cursor.execute(
        "SELECT * FROM orders WHERE user_id=%s AND status!='pending' ORDER BY created_at DESC",
        (user_id,)
    )
    orders = cursor.fetchall()

    # Для каждого заказа получаем товары
    for order in orders:
        cursor.execute(
            """SELECT p.name, oi.quantity, oi.price, oi.subtotal
               FROM order_items oi
               JOIN products p ON oi.product_id = p.id
               WHERE oi.order_id=%s""",
            (order["id"],)
        )
        order["items"] = cursor.fetchall()

    cursor.close()
    conn.close()
    return orders


# -----------------------------
# Работа с отзывами
# -----------------------------

def save_feedback(user_id, text):
    """ Сохранить отзыв пользователя. """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (user_id, message) VALUES (%s, %s)", (user_id, text))
    conn.commit()
    cursor.close()
    conn.close()
