import datetime
import unittest

from tna_utilities.datetime import (
    get_date_from_string,
    group_by_year_and_month,
    is_today_in_date_range,
    is_today_or_future,
    pretty_date,
    pretty_date_range,
    pretty_datetime,
    pretty_datetime_range,
    rfc_822_date_format,
    seconds_to_duration,
    seconds_to_iso_8601_duration,
)


class TestGetDateFromString(unittest.TestCase):
    def test_happy_dd_mm_yyyy(self):
        self.assertEqual(
            get_date_from_string("2006-05-04"),
            datetime.datetime(2006, 5, 4, 0, 0, 0),
        )

    def test_happy_mm_yyyy(self):
        self.assertEqual(
            get_date_from_string("2006-05"), datetime.datetime(2006, 5, 1, 0, 0, 0)
        )

    def test_happy_yyyy(self):
        self.assertEqual(
            get_date_from_string("2006"), datetime.datetime(2006, 1, 1, 0, 0, 0)
        )

    def test_happy_iso_8601(self):
        self.assertEqual(
            get_date_from_string("2006-05-04T01:02:03"),
            datetime.datetime(2006, 5, 4, 1, 2, 3),
        )

    def test_happy_iso_8601_microseconds(self):
        self.assertEqual(
            get_date_from_string("2006-05-04T01:02:03.999"),
            datetime.datetime(2006, 5, 4, 1, 2, 3, 999000),
        )

    def test_happy_iso_8601_timezone(self):
        self.assertEqual(
            get_date_from_string("2006-05-04T01:02:03+01:00"),
            datetime.datetime(
                2006,
                5,
                4,
                1,
                2,
                3,
                tzinfo=datetime.timezone(datetime.timedelta(hours=1)),
            ),
        )

    def test_happy_iso_8601_zulu(self):
        self.assertEqual(
            get_date_from_string("2006-05-04T01:02:03Z"),
            datetime.datetime(2006, 5, 4, 1, 2, 3, tzinfo=datetime.timezone.utc),
        )

    def test_happy_iso_8601_plain(self):
        self.assertEqual(
            get_date_from_string("1000"), datetime.datetime(1000, 1, 1, 0, 0, 0)
        )

    def test_unhappy_invalid_day(self):
        with self.assertRaises(ValueError):
            get_date_from_string("2006-12-32")

    def test_unhappy_invalid_month(self):
        with self.assertRaises(ValueError):
            get_date_from_string("2006-13")

    def test_unhappy_invalid_years(self):
        with self.assertRaises(ValueError):
            get_date_from_string("999")
        with self.assertRaises(ValueError):
            get_date_from_string("06")
        with self.assertRaises(ValueError):
            get_date_from_string("00")
        with self.assertRaises(ValueError):
            get_date_from_string("99")
        with self.assertRaises(ValueError):
            get_date_from_string("9")
        with self.assertRaises(ValueError):
            get_date_from_string("abc")

    def test_unhappy_blank_values(self):
        with self.assertRaises(ValueError):
            get_date_from_string("")
        with self.assertRaises(ValueError):
            get_date_from_string(None)
        with self.assertRaises(ValueError):
            get_date_from_string(False)


