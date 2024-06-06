import pytest
from solutions.CHK import checkout_solution


class TestChk:
    def test_valid_param_types(self):
        assert checkout_solution.checkout(123) == -1

    def test_input_is_all_alpha(self):
        assert checkout_solution.checkout("123") == -1
        assert checkout_solution.checkout("+/'") == -1

    def test_empty_string_returns_zero(self):
        assert checkout_solution.checkout("") == 0

