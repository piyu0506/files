import pytest

from calculator import *

def test_add():
    assert add(15, 23) == 38

def test_subtract():
    assert subtract(20, 11) == 9

def test_multiply():
    assert multiply(8, 9) == 72

def test_divide():
    assert divide(36, 6) == 6

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(15, 0)

# From PowerShell in Prac2:
# py -m pip install pytest
# py -m pytest -q
