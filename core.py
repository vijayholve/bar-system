import copy


class OrderManager:
    """Separation of business logic from UI. Manages current bill and saved orders."""
    def __init__(self, menu_data=None):
        # menu_data: list of [name, unit, rate]
        self.menu_data = menu_data or []
        # current_bill: key -> [name, unit, qty, rate]
        self.current_bill = {}
        # orders: list of order dicts
        self.orders = []

    def add_item(self, name, unit, rate, qty=1):
        key = f"{name}_{unit}"
        if key in self.current_bill:
            self.current_bill[key][2] += qty
        else:
            self.current_bill[key] = [name, unit, qty, rate]

    def set_qty(self, key, qty):
        if key in self.current_bill:
            if qty <= 0:
                del self.current_bill[key]
            else:
                self.current_bill[key][2] = qty

    def adjust_qty(self, key, delta):
        if key in self.current_bill:
            self.current_bill[key][2] += delta
            if self.current_bill[key][2] <= 0:
                del self.current_bill[key]

    def delete_item(self, key):
        if key in self.current_bill:
            del self.current_bill[key]

    def get_bill_items(self):
        # returns list of [name, unit, qty, rate]
        return [v for v in self.current_bill.values()]

    def get_grand_total(self):
        return sum(v[2] * v[3] for v in self.current_bill.values())

    def clear_bill(self):
        self.current_bill.clear()

    def save_order(self, table='NA', waiter='NA', paid=False):
        if not self.current_bill:
            return None
        order_id = len(self.orders) + 1
        items = [v.copy() for v in self.current_bill.values()]
        total = sum(v[2] * v[3] for v in items)
        order = {
            'id': order_id,
            'table': table or 'NA',
            'waiter': waiter or 'NA',
            'items': items,
            'total': total,
            'paid': bool(paid)
        }
        self.orders.append(order)
        return order

    def delete_order(self, order_id):
        self.orders = [o for o in self.orders if o['id'] != order_id]

    def find_order(self, order_id):
        return next((o for o in self.orders if o['id'] == order_id), None)

    def load_order_into_bill(self, order_id):
        order = self.find_order(order_id)
        if not order:
            return False
        self.current_bill.clear()
        for itm in order['items']:
            name, unit, qty, rate = itm
            self.current_bill[f"{name}_{unit}"] = [name, unit, qty, rate]
        return True
