from database.common_db import get_connection


# Добавить модель авто
def add_car_models(car_brand_id, name):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO car_models (car_brand_id, name) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (car_brand_id, name))
        print(f"✅ Добавлена модель авто: {name} (brand_id={car_brand_id})")
        conn.commit()
    except Exception as e:
        print("❌ Ошибка при добавлении car_model:", e)
    finally:
        cursor.close()
        conn.close()


# Получить все модели по бренду
def get_car_models_by_brand(car_brand_id):   # обязательно нужен аргумент
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT id, name FROM car_models WHERE car_brand_id = %s ORDER BY name"
    try:
        cursor.execute(sql, (car_brand_id,))
        return cursor.fetchall()
    except Exception as e:
        print("❌ Ошибка при получении моделей:", e)
        return []
    finally:
        cursor.close()
        conn.close()