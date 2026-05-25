import os
import csv
from abc import ABC, abstractmethod

class Person(ABC):
    """
    Абстрактный базовый класс Person (человек).
    Демонстрирует наследование.
    """

    def __init__(self, name, email):
        """
        Конструктор базового класса.

        Параметры:
            name: ФИО человека
            email: email человека
        """
        self._name = name
        self._email = email

    @property
    def name(self):
        """Геттер для имени"""
        return self._name

    @property
    def email(self):
        """Геттер для email"""
        return self._email

    def __setattr__(self, name, value):
        """
        Перегрузка __setattr__ для контроля записи свойств.
        Все свойства защищены - запись только через валидацию.
        """
        if name == '_name':
            if not value or not isinstance(value, str):
                raise ValueError("Имя должно быть непустой строкой!")
            object.__setattr__(self, name, value.strip())
        elif name == '_email':
            if not value or '@' not in value:
                raise ValueError("Email должен содержать символ '@'!")
            object.__setattr__(self, name, value.strip())
        else:
            object.__setattr__(self, name, value)

    @abstractmethod
    def get_info(self):
        """
        Абстрактный метод для получения информации о человеке.
        """
        pass

    def __repr__(self):
        """
        Перегрузка __repr__ для отладочного представления.
        """
        return f"{self.__class__.__name__}(name='{self._name}', email='{self._email}')"

    def __str__(self):
        """
        Перегрузка __str__ для строкового представления.
        """
        return f"{self._name} ({self._email})"

class Student(Person):
    """
    Класс Student (студент), наследуется от Person.
    Содержит информацию о студенте: номер, ФИО, email, группа.
    """

    # Статический счетчик для генерации ID (статическое поле)
    _id_counter = 1

    # Статический метод для получения следующего ID
    @staticmethod
    def get_next_id():
        """
        Статический метод для получения следующего ID студента.
        """
        current = Student._id_counter
        Student._id_counter += 1
        return current

    # Статический метод для валидации группы
    @staticmethod
    def validate_group(group):
        """
        Статический метод для проверки корректности группы.

        Параметры:
            group: название группы

        Возвращает:
            bool: True если группа корректна
        """
        return isinstance(group, str) and len(group) >= 2

    def __init__(self, student_id, name, email, group):
        """
        Конструктор класса Student.

        Параметры:
            student_id: номер студента
            name: ФИО
            email: email
            group: группа
        """
        super().__init__(name, email)
        self._student_id = student_id
        self._group = group

        # Обновляем статический счетчик, если ID больше текущего
        if student_id >= Student._id_counter:
            Student._id_counter = student_id + 1

    @property
    def student_id(self):
        """Геттер для номера студента"""
        return self._student_id

    @property
    def group(self):
        """Геттер для группы"""
        return self._group

    def __setattr__(self, name, value):
        """
        Перегрузка __setattr__ для контроля записи свойств в дочернем классе.
        """
        if name == '_student_id':
            if not isinstance(value, int) or value <= 0:
                raise ValueError("Номер студента должен быть положительным целым числом!")
            object.__setattr__(self, name, value)
        elif name == '_group':
            if not Student.validate_group(value):
                raise ValueError("Группа должна быть непустой строкой длиной не менее 2 символов!")
            object.__setattr__(self, name, value)
        else:
            super().__setattr__(name, value)

    def get_info(self):
        """
        Реализация абстрактного метода.
        """
        return f"Студент #{self._student_id}: {self._name}, группа {self._group}, email: {self._email}"

    def __repr__(self):
        """
        Перегрузка __repr__ для отладочного представления.
        """
        return f"Student(id={self._student_id}, name='{self._name}', email='{self._email}', group='{self._group}')"

    def __str__(self):
        """
        Перегрузка __str__ для строкового представления.
        """
        return f"{self._student_id:3d} | {self._name:35} | {self._email:25} | {self._group:^8}"

    def __eq__(self, other):
        """
        Перегрузка оператора == для сравнения студентов по ID.
        """
        if isinstance(other, Student):
            return self._student_id == other._student_id
        return False

    def __lt__(self, other):
        """
        Перегрузка оператора < для сортировки по ID.
        """
        if isinstance(other, Student):
            return self._student_id < other._student_id
        return NotImplemented

    def to_dict(self):
        """
        Преобразование студента в словарь для сохранения в CSV.

        Возвращает:
            dict: словарь с данными студента
        """
        return {
            '№': self._student_id,
            'ФИО': self._name,
            'email': self._email,
            'группа': self._group
        }

    @classmethod
    def from_dict(cls, data):
        """
        Классовый метод для создания студента из словаря.

        Параметры:
            data: словарь с данными студента

        Возвращает:
            Student: новый объект студента
        """
        return cls(data['№'], data['ФИО'], data['email'], data['группа'])

