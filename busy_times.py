import arrow
from dateutil import tz
import flask

import CONFIG

START_TIME = CONFIG.START_TIME
END_TIME = CONFIG.END_TIME


def get_busy_times(service):
    """
    Gets a list of busy times calculated from the user selected calendar's
    events.
    :param service: is the Google service from where the calendar is retrieved.
    :return: a list of busy times in ascending order.
    """
    begin_date = arrow.get(flask.session["begin_date"]).replace(hours=+9)
    end_date = arrow.get(flask.session['end_date']).replace(hours=+17)
    busy_dict = {}
    busy = []

    # TODO refactor because its too complicated

    for cal_id in flask.session['checked_calendars']:
        events = service.events().list(calendarId=cal_id).execute()
        for event in events['items']:
            available = is_available(event)
            event_start, event_end, is_all_day = get_start_end_datetime(event)
            day_start = event_start.replace(hour=START_TIME, minute=0)
            day_end = event_end.replace(hour=END_TIME, minute=0)

            # Catches events start after begin time or end before end time
            if ((event_start >= begin_date or event_end <= end_date) and
                    not available and not is_all_day and
                    event_start < day_end and event_end > day_start):
                if event_start < day_start:
                    event['start']['dateTime'] = day_start.isoformat()
                if event_end > day_end:
                    event['end']['dateTime'] = day_end.isoformat()

                busy_dict[event_start.isoformat()] = event

            # Catches all day events between beginning and ending times
            if (event_start >= begin_date and event_end <= end_date and
                    not available and is_all_day and
                    event_start < day_end and event_end > day_start):
                tmp = arrow.get(event['start']['date'])
                tmp = tmp.replace(hour=START_TIME, minute=0).isoformat()
                event['start']['dateTime'] = tmp
                tmp = arrow.get(event['end']['date'])
                tmp = tmp.replace(days=-1, hour=END_TIME, minute=0).isoformat()
                event['end']['dateTime'] = tmp

                busy_dict[event_start.isoformat()] = event

            # Catches events that start before beginning datetime and end
            # before or after the ending datetime
            if (event_start < begin_date < event_end and
                    not available):
                try:
                    start_tmp = arrow.get(event['start']['dateTime'])
                    end_tmp = arrow.get(event['end']['dateTime'])
                except:
                    start_tmp = arrow.get(event['start']['date'])
                    end_tmp = arrow.get(event['end']['date'])

                start_tmp = start_tmp.replace(hour=START_TIME,
                                              minute=0).isoformat()
                end_tmp = end_tmp.isoformat()
                event['start']['dateTime'] = start_tmp
                event['end']['dateTime'] = end_tmp

                busy_dict[event_start.isoformat()] = event

            # Catches all day events events that start before beginning datetime
            # and end before or after the ending datetime
            if (event_start < begin_date < event_end and
                    not available and is_all_day):
                try:
                    start_tmp = arrow.get(event['start']['dateTime'])
                    end_tmp = arrow.get(event['end']['dateTime'])
                except:
                    start_tmp = arrow.get(event['start']['date'])
                    end_tmp = arrow.get(event['end']['date'])

                start_tmp = start_tmp.replace(hour=START_TIME,
                                              minute=0,
                                              tzinfo=tz.tzlocal()).isoformat()
                end_tmp = end_tmp.replace(days=-1, hour=END_TIME,
                                          minute=0,
                                          tzinfo=tz.tzlocal()).isoformat()
                event['start']['dateTime'] = start_tmp
                event['end']['dateTime'] = end_tmp

                busy_dict[event_start.isoformat()] = event

    # check for all day events, remove other events that overlap with it
    remove_list = []
    for i in sorted(busy_dict):
        event = busy_dict[i]

        # if event is all day
        if 'date' in event['start']:
            tmp = event['start']['date']
            this_day = arrow.get(event['start']['dateTime']).format('dddd')
            for j in sorted(busy_dict):
                other_event = busy_dict[j]
                if event != other_event:
                    other_day = arrow.get(
                        other_event['start']['dateTime']).format('dddd')
                    if this_day == other_day:
                        remove_list.append(other_event)
        if event not in remove_list:
            busy.append(busy_dict[i])

    return busy


def is_available(event):
    """
    Checks if the event has the transparency attribute.
    :param event: is the event to check.
    :return: True if it is transparent and False if not
    """
    try:
        transparency = event['transparency']
        available = True
    except:
        available = False

    return available


def get_start_end_datetime(event):
    """
    Gets the event's start and end as arrow objects.
    :param event: is the event to check.
    :return: a 2-tuple of the events start and end as an arrow objects.
    """
    is_all_day = False

    try:
        event_start = arrow.get(event['start']['dateTime'])
        event_end = arrow.get(event['end']['dateTime'])
    except:
        event_start = arrow.get(event['start']['date'])
        event_end = arrow.get(event['end']['date'])
        is_all_day = True

    return event_start, event_end, is_all_day
