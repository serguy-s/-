from database.db_manager import get_connection
class Doctor:
    def __init__(self, doctor_id=None, specialty_id=None, full_name=None, schedule=None):
        self.doctor_id = doctor_id  # Переименовали в doctor_id
        self.specialty_id = specialty_id
        self.full_name = full_name
        self.schedule = schedule

    def save(self):
        """Сохраняет врача в БД"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            if self.doctor_id is None:
                cursor.execute('''
                    INSERT INTO doctors (specialty_id, full_name, schedule)
                    VALUES (?, ?, ?)
                ''', (self.specialty_id, self.full_name, self.schedule))
                self.doctor_id = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE doctors SET
                        specialty_id = ?,
                        full_name = ?,
                        schedule = ?
                    WHERE id = ?
                ''', (self.specialty_id, self.full_name, self.schedule, self.doctor_id))

            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def delete(self):
        """Удаляет врача из БД"""
        if self.doctor_id is not None:
            conn = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM doctors WHERE id = ?", (self.doctor_id,))
                conn.commit()
            except Exception as e:
                if conn:
                    conn.rollback()
                raise e
            finally:
                if conn:
                    conn.close()


def get_all_doctors():
    """Возвращает список всех врачей"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, specialty_id, full_name, schedule FROM doctors")
        return [Doctor(doctor_id=row[0], specialty_id=row[1], full_name=row[2], schedule=row[3])
                for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


def get_doctor_by_id(doctor_id):
    """Возвращает врача по ID"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, specialty_id, full_name, schedule FROM doctors WHERE id = ?", (doctor_id,))
        row = cursor.fetchone()
        return Doctor(doctor_id=row[0], specialty_id=row[1], full_name=row[2], schedule=row[3]) if row else None
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()