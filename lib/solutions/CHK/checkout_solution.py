import itertools
from collections import Counter, defaultdict

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

    def total_for_qty(self, qty: int) -> int:
        amount = 0
        remaining_qty = qty
        while remaining_qty > 0:
            largest_available_discounted_qty = max(
                discounted_qty
                for discounted_qty in self.prices.keys()
                if discounted_qty <= remaining_qty
            )
            amount += self.prices[largest_available_discounted_qty]
            remaining_qty -= largest_available_discounted_qty
        return amount

    def freebies_for_qty(self, qty: int) -> dict[str, int]:
        free_items_available: dict[str, int] = {}
        if self.freebie_qty > 0:
            item_qty = qty // self.freebie_qty
            free_items_available[self.freebie_item] = item_qty
        return free_items_available

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
    skus = skus.upper()
    try:
        return checkout_total(skus, PRICE_TABLE)
    except ValueError:
        return -1


def checkout_total(skus: str, price_table: dict) -> int:
    counts = sku_order_counts(skus)
    freebies = defaultdict(int)
    for sku, qty in counts.items():
        pricer = price_table.get(sku)
        if pricer:
            for sku, free_qty in pricer.freebies_for_qty(qty).items():
                freebies[sku] += free_qty
        else:
            raise KeyError(f"no pricer for {sku=}")
    for sku, total_free in freebies.items():
        counts[sku] = max(0, counts[sku] - total_free)
    total = 0
    for sku, qty in counts.items():
        pricer = price_table.get(sku)
        if pricer:
            total += pricer.total_for_qty(qty)
    return total


def sku_order_counts(skus: str) -> dict[str, int]:
    return Counter(skus)







