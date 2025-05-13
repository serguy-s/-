from models.categories import ServiceCategory, get_all_service_categories, get_service_category_by_code

def menu_service_categories():
    while True:
        print("\n=== 📩Управление категориями услуг ===")
        print("1. Показать все категории услуг")
        print("2. Добавить новую категорию услуги")
        print("3. Удалить категорию услуги")
        print("4. Редактировать категорию услуги")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            categories = get_all_service_categories()
            print("\n🦯Список категорий услуг:")
            for category in categories:
                print(f"Код: {category.category_code} | Название: {category.name}")
        
        elif choice == "2":
            print("\n🛠Добавление новой категории услуги")
            category_code = input("Код категории услуги: ")  # Запрашиваем код категории
            name = input("Название категории услуги: ")
            
            category = ServiceCategory(
                category_code=category_code,  # Передаем код категории
                name=name
            )
            category.save()
            print("Категория услуги добавлена!")
        
        elif choice == "3":
            category_code = input("Код категории услуги для удаления: ")
            category = get_service_category_by_code(category_code)
            if category:
                category.delete()
                print("Категория услуги удалена!")
            else:
                print("Категория услуги не найдена!")
        
        elif choice == "4":
            category_code = input("Код категории услуги для редактирования: ")
            category = get_service_category_by_code(category_code)
            if category:
                print("\nТекущие данные:")
                print(f"Код: {category.category_code}")
                print(f"Название: {category.name}")
                
                new_code = input("Новый код категории услуги (оставить пустым чтобы не менять): ")  # Новый код
                new_name = input("Новое название (оставить пустым чтобы не менять): ")

                if new_code:
                    category.category_code = new_code  # Обновляем код категории, если введен
                if new_name:
                    category.name = new_name  # Обновляем название, если введено
                
                category.save()
                print("Данные обновлены!")
            else:
                print("Категория услуги не найдена!")
        
        elif choice == "0":
            break
        
        else:
            print("Неверный выбор!")