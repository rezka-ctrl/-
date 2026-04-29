import tkinter as tk
from tkinter import ttk, messagebox

from validator import validate_amount, validate_date
from storage import load_data, save_data

CATEGORIES = ["еда", "транспорт", "развлечения", "здоровье", "одежда", "другое"]


def on_add():
    """Обработчик кнопки «Добавить расход»: валидирует и сохраняет запись."""
    amount_raw = amount_entry.get().strip()
    category = category_combo.get().strip()
    date = date_entry.get().strip()

    if not amount_raw:
        messagebox.showerror("Ошибка", "Введите сумму расхода.")
        return
    if not validate_amount(amount_raw):
        messagebox.showerror("Ошибка", "Сумма должна быть положительным числом.")
        return
    if not category:
        messagebox.showerror("Ошибка", "Выберите категорию.")
        return
    if not date:
        messagebox.showerror("Ошибка", "Введите дату.")
        return
    if not validate_date(date):
        messagebox.showerror("Ошибка", "Дата должна быть в формате YYYY-MM-DD.")
        return

    record = {
        "amount": float(amount_raw.replace(",", ".")),
        "category": category,
        "date": date,
    }
    all_records.append(record)
    save_data(all_records)
    amount_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    apply_filter()
    update_total()


def apply_filter():
    """Применяет фильтр по категории и дате, обновляет таблицу."""
    cat = filter_cat_combo.get()
    date = filter_date_entry.get().strip()

    filtered = all_records
    if cat and cat != "Все":
        filtered = [r for r in filtered if r["category"] == cat]
    if date:
        filtered = [r for r in filtered if r["date"] == date]

    refresh_table(filtered)
    update_total(filtered)


def clear_filter():
    """Сбрасывает фильтры."""
    filter_cat_combo.set("Все")
    filter_date_entry.delete(0, tk.END)
    refresh_table(all_records)
    update_total()


def refresh_table(records):
    """Перерисовывает таблицу расходов."""
    for row in tree.get_children():
        tree.delete(row)
    for rec in records:
        tree.insert("", tk.END, values=(rec["date"], rec["category"], f'{rec["amount"]:.2f}'))


def update_total(records=None):
    """Обновляет метку с суммой расходов."""
    if records is None:
        records = all_records
    total = sum(r["amount"] for r in records)
    total_var.set(f"Итого: {total:.2f} руб.")


# ── Главное окно ──────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Expense Tracker — Трекер расходов")
root.geometry("680x620")
root.resizable(False, False)

# ── Форма добавления ──────────────────────────────────────────────────────────
form = tk.LabelFrame(root, text="Добавить расход", padx=10, pady=8)
form.pack(fill=tk.X, padx=12, pady=8)

tk.Label(form, text="Сумма:").grid(row=0, column=0, sticky=tk.W, pady=3)
amount_entry = tk.Entry(form, width=20)
amount_entry.grid(row=0, column=1, sticky=tk.W, padx=6)

tk.Label(form, text="Категория:").grid(row=1, column=0, sticky=tk.W, pady=3)
category_combo = ttk.Combobox(form, values=CATEGORIES, state="readonly", width=18)
category_combo.grid(row=1, column=1, sticky=tk.W, padx=6)

tk.Label(form, text="Дата (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=3)
date_entry = tk.Entry(form, width=20)
date_entry.grid(row=2, column=1, sticky=tk.W, padx=6)

tk.Button(
    form, text="➕  Добавить расход", command=on_add,
    bg="#F44336", fg="white", padx=12, pady=4,
).grid(row=3, column=0, columnspan=2, pady=8)

# ── Фильтр ────────────────────────────────────────────────────────────────────
flt = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=6)
flt.pack(fill=tk.X, padx=12, pady=4)

tk.Label(flt, text="Категория:").grid(row=0, column=0, sticky=tk.W)
filter_cat_combo = ttk.Combobox(flt, values=["Все"] + CATEGORIES, state="readonly", width=16)
filter_cat_combo.set("Все")
filter_cat_combo.grid(row=0, column=1, padx=6)

tk.Label(flt, text="Дата:").grid(row=0, column=2, sticky=tk.W, padx=(12, 0))
filter_date_entry = tk.Entry(flt, width=14)
filter_date_entry.grid(row=0, column=3, padx=6)

tk.Button(flt, text="Применить", command=apply_filter, padx=8).grid(row=0, column=4, padx=4)
tk.Button(flt, text="Сбросить", command=clear_filter, padx=8).grid(row=0, column=5, padx=4)

# ── Таблица ───────────────────────────────────────────────────────────────────
tbl_frm = tk.LabelFrame(root, text="Расходы", padx=8, pady=6)
tbl_frm.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

columns = ("Дата", "Категория", "Сумма (руб.)")
tree = ttk.Treeview(tbl_frm, columns=columns, show="headings", height=12)
for col, w in zip(columns, [140, 160, 140]):
    tree.heading(col, text=col)
    tree.column(col, width=w, anchor=tk.CENTER)

sb = ttk.Scrollbar(tbl_frm, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=sb.set)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
sb.pack(side=tk.RIGHT, fill=tk.Y)

# ── Итого ─────────────────────────────────────────────────────────────────────
total_var = tk.StringVar()
tk.Label(root, textvariable=total_var, font=("Arial", 11, "bold"), anchor=tk.E).pack(
    fill=tk.X, padx=16, pady=4)

# ── Загрузка данных ───────────────────────────────────────────────────────────
all_records = load_data()
refresh_table(all_records)
update_total()

root.mainloop()
