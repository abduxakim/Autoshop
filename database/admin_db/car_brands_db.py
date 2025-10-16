from database.common_db import get_connection



# ===================================================
#   Получить список брендов
# ===================================================
def get_car_brands():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # ✅ теперь словари
    sql = "SELECT id, name FROM car_brands ORDER BY id"
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print("❌ Ошибка при получении car_brands:", e)
        return []
    finally:
        cursor.close()
        conn.close()
        
# ===================================================
#   Обновить бренд
# ===================================================
def update_car_brands(brand_id:int, new_name:str):
    conn = get_connection()
    cursor = conn.cursor()
    sql =  "UPDATE car_brands SET name=%s WHERE id=%s"

    try:
        cursor.execute(sql,(new_name,brand_id))
        conn.commit()
        print(f"✅ Бренд авто обновлен на: {new_name} где id={brand_id}")
    except Exception as e:
        print("❌ Ошибка при обновлении car_brands:", e)
        return []
    finally:
        cursor.close()
        conn.close()



# ===================================================
#   Удалить бренд
# ===================================================
def delete_car_brands(brand_id:int,old_name:str):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM car_brands WHERE id=%s"
    try:
        cursor.execute(sql,(brand_id,))
        conn.commit()
        print(f"✅ Бренд авто был удален:{old_name} где id={brand_id}")
    except Exception as e:
        print("❌ Ошибка при удалении car_brands:", e)
        return []
    finally:
        cursor.close()
        conn.close()


# ===================================================
#   Добавить новый бренд
# ===================================================
def add_car_brands(name):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO car_brands (name)
    VALUES(%s)
    """
    try:
        cursor.execute(sql, (name,)) # так как это tuple name,
        print(f"✅Добавлен бренд авто: {name}")
        conn.commit()
        print("Данные зафиксированы в базе")
    except Exception as e:
        print("❌ Ошибка при добавлении категории:", e)
    finally:
        cursor.close()
        conn.close()

