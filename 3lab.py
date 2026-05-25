import os
import csv
from datetime import datetime
import chardet

def detect_encoding(filename):
    """Определение кодировки файла."""
    with open(filename, 'rb') as file:
        raw_data = file.read(10000)  # Читаем первые 10000 байт для определения
        result = chardet.detect(raw_data)
        return result['encoding']

def count_files_in_directory(directory_path):
    """
    Подсчет количества файлов в указанной директории (без учета подпапок).

    Параметры:
        directory_path: путь к директории

    Возвращает:
        int: количество файлов
    """
    try:
        # Проверяем, существует ли директория
        if not os.path.exists(directory_path):
            print(f"Ошибка: Директория '{directory_path}' не существует!")
            return 0

        # Проверяем, является ли путь директорией
        if not os.path.isdir(directory_path):
            print(f"Ошибка: '{directory_path}' не является директорией!")
            return 0

        # Подсчитываем количество файлов (игнорируем поддиректории)
        file_count = 0
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                file_count += 1

        return file_count

    except PermissionError:
        print(f"Ошибка: Нет доступа к директории '{directory_path}'!")
        return 0
    except Exception as e:
        print(f"Ошибка при подсчете файлов: {e}")
        return 0

def read_students_from_csv(filename):
    """
    Чтение данных студентов из CSV-файла и преобразование в словарь.

    Параметры:
        filename: имя CSV-файла

    Возвращает:
        dict: словарь с данными студентов (ключ - № студента)
               и список ключей для сохранения порядка
    """
    students = {}
    fieldnames = []

    try:
        encoding = detect_encoding(filename)

        with open(filename, 'r', encoding=encoding) as file:
            # Используем DictReader для чтения CSV в словарь
            reader = csv.DictReader(file, delimiter=';')
            fieldnames = reader.fieldnames

            print(f"Заголовки столбцов: {reader.fieldnames}")

            for row in reader:
                # Преобразуем номер студента в целое число для числовой сортировки
                student_id = int(row['№'])
                students[student_id] = {
                    '№': student_id,
                    'ФИО': row['ФИО'],
                    'email': row['email'],
                    'группа': row['группа']
                }

        print(f"Файл '{filename}' успешно загружен.")
        return students, fieldnames

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден!")
        return {}, []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return {}, []