class StudentCollection:
    """
    Класс-контейнер для коллекции студентов.
    Реализует итератор, доступ по индексу, генераторы.
    """

    def __init__(self):
        """
        Конструктор коллекции студентов.
        """
        self._students = []
        self._index = 0  # для итератора

    def add_student(self, student):
        """
        Добавление студента в коллекцию.

        Параметры:
            student: объект Student или GraduateStudent
        """
        if not isinstance(student, Student):
            raise TypeError("Можно добавлять только объекты типа Student или его наследников")
        self._students.append(student)

    def remove_student(self, student_id):
        """
        Удаление студента по ID.

        Параметры:
            student_id: номер студента

        Возвращает:
            bool: True если удаление успешно
        """
        for i, student in enumerate(self._students):
            if student.student_id == student_id:
                del self._students[i]
                return True
        return False

    def get_student(self, student_id):
        """
        Получение студента по ID.

        Параметры:
            student_id: номер студента

        Возвращает:
            Student: найденный студент или None
        """
        for student in self._students:
            if student.student_id == student_id:
                return student
        return None

    def __getitem__(self, index):
        """
        Перегрузка __getitem__ для доступа к элементам коллекции по индексу.

        Параметры:
            index: индекс или срез

        Возвращает:
            студента или список студентов
        """
        if isinstance(index, slice):
            return self._students[index]
        if isinstance(index, int):
            if 0 <= index < len(self._students):
                return self._students[index]
            raise IndexError(f"Индекс {index} вне диапазона (0-{len(self._students) - 1})")
        raise TypeError(f"Неверный тип индекса: {type(index)}")

    def __len__(self):
        """
        Перегрузка len() для получения количества студентов.
        """
        return len(self._students)

    def __iter__(self):
        """
        Перегрузка __iter__ для создания итератора.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Перегрузка __next__ для реализации итератора.
        """
        if self._index < len(self._students):
            result = self._students[self._index]
            self._index += 1
            return result
        raise StopIteration

    def __repr__(self):
        """
        Перегрузка __repr__ для отладочного представления коллекции.
        """
        return f"StudentCollection(students={self._students})"

    def __str__(self):
        """
        Перегрузка __str__ для строкового представления коллекции.
        """
        if not self._students:
            return "Коллекция пуста"

        result = "\n" + "=" * 95 + "\n"
        result += f"{'№':^6} | {'ФИО':^35} | {'email':^25} | {'Группа':^8}\n"
        result += "-" * 95 + "\n"
        for student in self._students:
            result += str(student) + "\n"
        result += "=" * 95 + f"\nВсего студентов: {len(self._students)}\n"
        return result

    # ======================== ГЕНЕРАТОРЫ ========================

    def filter_by_group(self, group):
        """
        Генератор для фильтрации студентов по группе.

        Параметры:
            group: название группы

        Yields:
            Student: студенты из указанной группы
        """
        for student in self._students:
            if student.group == group:
                yield student

    def filter_by_id_range(self, min_id, max_id):
        """
        Генератор для фильтрации студентов по диапазону ID.

        Параметры:
            min_id: минимальный ID
            max_id: максимальный ID

        Yields:
            Student: студенты в указанном диапазоне
        """
        for student in self._students:
            if min_id <= student.student_id <= max_id:
                yield student

    def sorted_by_name(self, reverse=False):
        """
        Генератор для получения студентов в отсортированном по имени порядке.

        Параметры:
            reverse: сортировка в обратном порядке

        Yields:
            Student: студенты в отсортированном порядке
        """
        sorted_students = sorted(self._students, key=lambda s: s.name, reverse=reverse)
        for student in sorted_students:
            yield student


    def get_all_info(self):
        """
        Генератор для получения информации о каждом студенте.

        Yields:
            str: строка с информацией о студенте
        """
        for student in self._students:
            yield student.get_info()

