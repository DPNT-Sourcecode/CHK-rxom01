from collections import Counter, defaultdict
from typing import Iterable

# noinspection PyUnusedLocal
# skus = unicode string

ILLEGAL_INPUT: int = -1


class SkuPricer:
    def __init__(
        self,
        sku: str,
        prices: dict[int, int],
        freebies: tuple[int, str] | None = None,
    ) -> None:
        self.sku = sku
        self.prices = prices
        if freebies:
            self.freebie_qty = freebies[0]
            self.freebie_item = freebies[1]
            if self.freebie_item == self.sku:
                self.freebie_qty += 1
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


PRICE_TABLE = {
    pricer.sku: pricer
    for pricer in [
        SkuPricer("A", {1: 50, 3: 130, 5: 200}),
        SkuPricer("B", {1: 30, 2: 45}),
        SkuPricer("C", {1: 20}),
        SkuPricer("D", {1: 15}),
        SkuPricer("E", {1: 40}, (2, "B")),
        SkuPricer("F", {1: 10}, (2, "F")),
        SkuPricer("G", {1: 20}),
        SkuPricer("H", {1: 10, 5: 45, 10: 80}),
        SkuPricer("I", {1: 35}),
        SkuPricer("J", {1: 60}),
        SkuPricer("K", {1: 80, 2: 150}),
        SkuPricer("L", {1: 90}),
        SkuPricer("M", {1: 15}),
        SkuPricer("N", {1: 40}, (3, "M")),
        SkuPricer("O", {1: 10}),
        SkuPricer("P", {1: 50, 5: 200}),
        SkuPricer("Q", {1: 30, 3: 80}),
        SkuPricer("R", {1: 50}, (3, "Q")),
        SkuPricer("S", {1: 30}),
        SkuPricer("T", {1: 20}),
        SkuPricer("U", {1: 40}, (3, "U")),
        SkuPricer("V", {1: 50, 2: 90, 3: 130}),
        SkuPricer("W", {1: 20}),
        SkuPricer("X", {1: 90}),
        SkuPricer("Y", {1: 10}),
        SkuPricer("Z", {1: 50}),
    ]
}


class ComboPricer:
    def __init__(self, pricers: Iterable[SkuPricer], skus: str, qty: int, price: int):
        self.pricers = {pricer.sku: pricer for pricer in pricers if pricer.sku in skus}
        self.skus = skus
        self.qty: int = qty
        self.price: int = price
        self.total: int = 0
        self.priced_items: dict[str, int] = {}

    def calculate(self, skus: str) -> None:
        combo_skus = [sku for sku in skus if sku in self.skus]
        combo_skus.sort(key=lambda sku: self.pricers[sku].prices[1], reverse=True)
        combos_in_list = len(combo_skus) // self.qty
        self.total = self.price * combos_in_list
        combo_skus = combo_skus[: combos_in_list * self.qty]
        self.priced_items = Counter(combo_skus)


COMBO_PRICER = ComboPricer(PRICE_TABLE.values(), "STXYZ", 3, 45)


def checkout(skus: str) -> int:
    if not isinstance(skus, str):
        return ILLEGAL_INPUT
    if not all(c.isalpha() for c in skus):
        return ILLEGAL_INPUT
    if not skus.upper() == skus:
        return -1
    try:
        return checkout_total(skus, PRICE_TABLE)
    except KeyError:
        return -1


def checkout_total(
    skus: str, price_table: dict, combo: ComboPricer | None = None
) -> int:
    counts = sku_order_counts(skus)
    total = 0
    if combo:
        combo.calculate(skus)
        total += combo.total
        for sku, priced_qty in combo.priced_items.items():
            counts[sku] -= priced_qty
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
    for sku, qty in counts.items():
        pricer = price_table.get(sku)
        if pricer:
            total += pricer.total_for_qty(qty)
    return total


def sku_order_counts(skus: str) -> dict[str, int]:
    return Counter(skus)