class TestPrettyDate(unittest.TestCase):
    def test_happy_string(self):
        self.assertEqual(pretty_date("2000-01-01T12:00:00Z"), "1 January 2000")
        self.assertEqual(pretty_date("2000-01-01"), "1 January 2000")
        self.assertEqual(pretty_date("2000-12-31"), "31 December 2000")
        self.assertEqual(pretty_date("2000-01"), "January 2000")
        self.assertEqual(pretty_date("2000"), "2000")

    def test_happy_string_show_day(self):
        self.assertEqual(
            pretty_date("2000-01-01T12:00:00Z", show_day=True),
            "Saturday 1 January 2000",
        )
        self.assertEqual(
            pretty_date("2000-01-01", show_day=True), "Saturday 1 January 2000"
        )
        self.assertEqual(
            pretty_date("2000-12-31", show_day=True), "Sunday 31 December 2000"
        )
        self.assertEqual(pretty_date("2000-01", show_day=True), "January 2000")
        self.assertEqual(pretty_date("2000", show_day=True), "2000")
        self.assertEqual(
            pretty_date("2000-01-01T12:30:00Z", show_day=True),
            "Saturday 1 January 2000",
        )

    def test_happy_date(self):
        date = datetime.date(2000, 1, 1)
        self.assertEqual(pretty_date(date), "1 January 2000")
        self.assertEqual(pretty_date(date, show_day=True), "Saturday 1 January 2000")

    def test_happy_datetime(self):
        date = datetime.datetime(2000, 1, 1, 12, 30, 0)
        self.assertEqual(pretty_date(date), "1 January 2000")
        self.assertEqual(pretty_date(date, show_day=True), "Saturday 1 January 2000")

    def test_unhappy_none(self):
        with self.assertRaises(ValueError):
            pretty_date(None)


class TestPrettyDatetime(unittest.TestCase):
    def test_happy_string(self):
        self.assertEqual(
            pretty_datetime("2000-01-01T12:00:00Z"), "1 January 2000, 12:00"
        )
        self.assertEqual(pretty_datetime("2000-01-01"), "1 January 2000, 00:00")
        self.assertEqual(pretty_datetime("2000-01"), "1 January 2000, 00:00")
        self.assertEqual(pretty_datetime("2000"), "1 January 2000, 00:00")

    def test_happy_string_show_day(self):
        self.assertEqual(
            pretty_datetime("2000-01-01T12:00:00Z", show_day=True),
            "Saturday 1 January 2000, 12:00",
        )
        self.assertEqual(
            pretty_datetime("2000-01-01", show_day=True),
            "Saturday 1 January 2000, 00:00",
        )
        self.assertEqual(
            pretty_datetime("2000-01", show_day=True), "Saturday 1 January 2000, 00:00"
        )
        self.assertEqual(
            pretty_datetime("2000", show_day=True), "Saturday 1 January 2000, 00:00"
        )

    def test_happy_datetime(self):
        date = datetime.datetime(2000, 1, 1, 12, 30, 0)
        self.assertEqual(pretty_datetime(date), "1 January 2000, 12:30")
        self.assertEqual(
            pretty_datetime(date, show_day=True), "Saturday 1 January 2000, 12:30"
        )

    def test_unhappy_date(self):
        date = datetime.date(2000, 1, 1)
        with self.assertRaises(TypeError):
            pretty_datetime(date)

    def test_unhappy_none(self):
        with self.assertRaises(ValueError):
            pretty_datetime(None)


