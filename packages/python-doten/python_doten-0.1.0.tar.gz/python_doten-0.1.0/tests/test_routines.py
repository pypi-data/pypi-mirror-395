import unittest

from python_doten.routines import SimpleCountRoutine


class TestRoutines(unittest.TestCase):
    def test_simple_count_routine(self) -> None:
        r = SimpleCountRoutine(label="test")
        result = r.run()
        self.assertEqual(result.total_reps, 10)
        self.assertEqual(len(result.notes), 10)
        self.assertTrue(all("test-rep-" in note for note in result.notes))


if __name__ == "__main__":
    unittest.main()
