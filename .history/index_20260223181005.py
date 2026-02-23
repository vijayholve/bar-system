import tkinter as tk
from tkinter import messagebox

class HotellexaBarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotellexa - Bar Management System")
        self.root.geometry("1100x700")
        self.root.configure(bg="#008080")

        # --- Temporary Dummy Data ---
        # Stores: {Table_No: {"waiter": name, "bill": amount, "status": color}}
        self.table_data = {
            "R1": {"waiter": "SANDIP", "bill": "1002", "status": "red"},
            "R2": {"waiter": "VIJAY", "bill": "1005", "status": "black"},
            "R3": {"waiter": "PRANAV", "bill": "1008", "status": "green"},
            "R4": {"waiter": "ASHWINI", "bill": "1010", "status": "red"},
        }
        self.current_table = "R1"

        self.setup_bindings()
        self.create_widgets()
        self.load_table_info(self.current_table)

    def setup_bindings(self):
        """Keyboard Shortcuts mapping"""
        self.root.bind('<F1>', lambda e: self.print_bill())
        self.root.bind('<F2>', lambda e: self.add_item())
        self.root.bind('<F7>', lambda e: self.shift_table())
        self.root.bind('<Escape>', lambda e: self.exit_app())

    def create_widgets(self):
        # Header
        self.header = tk.Frame(self.root, bg="#008080", pady=15)
        self.header.pack(fill="x", padx=20)

        tk.Label(self.header, text="Table No:", font=("Arial", 12, "bold"), bg="#008080", fg="white").grid(row=0, column=0)
        self.lbl_table = tk.Label(self.header, text="", font=("Arial", 12, "bold"), bg="white", width=10)
        self.lbl_table.grid(row=0, column=1, padx=10)

        tk.Label(self.header, text="Waiter:", font=("Arial", 12, "bold"), bg="#008080", fg="white").grid(row=0, column=2, padx=10)
        self.lbl_waiter = tk.Label(self.header, text="", font=("Arial", 12), bg="white", width=15)
        self.lbl_waiter.grid(row=0, column=3)

        # Main Layout
        main_frame = tk.Frame(self.root, bg="#008080")
        main_frame.pack(fill="both", expand=True, padx=20)

        # Left Side (Visuals)
        self.canvas = tk.Canvas(main_frame, bg="black", highlightbackground="gold", highlightthickness=2)
        self.canvas.place(relx=0, rely=0.05, relwidth=0.7, relheight=0.7)
        self.canvas.create_text(350, 200, text="[ ROBOTIC SERVICE INTERFACE ]", fill="#00FF00", font=("Courier", 16))

        # Right Side (Table Selection)
        self.btn_frame = tk.LabelFrame(main_frame, text=" Select Table ", bg="#add8e6", font=("Arial", 10, "bold"))
        self.btn_frame.place(relx=0.72, rely=0.05, relwidth=0.25, relheight=0.7)

        for t_name, info in self.table_data.items():
            btn = tk.Button(self.btn_frame, text=t_name, bg=info["status"], fg="white",
                           font=("Arial", 14, "bold"), height=2,
                           command=lambda n=t_name: self.load_table_info(n))
            btn.pack(fill="x", padx=10, pady=5)

        # Footer (Shortcuts)
        footer = tk.Frame(self.root, bg="#008080", pady=20)
        footer.pack(side="bottom", fill="x")

        btns = [("F1 Print", self.print_bill), ("F2 Add", self.add_item), 
                ("F7 Shift", self.shift_table), ("Esc Exit", self.exit_app)]
        
        for i, (txt, cmd) in enumerate(btns):
            tk.Button(footer, text=txt, font=("Arial", 11, "bold"), width=15, 
                      bg="#e1f5fe", command=cmd).grid(row=0, column=i, padx=10)

    def load_table_info(self, table_name):
        """Update UI with data from our 'temporary database'"""
        self.current_table = table_name
        data = self.table_data[table_name]
        self.lbl_table.config(text=table_name)
        self.lbl_waiter.config(text=data["waiter"])
        print(f"Loaded {table_name} managed by {data['waiter']}")

    def print_bill(self):
        bill_no = self.table_data[self.current_table]["bill"]
        messagebox.showinfo("Billing", f"Printing Bill #{bill_no} for Table {self.current_table}")

    def add_item(self):
        messagebox.showinfo("Order", f"Opening Menu for Table {self.current_table}")

    def shift_table(self):
        """Logic to 'move' a guest to another table"""
        new_table = "R3" # Dummy shift target
        messagebox.showinfo("Shift", f"Shifting data from {self.current_table} to {new_table}")
        # Swap logic
        self.table_data[new_table]["status"] = "red"
        self.load_table_info(new_table)

    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotellexaBarApp(root)
    root.mainloop()