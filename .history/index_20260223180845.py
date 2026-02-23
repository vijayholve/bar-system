import tkinter as tk
from tkinter import messagebox

class BarManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bar Table Management - Hotellexa")
        self.root.geometry("1100x650")
        self.root.configure(bg="#008080")

        # Set up Key Bindings
        self.setup_bindings()
        
        # Build UI Components
        self.create_header()
        self.create_main_area()
        self.create_footer()

    def setup_bindings(self):
        """Bind physical keyboard keys to functions"""
        self.root.bind('<F1>', lambda e: self.handle_print())
        self.root.bind('<F2>', lambda e: self.handle_add_item())
        self.root.bind('<F3>', lambda e: self.handle_correction())
        self.root.bind('<F7>', lambda e: self.handle_shift())
        self.root.bind('<Escape>', lambda e: self.handle_exit())

    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#008080", pady=10)
        header_frame.pack(fill="x", padx=10)

        # Table Information Row
        tk.Label(header_frame, text="Table No:", font=("Arial", 12, "bold"), bg="#008080", fg="white").grid(row=0, column=0, sticky="w")
        self.table_entry = tk.Entry(header_frame, width=10, font=("Arial", 12))
        self.table_entry.insert(0, "2")
        self.table_entry.grid(row=0, column=1, padx=5)

        tk.Label(header_frame, text="Bill No:", font=("Arial", 12, "bold"), bg="#008080", fg="white").grid(row=0, column=2, padx=20)
        tk.Label(header_frame, text="1002", font=("Arial", 12, "bold"), bg="white", width=10, relief="sunken").grid(row=0, column=3)

        # Waiter Information Row
        tk.Label(header_frame, text="Waiter:", font=("Arial", 12, "bold"), bg="#008080", fg="white").grid(row=1, column=0, pady=10, sticky="w")
        self.waiter_entry = tk.Entry(header_frame, width=20, font=("Arial", 12))
        self.waiter_entry.insert(0, "SANDIP")
        self.waiter_entry.grid(row=1, column=1, columnspan=2, sticky="w", padx=5)

    def create_main_area(self):
        main_frame = tk.Frame(self.root, bg="#008080")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left: Visualization Canvas
        self.canvas = tk.Canvas(main_frame, width=600, height=350, bg="black", highlightthickness=2, highlightbackground="gold")
        self.canvas.grid(row=0, column=0, padx=10)
        self.canvas.create_text(300, 175, text="[ Robot Service Visualization Area ]", fill="white", font=("Arial", 14))

        # Right: Table Selection Buttons
        table_btn_frame = tk.Frame(main_frame, bg="#add8e6", bd=3, relief="ridge", padx=10, pady=10)
        table_btn_frame.grid(row=0, column=1, sticky="nsew")
        
        tk.Label(table_btn_frame, text="Table Status", bg="#add8e6", font=("Arial", 10, "bold")).pack()
        
        # Dummy data for tables
        tables = [("R1", "red"), ("R2", "black"), ("R3", "green"), ("R4", "red")]
        for name, color in tables:
            btn = tk.Button(table_btn_frame, text=name, bg=color, fg="white", 
                           font=("Arial", 12, "bold"), width=8, pady=5,
                           command=lambda n=name: print(f"Selected Table {n}"))
            btn.pack(pady=5)

    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg="#008080")
        footer_frame.pack(side="bottom", fill="x", pady=20)

        # Organizing buttons in a grid to match your layout
        buttons = [
            ("F1-Print Bill", self.handle_print),
            ("F2-Add Item", self.handle_add_item),
            ("F3-Bill Correction", self.handle_correction),
            ("F7-Table Shift", self.handle_shift),
            ("F8-Receipt", lambda: None),
            ("Esc-Exit", self.handle_exit)
        ]

        for i, (text, func) in enumerate(buttons):
            row = 0 if i < 3 else 1
            col = i if i < 3 else i - 3
            btn = tk.Button(footer_frame, text=text, bg="#e1f5fe", font=("Arial", 10),
                           width=25, height=2, command=func)
            btn.grid(row=row, column=col, padx=5, pady=5)

    # --- Logic Handlers ---
    def handle_print(self):
        messagebox.showinfo("Action", "F1 Pressed: Printing current bill...")

    def handle_add_item(self):
        messagebox.showinfo("Action", "F2 Pressed: Opening Item Menu...")

    def handle_correction(self):
        messagebox.showinfo("Action", "F3 Pressed: Correcting Bill...")

    def handle_shift(self):
        messagebox.showinfo("Action", "F7 Pressed: Shifting table data...")

    def handle_exit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to exit Hotellexa?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BarManagementApp(root)
    root.mainloop()