class CSVStudentManager:
    """
    Класс для управления чтением и записью студентов в CSV-файл.
    """

    @staticmethod
    def read_from_csv(filename):
        """
        Статический метод для чтения студентов из CSV-файла.

        Параметры:
            filename: имя CSV-файла

        Возвращает:
            StudentCollection: коллекция студентов
        """
        collection = StudentCollection()

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    student = Student(
                        int(row['№']),
                        row['ФИО'],
                        row['email'],
                        row['группа']
                    )
                    collection.add_student(student)

            print(f"Файл '{filename}' успешно загружен. Загружено {len(collection)} записей.")
            return collection

        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}' не найден!")
            return collection
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return collection

    @staticmethod
    def write_to_csv(filename, collection):
        """
        Статический метод для записи студентов в CSV-файл.

        Параметры:
            filename: имя CSV-файла
            collection: коллекция студентов
        """
        try:

            fieldnames = ['№', 'ФИО', 'email', 'группа']

            with open(filename, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                for student in collection:
                    writer.writerow(student.to_dict())

            print(f"Данные успешно сохранены в файл '{filename}'. Сохранено {len(collection)} записей.")

        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

def count_files_in_directory(directory_path):
    """
    Подсчет количества файлов в указанной директории.

    Параметры:
        directory_path: путь к директории

    Возвращает:
        int: количество файлов
    """
    try:
        if not os.path.exists(directory_path):
            print(f"Ошибка: Директория '{directory_path}' не существует!")
            return 0

        if not os.path.isdir(directory_path):
            print(f"Ошибка: '{directory_path}' не является директорией!")
            return 0

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

def main():
    """
    Главная функция программы.
    """
    print("=" * 95)
    print("ПРОГРАММА ДЛЯ РАБОТЫ СО СТУДЕНТАМИ (ООП-ВЕРСИЯ)")
    print("=" * 95)

    # ========== ЧАСТЬ 1: Подсчет файлов в директории ==========
    print("\n--- ЧАСТЬ 1: Подсчет файлов в директории ---")
    directory = input("Введите путь к директории (или Enter для текущей): ").strip()
    if not directory:
        directory = "."

    file_count = count_files_in_directory(directory)
    print(f"Количество файлов в директории '{directory}': {file_count}")

    # ========== ЧАСТЬ 2: Работа с CSV-файлом ==========
    print("\n--- ЧАСТЬ 2: Работа с CSV-файлом ---")

    # Проверяем наличие файла
    if not os.path.exists('data.csv'):
        print("Файл data.csv не найден")
        return

    # Чтение данных из CSV
    collection = CSVStudentManager.read_from_csv('data.csv')

    # ========== Демонстрация возможностей ООП ==========
    print("\n" + "=" * 95)
    print("ДЕМОНСТРАЦИЯ ВОЗМОЖНОСТЕЙ ООП")
    print("=" * 95)

    # 1. Демонстрация __str__ и __repr__
    print("\n1. Демонстрация __str__ (вывод коллекции):")
    print(collection)

    print("\n2. Демонстрация __repr__ (отладочное представление):")
    for student in collection[:3]:  # берем первых 3 студентов
        print(f"   {repr(student)}")

    # 2. Демонстрация __getitem__ (доступ по индексу)
    print("\n3. Демонстрация __getitem__ (доступ по индексу):")
    print(f"   Первый студент: {collection[0].name}")
    print(f"   Третий студент: {collection[2].name}")

    # 3. Демонстрация итератора
    print("\n4. Демонстрация итератора (проход по коллекции):")
    for i, student in enumerate(collection):
        if i >= 3:
            print("   ...")
            break
        print(f"   {i + 1}. {student.name}")

    # 4. Демонстрация статических методов
    print("\n5. Демонстрация статических методов:")
    print(f"   Валидация группы 'ИС-21': {Student.validate_group('ИС-21')}")
    print(f"   Валидация группы '': {Student.validate_group('')}")
    print(f"   Следующий ID студента: {Student.get_next_id()}")

    # 5. Демонстрация __setattr__ (контроль записи свойств)
    print("\n6. Демонстрация __setattr__ (попытка установить неверные значения):")
    try:
        invalid_student = Student(0, "Тест", "test@mail.ru", "ГР-01")
    except ValueError as e:
        print(f"   Ошибка при создании: {e}")

    # 6. Демонстрация генераторов
    print("\n7. Демонстрация генераторов:")

    print("\n   а) Фильтрация по группе 'ИС-21':")
    for student in collection.filter_by_group('ИС-21'):
        print(f"      {student.name}")

    print("\n   б) Сортировка по имени (генератор):")
    for student in collection.sorted_by_name():
        print(f"      {student.name}")

    print("\n   в) Информация о студентах (генератор):")
    for info in collection.get_all_info():
        print(f"      {info}")

    # ========== ИНТЕРАКТИВНОЕ МЕНЮ ==========
    while True:
        print("\n" + "-" * 50)
        print("МЕНЮ ОБРАБОТКИ ДАННЫХ")
        print("-" * 50)
        print("1. Вывести всех студентов")
        print("2. Сортировка по строковому полю (ФИО)")
        print("3. Сортировка по числовому полю (№ студента)")
        print("4. Фильтрация по группе")
        print("5. Добавить нового студента")
        print("6. Добавить аспиранта")
        print("7. Удалить студента")
        print("8. Найти студента по индексу")
        print("9. Сохранить данные в файл")
        print("0. Выход")

        choice = input("\nВаш выбор: ").strip()

        if choice == '1':
            print(collection)

        elif choice == '2':
            print("\nСтуденты, отсортированные по ФИО:")
            print("=" * 95)
            for student in collection.sorted_by_name():
                print(student)
            print("=" * 95)

        elif choice == '3':
            print("\nСтуденты, отсортированные по номеру:")
            print("=" * 95)
            sorted_by_id = sorted(collection, key=lambda s: s.student_id)
            for student in sorted_by_id:
                print(student)
            print("=" * 95)

        elif choice == '4':
            group = input("Введите название группы: ").strip()
            print(f"\nСтуденты группы '{group}':")
            print("=" * 95)
            for student in collection.filter_by_group(group):
                print(student)
            print("=" * 95)

        elif choice == '5':
            try:
                student_id = Student.get_next_id()
                name = input("Введите ФИО: ").strip()
                email = input("Введите email: ").strip()
                group = input("Введите группу: ").strip()

                new_student = Student(student_id, name, email, group)
                collection.add_student(new_student)
                print(f"Студент #{student_id} успешно добавлен!")
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == '6':
            try:
                student_id = int(input("Введите номер студента для удаления: "))
                if collection.remove_student(student_id):
                    print(f"Студент #{student_id} удален!")
                else:
                    print(f"Студент #{student_id} не найден!")
            except ValueError:
                print("Ошибка: введите целое число!")

        elif choice == '7':
            try:
                index = int(input(f"Введите индекс (0-{len(collection) - 1}): "))
                student = collection[index]
                print(f"Студент по индексу {index}:")
                print(student)
                print(f"Информация: {student.get_info()}")
            except IndexError as e:
                print(f"Ошибка: {e}")
            except ValueError:
                print("Ошибка: введите целое число!")

        elif choice == '8':
            CSVStudentManager.write_to_csv('data.csv', collection)

        elif choice == '9':
            save = input("Сохранить изменения перед выходом? (y/n): ")
            if save.lower() == 'y':
                CSVStudentManager.write_to_csv('data.csv', collection)
            print("Программа завершена!")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите пункт от 1 до 9.")

if __name__ == "__main__":
    main()