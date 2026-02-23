import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
def create_app():
    root = tk.Tk()
    root.title("Bar Table Management - Hotellexa")
    root.geometry("1000x600")
    root.configure(bg="#008080")  # Matching the teal background in your image

    # --- Header Section ---
    header_frame = tk.Frame(root, bg="#008080", pady=10)
    header_frame.pack(fill="x")

    # Table Info
    tk.Label(header_frame, text="Table No:", font=("Arial", 12, "bold"), bg="#008080", fg="black").grid(row=0, column=0, padx=5)
    table_entry = tk.Entry(header_frame, width=10)
    table_entry.insert(0, "2")
    table_entry.grid(row=0, column=1, padx=5)

    tk.Label(header_frame, text="Bill No:", font=("Arial", 12, "bold"), bg="#008080", fg="black").grid(row=0, column=2, padx=20)
    tk.Label(header_frame, text="2", font=("Arial", 12), bg="white", width=5).grid(row=0, column=3)

    # Waiter Info
    tk.Label(header_frame, text="Waiter:", font=("Arial", 12, "bold"), bg="#008080", fg="black").grid(row=1, column=0, pady=10)
    waiter_entry = tk.Entry(header_frame, width=15)
    waiter_entry.insert(0, "SANDIP")
    waiter_entry.grid(row=1, column=1)

    # --- Main Content Area ---
    main_frame = tk.Frame(root, bg="#008080")
    main_frame.pack(fill="both", expand=True, padx=10)

    # Left Side: Placeholder for Image/Visuals
    canvas = tk.Canvas(main_frame, width=500, height=300, bg="black", highlightthickness=2, highlightbackground="gold")
    canvas.grid(row=0, column=0, padx=10, pady=10)
    canvas.create_text(250, 150, text="Robot Service Visualization", fill="white")

    # Right Side: Table Status Buttons (R1, R2, R4 as seen in your image)
    table_btn_frame = tk.Frame(main_frame, bg="#add8e6", bd=2, relief="sunken", width=200, height=300)
    table_btn_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    
    tables = [("R1", "red"), ("R2", "black"), ("R4", "red")]
    for i, (name, color) in enumerate(tables):
        btn = tk.Button(table_btn_frame, text=name, bg=color, fg="white", font=("Arial", 10, "bold"), width=5)
        btn.grid(row=0, column=i, padx=5, pady=5)

    # --- Footer Function Keys ---
    footer_frame = tk.Frame(root, bg="#008080")
    footer_frame.pack(side="bottom", fill="x", pady=10)

    buttons = [
        "F1-Print Bill", "F2-Add Item", "F3-Bill Correction", 
        "F7-Table Shift", "F8-Receipt", "F9-Counter Cash"
    ]

    for i, btn_text in enumerate(buttons):
        row = 0 if i < 3 else 1
        col = i if i < 3 else i - 3
        tk.Button(footer_frame, text=btn_text, bg="#e1f5fe", width=20).grid(row=row, column=col, padx=2, pady=2)

    root.mainloop()

if __name__ == "__main__":
    create_app()
    def handle_f1(event=None):
    messagebox.showinfo("Print", "Printing Bill...")

def handle_f2(event=None):
    messagebox.showinfo("Item", "Opening Add Item Menu...")

def handle_exit(event=None):
    if messagebox.askokcancel("Quit", "Do you want to close the application?"):
        root.destroy()

    root = tk.Tk()

    # --- Binding the Keys ---
    # Use <F1>, <F2>, etc. for function keys
    root.bind('<F1>', handle_f1)
    root.bind('<F2>', handle_f2)
    root.bind('<Escape>', handle_exit)

    # Example button that also triggers the function
    btn_f1 = tk.Button(root, text="F1-Print Bill", command=handle_f1)
    btn_f1.pack(pady=20)

    root.mainloop()