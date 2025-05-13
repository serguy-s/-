from database.db_manager import get_connection


class Appointment:
    def __init__(self, appointment_id=None, patient_code=None, doctor_code=None,
                 appointment_date=None, appointment_time=None, status='Запланирован'):
        self.appointment_id = appointment_id
        self.patient_code = patient_code
        self.doctor_code = doctor_code
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status

    def save(self):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            if self.appointment_id is None:
                cursor.execute('''
                    INSERT INTO appointments 
                    (patient_code, doctor_code, appointment_date, appointment_time, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (self.patient_code, self.doctor_code, self.appointment_date,
                      self.appointment_time, self.status))
                self.appointment_id = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE appointments SET 
                        patient_code = ?, 
                        doctor_code = ?, 
                        appointment_date = ?, 
                        appointment_time = ?, 
                        status = ?
                    WHERE appointment_id = ?
                ''', (self.patient_code, self.doctor_code, self.appointment_date,
                      self.appointment_time, self.status, self.appointment_id))
            conn.commit()
        except Exception as e:
            print(f"Ошибка при сохранении записи: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def delete(self):
        if self.appointment_id:
            conn = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM appointments WHERE appointment_id = ?",
                               (self.appointment_id,))
                conn.commit()
            except Exception as e:
                print(f"Ошибка при удалении записи: {e}")
                if conn:
                    conn.rollback()
            finally:
                if conn:
                    conn.close()


def get_all_appointments():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments")
        rows = cursor.fetchall()
        return [Appointment(*row) for row in rows]
    except Exception as e:
        print(f"Ошибка при получении списка записей: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_appointment_by_id(appointment_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments WHERE appointment_id = ?",
                       (appointment_id,))
        row = cursor.fetchone()
        return Appointment(*row) if row else None
    except Exception as e:
        print(f"Ошибка при поиске записи: {e}")
        return None
    finally:
        if conn:
            conn.close()