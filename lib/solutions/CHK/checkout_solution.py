import itertools
from collections import Counter

# noinspection PyUnusedLocal
# skus = unicode string

ILLEGAL_INPUT: int = -1


class SkuPricer:
    def __init__(
        self,
        prices: dict[int, int],
        freebies: tuple[int, str] | None = None,
    ) -> None:
        self.prices = prices
        self.freebies = freebies
        self.total = 0
        self.free_items_available = []

    def calculate_outcome(self, qty: int) -> None:
        while qty > 0:
            largest_available_discounted_qty = max(
                discounted_qty
                for discounted_qty in self.prices.keys()
                if discounted_qty <= qty
            )
            self.total += self.prices[largest_available_discounted_qty]
            qty -= largest_available_discounted_qty
            if self.freebies and qty >= self.freebies[0]:
                self.free_items_available.append(self.freebies[1])
            # print(f"{largest_available_discounted_qty=}")
            # print(f"{qty=}")
            # print(f"{self.total=}")
            # print(f"{self.free_items_available=}")


PRICE_TABLE = {
    "A": SkuPricer({1: 50, 3: 130, 5: 200}),
    "B": SkuPricer({1: 30, 2: 45}),
    "C": SkuPricer({1: 20}),
    "D": SkuPricer({1: 15}),
    "E": SkuPricer({1: 40}, (2, "B")),
}


def checkout(skus: str) -> int:
    if not isinstance(skus, str):
        return ILLEGAL_INPUT
    if not all(c.isalpha() for c in skus):
        return ILLEGAL_INPUT
    try:
        return checkout_total(skus, PRICE_TABLE)
    except ValueError:
        return -1


def checkout_total(skus: str, price_table: dict) -> int:
    counts = sku_order_counts(skus)
    pricers = [
        pricer_for_item_and_quantity(sku, qty, price_table)
        for sku, qty in counts.items()
    ]
    total = sum(pricer.total for pricer in pricers)
    all_free_items = [pricer.free_items_available for pricer in pricers]
    free_items = itertools.chain.from_iterable(all_free_items)
    freebie_counts = Counter(free_items)
    discount_amount = 0
    print(f"{freebie_counts=}")
    for sku, free_qty in freebie_counts.items():
        ordered = max(0, counts.get(sku, 0) - free_qty)
        recalc_pricer = price_table[sku].calculate_outcome(ordered)
        discount_amount += recalc_pricer.total
    return total - discount_amount


def pricer_for_item_and_quantity(
    sku: str, qty: int, price_table: dict[str, SkuPricer]
) -> SkuPricer:
    pricer = price_table.get(sku)
    if not pricer:
        raise ValueError(f"no price info for sku {sku}")
    pricer.calculate_outcome(qty)
    return pricer


def sku_order_counts(skus: str) -> dict[str, int]:
    return Counter(skus)

