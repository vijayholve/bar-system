import tkinter as tk
from tkinter import ttk, messagebox

class BarPOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotellexa - Bar Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#008080")

        # --- Dummy Data ---
        # Brand Name: [Unit/Packing, Rate]
        self.menu_data = [
            ["ANDA BHURJI", "1", 90.00],
            ["ANDA BHURJI CURRY", "1", 190.00],
            ["ANDA BOILED 2PC", "1", 30.00],
            ["ANTIQUITY WHY", "QUAR", 1500.00],
            ["ANTIQUITY WHY", "NIP", 500.00],
            ["ANTIQUITY WHY", "PEG_L", 170.00],
            ["ANTIQUITY WHY", "PEG_S", 90.00]
        ]
        
        # Current Bill: {item_id: [Name, Packing, Qty, Rate]}
        self.current_bill = {}

        self.create_widgets()

    def create_widgets(self):
        # Top Info Bar
        top_bar = tk.Frame(self.root, bg="#008080")
        top_bar.pack(fill="x", padx=10, pady=5)
        
        tk.Label(top_bar, text="Table No: 11", font=("Arial", 12, "bold"), bg="#008080", fg="white").pack(side="left", padx=10)
        tk.Label(top_bar, text="Bill No: 11", font=("Arial", 12, "bold"), bg="#008080", fg="white").pack(side="left", padx=10)
        
        # Main Container
        main_frame = tk.Frame(self.root, bg="#008080")
        main_frame.pack(fill="both", expand=True, padx=10)

        # 1. Left Section: Brand/Item Selection (Yellow/Orange list)
        menu_frame = tk.Frame(main_frame, bg="#FFA500", bd=2, relief="ridge")
        menu_frame.place(relx=0, rely=0, relwidth=0.35, relheight=0.8)

        tk.Label(menu_frame, text="Brand / Item Menu", bg="#000000", fg="white", font=("Arial", 10, "bold")).pack(fill="x")
        
        for item in self.menu_data:
            btn_text = f"{item[0]} | {item[1]} | ₹{item[2]}"
            btn = tk.Button(menu_frame, text=btn_text, anchor="w", bg="#FFD700", 
                           font=("Arial", 9, "bold"), bd=1, relief="flat",
                           command=lambda i=item: self.add_to_bill(i))
            btn.pack(fill="x", pady=1)

        # 2. Middle Section: Billing Table (The Blue Grid)
        bill_frame = tk.Frame(main_frame, bg="#00CED1", bd=2, relief="ridge")
        bill_frame.place(relx=0.36, rely=0, relwidth=0.5, relheight=0.8)

        # Treeview for the bill items
        columns = ("SR", "ITEM", "QTY", "RATE", "AMT")
        self.tree = ttk.Treeview(bill_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor="center")
        self.tree.column("ITEM", width=180, anchor="w")
        self.tree.pack(fill="both", expand=True)

        # 3. Right Section: Action Controls (Delete/Increment)
        control_frame = tk.Frame(main_frame, bg="#008080")
        control_frame.place(relx=0.87, rely=0, relwidth=0.12, relheight=0.8)

        tk.Button(control_frame, text=" + QTY ", bg="green", fg="white", font=("Arial", 12, "bold"),
                  command=lambda: self.adjust_qty(1)).pack(fill="x", pady=5)
        tk.Button(control_frame, text=" - QTY ", bg="orange", fg="white", font=("Arial", 12, "bold"),
                  command=lambda: self.adjust_qty(-1)).pack(fill="x", pady=5)
        tk.Button(control_frame, text=" DELETE ", bg="red", fg="white", font=("Arial", 12, "bold"),
                  command=self.delete_item).pack(fill="x", pady=5)

        # 4. Bottom Section: Totals and Function Keys
        self.total_lbl = tk.Label(self.root, text="GRAND TOTAL: 0", font=("Arial", 24, "bold"), bg="#000080", fg="white")
        self.total_lbl.pack(side="bottom", fill="x", pady=5)

    def add_to_bill(self, item_info):
        """Adds or Increments an item when clicked from the left menu"""
        name_key = f"{item_info[0]}_{item_info[1]}"
        
        if name_key in self.current_bill:
            self.current_bill[name_key][2] += 1
        else:
            # [Name, Packing, Qty, Rate]
            self.current_bill[name_key] = [item_info[0], item_info[1], 1, item_info[2]]
        
        self.refresh_table()

    def adjust_qty(self, amount):
        """Adjusts quantity of the selected item in the bill table"""
        selected = self.tree.selection()
        if not selected:
            return
        
        item_text = self.tree.item(selected[0])['values'][1] # Get item name
        # We need the key to find it in our dict
        for key, data in self.current_bill.items():
            if data[0] in item_text:
                data[2] += amount
                if data[2] <= 0:
                    del self.current_bill[key]
                break
        self.refresh_table()

    def delete_item(self):
        """Removes the selected item entirely"""
        selected = self.tree.selection()
        if not selected: return
        item_text = self.tree.item(selected[0])['values'][1]
        
        for key, data in self.current_bill.items():
            if data[0] in item_text:
                del self.current_bill[key]
                break
        self.refresh_table()

    def refresh_table(self):
        """Clears and re-draws the billing table and grand total"""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        grand_total = 0
        for idx, (key, val) in enumerate(self.current_bill.items(), 1):
            name, packing, qty, rate = val
            amt = qty * rate
            grand_total += amt
            self.tree.insert("", "end", values=(idx, f"{name} {packing}", qty, rate, amt))
        
        self.total_lbl.config(text=f"GRAND TOTAL: {grand_total}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BarPOSApp(root)
    root.mainloop()