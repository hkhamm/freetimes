import arrow
from dateutil import tz
import flask

import CONFIG

START_TIME = CONFIG.START_TIME
END_TIME = CONFIG.END_TIME


def get_busy_times(events):
    """
    Gets a list of busy times calculated from the list of events.
    :param events: a list of calendar events.
    :return: a list of busy times in ascending order.
    """
    begin_date = arrow.get(flask.session["begin_date"]).replace(
        hours=+START_TIME)
    end_date = arrow.get(flask.session['end_date']).replace(hours=+END_TIME)

    busy_dict = get_busy_dict(events, begin_date, end_date)

    busy = get_busy_list(busy_dict)

    return busy


def get_busy_dict(events, begin_date, end_date):
    """
    Fills a dictionary with possible busy times from the list of events.
    :param events: a list of calendar events.
    :param begin_date: is the start of the selected time interval.
    :param end_date: is the end of the selected time interval.
    :return: a dict of events representing possible busy times.
    """
    busy_dict = {}

    for event in events:
        available = is_available(event)
        event_start, event_end, is_all_day = get_start_end_datetime(event)
        day_start = event_start.replace(hour=START_TIME, minute=0)
        day_end = event_end.replace(hour=END_TIME, minute=0)

        if is_all_day and not available:
            if day_start < begin_date:
                event['start']['dateTime'] = begin_date.isoformat()
            else:
                event['start']['dateTime'] = day_start.isoformat()

            event['end']['dateTime'] = day_end.replace(days=-1).isoformat()

            busy_dict[event['start']['dateTime']] = event
        elif ((event_start >= begin_date or event_end <= end_date) and
                not available and not is_all_day and
                event_start < day_end and event_end > day_start):
            if event_start < day_start:
                event['start']['dateTime'] = day_start.isoformat()
            if event_end > day_end:
                event['end']['dateTime'] = day_end.isoformat()

            busy_dict[event['start']['dateTime']] = event

    return busy_dict


def get_busy_list(busy_dict):
    """
    Removes or combines the possible busy times from the busy dictionary and
    returns a sorted list.
    :param busy_dict: a dict of events representing possible busy times.
    :return: a sorted list of events representing busy times.
    """
    busy = []

    remove_list = []
    for i in sorted(busy_dict):
        for j in sorted(busy_dict):
            event = busy_dict[i]
            event_start = arrow.get(event['start']['dateTime'])
            event_end = arrow.get(event['end']['dateTime'])
            event_end_time = event_end.format('HH:mm')
            other_event = busy_dict[j]
            other_event_start = arrow.get(other_event['start']['dateTime'])
            other_event_end = arrow.get(other_event['end']['dateTime'])
            other_event_start_time = other_event_start.format('HH:mm')
            other_event_start_mod = other_event_start.replace(days=-1,
                                                              hour=END_TIME)

            if event != other_event:
                if (other_event_start >= event_start and
                        other_event_end <= event_end):
                    remove_list.append(other_event)

                if (event_end_time == '17:00' and
                        other_event_start_time == '09:00' and
                        event_end == other_event_start_mod):
                    event['end']['dateTime'] = other_event['end']['dateTime']
                    remove_list.append(other_event)

                if event_end == other_event_start:
                    event['end']['dateTime'] = other_event['end']['dateTime']
                    remove_list.append(other_event)

    for i in sorted(busy_dict):
        if busy_dict[i] not in remove_list:
            busy.append(busy_dict[i])

    return busy


def get_events(service):
    """
    Gets a list of events from the Google calendar service.
    :param service: is the Google service from where the calendar is retrieved.
    :return: a list of events.
    """
    events = []

    for cal_id in flask.session['checked_calendars']:
        cal_items = service.events().list(calendarId=cal_id).execute()
        for cal_item in cal_items['items']:
            events.append(cal_item)

    return events


def is_available(event):
    """
    Checks if the event has the transparency attribute.
    :param event: is the event to check.
    :return: True if it is transparent and False if not
    """
    if 'transparency' in event:
        available = True
    else:
        available = False

    return available


def get_start_end_datetime(event):
    """
    Gets the event's start and end as arrow objects.
    :param event: is the event to check.
    :return: a 2-tuple of the events start and end as an arrow objects.
    """
    is_all_day = False

    if 'dateTime' in event['start']:
        event_start = arrow.get(
            event['start']['dateTime']).replace(tzinfo=tz.tzlocal())
        event_end = arrow.get(
            event['end']['dateTime']).replace(tzinfo=tz.tzlocal())
    else:
        event_start = arrow.get(
            event['start']['date']).replace(tzinfo=tz.tzlocal())
        event_end = arrow.get(
            event['end']['date']).replace(tzinfo=tz.tzlocal())
        is_all_day = True

    return event_start, event_end, is_all_day
