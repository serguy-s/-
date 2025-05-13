from models.service import Service, get_all_services, get_service_by_code

def menu_services():
    while True:
        print("\n=== 🧬Управление услугами🩸 ===")
        print("1. Показать все услуги")
        print("2. Добавить новую услугу")
        print("3. Удалить услугу")
        print("4. Редактировать услугу")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            services = get_all_services()
            print("\nСписок услуг:")
            for service in services:
                print(f"Код: {service.service_code} | Категория: {service.category_code} | Название: {service.name} | Описание: {service.description} | Цена: {service.price}")
        
        elif choice == "2":
            print("\nДобавление новой услуги")
            service_code = input("Код услуги: ")
            category_code = input("Код категории: ")
            name = input("Название услуги: ")
            description = input("Описание услуги: ")
            price = float(input("Цена услуги: "))
            
            service = Service(service_code=service_code, category_code=category_code, name=name, description=description, price=price)
            service.save()
            print("Услуга добавлена!")
        
        elif choice == "3":
            service_code = input("Код услуги для удаления: ")
            service = get_service_by_code(service_code)
            if service:
                service.delete()
                print("Услуга удалена!")
            else:
                print("Услуга не найдена!")
        
        elif choice == "4":
            service_code = input("Код услуги для редактирования: ")
            service = get_service_by_code(service_code)
            if service:
                print("\nТекущие данные услуги:")
                print(f"Код: {service.service_code}")
                print(f"Категория: {service.category_code}")
                print(f"Название: {service.name}")
                print(f"Описание: {service.description}")
                print(f"Цена: {service.price}")
                
                new_service_code = input("Новый код услуги (оставить пустым чтобы не менять): ")
                new_category_code = input("Новый код категории (оставить пустым чтобы не менять): ")
                new_name = input("Новое название услуги (оставить пустым чтобы не менять): ")
                new_description = input("Новое описание услуги (оставить пустым чтобы не менять): ")
                new_price = input("Новая цена услуги (оставить пустым чтобы не менять): ")
                
                if new_service_code:
                    service.service_code = new_service_code
                if new_category_code:
                    service.category_code = new_category_code
                if new_name:
                    service.name = new_name
                if new_description:
                    service.description = new_description
                if new_price:
                    service.price = float(new_price)
                
                service.save()
                print("Данные услуги обновлены!")
            else:
                print("Услуга не найдена!")
        
        elif choice == "0":
            break
        
        else:
            print("Неверный выбор!")