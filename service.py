from database.db_manager import get_connection
class Service:
    def __init__(self, service_id=None, name=None, description=None, price=None):
        self.service_id = service_id
        self.name = name
        self.description = description
        self.price = price
    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.service_id is None:
                cursor.execute('''
                    INSERT INTO services (name, description, price)
                    VALUES (?, ?, ?)
                ''', (self.name, self.description, self.price))
                self.service_id = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE services SET
                        name = ?,
                        description = ?,
                        price = ?
                    WHERE id = ?
                ''', (self.name, self.description, self.price, self.service_id))
            conn.commit()
    def delete(self):
        if self.service_id is not None:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM services WHERE id = ?", (self.service_id,))
                conn.commit()
# Вспомогательные функции
def get_all_services():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services")
        return [Service(service_id=row[0], name=row[1], description=row[2], price=row[3])
                for row in cursor.fetchall()]
def get_service_by_id(service_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services WHERE id = ?", (service_id,))
        row = cursor.fetchone()
        if row:
            return Service(service_id=row[0], name=row[1], description=row[2], price=row[3])
        return None