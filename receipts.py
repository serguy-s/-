from database.db_manager import get_connection
class Receipt:
    def __init__(self, receipt_id=None, appointment_id=None, total_amount=None, payment_status="Не оплачен"):
        self.receipt_id = receipt_id
        self.appointment_id = appointment_id
        self.total_amount = total_amount
        self.payment_status = payment_status

    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.receipt_id is None:
                cursor.execute('''
                    INSERT INTO receipts (appointment_id, total_amount, payment_status)
                    VALUES (?, ?, ?)
                ''', (self.appointment_id, self.total_amount, self.payment_status))
                self.receipt_id = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE receipts SET
                        appointment_id = ?,
                        total_amount = ?,
                        payment_status = ?
                    WHERE id = ?
                ''', (self.appointment_id, self.total_amount, self.payment_status, self.receipt_id))
            conn.commit()

    def delete(self):
        if self.receipt_id is not None:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM receipts WHERE id = ?", (self.receipt_id,))
                conn.commit()

def get_all_receipts():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM receipts")
        return [Receipt(*row) for row in cursor.fetchall()]

def get_receipt_by_id(receipt_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM receipts WHERE id = ?", (receipt_id,))
        row = cursor.fetchone()
        return Receipt(*row) if row else None