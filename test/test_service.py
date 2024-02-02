from datetime import datetime

from service import is_leave_early


def test_leave_early():
    time_in = datetime(2024, 2, 2, 9)
    minimum_working_hours = 8
    current_time = datetime(2024, 2, 2, 16)
    assert is_leave_early(time_in, minimum_working_hours, current_time)


def test_just_meet_minimum_hours():
    time_in = datetime(2024, 2, 2, 9)  # 早上 9 點上班
    minimum_working_hours = 8
    current_time = datetime(2024, 2, 2, 17)  # 下午 5 點離開，工作了 8 小時
    assert not is_leave_early(time_in, minimum_working_hours, current_time)


def test_work_more_than_minimum_hours():
    time_in = datetime(2024, 2, 2, 9)
    minimum_working_hours = 8
    current_time = datetime(2024, 2, 2, 18)
    assert not is_leave_early(time_in, minimum_working_hours, current_time)