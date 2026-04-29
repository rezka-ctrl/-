import re
from datetime import datetime


def validate_amount(amount_str: str) -> bool:
    """
    Проверяет, что строка представляет положительное число (сумма расхода).

    Args:
        amount_str: Строка с суммой.

    Returns:
        bool: True если сумма > 0.
    """
    try:
        value = float(amount_str.strip().replace(",", "."))
        return value > 0
    except ValueError:
        return False


def validate_date(date_str: str) -> bool:
    """
    Проверяет, что строка является датой в формате YYYY-MM-DD.

    Args:
        date_str: Строка с датой.

    Returns:
        bool: True если формат корректен.
    """
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str.strip()):
        return False
    try:
        datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False
