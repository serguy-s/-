from database.db_manager import get_connection


class Receipt:
    def __init__(self, receipt_code=None, patient_code=None, receipt_date=None,
                 total_cost=0.0, payment_status='Не оплачен'):
        self.receipt_code = receipt_code
        self.patient_code = patient_code
        self.receipt_date = receipt_date
        self.total_cost = total_cost
        self.payment_status = payment_status

    def save(self):
        """Сохраняет чек в базу данных с обработкой ошибок"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            if self.receipt_code is None:
                cursor.execute('''
                    INSERT INTO receipts 
                    (patient_code, receipt_date, total_cost, payment_status)
                    VALUES (?, ?, ?, ?)
                ''', (self.patient_code, self.receipt_date,
                      self.total_cost, self.payment_status))
                self.receipt_code = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE receipts SET 
                        patient_code = ?,
                        receipt_date = ?,
                        total_cost = ?,
                        payment_status = ?
                    WHERE receipt_code = ?
                ''', (self.patient_code, self.receipt_date,
                      self.total_cost, self.payment_status,
                      self.receipt_code))

            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при сохранении чека: {str(e)}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    def delete(self):
        """Удаляет чек из базы данных с обработкой ошибок"""
        if not self.receipt_code:
            return False

        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM receipts WHERE receipt_code = ?",
                           (self.receipt_code,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при удалении чека: {str(e)}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    def mark_as_paid(self):
        """Помечает чек как оплаченный"""
        if self.receipt_code:
            self.payment_status = 'Оплачен'
            return self.save()
        return False


def get_all_receipts():
    """Получает список всех чеков с обработкой ошибок"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT receipt_code, patient_code, receipt_date, 
                   total_cost, payment_status 
            FROM receipts
            ORDER BY receipt_date DESC
        """)
        return [Receipt(*row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Ошибка при получении списка чеков: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()


def get_receipt_by_code(receipt_code):
    """Находит чек по коду с обработкой ошибок"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT receipt_code, patient_code, receipt_date, 
                   total_cost, payment_status 
            FROM receipts 
            WHERE receipt_code = ?
        """, (receipt_code,))
        row = cursor.fetchone()
        return Receipt(*row) if row else None
    except Exception as e:
        print(f"Ошибка при поиске чека: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()


def get_receipts_by_patient(patient_code):
    """Получает чеки по коду пациента с обработкой ошибок"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT receipt_code, patient_code, receipt_date, 
                   total_cost, payment_status 
            FROM receipts 
            WHERE patient_code = ?
            ORDER BY receipt_date DESC
        """, (patient_code,))
        return [Receipt(*row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Ошибка при получении чеков пациента: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()


def get_unpaid_receipts():
    """Получает неоплаченные чеки с обработкой ошибок"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT receipt_code, patient_code, receipt_date, 
                   total_cost, payment_status 
            FROM receipts 
            WHERE payment_status != 'Оплачен'
            ORDER BY receipt_date
        """)
        return [Receipt(*row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Ошибка при получении неоплаченных чеков: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()