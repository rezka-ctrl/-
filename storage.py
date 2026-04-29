import json
import os

DATA_FILE = "data.json"


def load_data() -> list:
    """
    Загружает список расходов из файла data.json.

    Returns:
        list: Список записей. Пустой список при отсутствии файла или ошибке.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_data(records: list) -> None:
    """
    Сохраняет список расходов в файл data.json.

    Args:
        records: Список записей для сохранения.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=2)
