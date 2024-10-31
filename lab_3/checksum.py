import re
import pandas as pd
import json
import hashlib
from typing import List

from file_path import CSV_FILE_PATH, JSON_PATH

def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.
    :param row_numbers: список целочисленных номеров строк csv-файла, на которых были найдены ошибки валидации
    :return: md5 хеш для проверки через github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Метод для обновления результатов в существующем файле result.json.
    :param variant: номер вашего варианта
    :param checksum: контрольная сумма, вычисленная через calculate_checksum()
    """
    try:
        with open(JSON_PATH, "r") as f:
            result_data = json.load(f)
        
        result_data["variant"] = variant
        result_data["checksum"] = checksum
        
        with open(JSON_PATH, "w") as f:
             f.write(json.dumps(result_data))
        
    except FileNotFoundError:
        print("Ошибка: файл не найден.")
    except json.JSONDecodeError:
        print("Ошибка: файл содержит некорректный JSON.")
    except Exception as e:
        print(f"Произошла ошибка при обновлении файла: {e}")


def process_csv(file_path: str) -> None:
    """
    Основная функция для загрузки, валидации данных и расчета контрольной суммы.
    param: file_path as str
    return: None
    """
    regex_patterns = {
        'column_1': r"^[\w\.-]+@[\w\.-]+\.\w+$",
        'column_2': r"^^\d{3}(?:\s\w+)+$",
        'column_3': r"^\d{11}$",
        'column_4': r"^\d{2}\s\d{2}\s\d{6}$",
        'column_5': r"^(\d{1,3}\.){3}\d{1,3}$",
        'column_6': r"^-?(?:180|\d{1,2}|1[0-7]\d)(\.\d+)?$",
        'column_7': r"^#([A-Fa-f0-9]{6})$",
        'column_8': r"(?:\d{3}-)?\d-\d{5}-\d{3}-\d",
        'column_9': r"^[a-z]{2}(-[a-z]{2})?$",
        'column_10': r"^\d{2}:\d{2}:\d{2}\.\d{1,}$"
    }
    try:
        data = pd.read_csv(CSV_FILE_PATH, encoding='utf-16', sep=';', header=0)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{CSV_FILE_PATH}' не найден.")
        return
    except pd.errors.EmptyDataError:
        print("Ошибка: Файл пуст.")
        return
    except pd.errors.ParserError:
        print("Ошибка: Неверный формат файла.")
        return
    
    data.columns = [f'column_{i+1}' for i in range(10)]

    error_rows = []

    for index, row in data.iterrows():
        row_has_error = False
        for col, pattern in regex_patterns.items():
            if not re.match(pattern, str(row[col])):
                row_has_error = True
                break
        if row_has_error:
            error_rows.append(index - 1)

    checksum = calculate_checksum(error_rows)
    serialize_result(variant="17", checksum=checksum)
    
    print(f"Количество невалидных записей: {len(error_rows)}")

    print("Контрольная сумма:", checksum)


if __name__ == "__main__":
    process_csv(CSV_FILE_PATH)
