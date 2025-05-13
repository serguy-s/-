from database.db_manager import get_connection


class ServiceCategory:
    def __init__(self, category_code=None, name=None):
        self.category_code = category_code
        self.name = name

    def save(self):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            if self.category_code is None:
                cursor.execute('''
                    INSERT INTO service_categories (name)
                    VALUES (?)
                ''', (self.name,))
                self.category_code = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE service_categories SET 
                        name = ?
                    WHERE category_code = ?
                ''', (self.name, self.category_code))

            conn.commit()
        except Exception as e:
            print(f"Ошибка при сохранении категории услуг: {e}")
            if conn:
                conn.rollback()
            raise  # Можно убрать raise, если хотите просто логировать ошибку
        finally:
            if conn:
                conn.close()

    def delete(self):
        if not self.category_code:
            return

        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM service_categories WHERE category_code = ?",
                           (self.category_code,))
            conn.commit()
        except Exception as e:
            print(f"Ошибка при удалении категории услуг: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()


def get_all_service_categories():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service_categories")
        rows = cursor.fetchall()
        return [ServiceCategory(*row) for row in rows]
    except Exception as e:
        print(f"Ошибка при получении списка категорий услуг: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_service_category_by_code(category_code):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service_categories WHERE category_code = ?",
                       (category_code,))
        row = cursor.fetchone()
        return ServiceCategory(*row) if row else None
    except Exception as e:
        print(f"Ошибка при поиске категории услуг: {e}")
        return None
    finally:
        if conn:
            conn.close()