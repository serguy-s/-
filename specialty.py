from database.db_manager import get_connection  # Правильный импорт

class Specialty:
    def __init__(self, specialty_id =None, name=None):
        self.id = id
        self.name = name

    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute('INSERT INTO specialties (name) VALUES (?)', (self.name,))
                self.id = cursor.lastrowid
            else:
                cursor.execute('UPDATE specialties SET name = ? WHERE id = ?',
                             (self.name, self.id))
            conn.commit()

    def delete(self):
        if self.id is not None:
            with get_connection() as conn:
                conn.execute('DELETE FROM specialties WHERE id = ?', (self.id,))
                conn.commit()

# Отдельные функции вместо classmethod
def get_all_specialties():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM specialties')
        return [Specialty(specialty_id=row[0], name=row[1]) for row in cursor.fetchall()]

def get_specialty_by_id(specialty_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM specialties WHERE id = ?', (specialty_id,))
        row = cursor.fetchone()
        return Specialty(specialty_id =row[0], name=row[1]) if row else None