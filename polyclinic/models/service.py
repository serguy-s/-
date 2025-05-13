from database.db_manager import get_connection
class Service:
    def __init__(self, service_code=None, category_code=None, name=None, description=None, price=None):
        self.service_code = service_code
        self.category_code = category_code
        self.name = name
        self.description = description
        self.price = price
    def save(self):
        """Сохраняет услугу в базу данных с обработкой ошибок"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            if self.service_code is None:
                cursor.execute('''
                    INSERT INTO services 
                    (category_code, name, description, price)
                    VALUES (?, ?, ?, ?)
                ''', (self.category_code, self.name, self.description, self.price))
                self.service_code = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE services SET 
                        category_code = ?,
                        name = ?,
                        description = ?,
                        price = ?
                    WHERE service_code = ?
                ''', (self.category_code, self.name, self.description, self.price, self.service_code))
            conn.commit()
            return True
        except Exception as e:
            print(f"⛔ Ошибка при сохранении услуги: {str(e)}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
    def delete(self):
        """Удаляет услугу из базы данных с обработкой ошибок"""
        if not self.service_code:
            return False
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM services WHERE service_code = ?",
                           (self.service_code,))
            conn.commit()
            return True
        except Exception as e:
            print(f"⛔ Ошибка при удалении услуги: {str(e)}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
def get_all_services():
    """Получает список всех услуг с обработкой ошибок"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT service_code, category_code, name, description, price 
            FROM services
            ORDER BY name
        """)
        return [Service(*row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"⛔ Ошибка при получении списка услуг: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()
def get_service_by_code(service_code):
    """Находит услугу по коду с обработкой ошибок"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT service_code, category_code, name, description, price 
            FROM services 
            WHERE service_code = ?
        """, (service_code,))
        row = cursor.fetchone()
        return Service(*row) if row else None
    except Exception as e:
        print(f"⛔ Ошибка при поиске услуги: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()
def get_services_by_category(category_code):
    """Получает услуги по категории с обработкой ошибок"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT service_code, category_code, name, description, price 
            FROM services 
            WHERE category_code = ?
            ORDER BY name
        """, (category_code,))
        return [Service(*row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"⛔ Ошибка при получении услуг категории: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()