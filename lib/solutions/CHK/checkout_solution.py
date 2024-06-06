# noinspection PyUnusedLocal
# skus = unicode string

ILLEGAL_INPUT: int = -1


def checkout(skus: str) -> int:
    if not isinstance(skus, str):
        return ILLEGAL_INPUT
    if not all(c.isalpha() for c in skus):
        return ILLEGAL_INPUT
    return 0


