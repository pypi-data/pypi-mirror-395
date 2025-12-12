import datetime
import math
from typing import Optional, Union

"""
See https://design-system.nationalarchives.gov.uk/content/dates-and-times/
for more details on how dates and times should be presented within services
from The National Archives.
"""


def get_date_from_string(date_string: str) -> datetime.datetime:  # noqa: C901
    """
    Parses a date string into a datetime object.
    """

    if not date_string:
        raise ValueError("Empty string cannot be parsed as date")

    s = date_string.replace("Z", "+00:00")

    try:
        return datetime.datetime.fromisoformat(s)
    except ValueError:
        pass

    try:
        return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        pass

    try:
        return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        pass

    try:
        return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        pass

    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        pass

    try:
        return datetime.datetime.strptime(s, "%Y-%m")
    except ValueError:
        pass

    try:
        return datetime.datetime.strptime(s, "%Y")
    except ValueError:
        pass

    raise ValueError(f"Unable to parse date from string: {date_string}")


def pretty_date(
    date: Union[str, datetime.date, datetime.datetime],
    show_day: bool = False,
) -> str:
    """
    Formats a date into the format used by The National Archives.

    date: A date or datetime object or the date string in either YYYY-MM-DD, YYYY-MM, or YYYY format.

    If show_day is True, includes the day of the week.
    """

    if not date:
        raise ValueError("No date provided")

    if isinstance(date, datetime.date):
        if show_day:
            return date.strftime("%A %-d %B %Y")
        return date.strftime("%-d %B %Y")

    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        if show_day:
            return date.strftime("%A %-d %B %Y")
        return date.strftime("%-d %B %Y")
    except ValueError:
        pass

    try:
        date = datetime.datetime.strptime(date, "%Y-%m")
        return date.strftime("%B %Y")
    except ValueError:
        pass

    try:
        date = datetime.datetime.strptime(date, "%Y")
        return date.strftime("%Y")
    except ValueError:
        pass

    date = get_date_from_string(date)
    if show_day:
        return date.strftime("%A %-d %B %Y")
    return date.strftime("%-d %B %Y")


def pretty_datetime(
    date: Union[str, datetime.datetime],
    show_day: bool = False,
) -> str:
    """
    Formats a date and time into the format used by The National Archives.
    """

    if not date:
        raise ValueError("No date provided")

    if isinstance(date, datetime.datetime):
        if show_day:
            return date.strftime("%A %-d %B %Y, %H:%M")
        return date.strftime("%-d %B %Y, %H:%M")

    if isinstance(date, datetime.date):
        raise TypeError("Date object provided, datetime object expected")

    date = get_date_from_string(date)
    if show_day:
        return date.strftime("%A %-d %B %Y, %H:%M")
    return date.strftime("%-d %B %Y, %H:%M")


def pretty_date_range(  # noqa: C901
    date_from: Optional[Union[str, datetime.datetime]],
    date_to: Optional[Union[str, datetime.datetime]],
    omit_days: bool = False,
    lowercase_first: bool = False,
) -> str:
    """
    Formats a date range into the format used by The National Archives.
    """

    if date_from and isinstance(date_from, (datetime.date, datetime.datetime)):
        date_from = date_from
    else:
        try:
            date_from = get_date_from_string(date_from)
        except ValueError:
            pass

    if date_to and isinstance(date_to, (datetime.date, datetime.datetime)):
        date_to = date_to
    else:
        try:
            date_to = get_date_from_string(date_to)
        except ValueError:
            pass

    if not date_from and not date_to:
        raise ValueError("No dates provided")

    if date_from and date_to:
        if date_from > date_to:
            raise ValueError("From date is after to date")

        date_to_string = date_to.strftime("%B %Y" if omit_days else ("%-d %B %Y"))
        if (
            date_from.day == 1
            and date_from.month == 1
            and date_to.day == 31
            and date_to.month == 12
        ):
            if date_from.year == date_to.year:
                return str(date_from.year)

            return f"{date_from.year} to {date_to.year}"

        if date_from.year == date_to.year:
            if date_from.month == date_to.month:
                if date_from.day == date_to.day:
                    return date_from.strftime("%B %Y" if omit_days else "%-d %B %Y")

                if omit_days:
                    return date_to_string
                return f"{date_from.strftime('%-d')} to {date_to_string}"

            return f"{date_from.strftime('%B' if omit_days else '%-d %B')} to {date_to_string}"

        return f"{date_from.strftime('%B %Y' if omit_days else '%-d %B %Y')} to {date_to_string}"

    if date_from:
        start = "from" if lowercase_first else "From"
        return f"{start} {date_from.strftime('%B %Y' if omit_days else '%-d %B %Y')}"

    if date_to:
        start = "now to" if lowercase_first else "Now to"
        return f"{start} {date_to.strftime('%B %Y' if omit_days else '%-d %B %Y')}"


