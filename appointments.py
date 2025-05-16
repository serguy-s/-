from database.db_manager import get_connection

class Appointment:
    def __init__(self, appointment_id=None, patient_id=None, doctor_id=None, service_id=None,
                 appointment_date=None, appointment_time=None, status="Запланирован"):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.service_id = service_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status

    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.appointment_id is None:
                cursor.execute('''
                    INSERT INTO appointments 
                    (patient_id, doctor_id, service_id, appointment_date, appointment_time, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (self.patient_id, self.doctor_id, self.service_id,
                      self.appointment_date, self.appointment_time, self.status))
                self.appointment_id = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE appointments SET
                        patient_id = ?,
                        doctor_id = ?,
                        service_id = ?,
                        appointment_date = ?,
                        appointment_time = ?,
                        status = ?
                    WHERE id = ?
                ''', (self.patient_id, self.doctor_id, self.service_id,
                      self.appointment_date, self.appointment_time, self.status, self.appointment_id))
            conn.commit()

    def delete(self):
        if self.appointment_id is not None:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM appointments WHERE id = ?", (self.appointment_id,))
                conn.commit()

def get_all_appointments():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments")
        return [Appointment(
            appointment_id=row[0],
            patient_id=row[1],
            doctor_id=row[2],
            service_id=row[3],
            appointment_date=row[4],
            appointment_time=row[5],
            status=row[6]
        ) for row in cursor.fetchall()]

def get_appointment_by_id(appointment_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
        row = cursor.fetchone()
        if row:
            return Appointment(
                appointment_id=row[0],
                patient_id=row[1],
                doctor_id=row[2],
                service_id=row[3],
                appointment_date=row[4],
                appointment_time=row[5],
                status=row[6]
            )
        return None