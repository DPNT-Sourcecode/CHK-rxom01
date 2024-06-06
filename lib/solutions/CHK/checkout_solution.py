# noinspection PyUnusedLocal
# skus = unicode string

ILLEGAL_INPUT: int = -1


def checkout(skus: str) -> int:
    if not isinstance(skus, str):
        return ILLEGAL_INPUT
    if not all(c.isalpha() for c in skus):
        return ILLEGAL_INPUT
    return 0


def item_price_for_quantity(
    sku: str, qty: int, price_table: dict[str, dict[int, int]]
) -> int:
    prices = price_table.get(sku, {})
    if not prices:
        return -1
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
    return {}


