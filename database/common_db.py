import mysql.connector
import os
from dotenv import load_dotenv 
from contextlib import contextmanager

load_dotenv()


# TODO: вынести подключение в отдельный конфиг (.env)
# TODO: позже вынести эти данные в .env (через python-dotenv)
def get_connection():
    """Создаёт соединение с MySQL, используя данные из .env"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        use_unicode=True,
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci"
    )

# Контекстный менеджер для удобной работы с курсором
@contextmanager
def get_cursor(dictionary=True):
    conn = get_connection()
    cursor = conn.cursor(dictionary=dictionary)
    try:
        yield cursor
        conn.commit()
    finally:
        cursor.close()
        conn.close()




"""def get_brands():
    #TODO this
    #conn = mysql.connector.connect(**DB_CONFIG)
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name_ru, name_en, name_uz FROM brands")
        return cursor.fetchall()
    finally:
        conn.close()


def get_categories():
    #TODO this
    #conn = mysql.connector.connect(**DB_CONFIG)
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name_ru, name_en, name_uz FROM categories")
        return cursor.fetchall()
    finally:
        conn.close()

# -----------------------------
# Работа с товарами (общая)
# -----------------------------

def get_all_products(lang='ru'):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(""
        SELECT id, price, quantity, photo_path,
               name_ru, name_en, name_uz,
               description_ru, description_en, description_uz,
               category_id, subcategory_id, brand_id, car_model_id
        FROM products
    "")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    products = []
    for r in rows:
        name = r.get(f"name_{lang}") or r["name_ru"]
        desc = r.get(f"description_{lang}") or r["description_ru"]
        products.append({
            "id": r["id"],
            "name": name,
            "description": desc,
            "price": float(r["price"]),
            "qty": r["quantity"],
            "photo_path": r["photo_path"],
            "category_id": r["category_id"],
            "brand_id": r["brand_id"],
            "car_model_id": r["car_model_id"]
        })
    return products



#функцию для получения одного товара
def get_product_by_id(product_id):
    ""
    Получить один товар по ID.
    Удобно для корзины, редактирования и т.д.
    ""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, price, quantity, photo_path FROM products WHERE id=%s", (product_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "qty": row[4],             
            "photo_path": row[5]
        }
    return None"""

