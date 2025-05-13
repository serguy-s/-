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
    
    # Таблица специальностей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS specialties (
        specialty_code TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')
    
    # Таблица категорий услуг
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS service_categories (
        category_code TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')
    
    # Таблица врачей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_code TEXT PRIMARY KEY,
        specialty_code TEXT NOT NULL,
        full_name TEXT NOT NULL,
        specialization TEXT,
        schedule TEXT,
        FOREIGN KEY (specialty_code) REFERENCES specialties(specialty_code)
    )
    ''')
    
    # Таблица пациентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        patient_code TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        phone TEXT,
        medical_card TEXT UNIQUE
    )
    ''')
    
    # Таблица услуг
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS services (
        service_code TEXT PRIMARY KEY,
        category_code TEXT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        FOREIGN KEY (category_code) REFERENCES service_categories(category_code)
    )
    ''')
    
    # Таблица записей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_code TEXT NOT NULL,
        doctor_code TEXT NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        status TEXT DEFAULT 'Запланирован',
        FOREIGN KEY (patient_code) REFERENCES patients(patient_code),
        FOREIGN KEY (doctor_code) REFERENCES doctors(doctor_code)
    )
    ''')
    
    # Таблица чеков
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS receipts (
        receipt_code TEXT PRIMARY KEY,
        patient_code TEXT NOT NULL,
        receipt_date TEXT NOT NULL,
        total_cost REAL NOT NULL,
        payment_status TEXT DEFAULT 'Не оплачен',
        FOREIGN KEY (patient_code) REFERENCES patients(patient_code)
    )
    ''')
    
    # Таблица позиций в чеке
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS receipt_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        receipt_code TEXT NOT NULL,
        service_code TEXT NOT NULL,
        quantity INTEGER DEFAULT 1,
        item_price REAL NOT NULL,
        FOREIGN KEY (receipt_code) REFERENCES receipts(receipt_code),
        FOREIGN KEY (service_code) REFERENCES services(service_code)
    )
    ''')
    
    conn.commit()
    conn.close()
