from database.db_manager import get_connection


class ReceiptItem:
    def __init__(self, item_id=None, receipt_code=None, service_code=None, quantity=1, item_price=0.0):
        self.item_id = item_id
        self.receipt_code = receipt_code
        self.service_code = service_code
        self.quantity = quantity
        self.item_price = item_price

    def calculate_total(self):
        """Вычисляет общую стоимость позиции"""
        return self.quantity * self.item_price

    def save(self):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            if self.item_id is None:
                cursor.execute('''
                    INSERT INTO receipt_items 
                    (receipt_code, service_code, quantity, item_price)
                    VALUES (?, ?, ?, ?)
                ''', (self.receipt_code, self.service_code,
                      self.quantity, self.item_price))
                self.item_id = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE receipt_items SET 
                        receipt_code = ?, 
                        service_code = ?, 
                        quantity = ?, 
                        item_price = ?
                    WHERE item_id = ?
                ''', (self.receipt_code, self.service_code,
                      self.quantity, self.item_price, self.item_id))

            conn.commit()
        except Exception as e:
            print(f"Ошибка при сохранении позиции чека: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    def delete(self):
        if not self.item_id:
            return

        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM receipt_items WHERE item_id = ?",
                           (self.item_id,))
            conn.commit()
        except Exception as e:
            print(f"Ошибка при удалении позиции чека: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()


def get_all_receipt_items():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT item_id, receipt_code, service_code, quantity, item_price 
            FROM receipt_items
        """)
        rows = cursor.fetchall()
        return [ReceiptItem(*row) for row in rows]
    except Exception as e:
        print(f"Ошибка при получении списка позиций чеков: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_receipt_items_by_receipt_code(receipt_code):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT item_id, receipt_code, service_code, quantity, item_price 
            FROM receipt_items 
            WHERE receipt_code = ?
        """, (receipt_code,))
        rows = cursor.fetchall()
        return [ReceiptItem(*row) for row in rows]
    except Exception as e:
        print(f"Ошибка при получении позиций чека: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_receipt_item_by_id(item_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT item_id, receipt_code, service_code, quantity, item_price 
            FROM receipt_items 
            WHERE item_id = ?
        """, (item_id,))
        row = cursor.fetchone()
        return ReceiptItem(*row) if row else None
    except Exception as e:
        print(f"Ошибка при поиске позиции чека: {e}")
        return None
    finally:
        if conn:
            conn.close()