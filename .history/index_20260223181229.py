import tkinter as tk
from tkinter import messagebox, ttk

class HotellexaBarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotellexa - Bar Management System")
        self.root.geometry("1100x750")
        self.root.configure(bg="#008080")

        # --- Temporary Data Structure ---
        self.menu_items = {
            "Beer": 250, "Whiskey": 450, "Vodka": 350, 
            "Cocktail": 500, "Mocktail": 200, "Peanuts": 50
        }
        
        self.table_data = {
            "R1": {"waiter": "SANDIP", "items": [], "total": 0, "status": "red"},
            "R2": {"waiter": "VIJAY", "items": [], "total": 0, "status": "black"},
            "R3": {"waiter": "PRANAV", "items": [], "total": 0, "status": "green"},
            "R4": {"waiter": "ASHWINI", "items": [], "total": 0, "status": "red"},
        }
        self.current_table = "R1"

        self.setup_bindings()
        self.create_widgets()
        self.load_table_info(self.current_table)

    def setup_bindings(self):
        self.root.bind('<F1>', lambda e: self.print_bill())
        self.root.bind('<F2>', lambda e: self.open_menu_window())
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def create_widgets(self):
        # Header Info Area
        self.header = tk.Frame(self.root, bg="#008080", pady=10)
        self.header.pack(fill="x", padx=20)

        tk.Label(self.header, text="Table No:", font=("Arial", 12, "bold"), bg="#008080", fg="white").grid(row=0, column=0)
        self.lbl_table = tk.Label(self.header, text="", font=("Arial", 12, "bold"), bg="white", width=10)
        self.lbl_table.grid(row=0, column=1, padx=10)

        tk.Label(self.header, text="Waiter:", font=("Arial", 12, "bold"), bg="#008080", fg="white").grid(row=0, column=2, padx=10)
        self.lbl_waiter = tk.Label(self.header, text="", font=("Arial", 12), bg="white", width=15)
        self.lbl_waiter.grid(row=0, column=3)

        # Main Body
        main_frame = tk.Frame(self.root, bg="#008080")
        main_frame.pack(fill="both", expand=True, padx=20)

        # Left: Bill Display (Treeview)
        tk.Label(main_frame, text="Current Bill Items", bg="#008080", fg="gold", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.tree = ttk.Treeview(main_frame, columns=("Item", "Price"), show='headings', height=15)
        self.tree.heading("Item", text="Item Name")
        self.tree.heading("Price", text="Price (INR)")
        self.tree.grid(row=1, column=0, padx=5, pady=5)

        # Right: Table Selection
        self.btn_frame = tk.LabelFrame(main_frame, text=" Tables ", bg="#add8e6", font=("Arial", 10, "bold"))
        self.btn_frame.grid(row=1, column=1, sticky="nsew", padx=20)

        for t_name, info in self.table_data.items():
            btn = tk.Button(self.btn_frame, text=t_name, bg=info["status"], fg="white",
                           font=("Arial", 12, "bold"), width=10, pady=10,
                           command=lambda n=t_name: self.load_table_info(n))
            btn.pack(pady=5, padx=10)

        # Footer Total
        self.lbl_total = tk.Label(self.root, text="Total: 0.00", font=("Arial", 20, "bold"), bg="#008080", fg="white")
        self.lbl_total.pack(pady=10)

        # Shortcut Buttons
        footer = tk.Frame(self.root, bg="#008080", pady=20)
        footer.pack(side="bottom", fill="x")
        
        btns = [("F1 Print", self.print_bill), ("F2 Add Item", self.open_menu_window), ("Esc Exit", self.root.destroy)]
        for i, (txt, cmd) in enumerate(btns):
            tk.Button(footer, text=txt, font=("Arial", 10, "bold"), width=15, bg="#e1f5fe", command=cmd).grid(row=0, column=i, padx=20)

    def load_table_info(self, table_name):
        self.current_table = table_name
        data = self.table_data[table_name]
        self.lbl_table.config(text=table_name)
        self.lbl_waiter.config(text=data["waiter"])
        
        # Clear and reload bill items in Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item, price in data["items"]:
            self.tree.insert("", "end", values=(item, price))
        
        self.lbl_total.config(text=f"Total: {sum(p for i, p in data['items']):.2f}")

    def open_menu_window(self):
        """Creates a pop-up window to select items"""
        menu_win = tk.Toplevel(self.root)
        menu_win.title(f"Select Menu - Table {self.current_table}")
        menu_win.geometry("300x400")
        menu_win.grab_set() # Focus stays on this window

        tk.Label(menu_win, text="Select Item to Add", font=("Arial", 12, "bold")).pack(pady=10)

        for item, price in self.menu_items.items():
            btn = tk.Button(menu_win, text=f"{item} (₹{price})", width=25,
                           command=lambda i=item, p=price: self.add_item_to_table(i, p, menu_win))
            btn.pack(pady=2)

    def add_item_to_table(self, item, price, window):
        self.table_data[self.current_table]["items"].append((item, price))
        self.load_table_info(self.current_table) # Refresh UI
        window.destroy() # Close menu after selection

    def print_bill(self):
        total = sum(p for i, p in self.table_data[self.current_table]["items"])
        if total == 0:
            messagebox.showwarning("Empty", "No items to print!")
        else:
            messagebox.showinfo("Success", f"Bill Printed for {self.current_table}\nTotal: ₹{total}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotellexaBarApp(root)
    root.mainloop()