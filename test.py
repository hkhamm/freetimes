import arrow
from dateutil import tz

from free_times import get_free_times
from busy_times import get_start_end_datetime, is_available, get_busy_dict, \
    get_busy_list
from main import interpret_time, interpret_date, cal_sort_key


def get_busy_dict_1_test():
    """
    get_busy_dict_1_test: All day events that start before and end during the
    interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'date': '2015-11-12'},
               'end': {'date': '2015-11-16'}}]

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_2_test():
    """
    get_busy_dict_2_test: All day events that start during and end after the
    interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'date': '2015-11-20'},
               'end': {'date': '2015-11-22'}}]

    busy = {'2015-11-20T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-20T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_3_test():
    """
    get_busy_dict_3_test: All day, 2 day events that start during and end
    during the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'date': '2015-11-18'},
               'end': {'date': '2015-11-20'}}]

    busy = {'2015-11-18T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-18T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-19T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_4_test():
    """
    get_busy_dict_4_test: All day, 1 day events that start during and end
    during the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'date': '2015-11-19'},
               'end': {'date': '2015-11-20'}}]

    busy = {'2015-11-19T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-19T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_5_test():
    """
    get_busy_dict_5_test: All day events that start before and end after the
    interval.
    """

    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'date': '2015-11-15'},
               'end': {'date': '2015-11-21'}}]

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_6_test():
    """
    get_busy_dict_6_test: Sequential all day events during the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'date': '2015-11-16'},
               'end': {'date': '2015-11-17'}},
              {'start': {'date': '2015-11-17'},
               'end': {'date': '2015-11-18'}}]

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}},
            '2015-11-17T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-17T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_7_test():
    """
    get_busy_dict_7_test: One day events that start before and end during the
    interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'dateTime': '2015-11-16T08:00:00-08:00'},
               'end': {'dateTime': '2015-11-16T10:00:00-08:00'}}]

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T10:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_8_test():
    """
    get_busy_dict_8_test: One day events that start during and end after the
    interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
               'end': {'dateTime': '2015-11-16T18:00:00-08:00'}}]

    busy = {'2015-11-16T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_9_test():
    """
    get_busy_dict_9_test: One day events that start during and end during the
    interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
               'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}]

    busy = {'2015-11-16T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_10_test():
    """
    get_busy_dict_10_test: One day events that start before and end after the
    interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'dateTime': '2015-11-16T08:00:00-08:00'},
               'end': {'dateTime': '2015-11-16T18:00:00-08:00'}}]

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_11_test():
    """
    get_busy_dict_11_test: Sequential one day events during the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
               'end': {'dateTime': '2015-11-16T10:00:00-08:00'}},
              {'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
               'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}]

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T10:00:00-08:00'}},
            '2015-11-16T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-17T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-17T11:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_list_1_test():
    """
    get_busy_list_1_test: Sequential all day busy times.
    """
    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}},
            '2015-11-17T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-17T17:00:00-08:00'}}}

    busy_list = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
                  'end': {'dateTime': '2015-11-17T17:00:00-08:00'}}]

    assert busy_list == get_busy_list(busy)


def get_busy_list_2_test():
    """
    get_busy_list_2_test: Overlapping all day busy times and busy times
    within the same day.
    """

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}},
            '2015-11-16T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}}

    busy_list = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
                  'end': {'dateTime': '2015-11-16T17:00:00-08:00'}}]

    assert busy_list == get_busy_list(busy)


def get_busy_list_3_test():
    """
    get_busy_list_3_test: Sequential busy times within the same day.
    """

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T10:00:00-08:00'}},
            '2015-11-16T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}}

    busy_list = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
                  'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}]

    assert busy_list == get_busy_list(busy)


def get_busy_list_4_test():
    """
    get_busy_list_4_test: Sequential all day busy times and busy times within
    the same day.
    """
    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}},
            '2015-11-17T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-17T10:00:00-08:00'}}}

    busy_list = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
                  'end': {'dateTime': '2015-11-17T10:00:00-08:00'}}]

    assert busy_list == get_busy_list(busy)


def get_busy_list_5_test():
    """
    get_busy_list_5_test: Busy dict is empty.
    """
    busy = {}

    busy_list = []

    assert busy_list == get_busy_list(busy)


