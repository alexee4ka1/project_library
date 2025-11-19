import sqlite3
import os
import json
import csv
import yaml
import xml.etree.ElementTree as ET

DB = 'src/main/resources/database.db'

def showBooks():
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("""SELECT id, title, author, year, genre, inventory_number FROM books""")
    items = c.fetchmany(10)
    for row in items:
        print(f"{row[0]}. Название: {row[1]}. Автор: {row[2]}. Год выпуска: {row[3]}. Жанр: {row[4]}. Остаток: {row[5]}")
    db.close()
    input("Нажмите Enter для выхода...")

def createBook():
    title = input("Введите название: ")
    author = input("Введите автора: ")
    year = int(input("Введите год выпуска: "))
    genre = input("Введите жанр: ")
    number = int(input("Введите количество экземпляров: "))
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("""
        INSERT INTO books (title, author, year, genre, inventory_number)
        VALUES (?, ?, ?, ?, ?)
    """, (title, author, year, genre, number))
    db.commit()
    db.close()
    input("Нажмите Enter для выхода...")

def readBook():
    title = input("Введите название: ")
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("""SELECT id, title, author, year, genre, inventory_number 
                 FROM books WHERE title = ?""", (title,))
    item = c.fetchone()
    if item:
        print(f"ID: {item[0]}\nНазвание: {item[1]}\nАвтор: {item[2]}\nГод: {item[3]}\nЖанр: {item[4]}\nКоличество: {item[5]}")
    else:
        print("Совпадений нет")
    db.close()
    input("Нажмите Enter для выхода...")

def editBook():
    title = input("Введите название книги: ")
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("""SELECT id, title, author, year, genre, inventory_number 
                 FROM books WHERE title = ?""", (title,))
    item = c.fetchone()
    if not item:
        print("Книга не найдена")
        input("Нажмите Enter для выхода...")
        return
    print("Что изменить?")
    print("0. Название:", item[1])
    print("1. Автор:", item[2])
    print("2. Год выпуска:", item[3])
    print("3. Жанр:", item[4])
    print("4. Количество:", item[5])
    action = int(input("Ваш выбор: "))
    fields = ["title", "author", "year", "genre", "inventory_number"]
    new_value = input("Введите новое значение: ")
    c.execute(f"UPDATE books SET {fields[action]} = ? WHERE id = ?", (new_value, item[0]))
    db.commit()
    db.close()
    input("Нажмите Enter для выхода...")

def deleteBook():
    title = input("Введите название: ")
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("SELECT id FROM books WHERE title = ?", (title,))
    item = c.fetchone()
    if item:
        c.execute("DELETE FROM books WHERE id = ?", (item[0],))
        print("Книга удалена")
    else:
        print("Книга не найдена")
    db.commit()
    db.close()
    input("Нажмите Enter для выхода...")

def showReaders():
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("SELECT id, name, phone_number FROM readers")
    items = c.fetchmany(10)
    for row in items:
        print(f"{row[0]}. Имя: {row[1]}. Телефон: {row[2]}")
    db.close()
    input("Нажмите Enter для выхода...")

def readReader():
    name = input("Введите имя: ")
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("SELECT id, name, phone_number FROM readers WHERE name = ?", (name,))
    r = c.fetchone()
    if r:
        print(f"ID: {r[0]}\nИмя: {r[1]}\nНомер телефона: {r[2]}")
    else:
        print("Совпадений нет")
    db.close()
    input("Нажмите Enter для выхода...")

def createReader():
    name = input("Введите имя: ")
    phone = input("Введите номер телефона: ")
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("""
        INSERT INTO readers (name, phone_number) 
        VALUES (?, ?)
    """, (name, phone))

    db.commit()
    db.close()

def editReader():
    name = input("Введите имя читателя: ")
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("SELECT id, name, phone_number FROM readers WHERE name = ?", (name,))
    r = c.fetchone()
    if not r:
        print("Читатель не найден")
        return
    print("0. Имя:", r[1])
    print("1. Телефон:", r[2])
    action = int(input("Ваш выбор: "))
    field = ["name", "phone_number"][action]
    new_value = input("Введите новое значение: ")
    c.execute(f"UPDATE readers SET {field} = ? WHERE id = ?", (new_value, r[0]))
    db.commit()
    db.close()
    input("Нажмите Enter для выхода...")