class TestPrettyDateRange(unittest.TestCase):
    def test_happy_string(self):
        start_date = "2000-01-01"
        self.assertEqual(pretty_date_range(start_date, "2000-01-01"), "1 January 2000")
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-02"), "1 to 2 January 2000"
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-31"), "1 to 31 January 2000"
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-02-01"),
            "1 January to 1 February 2000",
        )
        self.assertEqual(pretty_date_range(start_date, "2000-12-31"), "2000")
        self.assertEqual(
            pretty_date_range(start_date, "2001-01-01"),
            "1 January 2000 to 1 January 2001",
        )
        self.assertEqual(pretty_date_range(start_date, "2001-12-31"), "2000 to 2001")
        self.assertEqual(
            pretty_date_range(None, "2001-12-31"), "Now to 31 December 2001"
        )
        self.assertEqual(pretty_date_range(start_date, None), "From 1 January 2000")

    def test_happy_date(self):
        start_date = datetime.date(2000, 1, 1)
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2000, 1, 1)),
            "1 January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2000, 1, 2)),
            "1 to 2 January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2000, 1, 31)),
            "1 to 31 January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2000, 2, 1)),
            "1 January to 1 February 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2000, 12, 31)), "2000"
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2001, 1, 1)),
            "1 January 2000 to 1 January 2001",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2001, 12, 31)), "2000 to 2001"
        )
        self.assertEqual(
            pretty_date_range(None, datetime.date(2001, 12, 31)),
            "Now to 31 December 2001",
        )
        self.assertEqual(pretty_date_range(start_date, None), "From 1 January 2000")
        self.assertEqual(
            pretty_date_range(None, datetime.date(2001, 12, 31), lowercase_first=True),
            "now to 31 December 2001",
        )
        self.assertEqual(
            pretty_date_range(start_date, None, lowercase_first=True),
            "from 1 January 2000",
        )

    def test_happy_datetime(self):
        start_date = datetime.datetime(2000, 1, 1)
        self.assertEqual(
            pretty_date_range(start_date, datetime.datetime(2000, 1, 1, 14, 45, 0)),
            "1 January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.datetime(2000, 1, 2, 14, 45, 0)),
            "1 to 2 January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.datetime(2000, 1, 31, 14, 45, 0)),
            "1 to 31 January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.datetime(2000, 2, 1, 14, 45, 0)),
            "1 January to 1 February 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.datetime(2000, 12, 31, 14, 45, 0)),
            "2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.datetime(2001, 1, 1, 14, 45, 0)),
            "1 January 2000 to 1 January 2001",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.datetime(2001, 12, 31, 14, 45, 0)),
            "2000 to 2001",
        )
        self.assertEqual(
            pretty_date_range(None, datetime.datetime(2001, 12, 31, 14, 45, 0)),
            "Now to 31 December 2001",
        )
        self.assertEqual(pretty_date_range(start_date, None), "From 1 January 2000")
        self.assertEqual(
            pretty_date_range(
                None, datetime.datetime(2001, 12, 31, 14, 45, 0), lowercase_first=True
            ),
            "now to 31 December 2001",
        )
        self.assertEqual(
            pretty_date_range(start_date, None, lowercase_first=True),
            "from 1 January 2000",
        )

    def test_happy_pretty_date_range_no_days(self):
        start_date = datetime.date(2000, 1, 1)
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2000, 1, 1), omit_days=True),
            "January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2000, 1, 2), omit_days=True),
            "January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2000, 1, 31), omit_days=True),
            "January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2000, 2, 1), omit_days=True),
            "January to February 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2000, 12, 31), omit_days=True),
            "2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2001, 1, 1), omit_days=True),
            "January 2000 to January 2001",
        )
        self.assertEqual(
            pretty_date_range(start_date, datetime.date(2001, 12, 31), omit_days=True),
            "2000 to 2001",
        )
        self.assertEqual(
            pretty_date_range(start_date, None, omit_days=True),
            "From January 2000",
        )
        self.assertEqual(
            pretty_date_range(None, datetime.date(2001, 12, 31), omit_days=True),
            "Now to December 2001",
        )
        self.assertEqual(
            pretty_date_range(start_date, None, omit_days=True, lowercase_first=True),
            "from January 2000",
        )
        self.assertEqual(
            pretty_date_range(
                None, datetime.date(2001, 12, 31), omit_days=True, lowercase_first=True
            ),
            "now to December 2001",
        )

    def test_unhappy_order(self):
        with self.assertRaises(ValueError):
            pretty_date_range(
                datetime.datetime(2001, 1, 1), datetime.datetime(2000, 1, 1)
            )

    def test_unhappy_none(self):
        with self.assertRaises(ValueError):
            pretty_date_range(None, None)


