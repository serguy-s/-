from models.appointments import get_all_appointments, get_appointment_by_id
from models.patient import get_all_patients
from models.doctor import get_all_doctors
from models.service import get_all_services
from models.appointments import Appointment  # Импортируем класс Appointment

def menu_appointments():
    while True:
        print("\n=== 📑Записи на прием📑 ===")
        print("1. Показать все записи")
        print("2. Создать новую запись")
        print("3. Отменить запись")
        print("4. Изменить статус записи")
        print("0. Назад в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":
            try:
                appointments = get_all_appointments()
                patients = {p.patient_id: p.full_name for p in get_all_patients()}
                doctors = {d.doctor_id: d.full_name for d in get_all_doctors()}
                services = {s.service_id: s.name for s in get_all_services()}

                print("\nСписок записей:")
                for a in appointments:
                    print(f"{a.appointment_id}. Пациент: {patients.get(a.patient_id, 'Неизвестно')} | "
                          f"Врач: {doctors.get(a.doctor_id, 'Неизвестно')} | "
                          f"Услуга: {services.get(a.service_id, 'Неизвестно')} | "
                          f"Дата: {a.appointment_date} {a.appointment_time} | "
                          f"Статус: {a.status}")
            except Exception as e:
                print(f"Ошибка при получении записей: {e}")

        elif choice == "2":
            try:
                print("\n=== Создание новой записи ===")

                print("Доступные пациенты:")
                patients = get_all_patients()
                for p in patients:
                    print(f"{p.patient_id}. {p.full_name}")
                patient_id = int(input("ID пациента: "))

                print("\nДоступные врачи:")
                doctors = get_all_doctors()
                for d in doctors:
                    print(f"{d.doctor_id}. {d.full_name}")
                doctor_id = int(input("ID врача: "))

                print("\nДоступные услуги:")
                services = get_all_services()
                for s in services:
                    print(f"{s.service_id}. {s.name} ({s.price} руб.)")
                service_id = int(input("ID услуги: "))

                appointment_date = input("Дата приема (ГГГГ-ММ-ДД): ")
                appointment_time = input("Время приема (ЧЧ:ММ): ")

                # Создаем запись с правильными параметрами
                appointment = Appointment(
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    service_id=service_id,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    status="Запланирован"
                )
                appointment.save()
                print("✅ Запись создана.")
            except Exception as e:
                print(f"Ошибка при создании записи: {e}")

        elif choice == "3":
            try:
                appointment_id = int(input("Введите ID записи для отмены: "))
                appointment = get_appointment_by_id(appointment_id)
                if appointment:
                    appointment.status = "Отменен"
                    appointment.save()
                    print("✅ Запись отменена.")
                else:
                    print("❌ Запись не найдена!")
            except Exception as e:
                print(f"Ошибка при отмене записи: {e}")

        elif choice == "4":
            try:
                appointment_id = int(input("Введите ID записи: "))
                appointment = get_appointment_by_id(appointment_id)
                if appointment:
                    print("Текущий статус:", appointment.status)
                    print("Доступные статусы: Запланирован, Завершен, Отменен")
                    new_status = input("Новый статус: ")
                    if new_status in ["Запланирован", "Завершен", "Отменен"]:
                        appointment.status = new_status
                        appointment.save()
                        print("✅ Статус обновлен.")
                    else:
                        print("❌ Неверный статус!")
                else:
                    print("❌ Запись не найдена!")
            except Exception as e:
                print(f"Ошибка при изменении статуса: {e}")

        elif choice == "0":
            break

        else:
            print("❌ Неверный ввод.")