from models.patient import Patient, get_all_patients, get_patient_by_id
def menu_patients():
    while True:
        print("\n=== 📊Пациенты🧧 ===")
        print("1. Показать всех пациентов")
        print("2. Добавить пациента")
        print("3. Удалить пациента")
        print("4. Изменить данные пациента")
        print("0. Назад в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":
            try:
                patients = get_all_patients()
                print("\nСписок пациентов:")
                if not patients:
                    print("Нет зарегистрированных пациентов")
                else:
                    for p in patients:
                        # Исправлено p.id на p.patient_id
                        print(f"{p.patient_id}. {p.full_name} | Телефон: {p.phone}")
            except Exception as e:
                print(f"Ошибка при получении списка пациентов: {str(e)}")

        elif choice == "2":
            try:
                print("\n=== Добавление нового пациента ===")
                full_name = input("ФИО: ").strip()
                if not full_name:
                    print("❌ ФИО не может быть пустым")
                    continue

                phone = input("Телефон: ").strip()
                patient = Patient(full_name=full_name, phone=phone)
                patient.save()
                print(f"✅ Пациент добавлен. ID: {patient.patient_id}")

                # Проверка сохранения
                check_patient = get_patient_by_id(patient.patient_id)
                if not check_patient:
                    print("⚠️ Предупреждение: не удалось найти только что добавленного пациента")
            except Exception as e:
                print(f"❌ Ошибка при добавлении пациента: {str(e)}")

        elif choice == "3":
            try:
                patient_id = input("Введите ID пациента для удаления: ")
                if not patient_id.isdigit():
                    print("❌ ID должен быть числом")
                    continue

                patient = get_patient_by_id(int(patient_id))
                if patient:
                    patient.delete()
                    print("✅ Пациент удален.")
                else:
                    print("❌ Пациент не найден!")
            except Exception as e:
                print(f"❌ Ошибка при удалении пациента: {str(e)}")

        elif choice == "4":
            try:
                patient_id = input("Введите ID пациента для редактирования: ")
                if not patient_id.isdigit():
                    print("❌ ID должен быть числом")
                    continue

                patient = get_patient_by_id(int(patient_id))
                if patient:
                    print("\nОставьте поле пустым, чтобы не изменять значение")
                    full_name = input(f"ФИО [{patient.full_name}]: ").strip() or patient.full_name
                    phone = input(f"Телефон [{patient.phone}]: ").strip() or patient.phone

                    patient.full_name = full_name
                    patient.phone = phone
                    patient.save()
                    print("✅ Данные пациента обновлены.")
                else:
                    print("❌ Пациент не найден!")
            except Exception as e:
                print(f"❌ Ошибка при редактировании пациента: {str(e)}")

        elif choice == "0":
            break

        else:
            print("❌ Неверный ввод. Пожалуйста, выберите пункт меню от 0 до 4")