class TestPrettyDatetimeRange(unittest.TestCase):
    def test_happy_string(self):
        start_date = "2000-01-01T12:30:00Z"
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-01-01T12:30:00Z"),
            "1 January 2000, 12:30",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-01-01T12:31:00Z"),
            "1 January 2000, 12:30 to 12:31",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-01-01T23:59:59Z"),
            "1 January 2000, 12:30 to 23:59",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-01-02T00:00:00Z"),
            "1 January 2000, 12:30 to 2 January 2000, 00:00",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-01-02T14:45:00Z"),
            "1 January 2000, 12:30 to 2 January 2000, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-01-31T14:45:00Z"),
            "1 January 2000, 12:30 to 31 January 2000, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-02-01T14:45:00Z"),
            "1 January 2000, 12:30 to 1 February 2000, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-12-31T14:45:00Z"),
            "1 January 2000, 12:30 to 31 December 2000, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2001-01-01T14:45:00Z"),
            "1 January 2000, 12:30 to 1 January 2001, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2001-12-31T14:45:00Z"),
            "1 January 2000, 12:30 to 31 December 2001, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, None),
            "From 1 January 2000, 12:30",
        )
        self.assertEqual(
            pretty_datetime_range(None, "2001-12-31T14:45:00Z"),
            "Now to 31 December 2001, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, None, lowercase_first=True),
            "from 1 January 2000, 12:30",
        )
        self.assertEqual(
            pretty_datetime_range(None, "2001-12-31T14:45:00Z", lowercase_first=True),
            "now to 31 December 2001, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(
                start_date, "2000-01-01T12:30:00Z", hide_date_if_single_day=True
            ),
            "12:30",
        )
        self.assertEqual(
            pretty_datetime_range(
                start_date, "2000-01-01T12:45:00Z", hide_date_if_single_day=True
            ),
            "12:30 to 12:45",
        )
        self.assertEqual(
            pretty_datetime_range(
                start_date, "2000-01-02T00:00:00Z", hide_date_if_single_day=True
            ),
            "1 January 2000, 12:30 to 2 January 2000, 00:00",
        )

    def test_happy_datetime(self):
        start_date = datetime.datetime(2000, 1, 1, 12, 30, 0)
        self.assertEqual(
            pretty_datetime_range(start_date, datetime.datetime(2000, 1, 1, 12, 30, 0)),
            "1 January 2000, 12:30",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, datetime.datetime(2000, 1, 1, 12, 31, 0)),
            "1 January 2000, 12:30 to 12:31",
        )
        self.assertEqual(
            pretty_datetime_range(
                start_date, datetime.datetime(2000, 1, 1, 23, 59, 59)
            ),
            "1 January 2000, 12:30 to 23:59",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, datetime.datetime(2000, 1, 2, 0, 0, 0)),
            "1 January 2000, 12:30 to 2 January 2000, 00:00",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, datetime.datetime(2000, 1, 2, 14, 45, 0)),
            "1 January 2000, 12:30 to 2 January 2000, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(
                start_date, datetime.datetime(2000, 1, 31, 14, 45, 0)
            ),
            "1 January 2000, 12:30 to 31 January 2000, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, datetime.datetime(2000, 2, 1, 14, 45, 0)),
            "1 January 2000, 12:30 to 1 February 2000, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(
                start_date, datetime.datetime(2000, 12, 31, 14, 45, 0)
            ),
            "1 January 2000, 12:30 to 31 December 2000, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, datetime.datetime(2001, 1, 1, 14, 45, 0)),
            "1 January 2000, 12:30 to 1 January 2001, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(
                start_date, datetime.datetime(2001, 12, 31, 14, 45, 0)
            ),
            "1 January 2000, 12:30 to 31 December 2001, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, None),
            "From 1 January 2000, 12:30",
        )
        self.assertEqual(
            pretty_datetime_range(None, datetime.datetime(2001, 12, 31, 14, 45, 0)),
            "Now to 31 December 2001, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, None, lowercase_first=True),
            "from 1 January 2000, 12:30",
        )
        self.assertEqual(
            pretty_datetime_range(
                None, datetime.datetime(2001, 12, 31, 14, 45, 0), lowercase_first=True
            ),
            "now to 31 December 2001, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(
                start_date,
                datetime.datetime(2000, 1, 1, 12, 30, 0),
                hide_date_if_single_day=True,
            ),
            "12:30",
        )
        self.assertEqual(
            pretty_datetime_range(
                start_date,
                datetime.datetime(2000, 1, 1, 12, 45, 0),
                hide_date_if_single_day=True,
            ),
            "12:30 to 12:45",
        )
        self.assertEqual(
            pretty_datetime_range(
                start_date,
                datetime.datetime(2000, 1, 2, 0, 0, 0),
                hide_date_if_single_day=True,
            ),
            "1 January 2000, 12:30 to 2 January 2000, 00:00",
        )

    def test_unhappy_date(self):
        with self.assertRaises(TypeError):
            pretty_datetime_range(datetime.date(2000, 1, 1), None)
        with self.assertRaises(TypeError):
            pretty_datetime_range(None, datetime.date(2000, 1, 1))

    def test_unhappy_order(self):
        with self.assertRaises(ValueError):
            pretty_datetime_range(
                datetime.datetime(2001, 1, 1), datetime.datetime(2000, 1, 1)
            )

    def test_unhappy_none(self):
        with self.assertRaises(ValueError):
            pretty_datetime_range(None, None)