def pretty_datetime_range(  # noqa: C901
    date_from: Optional[Union[str, datetime.date, datetime.datetime]],
    date_to: Optional[Union[str, datetime.date, datetime.datetime]],
    lowercase_first: bool = False,
    hide_date_if_single_day: bool = False,
) -> str:
    """
    Formats a date/time range into the format used by The National Archives.
    """

    if date_from and isinstance(date_from, datetime.datetime):
        date_from = date_from
    elif date_from and isinstance(date_from, datetime.date):
        raise TypeError("From date object provided, datetime object expected")
    else:
        try:
            date_from = get_date_from_string(date_from)
        except ValueError:
            pass

    if date_to and isinstance(date_to, datetime.datetime):
        date_to = date_to
    elif date_to and isinstance(date_to, datetime.date):
        raise TypeError("To date object provided, datetime object expected")
    else:
        try:
            date_to = get_date_from_string(date_to)
        except ValueError:
            pass

    if not date_from and not date_to:
        raise ValueError("No dates provided")

    if date_from and date_to:
        if date_from > date_to:
            raise ValueError("From date is after to date")

        if (
            date_from.year == date_to.year
            and date_from.month == date_to.month
            and date_from.day == date_to.day
        ):
            if date_from.hour != date_to.hour or date_from.minute != date_to.minute:
                if hide_date_if_single_day:
                    return (
                        f"{date_from.strftime('%H:%M')} to {date_to.strftime('%H:%M')}"
                    )

                return f"{date_from.strftime('%-d %B %Y, %H:%M')} to {date_to.strftime('%H:%M')}"

            if hide_date_if_single_day:
                return f"{date_from.strftime('%H:%M')}"

            return f"{date_from.strftime('%-d %B %Y, %H:%M')}"

        return f"{date_from.strftime('%-d %B %Y, %H:%M')} to {date_to.strftime('%-d %B %Y, %H:%M')}"

    if date_from:
        start = "from" if lowercase_first else "From"
        return f"{start} {date_from.strftime('%-d %B %Y, %H:%M')}"

    if date_to:
        start = "now to" if lowercase_first else "Now to"
        return f"{start} {date_to.strftime('%-d %B %Y, %H:%M')}"


def is_today_or_future(date: Union[datetime.date, datetime.datetime]) -> bool:
    """
    Determines if the given date string represents today or a future date.
    """

    if not date:
        raise ValueError("No date provided")

    if isinstance(date, datetime.datetime):
        date = date.date()

    today = datetime.datetime.now().date()
    return today <= date


def is_today_in_date_range(
    date_from: Union[datetime.date, datetime.datetime],
    date_to: Union[datetime.date, datetime.datetime],
) -> bool:
    """
    Determines if today's date falls within the given date range.
    """

    if not date_from or not date_to:
        raise ValueError("Both from and to dates must be provided")

    if isinstance(date_from, datetime.datetime):
        date_from = date_from.date()

    if isinstance(date_to, datetime.datetime):
        date_to = date_to.date()

    today = datetime.datetime.now().date()
    return date_from <= today <= date_to


