from datetime import datetime, timedelta

from service import is_leave_early, get_workday


def test_leave_early():
    time_in = datetime(2024, 2, 2, 9)
    minimum_working_hours = 8
    current_time = datetime(2024, 2, 2, 16)
    assert is_leave_early(time_in, minimum_working_hours, current_time)


def test_just_meet_minimum_hours():
    time_in = datetime(2024, 2, 2, 9)
    minimum_working_hours = 8
    current_time = datetime(2024, 2, 2, 17)
    assert not is_leave_early(time_in, minimum_working_hours, current_time)


def test_work_more_than_minimum_hours():
    time_in = datetime(2024, 2, 2, 9)
    minimum_working_hours = 8
    current_time = datetime(2024, 2, 2, 18)
    assert not is_leave_early(time_in, minimum_working_hours, current_time)


def test_get_workday_at_cutoff():
    date_time = datetime(2024, 2, 3, 8, 0)
    workday_cutoff_str = '08:00'
    assert get_workday(date_time, workday_cutoff_str) == datetime(2024, 2, 3).date()


def test_get_workday_after_cutoff():
    date_time = datetime(2024, 2, 3, 8, 1)
    workday_cutoff_str = '08:00'
    assert get_workday(date_time, workday_cutoff_str) == datetime(2024, 2, 3).date()


def test_get_workday_before_cutoff():
    date_time = datetime(2024, 2, 3, 7, 59)
    workday_cutoff_str = '08:00'
    assert get_workday(date_time, workday_cutoff_str) == datetime(2024, 2, 2).date()
