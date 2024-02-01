from functools import wraps


def cache_holiday_check(func):
    holiday_cache = {}

    @wraps(func)
    def wrapper_check_holiday(date, *args, **kwargs):
        if date in holiday_cache:
            print('has ')

            return holiday_cache[date]
        is_holiday = func(date, *args, **kwargs)
        holiday_cache[date] = is_holiday
        return is_holiday
    return wrapper_check_holiday