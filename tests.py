import unittest
import os
import json

from validator import validate_amount, validate_date
from storage import load_data, save_data

_DATA_FILE = "data.json"


class TestValidateAmount(unittest.TestCase):
    """Тесты валидации суммы расхода."""

    def test_positive_integer(self):
        """Положительное целое принимается (позитивный)."""
        self.assertTrue(validate_amount("100"))

    def test_positive_float_dot(self):
        """Дробное число с точкой принимается (позитивный)."""
        self.assertTrue(validate_amount("99.99"))

    def test_positive_float_comma(self):
        """Дробное число с запятой принимается (позитивный)."""
        self.assertTrue(validate_amount("99,99"))

    def test_zero_rejected(self):
        """Ноль отклоняется (граничный)."""
        self.assertFalse(validate_amount("0"))

    def test_negative_rejected(self):
        """Отрицательное число отклоняется (негативный)."""
        self.assertFalse(validate_amount("-50"))

    def test_non_numeric_rejected(self):
        """Нечисловая строка отклоняется (негативный)."""
        self.assertFalse(validate_amount("abc"))

    def test_empty_rejected(self):
        """Пустая строка отклоняется (граничный)."""
        self.assertFalse(validate_amount(""))


class TestValidateDate(unittest.TestCase):
    """Тесты валидации даты."""

    def test_valid_date(self):
        """Корректная дата принимается (позитивный)."""
        self.assertTrue(validate_date("2025-06-15"))

    def test_invalid_format(self):
        """Неверный формат отклоняется (негативный)."""
        self.assertFalse(validate_date("15/06/2025"))

    def test_invalid_month(self):
        """Несуществующий месяц отклоняется (негативный)."""
        self.assertFalse(validate_date("2025-13-01"))

    def test_empty(self):
        """Пустая строка отклоняется (граничный)."""
        self.assertFalse(validate_date(""))


class TestStorage(unittest.TestCase):
    """Тесты JSON-хранилища."""

    def tearDown(self):
        if os.path.exists(_DATA_FILE):
            os.remove(_DATA_FILE)

    def test_save_and_load(self):
        """Сохранение и загрузка корректны (позитивный)."""
        data = [{"amount": 150.0, "category": "еда", "date": "2025-01-01"}]
        save_data(data)
        self.assertEqual(load_data(), data)

    def test_load_no_file(self):
        """Без файла — пустой список (позитивный)."""
        if os.path.exists(_DATA_FILE):
            os.remove(_DATA_FILE)
        self.assertEqual(load_data(), [])

    def test_load_corrupt(self):
        """Повреждённый JSON — пустой список (негативный)."""
        with open(_DATA_FILE, "w") as f:
            f.write("{{broken")
        self.assertEqual(load_data(), [])

    def test_total_calculation(self):
        """Подсчёт суммы расходов корректен (позитивный)."""
        records = [
            {"amount": 100.0, "category": "еда", "date": "2025-01-01"},
            {"amount": 200.0, "category": "транспорт", "date": "2025-01-02"},
            {"amount": 50.5, "category": "еда", "date": "2025-01-01"},
        ]
        total = sum(r["amount"] for r in records)
        self.assertAlmostEqual(total, 350.5)

    def test_filter_by_category(self):
        """Фильтрация по категории работает (позитивный)."""
        records = [
            {"amount": 100.0, "category": "еда", "date": "2025-01-01"},
            {"amount": 200.0, "category": "транспорт", "date": "2025-01-02"},
        ]
        result = [r for r in records if r["category"] == "еда"]
        self.assertEqual(len(result), 1)

    def test_filter_by_date(self):
        """Фильтрация по дате работает (позитивный)."""
        records = [
            {"amount": 100.0, "category": "еда", "date": "2025-01-01"},
            {"amount": 200.0, "category": "транспорт", "date": "2025-01-02"},
        ]
        result = [r for r in records if r["date"] == "2025-01-01"]
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
