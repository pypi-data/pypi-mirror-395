from typing import Optional, Union


def currency(value: Union[float, str, int], simplify: bool = True) -> str:
    """
    Formats a number as a currency without the currency symbol.

    If simplify is True, removes unnecessary decimal places for whole numbers.
    """
    if not value:
        return "0" if simplify else "0.00"

    float_number = float(value)
    int_number = int(float_number)

    if simplify and int_number == float_number:
        return str("{:,}".format(int_number))

    return str("{:,.2f}".format(float_number))


def pretty_price(
    value: Union[float, str, int],
    simplify: bool = True,
    currency_symbol: str = "£",
) -> str:
    """
    Formats a number as a price.

    If the value is 0, returns "Free".
    Otherwise, returns the currency symbol followed by the formatted currency.
    """
    if value == 0 or value == "0" or round(float(value) * 100) == 0:
        return "Free"

    return f"{currency_symbol}{currency(value, simplify)}"


def pretty_price_range(
    value_from: Optional[Union[float, str, int]] = None,
    value_to: Optional[Union[float, str, int]] = None,
    simplify: bool = True,
    currency_symbol: str = "£",
) -> str:
    """
    Formats a price range.

    If both value_from and value_to are 0 or None, returns "Free".
    If value_from equals value_to, returns the pretty price of that value.
    If value_from is 0 or None, returns "Free to {value_to}".
    If value_to is 0 or None, returns "From {value_from}".
    Otherwise, returns "{min_price} to {max_price}".
    """

    if value_from is not None and (
        not isinstance(value_from, (str, float, int)) or type(value_from) is bool
    ):
        raise TypeError("value_from must be a string, float, int, or None")

    if value_to is not None and (
        not isinstance(value_to, (str, float, int)) or type(value_to) is bool
    ):
        raise TypeError("value_to must be a string, float, int, or None")

    value_from = float(value_from) if value_from is not None else 0
    value_to = float(value_to) if value_to is not None else 0

    if value_from == 0 and value_to == 0:
        return "Free"

    if value_from == value_to:
        return pretty_price(value_from, simplify, currency_symbol)

    if value_from == 0:
        return f"Free to {pretty_price(value_to, simplify, currency_symbol)}"

    if value_to == 0:
        return f"From {pretty_price(value_from, simplify, currency_symbol)}"

    (min_price, max_price) = sorted([float(value_from), float(value_to)])
    return f"{pretty_price(min_price, simplify, currency_symbol)} to {pretty_price(max_price, simplify, currency_symbol)}"
