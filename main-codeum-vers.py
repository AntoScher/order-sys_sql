import tkinter as tk
from tkinter import ttk
import sqlite3

class OrderSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Order System")
        self.init_db()
        self.create_widgets()

    def init_db(self):
        self.conn = sqlite3.connect("orders-for-codeum.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_name TEXT,
                order_details TEXT,
                status TEXT
            )
        """)
        self.conn.commit()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.frame1 = tk.Frame(self.notebook)
        self.frame2 = tk.Frame(self.notebook)
        self.frame3 = tk.Frame(self.notebook)

        self.notebook.add(self.frame1, text="Add Order")
        self.notebook.add(self.frame2, text="Complete Order")
        self.notebook.add(self.frame3, text="View Orders")

        # Add Order
        self.customer_name_label = tk.Label(self.frame1, text="Customer Name:")
        self.customer_name_label.pack()
        self.customer_name_entry = tk.Entry(self.frame1)
        self.customer_name_entry.pack()

        self.order_details_label = tk.Label(self.frame1, text="Order Details:")
        self.order_details_label.pack()
        self.order_details_entry = tk.Entry(self.frame1)
        self.order_details_entry.pack()

        self.add_order_button = tk.Button(self.frame1, text="Add Order", command=self.add_order)
        self.add_order_button.pack()

        # Complete Order
        self.order_id_label = tk.Label(self.frame2, text="Order ID:")
        self.order_id_label.pack()
        self.order_id_entry = tk.Entry(self.frame2)
        self.order_id_entry.pack()

        self.complete_order_button = tk.Button(self.frame2, text="Complete Order", command=self.complete_order)
        self.complete_order_button.pack()

        # View Orders
        self.tree = ttk.Treeview(self.frame3)
        self.tree["columns"] = ("id", "customer_name", "order_details", "status")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", anchor=tk.W, width=50)
        self.tree.column("customer_name", anchor=tk.W, width=150)
        self.tree.column("order_details", anchor=tk.W, width=200)
        self.tree.column("status", anchor=tk.W, width=100)
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("id", text="ID", anchor=tk.W)
        self.tree.heading("customer_name", text="Customer Name", anchor=tk.W)
        self.tree.heading("order_details", text="Order Details", anchor=tk.W)
        self.tree.heading("status", text="Status", anchor=tk.W)
        self.tree.pack()

        self.view_orders_button = tk.Button(self.frame3, text="View Orders", command=self.view_orders)
        self.view_orders_button.pack()

    def add_order(self):
        try:
            customer_name = self.customer_name_entry.get()
            order_details = self.order_details_entry.get()
            self.cursor.execute("INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'pending')", (customer_name, order_details))
            self.conn.commit()
            self.customer_name_entry.delete(0, tk.END)
            self.order_details_entry.delete(0, tk.END)
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def complete_order(self):
        try:
            order_id = int(self.order_id_entry.get())
            self.cursor.execute("UPDATE orders SET status = 'completed' WHERE id = ?", (order_id,))
            self.conn.commit()
            self.order_id_entry.delete(0, tk.END)
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def view_orders(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.cursor.execute("SELECT * FROM orders")
            rows = self.cursor.fetchall()
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except sqlite3.Error as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderSystem(root)
    root.mainloop()