class TestIsTodayOrFuture(unittest.TestCase):
    def test_happy(self):
        self.assertTrue(is_today_or_future(datetime.date(2999, 1, 1)))
        self.assertFalse(is_today_or_future(datetime.date(2000, 1, 1)))
        today = datetime.datetime.now()
        self.assertTrue(is_today_or_future(today))
        tomorrow = today + datetime.timedelta(days=1)
        self.assertTrue(is_today_or_future(tomorrow))
        yesterday = today + datetime.timedelta(days=-1)
        self.assertFalse(is_today_or_future(yesterday))

    def test_unhappy(self):
        with self.assertRaises(ValueError):
            is_today_or_future(None)


class TestIsTodayInDateRange(unittest.TestCase):
    def test_happy_date(self):
        self.assertFalse(
            is_today_in_date_range(datetime.date(2000, 1, 1), datetime.date(2001, 1, 1))
        )
        self.assertTrue(
            is_today_in_date_range(datetime.date(2000, 1, 1), datetime.date(2999, 1, 1))
        )
        self.assertFalse(
            is_today_in_date_range(datetime.date(2998, 1, 1), datetime.date(2999, 1, 1))
        )

    def test_unhappy_string(self):
        with self.assertRaises(ValueError):
            is_today_in_date_range(None, "2023-10-31")
        with self.assertRaises(ValueError):
            is_today_in_date_range("2023-10-01", None)
        with self.assertRaises(ValueError):
            is_today_in_date_range(None, None)

    def test_unhappy_invalid(self):
        with self.assertRaises(ValueError):
            is_today_in_date_range(None, "foo")
        with self.assertRaises(ValueError):
            is_today_in_date_range("bar", None)

    def test_unhappy_date(self):
        with self.assertRaises(ValueError):
            is_today_in_date_range(None, datetime.date(2023, 10, 31))
        with self.assertRaises(ValueError):
            is_today_in_date_range(datetime.date(2023, 10, 31), None)
        with self.assertRaises(ValueError):
            is_today_in_date_range(None, None)


