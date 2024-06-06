import pytest
from solutions.CHK import checkout_solution


class TestChk:
    def test_valid_param_types(self):
        with pytest.raises(AssertionError):
            assert checkout_solution.checkout(123) == 0

    def test_input_is_all_alpha(self):
        with pytest.raises(AssertionError):
            assert checkout_solution.checkout("123") == 0
            assert checkout_solution.checkout("+/'") == 0
