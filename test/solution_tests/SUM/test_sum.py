import pytest
from solutions.SUM import sum_solution


class TestSum:
    def test_sum(self):
        assert sum_solution.compute(1, 2) == 3

    def test_raises_if_not_ints(self):
        with pytest.raises(AssertionError):
            assert sum_solution.compute(1.1, 0.9) == 2

    def test_raises_if_out_of_range(self):
        with pytest.raises(AssertionError):
            assert sum_solution.compute(-1, 0) == -1
            assert sum_solution.compute(101, 0) == 101
            assert sum_solution.compute(0, -1) == -1
            assert sum_solution.compute(0, 101) == 101
            assert sum_solution.compute(-1, 101) == 100
            assert sum_solution.compute(101, -1) == 100
