import numpy as np
import os
from datetime import datetime


def generate_matrix(rows, cols, min_val=-50, max_val=50):
    """
    Генерация прямоугольной матрицы случайными целыми числами.

    Параметры:
        rows: количество строк (N)
        cols: количество столбцов (M)
        min_val: минимальное значение элемента (по умолчанию -50)
        max_val: максимальное значение элемента (по умолчанию 50)

    Возвращает: сгенерированная матрица размером rows x cols
    """
    # Генерация случайных целых чисел в заданном диапазоне
    matrix = np.random.randint(min_val, max_val + 1, size=(rows, cols))
    return matrix

def calculate_column_absolute_sums(matrix):
    """
    Вычисление суммы абсолютных значений элементов для каждого столбца.

    Параметры:
        matrix: исходная матрица

    Возвращает: массив сумм абсолютных значений для каждого столбца
    """
    # Вычисляем абсолютные значения элементов и суммируем по строкам (axis=0)
    abs_matrix = np.abs(matrix)
    column_sums = np.sum(abs_matrix, axis=0)
    return column_sums

def find_column_with_max_absolute_sum(column_sums):
    """
    Нахождение индекса столбца с максимальной суммой абсолютных значений.
    Если несколько столбцов имеют одинаковую сумму, выбирается первый.

    Параметры:
        column_sums: массив сумм по столбцам

    Возвращает:
        tuple: (индекс_столбца, максимальная_сумма)
    """
    # Находим максимальную сумму
    max_sum = np.max(column_sums)
    # Находим индекс первого столбца с максимальной суммой
    column_index = np.argmax(column_sums)

    return column_index, max_sum

def find_max_element_in_column(matrix, column_index):
    """
    Нахождение наибольшего элемента в указанном столбце матрицы.

    Параметры:
        matrix: - исходная матрица
        column_index: int - индекс столбца

    Возвращает:
        tuple: (наибольший_элемент, индекс_строки)
    """
    # Извлекаем указанный столбец
    column = matrix[:, column_index]
    # Находим максимальный элемент и его индекс
    max_element = np.max(column)
    row_index = np.argmax(column)

    return max_element, row_index

def save_results_to_file(filename, matrix, column_sums, target_column, max_element, element_position):
    """
    Сохранение исходных данных и результатов обработки в файл.

    Параметры:
        filename: имя файла для сохранения
        matrix: исходная матрица
        column_sums: массив сумм абсолютных значений по столбцам
        target_column: индекс целевого столбца
        max_element: наибольший элемент в целевом столбце
        element_position: позиция (строка) наибольшего элемента
    """
    with open(filename, 'w', encoding='utf-8') as file:
        # Записываем размер матрицы
        file.write(f"Размер матрицы: {matrix.shape[0]} строк x {matrix.shape[1]} столбцов\n\n")

        # Записываем исходную матрицу в отформатированном виде
        file.write("ИСХОДНАЯ МАТРИЦА A:\n")
        file.write("-" * 70 + "\n")

        # Заголовок столбцов
        header = "     " + "".join(f"Столбец {j + 1:3d}  " for j in range(matrix.shape[1]))
        file.write(header + "\n")
        file.write("     " + "-" * (11 * matrix.shape[1]) + "\n")

        # Записываем каждую строку матрицы
        for i in range(matrix.shape[0]):
            row_str = f"Строка {i + 1:2d}: "
            for j in range(matrix.shape[1]):
                row_str += f"{matrix[i, j]:7d}  "
            file.write(row_str + "\n")

        file.write("\n")

        # Записываем суммы абсолютных значений по столбцам
        file.write("СУММЫ АБСОЛЮТНЫХ ЗНАЧЕНИЙ ПО СТОЛБЦАМ:\n")
        for j, sum_val in enumerate(column_sums):
            file.write(f"  Столбец {j + 1}: сумма |элементов| = {sum_val}\n")

        file.write("\n")

        # Записываем результаты обработки
        file.write("РЕЗУЛЬТАТЫ ОБРАБОТКИ:\n")
        file.write(f"Столбец с максимальной суммой абсолютных значений: столбец {target_column + 1}\n")
        file.write(f"Максимальная сумма абсолютных значений: {column_sums[target_column]}\n")
        file.write(f"Наибольший элемент в этом столбце: {max_element}\n")
        file.write(f"Позиция наибольшего элемента: строка {element_position + 1}\n")

    print(f"Результаты успешно сохранены в файл: {filename}")

