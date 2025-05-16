from models.service import get_all_services, get_service_by_id
def menu_services():
    while True:
        print("\n=== 💊Медицинские услуги💉🩺 ===")
        print("1. Показать все услуги")
        print("2. Добавить услугу")
        print("3. Удалить услугу")
        print("4. Изменить данные услуги")
        print("0. Назад в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":
            try:
                services = get_all_services()
                print("\nСписок услуг:")
                for s in services:
                    print(f"{s.service_id}. {s.name} | Цена: {s.price} руб. | Описание: {s.description or 'нет'}")
            except Exception as e:
                print(f"Ошибка при получении услуг: {e}")

        elif choice == "2":
            try:
                print("\n=== Добавление новой услуги ===")
                from models.service import Service  # Локальный импорт

                name = input("Название услуги: ")
                description = input("Описание: ")
                price = float(input("Цена: "))

                service = Service(
                    name=name,
                    description=description,
                    price=price
                )
                service.save()
                print("✅ Услуга добавлена.")
            except Exception as e:
                print(f"Ошибка при добавлении услуги: {e}")

        elif choice == "3":
            try:
                service_id = input("Введите ID услуги для удаления: ")
                from models.service import Service  # Локальный импорт

                service = Service(service_id=int(service_id))
                service.delete()
                print("✅ Услуга удалена.")
            except Exception as e:
                print(f"Ошибка при удалении услуги: {e}")

        elif choice == "4":
            try:
                service_id = input("Введите ID услуги для редактирования: ")
                service = get_service_by_id(int(service_id))
                if service:
                    print("\nОставьте поле пустым, чтобы не изменять значение")
                    name = input(f"Название [{service.name}]: ") or service.name
                    description = input(f"Описание [{service.description}]: ") or service.description
                    price = input(f"Цена [{service.price}]: ") or service.price

                    service.name = name
                    service.description = description
                    service.price = float(price)
                    service.save()
                    print("✅ Данные услуги обновлены.")
                else:
                    print("❌ Услуга не найдена!")
            except Exception as e:
                print(f"Ошибка при редактировании услуги: {e}")

        elif choice == "0":
            break

        else:
            print("❌ Неверный ввод.")