# noinspection PyShadowingBuiltins,PyUnusedLocal
def compute(x: int, y: int) -> int:
    assert all(isinstance(param, int) for param in [x, y])
    assert all(0 <= param <= 100 for param in [x, y])
    return x + y
