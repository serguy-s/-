from database.db_manager import get_connection


class Patient:
    def __init__(self, patient_code=None, full_name=None, phone=None, medical_card=None):
        self.patient_code = patient_code
        self.full_name = full_name
        self.phone = phone
        self.medical_card = medical_card

    def save(self):
        """Сохраняет пациента в базу данных с обработкой ошибок"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            if self.patient_code is None:
                cursor.execute('''
                    INSERT INTO patients 
                    (full_name, phone, medical_card)
                    VALUES (?, ?, ?)
                ''', (self.full_name, self.phone, self.medical_card))
                self.patient_code = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE patients SET 
                        full_name = ?,
                        phone = ?,
                        medical_card = ?
                    WHERE patient_code = ?
                ''', (self.full_name, self.phone, self.medical_card, self.patient_code))

            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при сохранении пациента: {str(e)}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    def delete(self):
        """Удаляет пациента из базы данных с обработкой ошибок"""
        if not self.patient_code:
            return False

        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM patients WHERE patient_code = ?",
                           (self.patient_code,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при удалении пациента: {str(e)}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()


def get_all_patients():
    """Получает список всех пациентов с обработкой ошибок"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT patient_code, full_name, phone, medical_card 
            FROM patients
            ORDER BY full_name
        """)
        return [Patient(*row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Ошибка при получении списка пациентов: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()


def get_patient_by_code(patient_code):
    """Находит пациента по коду с обработкой ошибок"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT patient_code, full_name, phone, medical_card 
            FROM patients 
            WHERE patient_code = ?
        """, (patient_code,))
        row = cursor.fetchone()
        return Patient(*row) if row else None
    except Exception as e:
        print(f"Ошибка при поиске пациента: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()


def search_patients_by_name(name_part):
    """Поиск пациентов по части имени с обработкой ошибок"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT patient_code, full_name, phone, medical_card 
            FROM patients 
            WHERE full_name LIKE ?
            ORDER BY full_name
        """, (f"%{name_part}%",))
        return [Patient(*row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Ошибка при поиске пациентов: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()