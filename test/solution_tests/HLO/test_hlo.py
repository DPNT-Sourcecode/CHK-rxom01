import pytest
from solutions.HLO import hello_solution


class TestHlo:
    def test_types_are_valid(self):
        with pytest.raises(AssertionError):
            assert hello_solution.hello(123) == "Hello 123"
