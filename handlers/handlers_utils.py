from datetime import datetime

async def validate_date_input(date_str: str) -> str | bool:
    """Validate date input and show errors if needed"""
    if date_str == '/skip':
        return False
    if not date_str:
        return 'empty_date_error'

    if not is_valid_date_format(date_str):

        return 'invalid_date_format'

    if is_date_in_past(date_str):
        return 'date_in_past_error'

    return False


def is_valid_date_format(date_str: str) -> bool:
    """Check if date matches expected format (e.g., DD.MM.YYYY)"""
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False


def is_date_in_past(date_str: str) -> bool:
    """Check if date is in the past"""
    try:
        input_date = datetime.strptime(date_str, '%d.%m.%Y').date()
        return input_date < datetime.now().date()
    except ValueError:
        return False


