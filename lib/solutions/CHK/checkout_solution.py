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
        base_price: int,
        multiples_prices: dict[int, int] | None = None,
        freebies: dict[int, str] | None = None,
    ) -> None:
        self.base_price = base_price
        self.multiples_prices = multiples_prices or {}
        self.freebies = freebies or {}
        self.total = 0
        self.free_items_available = {}

    def calculate_outcome(self, qty: int) -> None:
        return


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
