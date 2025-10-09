from database.common_db import get_connection

#Получить список категорий
def get_categories():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # возвращаем dict вместо tuple
    sql = """
    SELECT id, name_ru, name_en, name_uz
    FROM categories
    ORDER BY id
    """
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows  # достаточно просто вернуть rows
    except Exception as e:
        print("❌ Ошибка при получении категорий:", e)
        return [] # при ошибке тоже возвращаем пустой список
    finally:
        cursor.close()
        conn.close()

#Добавить категорию
def add_category(name_ru,name_en,name_uz):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO categories (name_ru,name_en,name_uz)
    VALUES(%s, %s, %s)
    """
    try:
        cursor.execute(sql,(name_ru,name_en,name_uz))
        print(f"✅ Категория добавлена: {name_ru} / {name_en} / {name_uz}")
        conn.commit()
        print("Данные зафиксированы в базе")
    except Exception as e:
        print("❌ Ошибка при добавлении категории:", e)
    finally:
        cursor.close()
        conn.close()

def delete_category(category_id,name_ru):
    conn =  get_connection()
    cursor = conn.cursor()
    sql = """
    DELETE FROM categories WHERE id = %s
    """
    try:
        cursor.execute(sql, (category_id,))
        conn.commit()
        print(f"✅ Категория была удалена: {name_ru} (id={category_id})")
    except Exception as e:
        print("❌ Ошибка при удалении категории:", e)
    finally:
        cursor.close()
        conn.close()


def update_category_field(category_id: int, lang: str, new_name: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    field_map = {"ru": "name_ru", "en": "name_en", "uz": "name_uz"}
    field = field_map.get(lang)
    if not field:
        print("❌ Ошибка: неверный язык для обновления")
        return False

    sql = f"UPDATE categories SET {field} = %s WHERE id = %s"
    try:
        cursor.execute(sql, (new_name, category_id))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ Категория {category_id} обновлена: {field} = {new_name}")
            return True
        else:
            print(f"⚠️ Категория ID {category_id} не найдена.")
            return False
    except Exception as e:
        print("❌ Ошибка при обновлении категории:", e)
        return False
    finally:
        cursor.close()
        conn.close()

