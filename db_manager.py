import sqlite3
from pathlib import Path

# Путь к базе данных (в корне проекта)
DB_PATH = Path(__file__).parent.parent / "polyclinic.db"


def get_connection():
    """Устанавливает соединение с базой данных"""
    return sqlite3.connect(DB_PATH)


def initialize_db():
    """Инициализирует структуру базы данных"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS specialties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )''')
    # Таблица врачей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        specialty_id INTEGER NOT NULL,
        full_name TEXT NOT NULL,
        schedule TEXT,
        FOREIGN KEY (specialty_id) REFERENCES specialties(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT )''')

    # Таблица услуг
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL
    )
    ''')

    # Таблица записей на прием
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        service_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        status TEXT DEFAULT 'Запланирован',
        FOREIGN KEY (patient_id) REFERENCES patients(id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id),
        FOREIGN KEY (service_id) REFERENCES services(id)
    )
    ''')

    # Таблица чеков
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER NOT NULL,
        total_amount REAL NOT NULL,
        payment_status TEXT DEFAULT 'Не оплачен',
        FOREIGN KEY (appointment_id) REFERENCES appointments(id)
    )
    ''')

    conn.commit()
    conn.close()