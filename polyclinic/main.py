import sys
from pathlib import Path
# Добавляем корень проекта в пути Python
sys.path.append(str(Path(__file__).parent))
from database.db_manager import initialize_db
from ui.menu import show_main_menu
from ui.menu_specialty import menu_specialties
from ui.menu_doctors import menu_doctors
from ui.menu_patient import menu_patients
from ui.menu_service import menu_services
from ui.menu_appointments import menu_appointments
from ui.menu_receipts import menu_receipts

def main():
    initialize_db()
    while True:
        choice = show_main_menu()
        if choice == "1":
            menu_specialties()
        elif choice == "2":
            menu_doctors()
        elif choice == "3":
            menu_patients()
        elif choice == "4":
            menu_services()
        elif choice == "5":
            menu_appointments()
        elif choice == "6":
            menu_receipts()
        elif choice == "0":
            print("Выход из системы")
            break
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()