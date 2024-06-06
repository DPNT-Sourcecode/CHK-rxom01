from collections import Counter

# noinspection PyUnusedLocal
# skus = unicode string

ILLEGAL_INPUT: int = -1


PRICE_TABLE = {
    "A": {1: 50, 3: 130, 5: 200},
    "B": {1: 30, 2: 45},
    "C": {1: 20},
    "D": {1: 15},
    "E": {},
}


class SkuPricer:
    def __init__(
        self,
        prices: dict[int, int],
        freebies: tuple[int, str] | None = None,
    ) -> None:
        self.multiples_prices = prices
        self.freebies = freebies
        self.total = 0
        self.free_items_available = {}

    def calculate_outcome(self, qty: int) -> None:
        qty_priced = 0
        while qty > 0:
            largest_available_discounted_qty = max(
                discounted_qty for discounted_qty in self.multiples_prices.keys()
            )
            self.total += self.prices[largest_available_discounted_qty]
            qty -= largest_available_discounted_qty
            if

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
    counts = sku_order_counts(skus).items()
    return sum(item_price_for_quantity(sku, qty, price_table) for sku, qty in counts)


def item_price_for_quantity(
    sku: str, qty: int, price_table: dict[str, SkuPricer]
) -> SkuPricer:
    pricer = price_table.get(sku)
    if not pricer:
        raise ValueError(f"no price info for sku {sku}")
    pricer.calculate_outcome(qty)
    return pricer


def sku_order_counts(skus: str) -> dict[str, int]:
    return Counter(skus)

