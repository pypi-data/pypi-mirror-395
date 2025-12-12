from datetime import datetime
from time import strftime, gmtime
from typing import Optional
from dateutil import tz
from copy import copy


def second_to_strf(seconds: int, str_format: str = "%H:%M:%S") -> str:
    """Format seconds to format

    Args:
        @param seconds: seconds
        @param str_format: format

    Returns:
        str: seconds in string format

    """
    return strftime(str_format, gmtime(seconds))


def get_tz_info(tz_name: str):
    return tz.gettz(tz_name)


def str_to(str_date: str, date_format: str = '%d/%m/%y %H:%M:%S') -> datetime:
    return datetime.strptime(str_date, date_format)


def apply_tz(date_time: datetime, tz_name: Optional[str] = 'America/Mexico_City') -> datetime:
    tz_info = tz.gettz(tz_name)
    return date_time.astimezone(tz_info)


def change_timezone(date: datetime, from_tz: str, to_tz: str) -> datetime:
    return apply_tz(
        date_time=copy(date).replace(tzinfo=get_tz_info(from_tz)),
        tz_name=to_tz
    )


def to_utc(date: datetime, local_tz: Optional[str] = 'America/Mexico_City') -> datetime:
    return apply_tz(copy(date).replace(tzinfo=get_tz_info(local_tz)), 'UTC')
