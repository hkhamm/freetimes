import arrow

import CONFIG

START_TIME = CONFIG.START_TIME
END_TIME = CONFIG.END_TIME


def get_free_times(busy_times, begin_date, end_date):
    """
    Gets a list of free times calculated from a list of busy times.
    :param busy_times: is the list of busy times in ascending order.
    :param begin_date: is the start of the selected time interval.
    :param end_date: is the end of the selected time interval.
    :return: a list of free times.
    """
    begin_date = arrow.get(begin_date).replace(hour=9)
    begin_day = begin_date.format('YYYYMMDD')
    begin_time = '09:00'
    end_time = '17:00'
    end_date = arrow.get(end_date).replace(hour=17)
    end_day = end_date.format('YYYYMMDD')
    free_times = []
    stored_event = busy_times[0]
    busy_times = busy_times[1:]

    # TODO refactor using a table
    print('free times')

    for event in busy_times:
        event_start = arrow.get(event['start']['dateTime'])
        event_end = arrow.get(event['end']['dateTime'])
        event_start_time = event_start.format('HH:mm')
        event_end_time = event_end.format('HH:mm')
        event_start_day = event_start.format('YYYYMMDD')
        event_end_day = event_end.format('YYYYMMDD')
        day_start = event_start.replace(hour=START_TIME, minute=0).isoformat()
        stored_event_start = arrow.get(stored_event['start']['dateTime'])
        stored_event_start_time = stored_event_start.format('HH:mm')
        stored_event_start_day = arrow.get(
            stored_event['start']['dateTime']).format('YYYYMMDD')
        stored_event_end_day = arrow.get(
            stored_event['end']['dateTime']).format('YYYYMMDD')
        stored_event_end = stored_event['end']['dateTime']
        stored_event_end_time = arrow.get(stored_event_end).format('HH:mm')
        prev_day_end = arrow.get(stored_event_end).replace(hour=END_TIME,
                                                           minute=0).isoformat()
        event_start = event_start.isoformat()

        # starting free time
        if (stored_event_start_day == begin_day and
                stored_event_start_time != begin_time):
            free_times.append((begin_date.isoformat(),
                               stored_event_start.isoformat()))
            print('1 {} - {}'.format(stored_event_end, event_start))

        # middle free times
        if (stored_event_end < event_start and
                (stored_event_end, event_start) not in free_times):

            if event_start_time == '09:00':
                event_start = arrow.get(
                    event['start']['dateTime']).replace(
                    days=-1, hour=17).isoformat()

            if stored_event_end_time == '17:00':
                stored_event_end = arrow.get(
                    stored_event_end).replace(days=+1, hour=9).isoformat()

            free_times.append((stored_event_end, event_start))
            print('2 {} - {}'.format(stored_event_end, event_start))

        # ending free time
        if (event_end_day == end_day and
                event_end_time != end_time):
            free_times.append((event_end.isoformat(), end_date.isoformat()))
            print('3 {} - {}'.format(stored_event_end, event_start))

        stored_event = event

    print()

    return free_times



