from database.db_manager import get_connection
class Specialty:
    def __init__(self, specialty_code=None, name=None):
        self.specialty_code = specialty_code
        self.name = name
    def save(self):
        """Сохраняет специальность в базу данных с обработкой ошибок"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            if self.specialty_code is None:
                cursor.execute('''
                    INSERT INTO specialties (name)
                    VALUES (?)
                ''', (self.name,))
                self.specialty_code = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE specialties SET 
                        name = ?
                    WHERE specialty_code = ?
                ''', (self.name, self.specialty_code))
            conn.commit()
            return True
        except Exception as e:
            print(f"⛔ Ошибка при сохранении специальности: {str(e)}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
    def delete(self):
        """Удаляет специальность из базы данных с обработкой ошибок"""
        if not self.specialty_code:
            return False
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM specialties WHERE specialty_code = ?",
                           (self.specialty_code,))
            conn.commit()
            return True
        except Exception as e:
            print(f"⛔ Ошибка при удалении специальности: {str(e)}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
def get_all_specialties():
    """Возвращает список всех специальностей с обработкой ошибок"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT specialty_code, name 
            FROM specialties
            ORDER BY name
        """)
        return [Specialty(*row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"⛔ Ошибка при получении списка специальностей: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()
def get_specialty_by_code(specialty_code):
    """Возвращает специальность по коду с обработкой ошибок"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT specialty_code, name 
            FROM specialties 
            WHERE specialty_code = ?
        """, (specialty_code,))
        row = cursor.fetchone()
        return Specialty(*row) if row else None
    except Exception as e:
        print(f"⛔ Ошибка при поиске специальности: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()
def get_specialty_by_name(name):
    """Находит специальность по названию (точное совпадение)"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT specialty_code, name 
            FROM specialties 
            WHERE name = ?
        """, (name,))
        row = cursor.fetchone()
        return Specialty(*row) if row else None
    except Exception as e:
        print(f"⛔ Ошибка при поиске специальности по названию: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()