def get_free_times_1_test():
    """
    get_free_times_1_test: No busy times.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = []

    free = [('2015-11-16T09:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_2_test():
    """
    get_free_times_2_test: Only one busy time at beginning of the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T10:00:00-08:00'}}]

    free = [('2015-11-16T10:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_3_test():
    """
    get_free_times_3_test: Only one busy time at end of the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-20T16:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}]

    free = [('2015-11-16T09:00:00-08:00', '2015-11-20T16:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_4_test():
    """
    get_free_times_4_test: Only one busy time in the middle of the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}]

    free = [('2015-11-16T09:00:00-08:00', '2015-11-16T10:00:00-08:00'),
            ('2015-11-16T11:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_5_test():
    """
    get_free_times_5_test: Two busy times, one at the beginning and one in
    the middle of the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T10:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-20T16:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}]

    free = [('2015-11-16T10:00:00-08:00', '2015-11-20T16:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_6_test():
    """
    get_free_times_6_test: Two busy times in the middle of the interval and
    on the same day.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-16T12:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T13:00:00-08:00'}}]

    free = [('2015-11-16T09:00:00-08:00', '2015-11-16T10:00:00-08:00'),
            ('2015-11-16T11:00:00-08:00', '2015-11-16T12:00:00-08:00'),
            ('2015-11-16T13:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_7_test():
    """
    get_free_times_7_test: Two busy times, one in the middle of the start day
    and one on a different day.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-17T12:00:00-08:00'},
             'end': {'dateTime': '2015-11-17T13:00:00-08:00'}}]

    free = [('2015-11-16T09:00:00-08:00', '2015-11-16T10:00:00-08:00'),
            ('2015-11-16T11:00:00-08:00', '2015-11-17T12:00:00-08:00'),
            ('2015-11-17T13:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_8_test():
    """
    get_free_times_8_test: Two busy times, one in the middle not on the start
    day and one on a different day.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-17T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-17T11:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-18T12:00:00-08:00'},
             'end': {'dateTime': '2015-11-18T13:00:00-08:00'}}]

    free = [('2015-11-16T09:00:00-08:00', '2015-11-17T10:00:00-08:00'),
            ('2015-11-17T11:00:00-08:00', '2015-11-18T12:00:00-08:00'),
            ('2015-11-18T13:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_9_test():
    """
    get_free_times_9_test: Two busy times, one in the middle on the start
    day and one at the end.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-20T16:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}]

    free = [('2015-11-16T09:00:00-08:00', '2015-11-16T10:00:00-08:00'),
            ('2015-11-16T11:00:00-08:00', '2015-11-20T16:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_10_test():
    """
    get_free_times_10_test: Complex busy schedule.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-18T11:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-19T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-19T13:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-19T15:00:00-08:00'},
             'end': {'dateTime': '2015-11-19T16:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-20T16:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}]

    free = [('2015-11-18T11:00:00-08:00', '2015-11-18T17:00:00-08:00'),
            ('2015-11-19T13:00:00-08:00', '2015-11-19T15:00:00-08:00'),
            ('2015-11-19T16:00:00-08:00', '2015-11-20T16:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def is_available_true_test():
    event = {'transparency': 'transparent'}

    assert is_available(event)


def is_available_false_test():
    event = {}

    assert not is_available(event)


def get_start_end_datetime_is_datetime_test():
    event = {'start': {'dateTime': '2015-11-22T11:36:51.070854-08:00'},
             'end': {'dateTime': '2015-11-22T16:37:58.735355-08:00'}}

    start = arrow.get('2015-11-22T11:36:51.070854-08:00').replace(
        tzinfo=tz.tzlocal())

    end = arrow.get('2015-11-22T16:37:58.735355-08:00').replace(
        tzinfo=tz.tzlocal())

    is_all_day = False

    assert (start, end, is_all_day) == get_start_end_datetime(event)


def get_start_end_datetime_is_date_test():
    event = {'start': {'date': '2015-11-22T11:36:51.070854-08:00'},
             'end': {'date': '2015-11-22T16:37:58.735355-08:00'}}

    start = arrow.get('2015-11-22T11:36:51.070854-08:00').replace(
        tzinfo=tz.tzlocal())

    end = arrow.get('2015-11-22T16:37:58.735355-08:00').replace(
        tzinfo=tz.tzlocal())

    is_all_day = True

    assert (start, end, is_all_day) == get_start_end_datetime(event)


def interpret_time_test():
    time = '9:00'

    arrow_time = arrow.get(time, 'H:mm').replace(
        tzinfo=tz.tzlocal()).isoformat()

    assert arrow_time == interpret_time(time)


def interpret_date_test():
    date = '12/25/2015'

    arrow_date = arrow.get(date, 'MM/DD/YYYY').replace(
        tzinfo=tz.tzlocal()).isoformat()

    assert arrow_date == interpret_date(date)


def cal_sort_key_test():
    cal = {'selected': True,
           'kind': 'calendar#calendarListEntry',
           'primary': False,
           'id': 'fcl59tcklie15bv44kafivmmp4@group.calendar.google.com',
           'summary': 'test'}

    assert ('X', ' ', 'test') == cal_sort_key(cal)
