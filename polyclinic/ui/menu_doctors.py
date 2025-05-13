from models.doctor import Doctor, get_all_doctors, get_doctor_by_code
from models.specialty import get_all_specialties

def menu_doctors():
    while True:
        print("\n=== 🥼Управление врачами🥼 ===")
        print("1. Показать всех врачей")
        print("2. Добавить врача")
        print("3. Удалить врача")
        print("4. Редактировать врача")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            doctors = get_all_doctors()
            print("\nСписок врачей:")
            for doc in doctors:
                print(f"{doc.doctor_code}. {doc.full_name} | Специализация: {doc.specialization} | График: {doc.schedule}")
        
        elif choice == "2":
            print("\nДобавление нового врача")
            doctor_code = input("Код врача: ")  # Запрашиваем код врача
            full_name = input("ФИО врача: ")
            specialization = input("Специализация: ")
            schedule = input("График работы: ")
            
            print("\nДоступные специальности:")
            for spec in get_all_specialties():
                print(f"{spec.specialty_code} - {spec.name}")
            specialty_code = input("Код специальности: ")
            
            doctor = Doctor(
                doctor_code=doctor_code,  # Передаем код врача
                full_name=full_name,
                specialty_code=specialty_code,
                specialization=specialization,
                schedule=schedule
            )
            doctor.save()
            print("Врач добавлен!")
        
        elif choice == "3":
            code = input("Код врача для удаления: ")
            doctor = get_doctor_by_code(code)
            if doctor:
                doctor.delete()
                print("Врач удален!")
            else:
                print("Врач не найден!")
        
        elif choice == "4":
            code = input("Код врача для редактирования: ")
            doctor = get_doctor_by_code(code)
            if doctor:
                print("\nТекущие данные:")
                print(f"ФИО: {doctor.full_name}")
                print(f"Специализация: {doctor.specialization}")
                print(f"График: {doctor.schedule}")
                
                new_code = input("Новый код врача (оставить пустым чтобы не менять): ")
                new_name = input("Новое ФИО (оставить пустым чтобы не менять): ")
                new_spec = input("Новая специализация: ")
                new_schedule = input("Новый график: ")
                
                if new_code:
                    doctor.doctor_code = new_code  # Обновляем код врача, если введен
                if new_name:
                    doctor.full_name = new_name
                if new_spec:
                    doctor.specialization = new_spec
                if new_schedule:
                    doctor.schedule = new_schedule
                
                doctor.save()
                print("Данные обновлены!")
            else:
                print("Врач не найден!")
        
        elif choice == "0":
            break
        
        else:
            print("Неверный выбор!")