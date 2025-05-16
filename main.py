from database.db_manager import initialize_db
from ui.menu import show_main_menu
from ui.menu_patient import menu_patients
from ui.menu_doctors import menu_doctors
from ui.menu_appointments import menu_appointments
from ui.menu_service import menu_services
from ui.menu_receipts import menu_receipts

def main():
    initialize_db()
    while True:
        user_choice = show_main_menu()
        if user_choice == "1":
            menu_patients()
        elif user_choice == "2":
            menu_doctors()
        elif user_choice == "3":
            menu_services()
        elif user_choice == "4":
            menu_appointments()
        elif user_choice == "5":
            menu_receipts()
        elif user_choice == "0":
            print("Выход из программы. До свидания!")
            break
        else:
            print("❌ Неверный ввод.")

if __name__ == "__main__":
    main()