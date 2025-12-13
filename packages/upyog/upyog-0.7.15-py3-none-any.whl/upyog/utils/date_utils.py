from upyog.imports import *
import pytz


__all__ = [
    "get_YYYY_MM_DD", "get_date_YYYY_MM_DD", "get_date_DD_MM_YYYY",
    "get_current_time_pst", "get_current_time_ist", "get_current_time_utc",
]


def get_YYYY_MM_DD(sep="_") -> str:
    warnings.warn(f"`get_YYYY_MM_DD` is deprecated. Please call `get_date_YYYY_MM_DD()` instead")
    return get_date_YYYY_MM_DD()


def get_date_YYYY_MM_DD(sep="_") -> str:
    return datetime.now().strftime(f"%Y{sep}%m{sep}%d")


def get_date_DD_MM_YYYY(sep="_") -> str:
    return datetime.now().strftime(f"%d{sep}%m{sep}%Y")


_TIME_FORMAT_STRING = "%Y/%m/%d at %H:%M:%S"

def _utc_localized_time_now():
    return pytz.utc.localize(datetime.utcnow())


def get_current_time_pst(fmt_str: Optional[str] = _TIME_FORMAT_STRING):
    utc_now = _utc_localized_time_now()
    pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))

    return pst_now.strftime(fmt_str) if fmt_str else pst_now


def get_current_time_ist(fmt_str: Optional[str] = _TIME_FORMAT_STRING):
    utc_now = _utc_localized_time_now()
    ist_now = utc_now.astimezone(pytz.timezone("Asia/Kolkata"))

    return ist_now.strftime(fmt_str) if fmt_str else ist_now


def get_current_time_utc(fmt_str: Optional[str] = _TIME_FORMAT_STRING):
    utc_now = _utc_localized_time_now()
    return utc_now.strftime(fmt_str) if fmt_str else utc_now


# TODO
# def get_cest_time_now(fmt_str):
#     ...

# def get_pst_time_now(fmt_str):
#     ...

# def get_time_by_timezone(timezone: str, fmt_str: Optional[str]):
#     # switch by timezone
#     ...
