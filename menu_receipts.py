from models.receipts import get_all_receipts, get_receipt_by_id
from models.appointments import get_all_appointments, get_appointment_by_id
from models.service import get_service_by_id
def menu_receipts():
    while True:
        print("\n=== 📃Чеки💵 ===")
        print("1. Показать все чеки")
        print("2. Создать чек")
        print("3. Изменить статус оплаты")
        print("0. Назад в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":
            try:
                receipts = get_all_receipts()
                appointments = {a.appointment_id: a for a in get_all_appointments()}
                services = {}

                # Получаем услуги для всех назначений
                for a in appointments.values():
                    if a.service_id not in services:
                        services[a.service_id] = get_service_by_id(a.service_id)

                print("\nСписок чеков:")
                for r in receipts:
                    appointment = appointments.get(r.appointment_id)
                    service = services.get(appointment.service_id) if appointment else None
                    print(f"{r.receipt_id}. Запись ID: {r.appointment_id} | "
                          f"Услуга: {service.name if service else 'Неизвестно'} | "
                          f"Сумма: {r.total_amount} руб. | "
                          f"Статус: {r.payment_status}")
            except Exception as e:
                print(f"Ошибка при получении чеков: {e}")

        elif choice == "2":
            try:
                print("\n=== Создание чека ===")
                print("Доступные записи на прием:")

                appointments = get_all_appointments()
                for a in appointments:
                    print(f"{a.appointment_id}. Дата: {a.appointment_date} {a.appointment_time} | Статус: {a.status}")

                appointment_id = int(input("ID записи на прием: "))
                appointment = get_appointment_by_id(appointment_id)

                if appointment and appointment.status == "Завершен":
                    service = get_service_by_id(appointment.service_id)
                    if service:
                        from models.receipts import Receipt  # Локальный импорт
                        receipt = Receipt(
                            appointment_id=appointment_id,
                            total_amount=service.price,
                            payment_status="Не оплачен"
                        )
                        receipt.save()
                        print(f"✅ Чек создан. Сумма к оплате: {service.price} руб.")
                    else:
                        print("❌ Услуга не найдена!")
                else:
                    print("❌ Запись не найдена или не завершена!")
            except Exception as e:
                print(f"Ошибка при создании чека: {e}")

        elif choice == "3":
            try:
                receipt_id = int(input("Введите ID чека: "))
                receipt = get_receipt_by_id(receipt_id)
                if receipt:
                    print("Текущий статус:", receipt.payment_status)
                    print("Доступные статусы: Не оплачен, Оплачен")
                    new_status = input("Новый статус: ")
                    if new_status in ["Не оплачен", "Оплачен"]:
                        receipt.payment_status = new_status
                        receipt.save()
                        print("✅ Статус обновлен.")
                    else:
                        print("❌ Неверный статус!")
                else:
                    print("❌ Чек не найден!")
            except Exception as e:
                print(f"Ошибка при изменении статуса: {e}")

        elif choice == "0":
            break

        else:
            print("❌ Неверный ввод.")