from database.db_manager import get_connection


class Doctor:
    def __init__(self, doctor_code=None, specialty_code=None, full_name=None,
                 specialization=None, schedule=None):
        self.doctor_code = doctor_code
        self.specialty_code = specialty_code
        self.full_name = full_name
        self.specialization = specialization
        self.schedule = schedule

    def save(self):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            if self.doctor_code is None:
                cursor.execute('''
                    INSERT INTO doctors 
                    (specialty_code, full_name, specialization, schedule)
                    VALUES (?, ?, ?, ?)
                ''', (self.specialty_code, self.full_name,
                      self.specialization, self.schedule))
                self.doctor_code = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE doctors SET 
                        specialty_code = ?,
                        full_name = ?,
                        specialization = ?,
                        schedule = ?
                    WHERE doctor_code = ?
                ''', (self.specialty_code, self.full_name,
                      self.specialization, self.schedule,
                      self.doctor_code))

            conn.commit()
        except Exception as e:
            print(f"Ошибка при сохранении данных врача: {e}")
            if conn:
                conn.rollback()
            raise  # Можно заменить на return False если нужно подавить исключение
        finally:
            if conn:
                conn.close()
        return True

    def delete(self):
        if not self.doctor_code:
            return False

        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doctors WHERE doctor_code = ?",
                           (self.doctor_code,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при удалении врача: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()


def get_all_doctors():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT doctor_code, specialty_code, full_name, 
                   specialization, schedule 
            FROM doctors
            ORDER BY full_name
        """)
        return [Doctor(*row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Ошибка при получении списка врачей: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_doctor_by_code(doctor_code):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT doctor_code, specialty_code, full_name, 
                   specialization, schedule 
            FROM doctors 
            WHERE doctor_code = ?
        """, (doctor_code,))
        row = cursor.fetchone()
        return Doctor(*row) if row else None
    except Exception as e:
        print(f"Ошибка при поиске врача: {e}")
        return None
    finally:
        if conn:
            conn.close()


def get_doctors_by_specialty(specialty_code):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT doctor_code, specialty_code, full_name, 
                   specialization, schedule 
            FROM doctors 
            WHERE specialty_code = ?
            ORDER BY full_name
        """, (specialty_code,))
        return [Doctor(*row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Ошибка при поиске врачей по специальности: {e}")
        return []
    finally:
        if conn:
            conn.close()