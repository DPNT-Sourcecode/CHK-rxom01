import pytest
from solutions.CHK import checkout_solution as chk


class TestChk:
    def test_valid_param_types(self):
        assert chk.checkout(123) == -1

    def test_input_is_all_alpha(self):
        assert chk.checkout("123") == -1
        assert chk.checkout("+/'") == -1

    def test_empty_string_returns_zero(self):
        assert chk.checkout("") == 0

    def test_price_calc_from_table(self):
        pricer = chk.SkuPricer({1: 10, 3: 25})
        assert pricer.total_for_qty(1) == 10

    def test_multiple_requested_for_sku_no_discount(self):
        pricer = chk.SkuPricer({1: 1})
        assert pricer.total_for_qty(5) == 5

    def test_multiple_requested_for_sku_with_discount(self):
        price_table = {"A": chk.SkuPricer({1: 10, 2: 15})}
        assert chk.pricer_for_item_and_quantity("A", 3, price_table).total == 25

    def test_multiple_requested_for_sku_with_multiple_discount_levels(self):
        pricer = chk.SkuPricer({1: 10, 2: 18, 6: 48})
        assert pricer.total_for_qty(9) == 76

    def test_checkout_counts_skus_orders(self):
        assert chk.sku_order_counts("ABABACZA") == {
            "A": 4,
            "B": 2,
            "C": 1,
            "Z": 1,
        }

    def test_checkout_calculates_multiple_item_total(self):
        assert chk.checkout("AAAABBBCCD") == 180 + 75 + 40 + 15

    def test_multiple_Es_gets_a_free_B_when_ordered(self):
        price_table = {
            "E": chk.SkuPricer({1: 40}, (2, "B")),
            "B": chk.SkuPricer({1: 30}),
        }
        price = chk.checkout_total("EEB", price_table)
        assert price == 80

    def test_pricer_with_freebie_records_correctly(self):
        pricer = chk.SkuPricer({1: 1}, (2, "B"))
        assert pricer.freebies_for_qty(3) == {"B": 1}

    def test_multiple_Es_gets_a_free_B(self):
        price_table = {
            "E": chk.SkuPricer({1: 40}, (2, "B")),
            "B": chk.SkuPricer({1: 100}),
        }
        assert chk.checkout_total("EE", price_table) == 80


