import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import webbrowser, tempfile, os
from core import OrderManager


class BarPOSUI:
    def __init__(self, root, menu_data):
        self.root = root
        self.root.title("Hotellexa - Bar (Refactored)")
        self.root.geometry("1100x700")
        self.root.configure(bg="#111")

        self.manager = OrderManager(menu_data=menu_data)

        self.table_var = tk.StringVar()
        self.waiter_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.unit_default_var = tk.StringVar()
        self.use_unit_default = tk.BooleanVar(value=True)

        self.waiters = ["Select", "Waiter A", "Waiter B"]

        self.filtered_items = []

        self._build_ui()
        self._bind_shortcuts()

        self.root.after(100, lambda: self.table_entry.focus())

    def _build_ui(self):
        # Top bar
        top = tk.Frame(self.root, bg="#222")
        top.pack(fill='x', padx=6, pady=6)
        tk.Label(top, text="Table:", bg="#222", fg='white').pack(side='left')
        self.table_entry = tk.Entry(top, textvariable=self.table_var, width=8)
        self.table_entry.pack(side='left', padx=4)
        tk.Label(top, text="Waiter:", bg="#222", fg='white').pack(side='left', padx=8)
        self.waiter_cb = ttk.Combobox(top, values=self.waiters, textvariable=self.waiter_var, state='readonly', width=12)
        self.waiter_cb.current(0)
        self.waiter_cb.pack(side='left')

        main = tk.Frame(self.root, bg='#111')
        main.pack(fill='both', expand=True, padx=6, pady=6)

        # left: menu and search
        left = tk.Frame(main, bg='#1a1a1a')
        left.pack(side='left', fill='both', expand=True)

        sframe = tk.Frame(left, bg='#1a1a1a')
        sframe.pack(fill='x')
        tk.Label(sframe, text='Search', bg='#1a1a1a', fg='white').pack(side='left')
        self.search_entry = tk.Entry(sframe, textvariable=self.search_var)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=6)
        self.search_var.trace_add('write', lambda *a: self._filter_menu())

        self.menu_listbox = tk.Listbox(left)
        self.menu_listbox.pack(fill='both', expand=True, padx=6, pady=6)
        self.menu_listbox.bind('<Double-1>', lambda e: self.open_pending_from_listbox())

        # pending area
        pf = tk.Frame(left, bg='#222')
        pf.pack(fill='x', padx=6, pady=4)
        tk.Label(pf, text='Unit:', bg='#222', fg='white').pack(side='left')
        self.pending_unit_cb = ttk.Combobox(pf, values=[], width=8)
        self.pending_unit_cb.pack(side='left', padx=4)
        tk.Label(pf, text='Qty:', bg='#222', fg='white').pack(side='left', padx=4)
        self.pending_qty = tk.Entry(pf, width=6)
        self.pending_qty.pack(side='left')
        tk.Button(pf, text='Add', command=self.confirm_pending_add).pack(side='left', padx=6)

        # middle: bill
        mid = tk.Frame(main, bg='#111')
        mid.pack(side='left', fill='both', expand=True)
        cols = ("SR", "ITEM", "QTY", "RATE", "AMT")
        self.tree = ttk.Treeview(mid, columns=cols, show='headings', height=15)
        for c in cols:
            self.tree.heading(c, text=c)
        self.tree.pack(fill='both', expand=True, padx=6, pady=6)

        # right: total and actions
        right = tk.Frame(main, bg='#0a0a0a', width=260)
        right.pack(side='left', fill='y')
        self.total_lbl = tk.Label(right, text='0', font=('Helvetica', 36), bg='#0a0a0a', fg='#0f0')
        self.total_lbl.pack(pady=40)

        tk.Button(right, text='+ Qty', command=lambda: self._adjust_selected(1)).pack(fill='x', padx=8, pady=4)
        tk.Button(right, text='- Qty', command=lambda: self._adjust_selected(-1)).pack(fill='x', padx=8, pady=4)
        tk.Button(right, text='Delete Item', command=self._delete_selected).pack(fill='x', padx=8, pady=4)
        tk.Button(right, text='Save Order', command=lambda: self._save_order(False)).pack(fill='x', padx=8, pady=4)
        tk.Button(right, text='Save Paid', command=lambda: self._save_order(True)).pack(fill='x', padx=8, pady=4)

        # orders list
        of = tk.Frame(self.root, bg='#111')
        of.pack(fill='x', padx=6, pady=4)
        self.orders_tree = ttk.Treeview(of, columns=('TABLE','WAITER','TOTAL','STATUS'), show='headings', height=4)
        for c in ('TABLE','WAITER','TOTAL','STATUS'):
            self.orders_tree.heading(c, text=c)
        self.orders_tree.pack(fill='x', expand=True)
        self.orders_tree.bind('<Double-1>', lambda e: self._open_order_actions())

        # populate menu
        self._filter_menu()
        # start animation
        self._animate_total()

    # --- UI helpers ---
    def _filter_menu(self):
        q = self.search_var.get().strip().lower()
        self.menu_listbox.delete(0, 'end')
        self.filtered_items = []
        for it in self.manager.menu_data:
            display = f"{it[0]} | {it[1]} | ₹{it[2]}"
            if not q or q in it[0].lower() or q in str(it[1]).lower():
                self.menu_listbox.insert('end', display)
                self.filtered_items.append(it)

    def open_pending_from_listbox(self):
        sel = self.menu_listbox.curselection()
        if not sel: return
        itm = self.filtered_items[sel[0]]
        self.pending_unit_cb['values'] = [p[1] for p in self.manager.menu_data if p[0]==itm[0]]
        try:
            self.pending_unit_cb.current(0)
        except Exception:
            pass
        self.pending_qty.delete(0,'end')
        self.pending_qty.insert(0,'1')

    def confirm_pending_add(self):
        sel = self.menu_listbox.curselection()
        if not sel:
            return
        itm = self.filtered_items[sel[0]]
        name = itm[0]
        unit = self.pending_unit_cb.get() or itm[1]
        try:
            qty = int(self.pending_qty.get())
        except Exception:
            qty = 1
        # find rate
        rate = None
        for it in self.manager.menu_data:
            if it[0]==name and it[1]==unit:
                rate = it[2]; break
        rate = rate or itm[2]
        self.manager.add_item(name, unit, rate, qty=qty)
        self._refresh_table()

    def _refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, v in enumerate(self.manager.get_bill_items(), 1):
            name, unit, qty, rate = v
            amt = qty*rate
            self.tree.insert('', 'end', values=(idx, f"{name} {unit}", qty, rate, amt))
        total = self.manager.get_grand_total()
        self.total_lbl.config(text=f"{total}")

    def _adjust_selected(self, delta):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])['values'][1]
        # find key
        for k,v in self.manager.current_bill.items():
            if v[0] in item:
                self.manager.adjust_qty(k, delta)
                break
        self._refresh_table()

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])['values'][1]
        for k in list(self.manager.current_bill.keys()):
            if self.manager.current_bill[k][0] in item:
                self.manager.delete_item(k)
                break
        self._refresh_table()

    def _save_order(self, paid=False):
        if not self.manager.current_bill:
            messagebox.showinfo('Save','No items to save')
            return
        table = self.table_var.get() or 'NA'
        waiter = self.waiter_var.get() or 'NA'
        order = self.manager.save_order(table=table, waiter=waiter, paid=paid)
        if order:
            tag = 'PAID' if paid else 'PENDING'
            self.orders_tree.insert('', 'end', iid=str(order['id']), values=(order['table'], order['waiter'], f"{order['total']}", tag))
            if not paid:
                self.manager.clear_bill()
                self._refresh_table()
            messagebox.showinfo('Saved', f"Order {order['id']} saved ({tag})")

    def _open_order_actions(self):
        sel = self.orders_tree.selection()
        if not sel: return
        oid = int(sel[0])
        order = self.manager.find_order(oid)
        if not order: return
        d = tk.Toplevel(self.root)
        d.title(f"Order {oid}")
        tk.Label(d, text=f"Table: {order['table']}  Waiter: {order['waiter']}").pack(padx=8, pady=8)
        frm = tk.Frame(d)
        frm.pack(padx=8, pady=8)
        def on_view():
            lines = [f"{it[0]} {it[1]} x{it[2]} @ {it[3]} = {it[2]*it[3]}" for it in order['items']]
            messagebox.showinfo(f"Order {oid}", "\n".join(lines), parent=d)
        def on_edit():
            d.destroy()
            self.manager.load_order_into_bill(oid)
            self.table_var.set(order.get('table',''))
            try:
                self.waiter_cb.set(order.get('waiter',''))
            except Exception:
                pass
            self._refresh_table()
        def on_delete():
            if messagebox.askyesno('Delete', f'Delete order {oid}?', parent=d):
                self.manager.delete_order(oid)
                try:
                    self.orders_tree.delete(str(oid))
                except Exception:
                    pass
                d.destroy()
        tk.Button(frm, text='View', command=on_view).pack(side='left', padx=6)
        if not order['paid']:
            tk.Button(frm, text='Edit', command=on_edit).pack(side='left', padx=6)
            tk.Button(frm, text='Delete', command=on_delete).pack(side='left', padx=6)
        tk.Button(frm, text='Close', command=d.destroy).pack(side='left', padx=6)

    # --- printing ---
    def print_online(self):
        if not self.manager.current_bill:
            messagebox.showinfo('Print','No items to print')
            return
        rows = []
        total = 0
        for idx, v in enumerate(self.manager.get_bill_items(), 1):
            name, unit, qty, rate = v
            amt = qty*rate
            total += amt
            rows.append(f"<tr><td>{idx}</td><td>{name} {unit}</td><td>{qty}</td><td>{rate}</td><td>{amt}</td></tr>")
        html = f"""
        <html><body><h3>Bill</h3><table border='1'><thead><tr><th>SR</th><th>ITEM</th><th>QTY</th><th>RATE</th><th>AMT</th></tr></thead><tbody>{''.join(rows)}</tbody><tfoot><tr><td colspan='4'>TOTAL</td><td>{total}</td></tr></tfoot></table></body></html>
        """
        fd, path = tempfile.mkstemp(suffix='.html')
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(html)
        webbrowser.open('file://' + path)

    # --- shortcuts & animation ---
    def _bind_shortcuts(self):
        self.root.bind_all('<Control-t>', lambda e: self.table_entry.focus())
        self.root.bind_all('<Control-s>', lambda e: self.search_entry.focus())
        self.root.bind_all('<Control-Return>', lambda e: self.confirm_pending_add())
        self.root.bind_all('<F10>', lambda e: self.print_online())

    def _animate_total(self):
        # simple pulsing color animation for total label
        def pulse():
            cur = self.total_lbl.cget('fg')
            self.total_lbl.config(fg='#ff0' if cur=='#0f0' else '#0f0')
            self.root.after(600, pulse)
        pulse()
