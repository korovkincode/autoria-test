from datetime import datetime

def converted_time(full=False) -> str:
    now = datetime.now()
    if full:
        formatted = now.strftime("%d/%m/%Y %H:%M")
    else:
        formatted = now.strftime("%H:%M")
    return formatted

class StartTimeException(Exception):
    """Current time differs with .env start time"""
    ...

class ParsingException(Exception):
    """Error during parsing runtime"""
    ...