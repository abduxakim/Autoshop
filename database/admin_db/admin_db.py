"""
# Добавить товар
def add_product(name, desc, price, qty, photo_path):
    conn = get_connection()
    cursor = conn.cursor()
    sql = ""
    INSERT INTO products (name, description, price, quantity, photo_path)
    VALUES (%s, %s, %s, %s, %s)
    ""
    try:
        cursor.execute(sql, (name, desc, price, qty, photo_path))
        print("Сохраняем в базу:", name, desc, price, qty, photo_path)
        print("Добавлено строк:", cursor.rowcount)
        conn.commit()
        print("Данные зафиксированы в базе")
    except Exception as e:
        print("Ошибка при вставке:", e)
    finally:
        cursor.close()
        conn.close()

#функцию для получения одного товара
def get_product_by_id(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, description, price, quantity, photo_path FROM products WHERE id=%s",
        (product_id,)
    )
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
    return None



# Удалить товар
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()

#Изменить товар 
# Изменить все поля товара сразу
def update_product(product_id, name, description, price, qty, photo_path):
    conn = get_connection()
    cursor = conn.cursor()
    sql = ""
    UPDATE products
    SET name=%s, description=%s, price=%s, quantity=%s, photo_path=%s
    WHERE id=%s
    ""
    cursor.execute(sql, (name, description, price, qty, photo_path, product_id))
    conn.commit()
    cursor.close()
    conn.close()

"""
