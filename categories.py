import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Добавляем еще один уровень вверх, если database на том же уровне, что models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.db_manager import get_connection

class ServiceCategory:
    def __init__(self, category_code=None, name=None):
        self.category_code = category_code
        self.name = name

    def save(self):
        """Добавляет новую категорию услуг или обновляет существующую."""
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
        conn.close()

    def delete(self):
        """Удаляет категорию услуг."""
        if self.category_code is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM service_categories WHERE category_code = ?",
                           (self.category_code,))
            conn.commit()
            conn.close()

# Вспомогательные функции
def get_all_service_categories():
    """Возвращает все категории услуг."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM service_categories")
    rows = cursor.fetchall()
    conn.close()
    return [
        ServiceCategory(
            category_code=row[0],
            name=row[1]
        ) for row in rows
    ]

def get_service_category_by_code(category_code):
    """Возвращает категорию услуг по коду категории."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM service_categories WHERE category_code = ?",
                   (category_code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return ServiceCategory(
            category_code=row[0],
            name=row[1]
        )
    return None