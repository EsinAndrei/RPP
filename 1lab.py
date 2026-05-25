import random


def input_from_keyboard():
    """
    Ввод списка с клавиатуры
    """
    while True:
        try:
            # Ввод строки с числами
            input_str = input("Введите числа через пробел: ")
            # Разбиваем строку на части и преобразуем в целые числа
            numbers = list(map(int, input_str.split()))

            if len(numbers) == 0:
                print("Список не может быть пустым. Попробуйте снова.")
                continue

            return numbers
        except ValueError:
            print("Ошибка: введите только целые числа, разделенные пробелами.")

def generate_random_list():
    """
    Автоматическая генерация случайного списка
    """
    while True:
        try:
            # Запрос размера списка
            size = input("Введите размер списка (целое положительное число): ")
            size = int(size)

            if size <= 0:
                print("Размер списка должен быть положительным числом.")
                continue

            # Генерация случайных чисел от 0 до 20
            return [random.randint(0, 20) for _ in range(size)]
        except ValueError:
            print("Ошибка: введите целое число.")

def print_list(lst):
    """
    Вывод списка на экран
    """
    print(" ".join(map(str, lst)))

def remove_longest_even_chain_without_standard(lst):
    """
    Удаление самой длинной цепочки четных элементов
    БЕЗ использования стандартных функций (max, len, remove и т.д.)

    Алгоритм:
    1. Находим все цепочки четных элементов и их длину
    2. Определяем максимальную длину цепочки
    3. Удаляем первую найденную цепочку максимальной длины
    """
    if not lst:  # Если список пуст
        return

    # Этап 1: Находим все цепочки четных элементов
    # Проходим по списку и ищем непрерывные последовательности четных чисел
    chains = []  # Список кортежей (индекс_начала, длина)
    i = 0
    length = len(lst)

    while i < length:
        # Если текущий элемент четный
        if lst[i] % 2 == 0:
            start_index = i
            chain_length = 0

            # Считаем длину цепочки четных элементов
            j = i
            while j < length and lst[j] % 2 == 0:
                chain_length += 1
                j += 1

            # Сохраняем информацию о цепочке
            chains.append((start_index, chain_length))
            i = j  # Перемещаем указатель за конец цепочки
        else:
            i += 1

    # Если нет ни одной цепочки четных элементов
    if not chains:
        return

    # Этап 2: Находим максимальную длину цепочки (без использования max)
    max_length = chains[0][1]  # Берем длину первой цепочки как начальный максимум
    for _, chain_len in chains:
        if chain_len > max_length:
            max_length = chain_len

    # Этап 3: Находим первую цепочку с максимальной длиной
    start_to_remove = -1
    for start, chain_len in chains:
        if chain_len == max_length:
            start_to_remove = start
            break

    # Этап 4: Удаляем цепочку (без использования remove, pop, среза)
    # Создаем новый список вручную
    new_list = []
    i = 0
    while i < length:
        # Если мы в зоне удаления - пропускаем эти элементы
        if i == start_to_remove:
            i += max_length  # Прыгаем через удаляемую цепочку
        else:
            new_list.append(lst[i])
            i += 1

    # Очищаем исходный список и заполняем новыми значениями
    lst.clear()
    lst.extend(new_list)

def remove_longest_even_chain_with_standard(lst):
    """
    Удаление самой длинной цепочки четных элементов
    С использованием стандартных функций (len, max, срезы)

    Алгоритм:
    1. Находим все цепочки четных элементов и их длину
    2. Определяем максимальную длину цепочки
    3. Удаляем первую найденную цепочку максимальной длины
    """
    if not lst:  # Если список пуст
        return

    # Этап 1: Находим все цепочки четных элементов
    chains = []  # Список кортежей (индекс_начала, длина)
    i = 0
    length = len(lst)

    while i < length:
        if lst[i] % 2 == 0:
            start_index = i
            chain_length = 0

            # Считаем длину цепочки четных элементов
            while i < length and lst[i] % 2 == 0:
                chain_length += 1
                i += 1

            chains.append((start_index, chain_length))
        else:
            i += 1

    # Если нет ни одной цепочки четных элементов
    if not chains:
        return

    # Этап 2: Находим максимальную длину цепочки (с использованием max)
    # max_length = max(chain_len for _, chain_len in chains)
    # Альтернативный вариант с использованием стандартных функций:
    max_length = max(chains, key=lambda x: x[1])[1]

    # Этап 3: Находим первую цепочку с максимальной длиной
    # start_to_remove = next(start for start, chain_len in chains if chain_len == max_length)
    # Альтернативный вариант:
    start_to_remove = None
    for start, chain_len in chains:
        if chain_len == max_length:
            start_to_remove = start
            break

    # Этап 4: Удаляем цепочку (с использованием среза)
    del lst[start_to_remove:start_to_remove + max_length]

def get_method():
    """
    Выбор способа ввода списка
    """
    while True:
        print("\nВыберите способ ввода:")
        print("1. Ввод с клавиатуры")
        print("2. Автоматическая генерация")

        choice = input("Ваш выбор (1 или 2): ")

        if choice == '1':
            return 'keyboard'
        elif choice == '2':
            return 'random'
        else:
            print("Ошибка: введите 1 или 2.")

def main():
    """
    Главная функция программы
    """
    print("=" * 50)
    print("Программа: Удаление самой длинной цепочки четных элементов")
    print("=" * 50)

    try:
        # Выбор способа ввода
        method = get_method()

        # Ввод списка
        if method == 'keyboard':
            original_list = input_from_keyboard()
        else:  # random
            original_list = generate_random_list()

        # Вывод исходного списка
        print("\nИсходный список:")
        print_list(original_list)

        # Создание копий для двух методов
        list_without_standard = original_list.copy()
        list_with_standard = original_list.copy()

        # Применение метода БЕЗ стандартных функций
        print("\n" + "-" * 50)
        print("Метод 1: Без использования стандартных функций")
        remove_longest_even_chain_without_standard(list_without_standard)
        print("Результат:")
        print_list(list_without_standard)

        # Применение метода СО стандартными функциями
        print("\n" + "-" * 50)
        print("Метод 2: С использованием стандартных функций")
        remove_longest_even_chain_with_standard(list_with_standard)
        print("Результат:")
        print_list(list_with_standard)

        # Демонстрация работы на примере из задания
        print("\n" + "=" * 50)
        print("Проверка на примере из задания:")
        example = [4, 1, 4, 2, 1, 2, 4, 6]
        print(f"Исходный список: {example}")

        example_copy = example.copy()
        remove_longest_even_chain_with_standard(example_copy)
        print(f"Результат: {example_copy}")
        print("Ожидаемый результат: [4, 1, 4, 2, 1]")

    except Exception as e:
        print(f"\nНепредвиденная ошибка: {e}")


# Точка входа в программу
if __name__ == "__main__":
    main()