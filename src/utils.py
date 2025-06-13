from datetime import datetime


def converted_time(variant: str) -> str:
    """
    Returns the current time formatted based on the variant parameter.
    - "full": returns date and time as "DD/MM/YYYY HH:MM"
    - "date": returns date as "DD/MM/YYYY"
    - "hours-minutes": returns time as "HH:MM"
    """

    now = datetime.now()
    if variant == "full":
        formatted = now.strftime("%d/%m/%Y %H:%M")
    elif variant == "date":
        formatted = now.strftime("%d/%m/%Y")
    elif variant == "hours-minutes":
        formatted = now.strftime("%H:%M")
    return formatted


def converted_phone(phone_number: str) -> int:
    """
    Cleans a phone number string by removing parentheses and spaces,
    then prepends country code '38' and converts it to int.
    Example: "(067) 456 7890" -> 380674567890
    """

    for symbol in [")", "(", " "]:
        phone_number = phone_number.replace(symbol, "")
    phone_number = int("38" + phone_number)
    return phone_number


class StartTimeException(Exception):
    """Current time differs with .env start time"""
    ...


class ParsingException(Exception):
    """Error during parsing runtime"""
    ...