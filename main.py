import json
import os
from datetime import datetime

DATA_FILE = 'books.json'

def load_books():
    """Загружает список книг из JSON-файла."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_books(books):
    """Сохраняет список книг в JSON-файл."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def add_book(books):
    """Добавление новой книги с проверкой дубликатов."""
    print("\n--- Добавление новой книги ---")
    author = input("Автор: ").strip()
    title = input("Название: ").strip()
    
    # Проверка на дубликаты (автор + название)
    for book in books:
        if book['author'].lower() == author.lower() and book['title'].lower() == title.lower():
            print("❌ Ошибка: Такая книга уже существует в трекере!")
            return

    # Валидация оценки
    while True:
        try:
            rating = int(input("Оценка (1-5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("❌ Оценка должна быть от 1 до 5.")
        except ValueError:
            print("❌ Введите целое число.")

    # Валидация даты
    while True:
        date_str = input("Дата прочтения (ГГГГ-ММ-ДД): ")
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("❌ Неверный формат даты. Используйте ГГГГ-ММ-ДД.")

    book = {
        "author": author,
        "title": title,
        "rating": rating,
        "date_read": date_str
    }
    books.append(book)
    save_books(books)
    print(f"✅ Книга '{title}' успешно добавлена!")

def show_all_books(books):
    """Вывод списка всех книг."""
    print("\n--- Список прочитанных книг ---")
    if not books:
        print("Список пуст.")
        return
    for i, book in enumerate(books, 1):
        print(f"{i}. {book['author']} - '{book['title']}' | Оценка: {book['rating']}/5 | Дата: {book['date_read']}")

def show_average_rating(books):
    """Расчёт и вывод средней оценки."""
    print("\n--- Средняя оценка ---")
    if not books:
        print("Нет данных для расчета.")
        return
    avg = sum(book['rating'] for book in books) / len(books)
    print(f"Средняя оценка по всем книгам: {avg:.2f}")

def show_author_stats(books):
    """Статистика по авторам."""
    print("\n--- Статистика по авторам ---")
    if not books:
        print("Нет данных.")
        return
    stats = {}
    for book in books:
        author = book['author']
        stats[author] = stats.get(author, 0) + 1
    for author, count in stats.items():
        print(f"{author}: {count} книг(а/и)")

def delete_book(books):
    """Удаление книги по номеру."""
    print("\n--- Удаление книги ---")
    if not books:
        print("Список пуст. Нечего удалять.")
        return
    
    for i, book in enumerate(books, 1):
        print(f"{i}. {book['author']} - '{book['title']}'")
        
    try:
        idx = int(input("Введите номер книги для удаления: ")) - 1
        if 0 <= idx < len(books):
            removed = books.pop(idx)
            save_books(books)
            print(f"✅ Книга '{removed['title']}' удалена.")
        else:
            print("❌ Неверный номер.")
    except ValueError:
        print("❌ Введите число.")

def main():
    """Главный цикл приложения."""
    books = load_books()
    while True:
        print("\n" + "="*30)
        print("ТРЕКЕР ПРОЧИТАННЫХ КНИГ")
        print("="*30)
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == '1':
            add_book(books)
        elif choice == '2':
            show_all_books(books)
        elif choice == '3':
            show_average_rating(books)
        elif choice == '4':
            show_author_stats(books)
        elif choice == '5':
            delete_book(books)
        elif choice == '6':
            print("До свидания!")
            break
        else:
            print("❌ Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()