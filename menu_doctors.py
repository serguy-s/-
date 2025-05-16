from models.doctor import Doctor, get_all_doctors, get_doctor_by_id
from models.specialty import get_all_specialties
def menu_doctors():
    while True:
        print("\n=== 🥼Врачи💉🩸 ===")
        print("1. Показать всех врачей")
        print("2. Добавить врача")
        print("3. Удалить врача")
        print("4. Изменить данные врача")
        print("0. Назад в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":
            try:
                doctors = get_all_doctors()
                specialties = {s.specialty_id: s.name for s in get_all_specialties()}

                print("\nСписок врачей:")
                if not doctors:
                    print("Нет зарегистрированных врачей")
                else:
                    for doctor in doctors:
                        spec_name = specialties.get(doctor.specialty_id, "Неизвестно")
                        print(
                            f"ID: {doctor.doctor_id} | ФИО: {doctor.full_name} | Специальность: {spec_name} | График: {doctor.schedule}")
            except Exception as e:
                print(f"Ошибка при получении списка врачей: {e}")

        elif choice == "2":
            try:
                print("\n=== Добавление нового врача ===")

                specialties = get_all_specialties()
                print("Доступные специальности:")
                for spec in specialties:
                    print(f"{spec.specialty_id}. {spec.name}")

                specialty_id = int(input("ID специальности: "))
                full_name = input("ФИО врача: ").strip()
                schedule = input("График работы: ").strip()

                doctor = Doctor(
                    specialty_id=specialty_id,
                    full_name=full_name,
                    schedule=schedule
                )
                doctor.save()
                print(f"✅ Врач добавлен. ID: {doctor.doctor_id}")

            except Exception as e:
                print(f"Ошибка при добавлении врача: {e}")

        elif choice == "3":
            try:
                doctor_id = input("Введите ID врача для удаления: ")
                doctor = get_doctor_by_id(int(doctor_id))
                if doctor:
                    doctor.delete()
                    print("✅ Врач удален.")
                else:
                    print("❌ Врач не найден!")
            except Exception as e:
                print(f"Ошибка при удалении врача: {e}")

        elif choice == "4":
            try:
                doctor_id = input("Введите ID врача для редактирования: ")
                doctor = get_doctor_by_id(int(doctor_id))
                if doctor:
                    print("\nТекущие данные:")
                    print(f"ФИО: {doctor.full_name}")
                    print(f"График: {doctor.schedule}")

                    new_name = input("Новое ФИО (оставьте пустым для сохранения текущего): ").strip()
                    new_schedule = input("Новый график (оставьте пустым для сохранения текущего): ").strip()

                    if new_name:
                        doctor.full_name = new_name
                    if new_schedule:
                        doctor.schedule = new_schedule

                    doctor.save()
                    print("✅ Данные врача обновлены.")
                else:
                    print("❌ Врач не найден!")
            except Exception as e:
                print(f"Ошибка при редактировании врача: {e}")

        elif choice == "0":
            break

        else:
            print("❌ Неверный ввод")