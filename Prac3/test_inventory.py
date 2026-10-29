import pytest
from inventory import InventoryManager


def test_new_inventory_is_empty():
    inventory = InventoryManager()
    assert inventory.list_inventory() == {}


def test_add_item_records_quantity():
    inventory = InventoryManager()
    assert inventory.add_item("Notebook", 12) == 12


def test_adding_existing_item_increases_quantity():
    inventory = InventoryManager()
    inventory.add_item("Notebook", 12)
    assert inventory.add_item("Notebook", 3) == 15


@pytest.mark.parametrize("name", ["", "   ", None])
def test_add_item_rejects_invalid_name(name):
    inventory = InventoryManager()
    with pytest.raises(ValueError):
        inventory.add_item(name, 1)


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True])
def test_add_item_rejects_invalid_quantity(quantity):
    inventory = InventoryManager()
    with pytest.raises(ValueError):
        inventory.add_item("Notebook", quantity)


def test_get_stock_returns_current_quantity():
    inventory = InventoryManager()
    inventory.add_item("Notebook", 12)
    assert inventory.get_stock("Notebook") == 12


def test_get_stock_rejects_unknown_item():
    inventory = InventoryManager()
    with pytest.raises(KeyError):
        inventory.get_stock("Notebook")


def test_remove_item_reduces_quantity():
    inventory = InventoryManager()
    inventory.add_item("Notebook", 12)
    assert inventory.remove_item("Notebook", 5) == 7


def test_removing_all_stock_removes_item_from_inventory():
    inventory = InventoryManager()
    inventory.add_item("Notebook", 5)
    assert inventory.remove_item("Notebook", 5) == 0
    assert inventory.list_inventory() == {}


def test_remove_item_rejects_unknown_item():
    inventory = InventoryManager()
    with pytest.raises(KeyError):
        inventory.remove_item("Notebook", 1)


def test_remove_item_rejects_quantity_above_stock():
    inventory = InventoryManager()
    inventory.add_item("Notebook", 5)
    with pytest.raises(ValueError):
        inventory.remove_item("Notebook", 6)


def test_list_inventory_returns_a_copy():
    inventory = InventoryManager()
    inventory.add_item("Notebook", 5)
    listed = inventory.list_inventory()
    listed["Notebook"] = 0
    assert inventory.get_stock("Notebook") == 5

# Ordinary tests (PowerShell, from Prac3):
# py -m pip install pytest
# py -m pytest -q
#
# Mutation testing (WSL, from this same folder; Mutmut 3 requires fork support):
# python3 -m venv .venv-wsl
# source .venv-wsl/bin/activate
# python -m pip install pytest mutmut==3.8.0
# mutmut run
