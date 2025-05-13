from models.appointments import Appointment, get_all_appointments, get_appointment_by_id
from models.doctor import get_all_doctors
from models.patient import get_all_patients  

def menu_appointments():
    while True:
        print("\n=== Управление записями на прием ===")
        print("1. Показать все записи на прием")
        print("2. Добавить запись на прием")
        print("3. Удалить запись на прием")
        print("4. Редактировать запись на прием")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            appointments = get_all_appointments()
            print("\n📃Список записей на прием🧾:")
            for appointment in appointments:
                print(f"ID: {appointment.appointment_id} | Пациент: {appointment.patient_code} | Врач: {appointment.doctor_code} | Дата: {appointment.appointment_date} | Время: {appointment.appointment_time} | Статус: {appointment.status}")
        elif choice == "2":
            print("\n🖋Добавление новой записи на прием🖌")
            patient_code = input("Код пациента: ")
            doctor_code = input("Код врача: ")
            appointment_date = input("Дата записи (гггг-мм-дд): ")
            appointment_time = input("Время записи (чч:мм): ")
            status = input("Статус (по умолчанию 'Запланирован'): ") or 'Запланирован'
            
            appointment = Appointment(
                patient_code=patient_code,
                doctor_code=doctor_code,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status=status
            )
            appointment.save()
            print("Запись добавлена!")
        
        elif choice == "3":
            appointment_id = input("ID записи для удаления: ")
            appointment = get_appointment_by_id(appointment_id)
            if appointment:
                appointment.delete()
                print("Запись удалена!")
            else:
                print("Запись не найдена!")
        
        elif choice == "4":
            appointment_id = input("ID записи для редактирования: ")
            appointment = get_appointment_by_id(appointment_id)
            if appointment:
                print("\n📕Текущие данные:")
                print(f"Пациент: {appointment.patient_code}")
                print(f"Врач: {appointment.doctor_code}")
                print(f"Дата: {appointment.appointment_date}")
                print(f"Время: {appointment.appointment_time}")
                print(f"Статус: {appointment.status}")
                
                new_patient_code = input("Новый код пациента (оставить пустым чтобы не менять): ")
                new_doctor_code = input("Новый код врача (оставить пустым чтобы не менять): ")
                new_date = input("Новая дата (оставить пустым чтобы не менять): ")
                new_time = input("Новое время (оставить пустым чтобы не менять): ")
                new_status = input("Новый статус (оставить пустым чтобы не менять): ")

                if new_patient_code:
                    appointment.patient_code = new_patient_code
                if new_doctor_code:
                    appointment.doctor_code = new_doctor_code
                if new_date:
                    appointment.appointment_date = new_date
                if new_time:
                    appointment.appointment_time = new_time
                if new_status:
                    appointment.status = new_status
                
                appointment.save()
                print("Данные обновлены!")
            else:
                print("Запись не найдена!")
        
        elif choice == "0":
            break
        else:
            print("Неверный выбор!")