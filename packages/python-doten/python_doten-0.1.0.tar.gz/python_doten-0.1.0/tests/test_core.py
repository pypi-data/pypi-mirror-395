import unittest

from python_doten.core import Step, TenRun


class TestCore(unittest.TestCase):
    def test_tenrun_executes_ten_by_default(self) -> None:
        reps = []

        def record(rep: int) -> int:
            reps.append(rep)
            return rep

        ten = TenRun(Step("test", record))
        result = ten.execute()
        self.assertEqual(len(result), 10)
        self.assertEqual(reps, list(range(1, 11)))

    def test_tenrun_clamps_max_reps(self) -> None:
        def record(rep: int) -> int:
            return rep

        ten = TenRun(Step("test", record))
        result = ten.execute(max_reps=1000)
        self.assertEqual(len(result), 10)


if __name__ == "__main__":
    unittest.main()
