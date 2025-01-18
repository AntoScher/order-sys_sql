import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def init_db():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    order_details TEXT NOT NULL,
    status TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def add_order():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
        (customer_name_entry.get(), order_details_entry.get()))

    conn.commit()
    conn.close()

    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)

    view_orders()

def view_orders():
    for i in tree.get_children():
        tree.delete(i)

    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    conn.close()

def complete_order():
    selected_item = tree.selection()

    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]

        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()

        cur.execute("UPDATE orders SET status='Завершён' WHERE id=?", (order_id,))

        conn.commit()
        conn.close()

        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для завершения")

def delete_order():
    selected_item = tree.selection()

    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]

        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()

        cur.execute("DELETE FROM orders WHERE id=?", (order_id,))

        conn.commit()
        conn.close()

        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для удаления")

def edit_order():
    selected_item = tree.selection()

    if selected_item:
        order_id, customer_name, order_details, status = tree.item(selected_item, 'values')

        edit_window = tk.Toplevel(app)
        edit_window.title("Редактировать заказ")

        tk.Label(edit_window, text="Имя клиента").pack()
        customer_name_entry_edit = tk.Entry(edit_window)
        customer_name_entry_edit.pack()
        customer_name_entry_edit.insert(tk.END, customer_name)

        tk.Label(edit_window, text="Детали заказа").pack()
        order_details_entry_edit = tk.Entry(edit_window)
        order_details_entry_edit.pack()
        order_details_entry_edit.insert(tk.END, order_details)

        def save_changes():
            conn = sqlite3.connect('business_orders.db')
            cur = conn.cursor()

            cur.execute("UPDATE orders SET customer_name=?, order_details=? WHERE id=?",
                        (customer_name_entry_edit.get(), order_details_entry_edit.get(), order_id))

            conn.commit()
            conn.close()

            view_orders()
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Сохранить изменения", command=save_changes)
        save_button.pack()

    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для редактирования")

app = tk.Tk()
app.title("Система управления заказами")

tk.Label(app, text="Имя клиента").pack()
customer_name_entry = tk.Entry(app)
customer_name_entry.pack()

tk.Label(app, text="Детали заказа").pack()
order_details_entry = tk.Entry(app)
order_details_entry.pack()

buttons_frame = tk.Frame(app)
buttons_frame.pack()

add_button = tk.Button(buttons_frame, text="Добавить заказ", command=add_order)
add_button.pack(side=tk.LEFT)

complete_button = tk.Button(buttons_frame, text="Завершить заказ", command=complete_order)
complete_button.pack(side=tk.LEFT)

delete_button = tk.Button(buttons_frame, text="Удалить заказ", command=delete_order)
delete_button.pack(side=tk.LEFT)

edit_button = tk.Button(buttons_frame, text="Редактировать заказ", command=edit_order)
edit_button.pack(side=tk.LEFT)

columns = ("id", "customer_name", "order_details", "status")
tree = ttk.Treeview(app, columns=columns, show="headings")
for column in columns:
    tree.heading(column, text=column)
tree.pack()

init_db()
view_orders()

app.mainloop()
