class InventoryManager:
    def __init__(self):
        self._stock = {}

    def add_item(self, name, quantity):
        self._validate_item(name, quantity)
        self._stock[name] = self._stock.get(name, 0) + quantity
        return self._stock[name]

    def remove_item(self, name, quantity):
        self._validate_item(name, quantity)
        if name not in self._stock:
            raise KeyError("Item is not in inventory")
        if quantity > self._stock[name]:
            raise ValueError("Insufficient stock")

        self._stock[name] -= quantity
        if self._stock[name] == 0:
            del self._stock[name]
        return self._stock.get(name, 0)

    def get_stock(self, name):
        if name not in self._stock:
            raise KeyError("Item is not in inventory")
        return self._stock[name]

    def list_inventory(self):
        return self._stock.copy()

    @staticmethod
    def _validate_item(name, quantity):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Item name must not be empty")
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

# Run steps for Prac3:
# 1. Open terminal in this folder.
# 2. Run: python -m pytest -q
# 3. Optional: use Python shell to create InventoryManager and check add/remove behavior.
