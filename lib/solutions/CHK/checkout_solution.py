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
        if freebies:
            self.freebie_qty = freebies[0]
            self.freebie_item = freebies[1]
        else:
            self.freebie_qty = 0
            self.freebie_item = ""
        self.total = 0
        self.free_items_available = []

    def calculate_outcome(self, qty: int) -> None:
        self.total = 0
        self.free_items_available = []
        remaining_qty = qty
        while remaining_qty > 0:
            largest_available_discounted_qty = max(
                discounted_qty
                for discounted_qty in self.prices.keys()
                if discounted_qty <= remaining_qty
            )
            self.total += self.prices[largest_available_discounted_qty]
            remaining_qty -= largest_available_discounted_qty
        if self.freebie_qty > 0:
            item_qty = qty // self.freebie_qty
            items = [self.freebie_item] * item_qty
            self.free_items_available = items

    def __repr__(self) -> str:
        return f"prices: {self.prices}, freebies: {self.freebie_item} * {self.freebie_qty}, total:{self.total}, free_items: {self.free_items_available}"


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

    free_items = itertools.chain.from_iterable(
        [pricer.free_items_available for pricer in pricers]
    )

    free_item_counts = Counter(free_items)

    for sku, free_qty in free_item_counts.items():
        deductible = max(0, counts[sku] - free_qty)
        deduction_pricer = pricer_for_item_and_quantity(sku, deductible, price_table)
        deduction = deduction_pricer.total
        total -= deduction

    return total


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