def deleteReader():
    name = input("Введите имя: ")
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("SELECT id FROM readers WHERE name = ?", (name,))
    r = c.fetchone()
    if r:
        c.execute("DELETE FROM readers WHERE id = ?", (r[0],))
        print("Читатель удалён")
    else:
        print("Читатель не найден")
    db.commit()
    db.close()
    input("Нажмите Enter для выхода...")

def showLoans():
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("""
        SELECT loans.id, readers.name, books.title, date_start, date_due, date_return, status 
        FROM loans
        JOIN readers ON loans.reader_id = readers.id
        JOIN books   ON loans.book_id = books.id
    """)
    for row in c.fetchall():
        print(*row)
    db.close()
    input("Нажмите Enter для выхода...")

def createLoan():
    name = input("Введите имя читателя: ")
    title = input("Введите название книги: ")
    date_start = input("Введите дату выдачи: ")
    date_due = input("Введите плановую дату возврата: ")
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("SELECT id FROM readers WHERE name = ?", (name,))
    reader = c.fetchone()
    c.execute("SELECT id, inventory_number FROM books WHERE title = ?", (title,))
    book = c.fetchone()
    if not reader or not book:
        print("Ошибка: читатель или книга не найдены")
        return
    if book[1] <= 0:
        print("Нет доступных экземпляров")
        return
    c.execute("""
        INSERT INTO loans (reader_id, book_id, date_start, date_due, status)
        VALUES (?, ?, ?, ?, 0)
    """, (reader[0], book[0], date_start, date_due))
    c.execute("UPDATE books SET inventory_number = ? WHERE id = ?",
              (book[1] - 1, book[0]))
    db.commit()
    db.close()
    input("Нажмите Enter для выхода...")

def showPersonLoans():
    name = input("Введите имя: ")
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("SELECT id FROM readers WHERE name = ?", (name,))
    reader = c.fetchone()
    if not reader:
        print("Читатель не найден")
        db.close()
        input("Нажмите Enter для выхода...")
        return
    reader_id = reader[0]
    c.execute("""
        SELECT loans.id, books.title, loans.date_start, loans.date_due, loans.date_return, loans.status
        FROM loans
        JOIN books ON loans.book_id = books.id
        WHERE loans.reader_id = ?
    """, (reader_id,))
    loans = c.fetchall()
    if not loans:
        print("У этого читателя нет выдач")
        db.close()
        input("Нажмите Enter для выхода...")
        return
    print("\nВыдачи читателя:")
    for loan in loans:
        loan_id, title, d_start, d_due, d_ret, status = loan
        status_text = "На руках" if status == 0 else "Возвращена"
        print(f"""ID выдачи: {loan_id}. Книга: {title}. Дата выдачи: {d_start}. Вернуть до: {d_due}. Дата возврата: {d_ret if d_ret else "-"}. Статус: {status_text}""")
    db.close()
    input("Нажмите Enter для выхода...")

def showPersonalLoans(name):
    print("Ваши выдачи:\n")
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("SELECT id FROM readers WHERE name = ?", (name,))
    reader = c.fetchone()
    if not reader:
        print("Читатель не найден")
        db.close()
        input("Нажмите Enter для выхода...")
        return
    reader_id = reader[0]
    c.execute("""
        SELECT loans.id, books.title, loans.date_start, loans.date_due, loans.date_return, loans.status
        FROM loans
        JOIN books ON loans.book_id = books.id
        WHERE loans.reader_id = ?
    """, (reader_id,))
    loans = c.fetchall()
    if not loans:
        print("У вас нет выдач")
        db.close()
        input("Нажмите Enter для выхода...")
        return
    for loan in loans:
        loan_id, title, d_start, d_due, d_ret, status = loan
        status_text = "На руках" if status == 0 else "Возвращена"
        print(f"""ID выдачи: {loan_id}. Книга: {title}. Дата выдачи: {d_start}. Вернуть до: {d_due}. Дата возврата: {d_ret if d_ret else '-'}. Статус: {status_text}""")
    db.close()
    input("Нажмите Enter для выхода...")

