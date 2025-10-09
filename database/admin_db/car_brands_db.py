from database.common_db import get_connection



# Получить все бренды авто
def get_car_brands():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # ✅ теперь словари
    sql = "SELECT id, name FROM car_brands ORDER BY name"
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print("❌ Ошибка при получении car_brands:", e)
        return []
    finally:
        cursor.close()
        conn.close()


#добавить марку авто.
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