def save_students_to_csv(filename, students, fieldnames):
    """
    Сохранение данных студентов обратно в CSV-файл.

    Параметры:
        filename: имя CSV-файла
        students: словарь с данными студентов
        fieldnames: список заголовков столбцов
    """
    try:

        encoding = detect_encoding(filename)

        with open(filename, 'w', encoding=encoding, newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()

            # Сортируем студентов по номеру для сохранения в файл
            for student_id in sorted(students.keys()):
                writer.writerow(students[student_id])

        print(f"Данные успешно сохранены в файл '{filename}'.")

    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

def sort_students_by_string_field(students, field_name):
    """
    Сортировка студентов по строковому полю (например, по ФИО или группе).

    Параметры:
        students: словарь с данными студентов
        field_name: имя поля для сортировки

    Возвращает:
        list: отсортированный список студентов
    """
    # Преобразуем словарь в список для сортировки
    student_list = list(students.values())
    # Сортируем по указанному строковому полю
    student_list.sort(key=lambda x: x[field_name])
    return student_list

def sort_students_by_numeric_field(students, field_name='№'):
    """
    Сортировка студентов по числовому полю (по номеру студента).

    Параметры:
        students: словарь с данными студентов
        field_name: имя поля для сортировки (обычно '№')

    Возвращает:
        list: отсортированный список студентов
    """
    student_list = list(students.values())
    # Сортируем по числовому полю
    student_list.sort(key=lambda x: x[field_name])
    return student_list

def filter_students_by_criteria(students, field_name, criteria_value):
    """
    Фильтрация студентов по заданному критерию.

    Параметры:
        students: словарь с данными студентов
        field_name: имя поля для фильтрации
        criteria_value: значение для фильтрации

    Возвращает:
        list: отфильтрованный список студентов
    """
    filtered_students = []

    for student in students.values():
        if student[field_name] == criteria_value:
            filtered_students.append(student)

    return filtered_students

def print_students_table(students_list):
    """
    Вывод списка студентов в виде таблицы.

    Параметры:
        students_list: список студентов для вывода
        title: заголовок таблицы
    """
    if not students_list:
        print("Нет данных для отображения.")
        return

    print("=" * 90)
    print(f"{'№':^6} | {'ФИО':^35} | {'email':^25} | {'Группа':^10}")
    print("-" * 90)

    for student in students_list:
        print(f"{student['№']:^6} | {student['ФИО']:35} | {student['email']:25} | {student['группа']:^10}")

    print("=" * 90)
    print(f"Всего студентов: {len(students_list)}")
    print("=" * 90)

def add_new_student(students, next_id):
    """
    Добавление нового студента.

    Параметры:
        students: словарь с данными студентов
        next_id: следующий доступный номер

    Возвращает:
        bool: True если добавление успешно
    """
    print("\n--- Добавление нового студента ---")

    try:
        # Ввод данных нового студента
        full_name = input("Введите ФИО студента: ").strip()
        if not full_name:
            print("Ошибка: ФИО не может быть пустым!")
            return False

        email = input("Введите email студента: ").strip()
        if not email:
            print("Ошибка: email не может быть пустым!")
            return False

        group = input("Введите группу студента: ").strip()
        if not group:
            print("Ошибка: группа не может быть пустой!")
            return False

        # Добавляем студента
        students[next_id] = {
            '№': next_id,
            'ФИО': full_name,
            'email': email,
            'группа': group
        }

        print(f"Студент успешно добавлен с номером {next_id}!")
        return True

    except Exception as e:
        print(f"Ошибка при добавлении студента: {e}")
        return False

def edit_student(students, student_id):
    """
    Редактирование данных студента.

    Параметры:
        students: словарь с данными студентов
        student_id: номер студента для редактирования
    """
    if student_id not in students:
        print(f"Студент с номером {student_id} не найден!")
        return

    print(f"\n--- Редактирование студента №{student_id} ---")
    student = students[student_id]

    print(f"Текущие данные: ФИО: {student['ФИО']}, email: {student['email']}, группа: {student['группа']}")

    # Ввод новых данных (оставьте пустым, чтобы не менять)
    new_name = input("Новое ФИО (Enter - оставить без изменений): ").strip()
    if new_name:
        student['ФИО'] = new_name

    new_email = input("Новый email (Enter - оставить без изменений): ").strip()
    if new_email:
        student['email'] = new_email

    new_group = input("Новая группа (Enter - оставить без изменений): ").strip()
    if new_group:
        student['группа'] = new_group

    print("Данные студента успешно обновлены!")

def delete_student(students, student_id):
    """
    Удаление студента.

    Параметры:
        students: словарь с данными студентов
        student_id: номер студента для удаления
    """
    if student_id not in students:
        print(f"Студент с номером {student_id} не найден!")
        return

    confirm = input(f"Вы уверены, что хотите удалить студента №{student_id}? (y/n): ")
    if confirm.lower() == 'y':
        del students[student_id]
        print(f"Студент №{student_id} успешно удален!")
    else:
        print("Удаление отменено.")

def main():
    """
    Главная функция программы.
    """

    print("Подсчет файлов в директории")

    # Запрашиваем путь к директории
    directory = input("Введите путь к директории (или Enter для текущей): ").strip()
    if not directory:
        directory = "."

    file_count = count_files_in_directory(directory)
    print(f"Количество файлов в директории '{directory}': {file_count}")

    print("Работа с CSV-файлом студентов")
    csv_filename = "data.csv"

    # Читаем данные из файла
    students, fieldnames = read_students_from_csv(csv_filename)

    if not students:
        print("Нет данных для обработки. Создайте файл data.csv с данными студентов.")
        return

    while True:
        print("1. Вывести всех студентов")
        print("2. Сортировка по строковому полю (ФИО)")
        print("3. Сортировка по числовому полю (№ студента)")
        print("4. Фильтрация по группе")
        print("5. Добавить нового студента")
        print("6. Редактировать студента")
        print("7. Удалить студента")
        print("8. Сохранить данные в файл")
        print("9. Выход")

        choice = input("\nВаш выбор: ").strip()

        if choice == '1':
            # Вывод всех студентов
            all_students = list(students.values())
            all_students.sort(key=lambda x: x['№'])
            print_students_table(all_students)

        elif choice == '2':
            # Сортировка по строковому полю (ФИО)
            sorted_students = sort_students_by_string_field(students, 'ФИО')
            print_students_table(sorted_students)

        elif choice == '3':
            # Сортировка по числовому полю (№ студента)
            sorted_students = sort_students_by_numeric_field(students, '№')
            print_students_table(sorted_students)

        elif choice == '4':
            # Фильтрация по группе
            group = input("Введите название группы для фильтрации: ").strip()
            filtered_students = filter_students_by_criteria(students, 'группа', group)
            print_students_table(filtered_students)

        elif choice == '5':
            # Добавление нового студента
            next_id = max(students.keys()) + 1 if students else 1
            add_new_student(students, next_id)

        elif choice == '6':
            # Редактирование студента
            try:
                student_id = int(input("Введите номер студента для редактирования: "))
                edit_student(students, student_id)
            except ValueError:
                print("Ошибка: введите целое число!")

        elif choice == '7':
            # Удаление студента
            try:
                student_id = int(input("Введите номер студента для удаления: "))
                delete_student(students, student_id)
            except ValueError:
                print("Ошибка: введите целое число!")

        elif choice == '8':
            # Сохранение данных в файл
            save_students_to_csv(csv_filename, students, fieldnames)

        elif choice == '9':
            # Выход
            print("Программа завершена!")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите пункт от 0 до 9.")

if __name__ == "__main__":
    # Проверяем наличие файла data.csv, если нет - создаем пример
    if not os.path.exists('data.csv'):
        print("Файл data.csv не найден")

    main()