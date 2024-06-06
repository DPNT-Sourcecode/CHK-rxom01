import pytest
from solutions.HLO import hello_solution


class TestHlo:
    def test_types_are_valid(self):
        with pytest.raises(AssertionError):
            assert hello_solution.hello(123) == "Hello 123"

    def test_includes_friend_name(self):
        assert hello_solution.hello("Bob") == "Hello, Bob!"