class TestGroupByYearAndMonth(unittest.TestCase):
    def test_happy_strings(self):
        self.maxDiff = None
        input_data = [
            {"id": 1, "date": "2022-05-15"},
            {"id": 2, "date": "2022-05-20"},
            {"id": 3, "date": "2022-06-10"},
            {"id": 4, "date": "2021-12-25"},
            {"id": 5, "date": "2021-11-11"},
            {"id": 6, "date": "2022-06-15"},
            {"id": 7, "date": "foobar"},
        ]
        result = group_by_year_and_month({"items": input_data}, "date")
        expected = [
            {
                "heading": "2021",
                "index": 2021,
                "items": [
                    {
                        "heading": "November",
                        "index": 11,
                        "items": [{"id": 5, "date": "2021-11-11"}],
                    },
                    {
                        "heading": "December",
                        "index": 12,
                        "items": [{"id": 4, "date": "2021-12-25"}],
                    },
                ],
            },
            {
                "heading": "2022",
                "index": 2022,
                "items": [
                    {
                        "heading": "May",
                        "index": 5,
                        "items": [
                            {"id": 1, "date": "2022-05-15"},
                            {"id": 2, "date": "2022-05-20"},
                        ],
                    },
                    {
                        "heading": "June",
                        "index": 6,
                        "items": [
                            {"id": 3, "date": "2022-06-10"},
                            {"id": 6, "date": "2022-06-15"},
                        ],
                    },
                ],
            },
        ]
        self.assertEqual(result, expected)

    def test_happy_datetime(self):
        input_data = [
            {"id": 1, "date": datetime.date(2022, 5, 15)},
            {"id": 2, "date": datetime.date(2022, 5, 20)},
            {"id": 3, "date": datetime.date(2022, 6, 10)},
            {"id": 4, "date": datetime.date(2021, 12, 25)},
            {"id": 5, "date": datetime.date(2021, 11, 11)},
            {"id": 6, "date": datetime.date(2022, 6, 15)},
            {"id": 7, "date": None},
        ]
        result = group_by_year_and_month({"items": input_data}, "date")
        expected = [
            {
                "heading": "2021",
                "index": 2021,
                "items": [
                    {
                        "heading": "November",
                        "index": 11,
                        "items": [{"id": 5, "date": datetime.date(2021, 11, 11)}],
                    },
                    {
                        "heading": "December",
                        "index": 12,
                        "items": [{"id": 4, "date": datetime.date(2021, 12, 25)}],
                    },
                ],
            },
            {
                "heading": "2022",
                "index": 2022,
                "items": [
                    {
                        "heading": "May",
                        "index": 5,
                        "items": [
                            {"id": 1, "date": datetime.date(2022, 5, 15)},
                            {"id": 2, "date": datetime.date(2022, 5, 20)},
                        ],
                    },
                    {
                        "heading": "June",
                        "index": 6,
                        "items": [
                            {"id": 3, "date": datetime.date(2022, 6, 10)},
                            {"id": 6, "date": datetime.date(2022, 6, 15)},
                        ],
                    },
                ],
            },
        ]
        self.assertEqual(result, expected)

    def test_happy_strings_reverse(self):
        self.maxDiff = None
        input_data = [
            {"id": 1, "date": "2022-05-15"},
            {"id": 2, "date": "2022-05-20"},
            {"id": 3, "date": "2022-06-10"},
            {"id": 4, "date": "2021-12-25"},
            {"id": 5, "date": "2021-11-11"},
            {"id": 6, "date": "2022-06-15"},
            {"id": 7, "date": "foobar"},
        ]
        result = group_by_year_and_month({"items": input_data}, "date", reverse=True)
        expected = [
            {
                "heading": "2022",
                "index": 2022,
                "items": [
                    {
                        "heading": "June",
                        "index": 6,
                        "items": [
                            {"id": 6, "date": "2022-06-15"},
                            {"id": 3, "date": "2022-06-10"},
                        ],
                    },
                    {
                        "heading": "May",
                        "index": 5,
                        "items": [
                            {"id": 2, "date": "2022-05-20"},
                            {"id": 1, "date": "2022-05-15"},
                        ],
                    },
                ],
            },
            {
                "heading": "2021",
                "index": 2021,
                "items": [
                    {
                        "heading": "December",
                        "index": 12,
                        "items": [{"id": 4, "date": "2021-12-25"}],
                    },
                    {
                        "heading": "November",
                        "index": 11,
                        "items": [{"id": 5, "date": "2021-11-11"}],
                    },
                ],
            },
        ]
        self.assertEqual(result, expected)

    def test_happy_datetime_reverse(self):
        input_data = [
            {"id": 1, "date": datetime.date(2022, 5, 15)},
            {"id": 2, "date": datetime.date(2022, 5, 20)},
            {"id": 3, "date": datetime.date(2022, 6, 10)},
            {"id": 4, "date": datetime.date(2021, 12, 25)},
            {"id": 5, "date": datetime.date(2021, 11, 11)},
            {"id": 6, "date": datetime.date(2022, 6, 15)},
            {"id": 7, "date": None},
        ]
        result = group_by_year_and_month({"items": input_data}, "date", reverse=True)
        expected = [
            {
                "heading": "2022",
                "index": 2022,
                "items": [
                    {
                        "heading": "June",
                        "index": 6,
                        "items": [
                            {"id": 6, "date": datetime.date(2022, 6, 15)},
                            {"id": 3, "date": datetime.date(2022, 6, 10)},
                        ],
                    },
                    {
                        "heading": "May",
                        "index": 5,
                        "items": [
                            {"id": 2, "date": datetime.date(2022, 5, 20)},
                            {"id": 1, "date": datetime.date(2022, 5, 15)},
                        ],
                    },
                ],
            },
            {
                "heading": "2021",
                "index": 2021,
                "items": [
                    {
                        "heading": "December",
                        "index": 12,
                        "items": [{"id": 4, "date": datetime.date(2021, 12, 25)}],
                    },
                    {
                        "heading": "November",
                        "index": 11,
                        "items": [{"id": 5, "date": datetime.date(2021, 11, 11)}],
                    },
                ],
            },
        ]
        self.assertEqual(result, expected)


