import re
import pandas as pd
import json
import hashlib
from typing import List

from file_path import CSV_FILE_PATH, JSON_PATH, REGEX_PATTERNS


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


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Загружает CSV файл и обрабатывает возможные исключения.
    param: file_path as str
    return: data
    """
    try:
        data = pd.read_csv(CSV_FILE_PATH, encoding='utf-16', sep=';', header=0)
        return data
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
    except pd.errors.EmptyDataError:
        print("Ошибка: Файл пуст.")
    except pd.errors.ParserError:
        print("Ошибка: Неверный формат файла.")
    return None


def process_data(file_path: str) -> list:
    """
    Функция для загрузки, валидации данных и расчета контрольной суммы.
    param: file_path as str
    return: error_rows as list
    """
    data = load_csv(file_path)

    data.columns = [f'column_{i+1}' for i in range(10)]
    
    error_rows = []
    
    for index, row in data.iterrows():
        row_has_error = False
        for col, pattern in REGEX_PATTERNS.items():
            if not re.match(pattern, str(row[col])):
                row_has_error = True
                break
        if row_has_error:
            error_rows.append(index)
    
    return error_rows


def process_main(file_path: str) -> None:
    """
    Основная функция.
    param: file_path as str
    return: None
    """
    rows = process_data(file_path)
    checksum = calculate_checksum(rows)
    
    serialize_result(variant="17", checksum=checksum)
    
    print(f"Количество невалидных записей: {len(rows)}")
    print("Контрольная сумма:", checksum)


if __name__ == "__main__":
    process_main(CSV_FILE_PATH)
