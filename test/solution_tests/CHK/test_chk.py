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

    def test_lowercase_alpha_invalid(self):
        assert chk.checkout("aaaB") == -1

    def test_price_calc_from_table(self):
        pricer = chk.SkuPricer("A", {1: 10, 3: 25})
        assert pricer.total_for_qty(1) == 10

    def test_multiple_requested_for_sku_no_discount(self):
        pricer = chk.SkuPricer("A", {1: 1})
        assert pricer.total_for_qty(5) == 5

    def test_multiple_requested_for_sku_with_discount(self):
        pricer = chk.SkuPricer("A", {1: 10, 2: 15})
        assert pricer.total_for_qty(3) == 25

    def test_multiple_requested_for_sku_with_multiple_discount_levels(self):
        pricer = chk.SkuPricer("A", {1: 10, 2: 18, 6: 48})
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
            "E": chk.SkuPricer("E", {1: 40}, (2, "B")),
            "B": chk.SkuPricer("B", {1: 30}),
        }
        price = chk.checkout_total("EEB", price_table)
        assert price == 80

    def test_pricer_with_freebie_records_correctly(self):
        pricer = chk.SkuPricer("A", {1: 1}, (2, "B"))
        assert pricer.freebies_for_qty(3) == {"B": 1}

    def test_multiple_Es_gets_a_free_B(self):
        price_table = {
            "E": chk.SkuPricer("E", {1: 40}, (2, "B")),
            "B": chk.SkuPricer("B", {1: 100}),
        }
        assert chk.checkout_total("EE", price_table) == 80

    def test_bogof(self):
        pricer = chk.SkuPricer("F", {1: 10}, (2, "F"))
        price_table = {"F": pricer}
        assert chk.checkout_total("FFF", price_table) == 20

    def test_combo(self):
        pricers = {
            p.sku: p
            for p in [
                chk.SkuPricer("A", {1: 10}),
                chk.SkuPricer("B", {1: 11}),
                chk.SkuPricer("C", {1: 12}),
            ]
        }
        combo = chk.ComboPricer(pricers.values(), "AB", 2, 18)
        assert chk.checkout_total("AAABB", pricers, combo) == 46


