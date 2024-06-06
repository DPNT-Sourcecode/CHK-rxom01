from collections import Counter

# noinspection PyUnusedLocal
# skus = unicode string

ILLEGAL_INPUT: int = -1

PRICE_TABLE = {
    "A": {1: 50, 3: 130},
    "B": {1: 30, 2: 45},
    "C": {1: 20},
    "D": {1: 15},
}


def checkout(skus: str) -> int:
    if not isinstance(skus, str):
        return ILLEGAL_INPUT
    if not all(c.isalpha() for c in skus):
        return ILLEGAL_INPUT
    try:
        counts = sku_order_counts(skus).items()
        print(counts)
        return sum(
            item_price_for_quantity(sku, qty, PRICE_TABLE) for sku, qty in counts
        )
    except ValueError:
        return -1


def item_price_for_quantity(
    sku: str, qty: int, price_table: dict[str, dict[int, int]]
) -> int:
    prices = price_table.get(sku, {})
    if not prices:
        raise ValueError(f"no price table for sku {sku}")
    qty_priced = 0
    total = 0
    while qty_priced < qty:
        largest_available_discounted_qty = max(
            discountable_qty
            for discountable_qty in prices.keys()
            if discountable_qty <= (qty - qty_priced)
        )
        total += prices[largest_available_discounted_qty]
        qty_priced += largest_available_discounted_qty
    return total


def sku_order_counts(skus: str) -> dict[str, int]:
    return Counter(skus)





