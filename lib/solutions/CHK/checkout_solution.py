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

    def freebies_for_qty(self, qty) -> dict[str, int]:
        free_items_available = {}
        if self.freebie_qty > 0:
            item_qty = qty // self.freebie_qty
            items = [self.freebie_item] * item_qty
            free_items_available = items
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
    try:
        return checkout_total(skus, PRICE_TABLE)
    except ValueError:
        return -1


def checkout_total(skus: str, price_table: dict) -> int:
    counts = sku_order_counts(skus)
    freebies = defaultdict(int)
    for sku, qty in counts:
        pricer = price_table.get(sku)
        if pricer:
            for sku, free_qty in pricer.freebies_for_qty(qty).items():
                freebies[sku] += free_qty
        else:
            raise KeyError(f"no pricer for {sku=}")

    free_items = itertools.chain.from_iterable(
        [pricer.free_items_available for pricer in pricers]
    )

    free_item_counts = Counter(free_items)

    for sku, free_qty in free_item_counts.items():
        ordered = counts[sku]
        deductible = min(free_qty, ordered)
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