def print_matrix_with_highlight(matrix, target_column, max_element_row):
    """
    Вывод матрицы на экран с выделением целевого столбца и найденного элемента.

    Параметры:
        matrix: исходная матрица
        target_column: индекс целевого столбца
        max_element_row: индекс строки с наибольшим элементом
    """
    print("\nМатрица A (целевой столбец отмечен знаком *):")

    # Заголовок столбцов
    header = "     "
    for j in range(matrix.shape[1]):
        if j == target_column:
            header += f" *{j + 1:3d}  "
        else:
            header += f"  {j + 1:3d}  "
    print(header)
    print("     " + "-" * (7 * matrix.shape[1]))

    # Вывод строк матрицы
    for i in range(matrix.shape[0]):
        if i == max_element_row:
            row_str = f">Строка {i + 1:2d}: "
        else:
            row_str = f" Строка {i + 1:2d}: "

        for j in range(matrix.shape[1]):
            if j == target_column and i == max_element_row:
                row_str += f"[{matrix[i, j]:4d}] "
            elif j == target_column:
                row_str += f" {matrix[i, j]:4d}  "
            else:
                row_str += f" {matrix[i, j]:4d}  "

        if i == max_element_row:
            row_str += " ← наибольший элемент"
        print(row_str)

    print("-" * 60)

def get_matrix_dimensions():
    """
    Получение размеров матрицы от пользователя с обработкой ошибок.

    Возвращает:
        tuple: (количество строк, количество столбцов)
    """
    while True:
        try:
            print("\nВведите размеры прямоугольной матрицы:")
            rows = int(input("Количество строк (N): "))
            cols = int(input("Количество столбцов (M): "))

            if rows <= 0 or cols <= 0:
                print("Ошибка: размеры должны быть положительными числами. Попробуйте снова.")
                continue

            return rows, cols
        except ValueError:
            print("Ошибка: введите целые числа.")

def main():
    """
    Главная функция программы.
    """
    try:
        # Получение размеров матрицы
        N, M = get_matrix_dimensions()

        # Автоматическая генерация матрицы (по требованию задания)
        print(f"\nГенерируем матрицу размером {N}x{M} со случайными числами...")
        matrix = generate_matrix(N, M)

        # Вывод сгенерированной матрицы
        print("\nСгенерированная матрица:")
        print(matrix)

        # Вычисление сумм абсолютных значений по столбцам
        print("ХОД ВЫЧИСЛЕНИЙ:")

        print("\n1. Вычисляем сумму абсолютных значений для каждого столбца:")
        column_sums = calculate_column_absolute_sums(matrix)
        for j, sum_val in enumerate(column_sums):
            abs_values = [abs(matrix[i, j]) for i in range(N)]
            print(f"   Столбец {j + 1}: |{'| + |'.join(map(str, matrix[:, j]))}| = {sum_val}")

        # Нахождение столбца с максимальной суммой
        print("\n Находим столбец с максимальной суммой абсолютных значений:")
        target_column, max_sum = find_column_with_max_absolute_sum(column_sums)
        print(f"   Максимальная сумма = {max_sum} (столбец {target_column + 1})")

        # ШАГ 3: Нахождение наибольшего элемента в целевом столбце
        print(f"\n Находим наибольший элемент в столбце {target_column + 1}:")
        column_values = matrix[:, target_column]
        print(f"   Значения столбца: {column_values}")

        max_element, max_element_row = find_max_element_in_column(matrix, target_column)
        print(f"   Наибольший элемент = {max_element} (строка {max_element_row + 1})")

        # Вывод результатов
        print("ИТОГОВЫЙ РЕЗУЛЬТАТ:")
        print(f"Наибольший элемент столбца с максимальной суммой |элементов|: {max_element}")

        # Визуальное представление матрицы с выделением
        print_matrix_with_highlight(matrix, target_column, max_element_row)

        # Сохранение результатов в файл
        filename = f"matrix_results.txt"
        save_results_to_file(filename, matrix, column_sums, target_column, max_element, max_element_row)

        print("Программа успешно завершена!")

    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        import traceback
        traceback.print_exc()
        print("Программа будет завершена.")

# Точка входа в программу
if __name__ == "__main__":
    main()