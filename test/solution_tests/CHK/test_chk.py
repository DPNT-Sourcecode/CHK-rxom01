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

    def test_price_calc_from_table(self):
        price_table = {"A": {1: 10, 3: 25}}
        assert checkout_solution.item_price_for_quantity("A", 1, price_table) == 10

    def test_no_price_for_sku_returns_negative_one(self):
        price_table = {}
        with pytest.raises(ValueError):
            assert checkout_solution.item_price_for_quantity("A", 1, price_table) == -1

    def test_multiple_requested_for_sku_no_discount(self):
        price_table = {"A": {1: 1}}
        assert checkout_solution.item_price_for_quantity("A", 5, price_table) == 5

    def test_multiple_requested_for_sku_with_discount(self):
        price_table = {"A": {1: 10, 2: 15}}
        assert checkout_solution.item_price_for_quantity("A", 3, price_table) == 25

    def test_checkout_counts_skus_orders(self):
        assert checkout_solution.sku_order_counts("ABABACZA") == {
            "A": 4,
            "B": 2,
            "C": 1,
            "Z": 1,
        }

    def test_checkout_calculates_multiple_item_total(self):
        assert checkout_solution.checkout("AAAABBBCCD") == 180 + 75 + 40 + 15

    def test_multiple_Es_gets_a_free_B(self):
        assert False
