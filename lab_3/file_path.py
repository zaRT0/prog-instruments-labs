CSV_FILE_PATH = "lab_3/17.csv"
JSON_PATH = "lab_3/result.json"
REGEX_PATTERNS = {
        'column_1': r"^[\w\.-]+@[\w\.-]+\.\w+$",
        'column_2': r"^\d{3}(?:\s\w+)+$",
        'column_3': r"^\d{11}$",
        'column_4': r"^\d{2}\s\d{2}\s\d{6}$",
        'column_5': r"^(\d{1,3}\.){3}\d{1,3}$",
        'column_6': r"^-?(?:180|\d{1,2}|1[0-7]\d)(\.\d+)?$",
        'column_7': r"^#([A-Fa-f0-9]{6})$",
        'column_8': r"(?:\d{3}-)?\d-\d{5}-\d{3}-\d",
        'column_9': r"^[a-z]{2}(-[a-z]{2})?$",
        'column_10': r"^\d{2}:\d{2}:\d{2}\.\d{1,}$"
    }