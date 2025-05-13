from models.receipts import Receipt, get_all_receipts, get_receipt_by_code

def menu_receipts():
    while True:
        print("\n=== 🖨Управление чеками⌨ ===")
        print("1. Показать все чеки")
        print("2. Добавить новый чек")
        print("3. Удалить чек")
        print("4. Редактировать чек")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            receipts = get_all_receipts()
            print("\nСписок чеков:")
            for receipt in receipts:
                print(f"Код: {receipt.receipt_code} | Код пациента: {receipt.patient_code} | Дата: {receipt.receipt_date} | Общая стоимость: {receipt.total_cost} | Статус оплаты: {receipt.payment_status}")
        
        elif choice == "2":
            print("\nДобавление нового чека")
            receipt_code = input("Код чека: ")  # Запрашиваем код чека
            patient_code = input("Код пациента: ")
            receipt_date = input("Дата чека (YYYY-MM-DD): ")
            total_cost = float(input("Общая стоимость: "))
            payment_status = input("Статус оплаты (Не оплачено/Оплачено): ")

            receipt = Receipt(
                receipt_code=receipt_code,  # Передаем код чека
                patient_code=patient_code, 
                receipt_date=receipt_date, 
                total_cost=total_cost, 
                payment_status=payment_status
            )
            receipt.save()
            print("Чек добавлен!")
        
        elif choice == "3":
            receipt_code = input("Код чека для удаления: ")
            receipt = get_receipt_by_code(receipt_code)
            if receipt:
                receipt.delete()
                print("Чек удален!")
            else:
                print("Чек не найден!")
        
        elif choice == "4":
            receipt_code = input("Код чека для редактирования: ")
            receipt = get_receipt_by_code(receipt_code)
            if receipt:
                print("\nТекущие данные чека:")
                print(f"Код: {receipt.receipt_code}")
                print(f"Код пациента: {receipt.patient_code}")
                print(f"Дата: {receipt.receipt_date}")
                print(f"Общая стоимость: {receipt.total_cost}")
                print(f"Статус оплаты: {receipt.payment_status}")
                
                new_patient_code = input("Новый код пациента (оставить пустым чтобы не менять): ")
                new_receipt_date = input("Новая дата чека (оставить пустым чтобы не менять): ")
                new_total_cost = input("Новая общая стоимость (оставить пустым чтобы не менять): ")
                new_payment_status = input("Новый статус оплаты (оставить пустым чтобы не менять): ")
                
                if new_patient_code:
                    receipt.patient_code = new_patient_code
                if new_receipt_date:
                    receipt.receipt_date = new_receipt_date
                if new_total_cost:
                    receipt.total_cost = float(new_total_cost)
                if new_payment_status:
                    receipt.payment_status = new_payment_status
                
                receipt.save()
                print("Данные чека обновлены!")
            else:
                print("Чек не найден!")
        
        elif choice == "0":
            break
        
        else:
            print("Неверный выбор!")