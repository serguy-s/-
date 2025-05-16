from database.db_manager import get_connection
class Patient:
    def __init__(self, patient_id=None, full_name=None, phone=None):
        self.patient_id = patient_id  # Переименовали параметр
        self.full_name = full_name
        self.phone = phone

    def save(self):
        """Сохраняет пациента в БД"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            if self.patient_id is None:
                cursor.execute('''
                    INSERT INTO patients (full_name, phone)
                    VALUES (?, ?)
                ''', (self.full_name, self.phone))
                self.patient_id = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE patients SET
                        full_name = ?,
                        phone = ?
                    WHERE id = ?
                ''', (self.full_name, self.phone, self.patient_id))
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    def delete(self):
        """Удаляет пациента из базы данных"""
        if self.patient_id is not None:
            conn = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM patients WHERE id = ?", (self.patient_id,))
                conn.commit()
            except Exception as e:
                if conn:
                    conn.rollback()
                raise e
            finally:
                if conn:
                    conn.close()
def get_all_patients():
    """Возвращает список всех пациентов"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, phone FROM patients")
        return [Patient(patient_id=row[0], full_name=row[1], phone=row[2])
                for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()
def get_patient_by_id(patient_id):
    """Возвращает пациента по ID"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, phone FROM patients WHERE id = ?", (patient_id,))
        row = cursor.fetchone()
        return Patient(patient_id=row[0], full_name=row[1], phone=row[2]) if row else None
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()