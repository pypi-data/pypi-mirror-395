import re
from datetime import date
from datetime import datetime

MO_INFINITY = None
SD_INFINITY: str = "9999-12-31"
DATE_FORMAT = "%Y-%m-%d"
DATE_REGEX = re.compile("[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])")


def sd_date_to_mo_date(sd_date: date) -> date | None:
    """
    Convert an SD date to a MO date (or None for infinity)

    Args:
        sd_date: the date in SD

    Returns:
         MO date or None for infinity
    """

    if sd_date == datetime.strptime(SD_INFINITY, DATE_FORMAT).date():
        return None

    return sd_date


def sd_date_str_to_mo_date(sd_date: str) -> date | None:
    """
    Convert an SD date string to a MO date (or None for infinity)

    Args:
        sd_date: the SD string

    Returns:
         MO date or None for infinity
    """

    assert DATE_REGEX.match(sd_date)  # type: ignore
    if sd_date == SD_INFINITY:
        return None

    return datetime.strptime(sd_date, DATE_FORMAT).date()


def sd_date_to_str(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def mo_date_to_str(d: date | datetime | None) -> str | None:
    """
    Convert MO date to string

    Args:
        d: the MO date(time) to convert

    Returns:
        MO date string (or None) to be used in GraphQL queries
    """

    return d.isoformat() if d is not None else None


def sd_date_to_mo_date_str(sd_date: date) -> str | None:
    return mo_date_to_str(sd_date_to_mo_date(sd_date))


def sd_date_str_to_mo_date_str(sd_date: str) -> str | None:
    return mo_date_to_str(sd_date_str_to_mo_date(sd_date))
