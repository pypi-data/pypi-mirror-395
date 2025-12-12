"""Tests for prsdm.operations module."""

import pytest

from prsdm.operations import add, divide, multiply, subtract


def test_add():
    """Test addition operation."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    """Test subtraction operation."""
    assert subtract(5, 3) == 2
    assert subtract(0, 1) == -1
    assert subtract(10, 10) == 0


def test_multiply():
    """Test multiplication operation."""
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    assert multiply(0, 100) == 0


def test_divide():
    """Test division operation."""
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0
    assert divide(1, 2) == 0.5


def test_divide_by_zero():
    """Test division by zero raises error."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