def group_by_year_and_month(
    items: list[dict], date_key: str, reverse: bool = False
) -> dict:  # noqa: C901
    """
    Groups a list of items by year and month based on a date key in each item.
    """

    grouped = []

    for item in items.get("items", []):
        if request_date := item.get(date_key):
            if isinstance(request_date, (datetime.datetime, datetime.date)):
                request_datetime = request_date
            else:
                try:
                    request_datetime = get_date_from_string(request_date)
                except ValueError:
                    continue

            if request_datetime:
                month = request_datetime.strftime("%B")
                month_index = int(request_datetime.strftime("%-m"))
                year = request_datetime.strftime("%Y")
                year_index = int(year)
                existing_year_index = next(
                    (i for i, d in enumerate(grouped) if d["index"] == year_index), None
                )
                if existing_year_index is None:
                    grouped.append(
                        {
                            "heading": year,
                            "index": year_index,
                            "items": [
                                {
                                    "heading": month,
                                    "index": month_index,
                                    "items": [item],
                                }
                            ],
                        }
                    )
                else:
                    existing_month_index = next(
                        (
                            i
                            for i, m in enumerate(grouped[existing_year_index]["items"])
                            if m["index"] == month_index
                        ),
                        None,
                    )
                    if existing_month_index is None:
                        grouped[existing_year_index]["items"].append(
                            {
                                "heading": month,
                                "index": month_index,
                                "items": [item],
                            }
                        )
                    else:
                        grouped[existing_year_index]["items"][existing_month_index][
                            "items"
                        ].append(item)

    for year_group in grouped:
        year_group["items"].sort(key=lambda x: x["index"], reverse=reverse)
        for month_group in year_group["items"]:
            month_group["items"].sort(
                key=lambda x: (
                    x.get(date_key)
                    if isinstance(x.get(date_key), (datetime.date, datetime.datetime))
                    else get_date_from_string(x.get(date_key))
                ),
                reverse=reverse,
            )
    grouped.sort(key=lambda x: x["index"], reverse=reverse)

    return grouped


def seconds_to_iso_8601_duration(total_seconds: int) -> str:
    """
    Converts a total number of seconds into an ISO 8601 duration string.
    """

    if not total_seconds:
        return "PT0S"

    if total_seconds < 0:
        raise ValueError("Total seconds cannot be negative")

    hours = math.floor(total_seconds / 3600)
    minutes = math.floor((total_seconds - (hours * 3600)) / 60)
    seconds = total_seconds - (hours * 3600) - (minutes * 60)
    if hours:
        return f"PT{hours}H{minutes}M{seconds}S"

    if minutes:
        return f"PT{minutes}M{seconds}S"

    return f"PT{seconds}S"


def seconds_to_duration(total_seconds: int, simplify: bool = False) -> str:
    """
    Converts a total number of seconds into a human-readable duration string.
    """

    if not total_seconds:
        return "00s" if simplify else "00h 00m 00s"

    if total_seconds < 0:
        raise ValueError("Total seconds cannot be negative")

    hours = math.floor(total_seconds / 3600)
    minutes = math.floor((total_seconds - (hours * 3600)) / 60)
    seconds = total_seconds - (hours * 3600) - (minutes * 60)

    hours_string = f"{str(hours).rjust(2, '0')}h"
    minutes_string = f"{str(minutes).rjust(2, '0')}m"
    seconds_string = f"{str(seconds).rjust(2, '0')}s"

    return_values = []
    if simplify:
        if hours:
            return_values.append(hours_string)
            return_values.append(minutes_string)
        elif minutes:
            return_values.append(minutes_string)
    else:
        return_values.append(hours_string)
        return_values.append(minutes_string)
    return_values.append(seconds_string)

    return " ".join(return_values)


def rfc_822_date_format(date: Union[datetime.date, datetime.datetime]) -> str:
    """
    Formats a date into RFC 822 format.
    """

    if not date:
        raise ValueError("No date provided")

    return date.strftime("%a, %-d %b %Y %H:%M:%S GMT")
