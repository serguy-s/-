from models.patient import Patient, get_all_patients, get_patient_by_code

def menu_patients():
    while True:
        print("\n=== 🔩Управление пациентами🔧 ===")
        print("1. Показать всех пациентов")
        print("2. Добавить нового пациента")
        print("3. Удалить пациента")
        print("4. Редактировать пациента")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            patients = get_all_patients()
            print("\nСписок пациентов:")
            for patient in patients:
                print(f"Код: {patient.patient_code} | ФИО: {patient.full_name} | Телефон: {patient.phone} | Медицинская карта: {patient.medical_card}")
        
        elif choice == "2":
            print("\nДобавление нового пациента")
            patient_code = input("Код пациента: ")  # Запрашиваем код пациента
            full_name = input("ФИО пациента: ")
            phone = input("Телефон пациента: ")
            medical_card = input("Номер медицинской карты: ")
            
            patient = Patient(
                patient_code=patient_code,  # Передаем код пациента
                full_name=full_name,
                phone=phone,
                medical_card=medical_card
            )
            patient.save()
            print("Пациент добавлен!")
        
        elif choice == "3":
            patient_code = input("Код пациента для удаления: ")
            patient = get_patient_by_code(patient_code)
            if patient:
                patient.delete()
                print("Пациент удален!")
            else:
                print("Пациент не найден!")
        
        elif choice == "4":
            patient_code = input("Код пациента для редактирования: ")
            patient = get_patient_by_code(patient_code)
            if patient:
                print("\nТекущие данные пациента:")
                print(f"Код: {patient.patient_code}")
                print(f"ФИО: {patient.full_name}")
                print(f"Телефон: {patient.phone}")
                print(f"Медицинская карта: {patient.medical_card}")
                
                new_full_name = input("Новое ФИО (оставить пустым чтобы не менять): ")
                new_phone = input("Новый телефон (оставить пустым чтобы не менять): ")
                new_medical_card = input("Новая медицинская карта (оставить пустым чтобы не менять): ")

                if new_full_name:
                    patient.full_name = new_full_name
                if new_phone:
                    patient.phone = new_phone
                if new_medical_card:
                    patient.medical_card = new_medical_card
                
                patient.save()
                print("Данные пациента обновлены!")
            else:
                print("Пациент не найден!")
        
        elif choice == "0":
            break
        
        else:
            print("Неверный выбор!")