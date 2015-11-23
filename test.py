import arrow
import flask
from dateutil import tz

from free_times import get_free_times
from busy_times import get_start_end_datetime, is_available, get_busy_dict, \
    get_busy_list
from main import interpret_time, interpret_date, cal_sort_key


def get_busy_dict_test():
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=9,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=9,
        month=11, year=2015)

    print(begin_date.isoformat())
    print(end_date.isoformat())

    events = [{'start': {'dateTime': '2015-11-11T07:00:00-08:00'},
              'end': {'dateTime': '2015-11-11T08:00:00-08:00'}},
              {'start': {'dateTime': '2015-11-10T08:00:00-08:00'},
              'end': {'dateTime': '2015-11-10T18:00:00-08:00'}},
              {'start': {'dateTime': '2015-11-11T08:00:00-08:00'},
              'end': {'dateTime': '2015-11-11T10:00:00-08:00'}},
              {'start': {'dateTime': '2015-11-12T11:00:00-08:00'},
              'end': {'dateTime': '2015-11-12T12:00:00-08:00'}},
              {'start': {'dateTime': '2015-11-12T12:00:00-08:00'},
              'end': {'dateTime': '2015-11-12T13:00:00-08:00'}},
              {'start': {'dateTime': '2015-11-09T10:00:00-08:00'},
              'end': {'dateTime': '2015-11-09T11:00:00-08:00'}},
              {'start': {'dateTime': '2015-11-13T16:00:00-08:00'},
              'end': {'dateTime': '2015-11-13T18:00:00-08:00'}},
              {'start': {'dateTime': '2015-11-12T15:00:00-08:00'},
              'end': {'dateTime': '2015-11-12T16:00:00-08:00'}},
              {'start': {'dateTime': '2015-11-11T10:00:00-08:00'},
              'end': {'dateTime': '2015-11-11T11:00:00-08:00'}},
              {'start': {'dateTime': '2015-11-12T09:00:00-08:00'},
              'end': {'dateTime': '2015-11-12T11:00:00-08:00'}},
              {'start': {'date': '2015-11-08'},
              'end': {'date': '2015-11-10'}}]

    busy = {'2015-11-12T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-12T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-12T11:00:00-08:00'}},
            '2015-11-13T16:00:00-08:00':
            {'start': {'dateTime': '2015-11-13T16:00:00-08:00'},
             'end': {'dateTime': '2015-11-13T17:00:00-08:00'}},
            '2015-11-09T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-09T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-09T17:00:00-08:00'}},
            '2015-11-12T12:00:00-08:00':
            {'start': {'dateTime': '2015-11-12T12:00:00-08:00'},
             'end': {'dateTime': '2015-11-12T13:00:00-08:00'}},
            '2015-11-12T15:00:00-08:00':
            {'start': {'dateTime': '2015-11-12T15:00:00-08:00'},
             'end': {'dateTime': '2015-11-12T16:00:00-08:00'}},
            '2015-11-12T11:00:00-08:00':
            {'start': {'dateTime': '2015-11-12T11:00:00-08:00'},
             'end': {'dateTime': '2015-11-12T12:00:00-08:00'}},
            '2015-11-10T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-10T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-10T17:00:00-08:00'}},
            '2015-11-09T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-09T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-09T11:00:00-08:00'}},
            '2015-11-11T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-11T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-11T11:00:00-08:00'}},
            '2015-11-11T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-11T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-11T10:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_list_test():
    busy = {'2015-11-12T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-12T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-12T11:00:00-08:00'}},
            '2015-11-13T16:00:00-08:00':
            {'start': {'dateTime': '2015-11-13T16:00:00-08:00'},
             'end': {'dateTime': '2015-11-13T17:00:00-08:00'}},
            '2015-11-09T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-09T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-09T17:00:00-08:00'}},
            '2015-11-12T12:00:00-08:00':
            {'start': {'dateTime': '2015-11-12T12:00:00-08:00'},
             'end': {'dateTime': '2015-11-12T13:00:00-08:00'}},
            '2015-11-12T15:00:00-08:00':
            {'start': {'dateTime': '2015-11-12T15:00:00-08:00'},
             'end': {'dateTime': '2015-11-12T16:00:00-08:00'}},
            '2015-11-12T11:00:00-08:00':
            {'start': {'dateTime': '2015-11-12T11:00:00-08:00'},
             'end': {'dateTime': '2015-11-12T12:00:00-08:00'}},
            '2015-11-10T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-10T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-10T17:00:00-08:00'}},
            '2015-11-09T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-09T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-09T11:00:00-08:00'}},
            '2015-11-11T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-11T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-11T11:00:00-08:00'}},
            '2015-11-11T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-11T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-11T10:00:00-08:00'}}}

    busy_list = [{'start': {'dateTime': '2015-11-09T09:00:00-08:00'},
                 'end': {'dateTime': '2015-11-11T11:00:00-08:00'}},
                 {'start': {'dateTime': '2015-11-12T09:00:00-08:00'},
                 'end': {'dateTime': '2015-11-12T13:00:00-08:00'}},
                 {'start': {'dateTime': '2015-11-12T15:00:00-08:00'},
                 'end': {'dateTime': '2015-11-12T16:00:00-08:00'}},
                 {'start': {'dateTime': '2015-11-13T16:00:00-08:00'},
                 'end': {'dateTime': '2015-11-13T17:00:00-08:00'}}]

    assert busy_list == get_busy_list(busy)


def get_free_times_test():
    begin_date = arrow.get(
        '11/09/2015 09:00', 'MM/DD/YYYY HH:mm').replace(
        tzinfo=tz.tzlocal()).isoformat()
    end_date = arrow.get(
        '11/13/2015 17:00', 'MM/DD/YYYY HH:mm').replace(
        tzinfo=tz.tzlocal()).isoformat()

    busy = [{'start': {'dateTime': '2015-11-09T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-11T11:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-12T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-12T13:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-12T15:00:00-08:00'},
             'end': {'dateTime': '2015-11-12T16:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-13T16:00:00-08:00'},
             'end': {'dateTime': '2015-11-13T17:00:00-08:00'}}]

    free = [('2015-11-11T11:00:00-08:00', '2015-11-11T17:00:00-08:00'),
            ('2015-11-12T13:00:00-08:00', '2015-11-12T15:00:00-08:00'),
            ('2015-11-12T16:00:00-08:00', '2015-11-13T16:00:00-08:00')]

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