class TestSecondsToIso8601Duration(unittest.TestCase):
    def test_happy(self):
        self.assertEqual(seconds_to_iso_8601_duration(0), "PT0S")
        self.assertEqual(seconds_to_iso_8601_duration(1), "PT1S")
        self.assertEqual(seconds_to_iso_8601_duration(59), "PT59S")
        self.assertEqual(seconds_to_iso_8601_duration(60), "PT1M0S")
        self.assertEqual(seconds_to_iso_8601_duration(61), "PT1M1S")
        self.assertEqual(seconds_to_iso_8601_duration(1337), "PT22M17S")
        self.assertEqual(seconds_to_iso_8601_duration(3599), "PT59M59S")
        self.assertEqual(seconds_to_iso_8601_duration(3600), "PT1H0M0S")
        self.assertEqual(seconds_to_iso_8601_duration(3601), "PT1H0M1S")

    def test_unhappy_negative(self):
        with self.assertRaises(ValueError):
            seconds_to_iso_8601_duration(-1)


class TestSecondsToTime(unittest.TestCase):
    def test_happy(self):
        self.assertEqual(seconds_to_duration(0), "00h 00m 00s")
        self.assertEqual(seconds_to_duration(1), "00h 00m 01s")
        self.assertEqual(seconds_to_duration(59), "00h 00m 59s")
        self.assertEqual(seconds_to_duration(60), "00h 01m 00s")
        self.assertEqual(seconds_to_duration(61), "00h 01m 01s")
        self.assertEqual(seconds_to_duration(1337), "00h 22m 17s")
        self.assertEqual(seconds_to_duration(3599), "00h 59m 59s")
        self.assertEqual(seconds_to_duration(3600), "01h 00m 00s")
        self.assertEqual(seconds_to_duration(3601), "01h 00m 01s")

    def test_happy_simplified(self):
        self.assertEqual(seconds_to_duration(0, simplify=True), "00s")
        self.assertEqual(seconds_to_duration(1, simplify=True), "01s")
        self.assertEqual(seconds_to_duration(59, simplify=True), "59s")
        self.assertEqual(seconds_to_duration(60, simplify=True), "01m 00s")
        self.assertEqual(seconds_to_duration(61, simplify=True), "01m 01s")
        self.assertEqual(seconds_to_duration(1337, simplify=True), "22m 17s")
        self.assertEqual(seconds_to_duration(3599, simplify=True), "59m 59s")
        self.assertEqual(seconds_to_duration(3600, simplify=True), "01h 00m 00s")
        self.assertEqual(seconds_to_duration(3601, simplify=True), "01h 00m 01s")

    def test_unhappy_negative(self):
        with self.assertRaises(ValueError):
            seconds_to_duration(-1)


class TestRfc822DateFormat(unittest.TestCase):
    def test_happy(self):
        self.assertEqual(
            rfc_822_date_format(datetime.datetime(2000, 1, 1, 12, 30, 45)),
            "Sat, 1 Jan 2000 12:30:45 GMT",
        )
