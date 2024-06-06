# noinspection PyUnusedLocal
# friend_name = unicode string
def hello(friend_name: str) -> str:
    assert isinstance(friend_name, str)
    return f"Hello {friend_name}"


