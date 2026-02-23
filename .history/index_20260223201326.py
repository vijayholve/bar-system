import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import webbrowser
import tempfile
import os


class BarPOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotellexa - Bar Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#008080")

        # --- Dummy Data ---
        # Brand Name: [Unit/Packing, Rate]
        self.menu_data = [
            ["PANEER TIKKA", "1", 240.00],
            ["PANEER BUTTER MASALA", "1", 280.00],
            ["VEG CRISPY", "1", 180.00],
            ["DAL TADKA", "1", 150.00],
            ["CHICKEN LOLLIPOP", "6PC", 220.00],
            ["CHICKEN TANDOORI", "FULL", 450.00],
            ["CHICKEN TANDOORI", "HALF", 240.00],
            ["MUTTON ROGAN JOSH", "1", 380.00],
            ["FISH FRY SURMAI", "1", 420.00],
            ["EGG BIRYANI", "1", 180.00],
            ["CHICKEN DUM BIRYANI", "1", 260.00],
            ["STEAMED RICE", "FULL", 120.00],
            ["JEERA RICE", "FULL", 140.00],
            ["BUTTER NAAN", "1", 45.00],
            ["GARLIC NAAN", "1", 60.00],
            ["TANDOORI ROTI", "1", 25.00],
            ["MASALA PAPAD", "1", 40.00],
            ["GREEN SALAD", "1", 60.00],
            ["ROYAL STAG", "QUAR", 850.00],
            ["ROYAL STAG", "NIP", 290.00],
            ["ROYAL STAG", "PEG_L", 110.00],
            ["ROYAL STAG", "PEG_S", 60.00],
            ["BLENDERS PRIDE", "QUAR", 1100.00],
            ["BLENDERS PRIDE", "NIP", 380.00],
            ["BLENDERS PRIDE", "PEG_L", 140.00],
            ["BLENDERS PRIDE", "PEG_S", 80.00],
            ["OLD MONK RUM", "QUAR", 600.00],
            ["OLD MONK RUM", "NIP", 210.00],
            ["OLD MONK RUM", "PEG_L", 90.00],
            ["MAGIC MOMENTS", "QUAR", 750.00],
            ["MAGIC MOMENTS", "NIP", 260.00],
            ["BUDWEISER BEER", "BTL", 220.00],
            ["KINGFISHER PREMIUM", "BTL", 190.00],
            ["TUBORG", "BTL", 180.00],
            ["COKE 500ML", "1", 60.00],
            ["THUMS UP 500ML", "1", 60.00],
            ["MINERAL WATER", "1L", 30.00],
            ["FRESH LIME SODA", "1", 50.00],
            ["CHICKEN CHILLI", "1", 210.00],
            ["VEG MANCHURIAN", "1", 170.00],
            ["HAKKA NOODLES", "1", 160.00],
            ["CHICKEN FRIED RICE", "1", 190.00],
            ["SCHEZWAN CHICKEN", "1", 230.00],
            ["PRAWNS KOLIWADA", "1", 350.00],
            ["CHICKEN MASALA", "1", 270.00],
            ["MUTTON HANDI", "FULL", 750.00],
            ["MUTTON HANDI", "HALF", 400.00],
            ["LEMON CHICKEN", "1", 240.00],
            ["BOILED EGG MASALA", "1", 110.00],
            ["EGG CURRY", "1", 160.00]
        ]

        # Current Bill: {item_id: [Name, Packing, Qty, Rate]}
        self.current_bill = {}

        # App state
        self.table_var = tk.StringVar()
        self.waiter_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.unit_default_var = tk.StringVar()
        self.use_unit_default = tk.BooleanVar(value=True)

        # Simple waiter list
        self.waiters = ["Select", "Waiter A", "Waiter B", "Waiter C"]

        # chosen index mapping for listbox
        self.filtered_items = []

        self.create_widgets()
        self.bind_shortcuts()

        # cash counter toggle
        self.cash_counter_on = False

        # Start flow: focus table entry
        self.root.after(100, lambda: self.table_entry.focus())

    def create_widgets(self):
        # Top Info Bar with Table & Waiter inputs
        top_bar = tk.Frame(self.root, bg="#008080")
        top_bar.pack(fill="x", padx=10, pady=5)

        tk.Label(top_bar, text="Table No:", font=("Arial", 12, "bold"), bg="#008080", fg="white").pack(side="left", padx=(10, 2))
        self.table_entry = tk.Entry(top_bar, textvariable=self.table_var, width=8, font=("Arial", 12, "bold"))
        self.table_entry.pack(side="left")
        tk.Label(top_bar, text="(Ctrl+T)", bg="#008080", fg="white").pack(side="left", padx=(4, 12))

        tk.Label(top_bar, text="Waiter:", font=("Arial", 12, "bold"), bg="#008080", fg="white").pack(side="left")
        self.waiter_cb = ttk.Combobox(top_bar, values=self.waiters, textvariable=self.waiter_var, width=12, state="readonly")
        self.waiter_cb.current(0)
        self.waiter_cb.pack(side="left", padx=(4, 10))
        tk.Label(top_bar, text="(Ctrl+W)", bg="#008080", fg="white").pack(side="left")

        # Main Container
        main_frame = tk.Frame(self.root, bg="#008080")
        main_frame.pack(fill="both", expand=True, padx=10)

        # 1. Left Section: Searchable Menu list
        menu_frame = tk.Frame(main_frame, bg="#FFA500", bd=2, relief="ridge")
        menu_frame.place(relx=0, rely=0, relwidth=0.35, relheight=0.8)

        header = tk.Frame(menu_frame, bg="#000000")
        header.pack(fill="x")
        tk.Label(header, text="Brand / Item Menu", bg="#000000", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=4)

        # Search box
        search_frame = tk.Frame(menu_frame, bg="#FFA500")
        search_frame.pack(fill="x", padx=4, pady=4)
        tk.Label(search_frame, text="Search:", bg="#FFA500").pack(side="left")
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(4, 4))
        tk.Label(search_frame, text="(Ctrl+S)", bg="#FFA500").pack(side="left")

        # Unit default controls
        unit_frame = tk.Frame(menu_frame, bg="#FFA500")
        unit_frame.pack(fill="x", padx=4)
        tk.Checkbutton(unit_frame, text="Use Default Unit (Ctrl+U)", variable=self.use_unit_default, bg="#FFA500").pack(side="left")
        # populate default with first item's packing
        self.unit_default_var.set(self.menu_data[0][1])
        self.unit_cb = ttk.Combobox(unit_frame, values=list({it[1] for it in self.menu_data}), textvariable=self.unit_default_var, width=8)
        self.unit_cb.pack(side="left", padx=6)

        # listbox for menu
        self.menu_listbox = tk.Listbox(menu_frame, activestyle='none')
        self.menu_listbox.pack(fill="both", expand=True, padx=4, pady=4)
        self.menu_listbox.bind('<Double-1>', lambda e: self.open_pending_from_listbox())
        self.menu_listbox.bind('<Return>', lambda e: self.open_pending_from_listbox())

        # fill listbox
        self.filter_menu()
        self.search_var.trace_add('write', lambda *a: self.filter_menu())

        # Pending add area (hidden until selection)
        pending_frame = tk.Frame(menu_frame, bg="#FFDAB9")
        pending_frame.pack(fill="x", padx=4, pady=2)
        tk.Label(pending_frame, text="Selected:", bg="#FFDAB9").pack(side="left")
        self.pending_label = tk.Label(pending_frame, text="None", bg="#FFDAB9")
        self.pending_label.pack(side="left", padx=(4, 10))

        tk.Label(pending_frame, text="Unit:", bg="#FFDAB9").pack(side="left")
        self.pending_unit_cb = ttk.Combobox(pending_frame, values=[], width=8)
        self.pending_unit_cb.pack(side="left", padx=4)

        tk.Label(pending_frame, text="Qty:", bg="#FFDAB9").pack(side="left", padx=(6, 0))
        self.pending_qty = tk.Entry(pending_frame, width=6)
        self.pending_qty.pack(side="left", padx=4)
        self.pending_qty.bind('<Return>', lambda e: self.confirm_pending_add())
        # Escape to cancel
        self.pending_qty.bind('<Escape>', lambda e: self.hide_pending())

        self.add_pending_btn = tk.Button(pending_frame, text="Add (Enter)", command=self.confirm_pending_add)
        self.add_pending_btn.pack(side="left", padx=6)
        self.cancel_pending_btn = tk.Button(pending_frame, text="Cancel (Esc)", command=self.hide_pending)
        self.cancel_pending_btn.pack(side="left")

        # hide initially
        self.pending_frame = pending_frame
        self.hide_pending()

        # 2. Middle Section: Billing Table
        bill_frame = tk.Frame(main_frame, bg="#00CED1", bd=2, relief="ridge")
        bill_frame.place(relx=0.36, rely=0, relwidth=0.5, relheight=0.8)

        columns = ("SR", "ITEM", "QTY", "RATE", "AMT")
        self.tree = ttk.Treeview(bill_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor="center")
        self.tree.column("ITEM", width=180, anchor="w")
        self.tree.pack(fill="both", expand=True)

        # 3. Right Section: Quick Actions
        control_frame = tk.Frame(main_frame, bg="#008080")
        control_frame.place(relx=0.87, rely=0, relwidth=0.12, relheight=0.8)

        tk.Button(control_frame, text=" + QTY ", bg="green", fg="white", font=("Arial", 12, "bold"), command=lambda: self.adjust_qty(1)).pack(fill="x", pady=5)
        tk.Button(control_frame, text=" - QTY ", bg="orange", fg="white", font=("Arial", 12, "bold"), command=lambda: self.adjust_qty(-1)).pack(fill="x", pady=5)
        tk.Button(control_frame, text=" DELETE ", bg="red", fg="white", font=("Arial", 12, "bold"), command=self.delete_item).pack(fill="x", pady=5)
        tk.Button(control_frame, text=" PRINT ", bg="#0044cc", fg="white", font=("Arial", 12, "bold"), command=self.print_online).pack(fill="x", pady=5)

        # Orders list (previous orders) on the right below controls
        orders_frame = tk.Frame(main_frame, bg="#006060", bd=1, relief='sunken')
        orders_frame.place(relx=0.87, rely=0.82, relwidth=0.12, relheight=0.18)
        tk.Label(orders_frame, text="Orders", bg="#006060", fg="white", font=("Arial", 9, "bold")).pack(fill='x')
        self.orders_tree = ttk.Treeview(orders_frame, columns=("TABLE","WAITER","TOTAL","STATUS"), show='headings', height=4)
        for c, w in (('TABLE',40), ('WAITER',60), ('TOTAL',60), ('STATUS',60)):
            self.orders_tree.heading(c, text=c)
            self.orders_tree.column(c, width=w, anchor='center')
        self.orders_tree.pack(fill='both', expand=True)
        self.orders_tree.bind('<Double-1>', lambda e: self.show_order_details())
        # configure tags for paid/unpaid
        self.orders_tree.tag_configure('paid', background='#c8f7c5')
        self.orders_tree.tag_configure('unpaid', background='#f7c5c5')

        # orders storage
        self.orders = []

        # Function-key toolbar (shown above totals)
        fk_frame = tk.Frame(self.root, bg="#004040")
        fk_frame.pack(side="bottom", fill="x", padx=2, pady=(4,0))

        # helper to create key label/button
        def fk_btn(text, cmd=None, width=10):
            b = tk.Button(fk_frame, text=text, width=width, relief='raised', bg='#202020', fg='white', font=("Arial",9,"bold"))
            if cmd:
                b.config(command=cmd)
            b.pack(side='left', padx=2, pady=2)
            return b

        fk_btn('New Order', lambda: self.new_order())
        fk_btn('F1 Print', self.print_online)
        fk_btn('F2 AddNew', self.add_new_item_dialog)
        fk_btn('F3 Corr', self.bill_correction_dialog)
        fk_btn('F4 KOT', self.print_kot)
        fk_btn('F5 Clear', self.clear_blank)
        fk_btn('F6 Save', lambda: self.save_order(paid=False))
        fk_btn('F7 Table', lambda: self.table_entry.focus())
        fk_btn('F8 Pay', self.payment_dialog)
        fk_btn('F9 Counter', self.toggle_cash_counter)
        fk_btn('F10 Print', self.print_online)

        # Bottom Total
        self.total_lbl = tk.Label(self.root, text="GRAND TOTAL: 0", font=("Arial", 24, "bold"), bg="#000080", fg="white")
        self.total_lbl.pack(side="bottom", fill="x", pady=5)

    # ----------------- Menu / Search -----------------
    def filter_menu(self):
        query = self.search_var.get().strip().lower()
        self.menu_listbox.delete(0, 'end')
        self.filtered_items = []
        for item in self.menu_data:
            display = f"{item[0]} | {item[1]} | ₹{item[2]}"
            if not query or query in item[0].lower() or query in str(item[1]).lower():
                self.menu_listbox.insert('end', display)
                self.filtered_items.append(item)
        # auto-select first item if available for quick keyboard selection
        if self.filtered_items:
            try:
                self.menu_listbox.selection_clear(0, 'end')
                self.menu_listbox.selection_set(0)
                self.menu_listbox.activate(0)
                self.menu_listbox.see(0)
            except Exception:
                pass

    def add_selected_from_listbox(self):
        sel = self.menu_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        item = self.filtered_items[idx]
        # quick add: if default unit is enabled and user pressed Ctrl+Return we can add immediately
        if self.use_unit_default.get():
            item_to_add = [item[0], self.unit_default_var.get(), item[2]]
            self.add_to_bill(item_to_add)
            self.search_var.set("")
            self.search_entry.focus()
        else:
            # show pending UI to choose unit/qty
            self.open_pending_for_item(item)

    def open_pending_from_listbox(self):
        # called by Enter or double click
        sel = self.menu_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        item = self.filtered_items[idx]
        self.open_pending_for_item(item)

    def move_listbox(self, delta):
        # move selection up/down by delta (used by PageUp/PageDown)
        size = len(self.filtered_items)
        if size == 0:
            return
        sel = self.menu_listbox.curselection()
        if not sel:
            idx = 0
        else:
            idx = sel[0]
        new = idx + delta
        if new < 0:
            new = 0
        if new >= size:
            new = size - 1
        try:
            self.menu_listbox.selection_clear(0, 'end')
            self.menu_listbox.selection_set(new)
            self.menu_listbox.activate(new)
            self.menu_listbox.see(new)
        except Exception:
            pass

    def _global_key_handler(self, event):
        # handle platform variations where PageUp/PageDown may not trigger <Next>/<Prior> binds
        ks = getattr(event, 'keysym', '')
        if ks in ('Next', 'Prior'):
            if ks == 'Next':
                self.move_listbox(1)
            else:
                self.move_listbox(-1)
            return 'break'
        return None

    def open_pending_for_item(self, item):
        # item: [name, packing, rate]
        name = item[0]
        # find all packings available for this name
        packings = []
        for it in self.menu_data:
            if it[0] == name and it[1] not in packings:
                packings.append(it[1])
        # include global default
        if self.unit_default_var.get() and self.unit_default_var.get() not in packings:
            packings.insert(0, self.unit_default_var.get())
        if not packings:
            packings = [item[1]]
        self.pending_label.config(text=name)
        self.pending_unit_cb['values'] = packings
        # select first
        try:
            self.pending_unit_cb.current(0)
        except Exception:
            pass
        # default qty 1
        self.pending_qty.delete(0, 'end')
        self.pending_qty.insert(0, '1')
        # show pending
        self.show_pending()
        # focus qty so typing numbers goes there
        self.pending_qty.focus()

    def show_pending(self):
        self.pending_frame.pack_configure()

    def hide_pending(self):
        self.pending_frame.pack_forget()
        self.pending_label.config(text='None')

    # ----------------- Billing -----------------
    def add_to_bill(self, item_info):
        name_key = f"{item_info[0]}_{item_info[1]}"
        if name_key in self.current_bill:
            self.current_bill[name_key][2] += 1
        else:
            self.current_bill[name_key] = [item_info[0], item_info[1], 1, item_info[2]]
        self.refresh_table()

    def adjust_qty(self, amount):
        selected = self.tree.selection()
        if not selected:
            return
        item_text = self.tree.item(selected[0])['values'][1]
        for key, data in list(self.current_bill.items()):
            if data[0] in item_text:
                data[2] += amount
                if data[2] <= 0:
                    del self.current_bill[key]
                break
        self.refresh_table()

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            return
        item_text = self.tree.item(selected[0])['values'][1]
        for key, data in list(self.current_bill.items()):
            if data[0] in item_text:
                del self.current_bill[key]
                break
        self.refresh_table()

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        grand_total = 0
        for idx, (key, val) in enumerate(self.current_bill.items(), 1):
            name, packing, qty, rate = val
            amt = qty * rate
            grand_total += amt
            self.tree.insert("", "end", values=(idx, f"{name} {packing}", qty, rate, amt))
        self.total_lbl.config(text=f"GRAND TOTAL: {grand_total}")

    # ----------------- Printing -----------------
    def print_online(self):
        # Create a simple HTML and open in the default browser so user can use browser's print
        if not self.current_bill:
            messagebox.showinfo("Print", "No items in bill to print")
            return
        rows = []
        total = 0
        for idx, (k, v) in enumerate(self.current_bill.items(), 1):
            name, packing, qty, rate = v
            amt = qty * rate
            total += amt
            rows.append(f"<tr><td>{idx}</td><td>{name} {packing}</td><td>{qty}</td><td>{rate}</td><td>{amt}</td></tr>")
        html = f"""
        <html><head><meta charset='utf-8'><title>Bill</title></head>
        <body>
        <h2>Table: {self.table_var.get()} &nbsp;&nbsp; Waiter: {self.waiter_var.get()}</h2>
        <table border='1' cellpadding='6' cellspacing='0'>
        <thead><tr><th>SR</th><th>ITEM</th><th>QTY</th><th>RATE</th><th>AMT</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
        <tfoot><tr><td colspan='4' align='right'><b>GRAND TOTAL</b></td><td><b>{total}</b></td></tr></tfoot>
        </table>
        </body></html>
        """
        fd, path = tempfile.mkstemp(suffix='.html')
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(html)
        webbrowser.open('file://' + path)

    def confirm_pending_add(self):
        # read pending selection and add item accordingly
        name = self.pending_label.cget('text')
        if not name or name == 'None':
            return
        unit = self.pending_unit_cb.get() or self.unit_default_var.get()
        qty_text = self.pending_qty.get().strip()
        try:
            qty = int(qty_text)
            if qty <= 0:
                qty = 1
        except Exception:
            qty = 1
        # find rate for name+unit if exists, else fallback to first match
        rate = None
        for it in self.menu_data:
            if it[0] == name and it[1] == unit:
                rate = it[2]
                break
        if rate is None:
            for it in self.menu_data:
                if it[0] == name:
                    rate = it[2]
                    break
        if rate is None:
            rate = 0

        item_to_add = [name, unit, rate]
        # add qty times (or set qty)
        # ensure dict uses qty value
        name_key = f"{name}_{unit}"
        if name_key in self.current_bill:
            self.current_bill[name_key][2] += qty
        else:
            self.current_bill[name_key] = [name, unit, qty, rate]
        self.refresh_table()
        # clear pending and return focus to search
        self.hide_pending()
        self.search_var.set("")
        self.search_entry.focus()

    # ----------------- Function Key Actions -----------------
    def add_new_item_dialog(self):
        name = simpledialog.askstring("Add Item", "Item name:", parent=self.root)
        if not name:
            return
        unit = simpledialog.askstring("Add Item", "Unit/ Packing:", parent=self.root) or '1'
        try:
            rate = float(simpledialog.askstring("Add Item", "Rate:", parent=self.root) or '0')
        except Exception:
            rate = 0.0
        self.menu_data.append([name.strip().upper(), unit.strip(), rate])
        # refresh menu and ensure added item shows
        self.filter_menu()
        messagebox.showinfo("Add Item", f"Added {name} | {unit} | {rate}")

    def bill_correction_dialog(self):
        # allow setting quantity of selected bill item
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Correction", "Select an item in bill to correct")
            return
        item_text = self.tree.item(selected[0])['values'][1]
        # find matching key
        for key, data in list(self.current_bill.items()):
            if data[0] in item_text:
                new_qty = simpledialog.askinteger("Correction", f"Set quantity for {data[0]}:", initialvalue=data[2], parent=self.root)
                if new_qty is None:
                    return
                if new_qty <= 0:
                    del self.current_bill[key]
                else:
                    self.current_bill[key][2] = new_qty
                self.refresh_table()
                return

    def print_kot(self):
        if not self.current_bill:
            messagebox.showinfo("KOT", "No items for KOT")
            return
        rows = []
        for idx, (k, v) in enumerate(self.current_bill.items(), 1):
            name, packing, qty, rate = v
            rows.append(f"<tr><td>{idx}</td><td>{name} {packing}</td><td>{qty}</td></tr>")
        html = f"""
        <html><body><h3>KOT</h3><table border='1'><thead><tr><th>SR</th><th>ITEM</th><th>QTY</th></tr></thead><tbody>{''.join(rows)}</tbody></table></body></html>
        """
        fd, path = tempfile.mkstemp(suffix='.html')
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(html)
        webbrowser.open('file://' + path)

    def save_order(self, paid=False):
        # Save current bill as an order. paid=False means saved but unpaid.
        if not self.current_bill:
            messagebox.showinfo("Save", "No items to save")
            return
        total = sum(v[2] * v[3] for v in self.current_bill.values())
        order_id = len(self.orders) + 1
        # snapshot items
        items = [v.copy() for v in self.current_bill.values()]
        order = {
            'id': order_id,
            'table': self.table_var.get() or 'NA',
            'waiter': self.waiter_var.get() or 'NA',
            'items': items,
            'total': total,
            'paid': bool(paid)
        }
        self.orders.append(order)
        tag = 'paid' if paid else 'unpaid'
        self.orders_tree.insert('', 'end', iid=str(order_id), values=(order['table'], order['waiter'], f"{total}", 'PAID' if paid else 'PENDING'), tags=(tag,))
        messagebox.showinfo("Save", f"Order saved (ID {order_id}) - {'PAID' if paid else 'PENDING'}")
        # if saving unpaid, clear current bill and start next order
        if not paid:
            self.current_bill.clear()
            self.refresh_table()

    def show_order_details(self):
        sel = self.orders_tree.selection()
        if not sel:
            return
        oid = int(sel[0])
        order = next((o for o in self.orders if o['id'] == oid), None)
        if not order:
            return
        lines = [f"Table: {order['table']}  Waiter: {order['waiter']}  Status: {'PAID' if order['paid'] else 'PENDING'}\n"]
        for itm in order['items']:
            lines.append(f"{itm[0]} {itm[1]} x{itm[2]} @ {itm[3]} = {itm[2]*itm[3]}")
        lines.append(f"\nTotal: {order['total']}")
        messagebox.showinfo(f"Order {order['id']}", "\n".join(lines))

    def clear_blank(self):
        # clear search and pending area
        self.search_var.set("")
        self.hide_pending()
        self.search_entry.focus()

    def payment_dialog(self):
        if not self.current_bill:
            messagebox.showinfo("Payment", "No items in bill")
            return
        total = sum(v[2] * v[3] for v in self.current_bill.values())
        paid = simpledialog.askfloat("Payment", f"Grand total {total}. Enter paid amount:", parent=self.root)
        if paid is None:
            return
        change = paid - total
        messagebox.showinfo("Payment", f"Paid: {paid}\nChange: {change}")
        # mark saved unpaid order as paid if exists (match by table+items), otherwise save as paid
        matched = False
        # create comparable items signature
        curr_items_sig = sorted([(v[0], v[1], v[2], v[3]) for v in self.current_bill.values()])
        for o in self.orders:
            if (o['table'] == (self.table_var.get() or 'NA') and
                sorted([(it[0], it[1], it[2], it[3]) for it in o['items']]) == curr_items_sig and
                not o['paid']):
                o['paid'] = True
                # update tree
                iid = str(o['id'])
                self.orders_tree.item(iid, values=(o['table'], o['waiter'], f"{o['total']}", 'PAID'))
                self.orders_tree.item(iid, tags=('paid',))
                matched = True
                break
        if not matched:
            # save as new paid order
            self.save_order(paid=True)
        # clear bill after payment
        self.current_bill.clear()
        self.refresh_table()

    def toggle_cash_counter(self):
        self.cash_counter_on = not getattr(self, 'cash_counter_on', False)
        state = 'ON' if self.cash_counter_on else 'OFF'
        messagebox.showinfo("Counter Cash", f"Counter Cash is now {state}")

    # ----------------- Shortcuts -----------------
    def bind_shortcuts(self):
        # Focus table: Ctrl+T
        self.root.bind_all('<Control-t>', lambda e: self.table_entry.focus())
        # Confirm table: Enter when in table -> focus waiter
        self.table_entry.bind('<Return>', lambda e: self.waiter_cb.focus())
        # Focus waiter: Ctrl+W
        self.root.bind_all('<Control-w>', lambda e: self.waiter_cb.focus())
        # Confirm waiter: Enter -> focus search
        self.waiter_cb.bind('<Return>', lambda e: self.search_entry.focus())
        # Focus search: Ctrl+S
        self.root.bind_all('<Control-s>', lambda e: self.search_entry.focus())
        # Add selected item: Ctrl+Return while searching/listbox
        self.root.bind_all('<Control-Return>', lambda e: self.add_selected_from_listbox())
        # Toggle unit default: Ctrl+U
        self.root.bind_all('<Control-u>', lambda e: self.use_unit_default.set(not self.use_unit_default.get()))
        # Qty adjustments via + and - keys (when tree focused)
        self.root.bind_all('+', lambda e: self.adjust_qty(1))
        self.root.bind_all('-', lambda e: self.adjust_qty(-1))
        # Delete key to remove
        self.root.bind_all('<Delete>', lambda e: self.delete_item())
        # Print F10
        self.root.bind_all('<F10>', lambda e: self.print_online())
        # Function keys F1-F10
        self.root.bind_all('<F1>', lambda e: self.print_online())
        self.root.bind_all('<F2>', lambda e: self.add_new_item_dialog())
        self.root.bind_all('<F3>', lambda e: self.bill_correction_dialog())
        self.root.bind_all('<F4>', lambda e: self.print_kot())
        self.root.bind_all('<F5>', lambda e: self.clear_blank())
        self.root.bind_all('<F7>', lambda e: self.table_entry.focus())
        self.root.bind_all('<F8>', lambda e: self.payment_dialog())
        self.root.bind_all('<F9>', lambda e: self.toggle_cash_counter())
        self.root.bind_all('<F6>', lambda e: self.save_order(paid=False))
        # PageDown / PageUp to navigate listbox selection
        self.root.bind_all('<Next>', lambda e: self.move_listbox(1))
        self.root.bind_all('<Prior>', lambda e: self.move_listbox(-1))
        # also bind generic key events to catch variations
        self.root.bind_all('<Key>', self._global_key_handler)


if __name__ == "__main__":
    root = tk.Tk()
    app = BarPOSApp(root)
    root.mainloop()