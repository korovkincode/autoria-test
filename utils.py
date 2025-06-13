from datetime import datetime

def converted_time(full: bool = False) -> str:
    now = datetime.now()
    if full:
        formatted = now.strftime("%d/%m/%Y %H:%M")
    else:
        formatted = now.strftime("%H:%M")
    return formatted

def converted_phone(phone_number: str) -> int:
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