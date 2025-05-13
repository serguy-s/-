from models.specialty import Specialty, get_all_specialties, get_specialty_by_code

def menu_specialties():
    while True:
        print("\n=== 📝Управление специальностями🗃 ===")
        print("1. Показать все специальности")
        print("2. Добавить новую специальность")
        print("3. Удалить специальность")
        print("4. Редактировать специальность")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            specialties = get_all_specialties()
            print("\nСписок специальностей:")
            for specialty in specialties:
                print(f"Код: {specialty.specialty_code} | Название: {specialty.name}")
        
        elif choice == "2":
            print("\nДобавление новой специальности")
            specialty_code = input("Код специальности: ")  # Запрашиваем код специальности
            name = input("Название специальности: ")
            
            specialty = Specialty(specialty_code=specialty_code, name=name)  # Передаем код специальности
            specialty.save()
            print("Специальность добавлена!")
        
        elif choice == "3":
            specialty_code = input("Код специальности для удаления: ")
            specialty = get_specialty_by_code(specialty_code)
            if specialty:
                specialty.delete()
                print("Специальность удалена!")
            else:
                print("Специальность не найдена!")
        
        elif choice == "4":
            specialty_code = input("Код специальности для редактирования: ")
            specialty = get_specialty_by_code(specialty_code)
            if specialty:
                print("\nТекущие данные:")
                print(f"Код: {specialty.specialty_code}")
                print(f"Название: {specialty.name}")
                
                new_code = input("Новый код специальности (оставить пустым чтобы не менять): ")
                new_name = input("Новое название (оставить пустым чтобы не менять): ")

                if new_code:
                    specialty.specialty_code = new_code  # Обновляем код специальности, если введен
                if new_name:
                    specialty.name = new_name  # Обновляем название, если введено
                
                specialty.save()
                print("Данные обновлены!")
            else:
                print("Специальность не найдена!")
        
        elif choice == "0":
            break
        
        else:
            print("Неверный выбор!")