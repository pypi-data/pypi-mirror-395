import unittest
from datetime import date

from vha_toolbox import (
    get_last_day_of_year,
    get_first_day_of_year,
    get_first_day_of_month,
    get_last_day_of_month,
    get_last_day_of_quarter,
    get_first_day_of_quarter,
    is_renewal_due,
    next_renewal_date
)


class DateUtilsTestCase(unittest.TestCase):
    def test_get_first_day_of_year(self):
        dt = date(2023, 6, 15)
        result = get_first_day_of_year(dt)
        self.assertEqual(result, date(2023, 1, 1))

    def test_get_last_day_of_year(self):
        dt = date(2023, 6, 15)
        result = get_last_day_of_year(dt)
        self.assertEqual(result, date(2023, 12, 31))

    def test_get_first_day_of_quarter(self):
        dt = date(2023, 6, 15)
        result = get_first_day_of_quarter(dt)
        self.assertEqual(result, date(2023, 4, 1))

    def test_get_last_day_of_quarter(self):
        dt = date(2023, 6, 15)
        result = get_last_day_of_quarter(dt)
        self.assertEqual(result, date(2023, 6, 30))

    def test_get_first_day_of_month(self):
        dt = date(2023, 6, 15)
        result = get_first_day_of_month(dt)
        self.assertEqual(result, date(2023, 6, 1))

    def test_get_first_day_of_month_2(self):
        dt = date(2024, 2, 10)
        result = get_first_day_of_month(dt)
        self.assertEqual(result, date(2024, 2, 1))

    def test_get_last_day_of_month(self):
        dt = date(2023, 6, 15)
        result = get_last_day_of_month(dt)
        self.assertEqual(result, date(2023, 6, 30))

    def test_get_last_day_of_month_2(self):
        dt = date(2024, 2, 10)
        result = get_last_day_of_month(dt)
        self.assertEqual(result, date(2024, 2, 29))

    def test_get_last_day_of_month_3(self):
        dt = date(2021, 2, 10)
        result = get_last_day_of_month(dt)
        self.assertEqual(result, date(2021, 2, 28))

    # Existing tests
    def test_is_renewal_due_same_day(self):
        self.assertFalse(is_renewal_due(date(2023, 6, 15), date(2023, 6, 15)))

    def test_is_renewal_due_next_day(self):
        self.assertFalse(is_renewal_due(date(2023, 6, 15), date(2023, 6, 16)))

    def test_is_renewal_due_next_month(self):
        self.assertTrue(is_renewal_due(date(2023, 6, 15), date(2023, 7, 15)))

    def test_is_renewal_due_next_year(self):
        self.assertTrue(is_renewal_due(date(2023, 6, 15), date(2024, 7, 15)))

    def test_leap_year_feb_29(self):
        self.assertTrue(is_renewal_due(date(2020, 2, 29), date(2021, 2, 28)))
        self.assertFalse(is_renewal_due(date(2020, 2, 29), date(2021, 3, 1)))

    def test_non_leap_year_feb_28(self):
        self.assertFalse(is_renewal_due(date(2023, 2, 28), date(2024, 2, 27)))
        self.assertTrue(is_renewal_due(date(2023, 2, 28), date(2024, 2, 28)))

    def test_30_day_month_to_31_day_month(self):
        self.assertTrue(is_renewal_due(date(2023, 4, 30), date(2024, 4, 30)))
        self.assertFalse(is_renewal_due(date(2023, 4, 30), date(2024, 5, 1)))

    def test_31_day_month_to_30_day_month(self):
        self.assertFalse(is_renewal_due(date(2023, 5, 31), date(2024, 5, 30)))
        self.assertTrue(is_renewal_due(date(2023, 5, 31), date(2024, 5, 31)))

    def test_past_date(self):
        self.assertTrue(is_renewal_due(date(2020, 1, 1), date(2024, 1, 1)))

    def test_future_date(self):
        self.assertFalse(is_renewal_due(date(2025, 1, 1), date(2024, 1, 1)))

    def test_standard_month_transition(self):
        self.assertEqual(next_renewal_date(date(2023, 5, 15)), date(2023, 6, 15))

    def test_end_of_year_transition(self):
        self.assertEqual(next_renewal_date(date(2023, 12, 15)), date(2024, 1, 15))

    def test_leap_year_feb(self):
        self.assertEqual(next_renewal_date(date(2024, 2, 29)), date(2024, 3, 29))

    def test_non_leap_year_feb(self):
        self.assertEqual(next_renewal_date(date(2023, 2, 28)), date(2023, 3, 28))

    def test_30_day_month_transition(self):
        self.assertEqual(next_renewal_date(date(2023, 4, 30)), date(2023, 5, 30))

    def test_31_day_month_transition_to_30_day_month(self):
        self.assertEqual(next_renewal_date(date(2023, 5, 31)), date(2023, 6, 30))

    def test_multiple_months_advance(self):
        self.assertEqual(next_renewal_date(date(2023, 1, 15), 3), date(2023, 4, 15))

    def test_end_of_month_feb_to_non_leap_march(self):
        self.assertEqual(next_renewal_date(date(2023, 1, 31), 1), date(2023, 2, 28))

    def test_end_of_month_feb_to_leap_march(self):
        self.assertEqual(next_renewal_date(date(2024, 1, 31), 1), date(2024, 2, 29))

    def test_transition_over_a_year(self):
        self.assertEqual(next_renewal_date(date(2023, 5, 15), 12), date(2024, 5, 15))

    def test_multiple_months_advance_standard(self):
        # Test advancing multiple months from a standard date
        self.assertEqual(next_renewal_date(date(2023, 1, 15), 6), date(2023, 7, 15))

    def test_end_of_year_multiple_months_advance(self):
        # Test advancing over the end of the year
        self.assertEqual(next_renewal_date(date(2023, 10, 31), 4), date(2024, 2, 29))

    def test_leap_year_multiple_months_advance(self):
        # Test advancing multiple months including a leap year February
        self.assertEqual(next_renewal_date(date(2023, 12, 31), 14), date(2025, 2, 28))

    def test_non_leap_year_february_advance(self):
        # Test advancing from a non-leap year February
        self.assertEqual(next_renewal_date(date(2023, 2, 28), 12), date(2024, 2, 28))

    def test_long_term_advance(self):
        # Test advancing a significant number of months
        self.assertEqual(next_renewal_date(date(2023, 1, 31), 36), date(2026, 1, 31))

    def test_end_of_month_transition_through_leap_year(self):
        # Test advancing from the end of a month through a leap year
        self.assertEqual(next_renewal_date(date(2023, 1, 31), 13), date(2024, 2, 29))

    def test_end_of_month_transition_non_leap_year(self):
        # Test advancing from the end of a month through a non-leap year
        self.assertEqual(next_renewal_date(date(2023, 1, 31), 1), date(2023, 2, 28))


if __name__ == '__main__':
    unittest.main()