def editLoan():
    loan_id = int(input("Введите ID выдачи: "))
    date_return = input("Введите дату возврата: ")
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("SELECT book_id FROM loans WHERE id = ?", (loan_id,))
    loan = c.fetchone()
    if not loan:
        print("Выдача не найдена")
        return
    book_id = loan[0]
    c.execute("""
        UPDATE loans
        SET date_return = ?, status = 1
        WHERE id = ?
    """, (date_return, loan_id))
    c.execute("UPDATE books SET inventory_number = inventory_number + 1 WHERE id = ?", (book_id,))
    db.commit()
    db.close()

def generatePersonLoansFiles():
    name = str(input("Введите имя читателя: "))
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("SELECT id FROM readers WHERE name = ?", (name,))
    reader = c.fetchone()
    if not reader:
        print("Читатель не найден")
        db.close()
        return
    reader_id = reader[0]
    c.execute("""
        SELECT loans.id, books.title, loans.date_start, loans.date_due, loans.date_return, loans.status
        FROM loans
        JOIN books ON loans.book_id = books.id
        WHERE loans.reader_id = ?
    """, (reader_id,))
    loans = c.fetchall()
    db.close()
    if not loans:
        print("У читателя нет выдач")
        return
    loans_data = []
    for loan in loans:
        loan_id, title, d_start, d_due, d_ret, status = loan
        loans_data.append({
            "loan_id": loan_id,
            "title": title,
            "date_start": d_start,
            "date_due": d_due,
            "date_return": d_ret,
            "status": "Returned" if status else "Active"
        })
    folder = f"out/reader_{reader_id}"
    os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/loans.json", "w", encoding="utf-8") as f:
        json.dump(loans_data, f, indent=4, ensure_ascii=False)
    with open(f"{folder}/loans.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["loan_id", "title", "date_start", "date_due", "date_return", "status"])
        for loan in loans_data:
            writer.writerow(loan.values())
    root = ET.Element("loans")
    for loan in loans_data:
        entry = ET.SubElement(root, "loan")
        for key, value in loan.items():
            el = ET.SubElement(entry, key)
            el.text = str(value)
    tree = ET.ElementTree(root)
    tree.write(f"{folder}/loans.xml", encoding="utf-8", xml_declaration=True)
    with open(f"{folder}/loans.yaml", "w", encoding="utf-8") as f:
        yaml.dump(loans_data, f, allow_unicode=True)
    print(f"Файлы успешно созданы в каталоге: {folder}")
    input("Нажмите Enter для выхода...")

def menuLibrarian():
    print("Введите пароль:")
    if input() != open('src/main/resources/tochno_ne_parol.txt').readline().strip():
        print("Пароль неправильный")
        return
    while True:
        os.system('clear')
        print("=== МЕНЮ БИБЛИОТЕКАРЯ ===")
        print("1. Показать список книг")
        print("2. Найти книгу")
        print("3. Создать книгу")
        print("4. Редактировать книгу")
        print("5. Удалить книгу")
        print("6. Показать список читателей")
        print("7. Найти читателя")
        print("8. Создать читателя")
        print("9. Редактировать читателя")
        print("10. Удалить читателя")
        print("11. Показать список всех выдач")
        print("12. Показать выдачи конкретного читателя")
        print("13. Создать выдачу")
        print("14. Закрыть выдачу (возврат книги)")
        print("15. Создать файлы о читателе")
        print("16. Выход")
        try:
            action = int(input("Ваш выбор: "))
        except:
            continue
        if action == 1: showBooks()
        elif action == 2: readBook()
        elif action == 3: createBook()
        elif action == 4: editBook()
        elif action == 5: deleteBook()
        elif action == 6: showReaders()
        elif action == 7: readReader()
        elif action == 8: createReader()
        elif action == 9: editReader()
        elif action == 10: deleteReader()
        elif action == 11: showLoans()
        elif action == 12: showPersonLoans()
        elif action == 13: createLoan()
        elif action == 14: editLoan()
        elif action == 15: generatePersonLoansFiles()
        elif action == 16: break


def menuReader():
    name = input("Введите ваше имя: ")
    while True:
        os.system('clear')
        print("=== МЕНЮ ЧИТАТЕЛЯ ===")
        print("1. Показать список книг")
        print("2. Найти книгу")
        print("3. Показать мои выдачи")
        print("4. Выход")
        try:
            action = int(input("Ваш выбор: "))
        except:
            continue
        if action == 1: showBooks()
        elif action == 2: readBook()
        elif action == 3: showPersonalLoans(name)
        elif action == 4: break