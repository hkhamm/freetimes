import arrow

import CONFIG

START_TIME = CONFIG.START_TIME
END_TIME = CONFIG.END_TIME


def get_free_times(busy_times):
    """
    Gets a list of free times calculated from a list of busy times.
    :param busy_times: is the list of busy times
    :return: a list of free times in ascending order.
    """
    free_times = []
    is_first = True
    stored_event = arrow.now()

    # TODO refactor using a table
    print('free times')

    for event in busy_times:
        if is_first:
            stored_event = event

        event_start = arrow.get(event['start']['dateTime'])
        event_end = arrow.get(event['end']['dateTime'])
        start_time = int(event_start.format('HHmm'))
        end_time = int(event_end.format('HHmm'))
        event_day = int(arrow.get(
            event['start']['dateTime']).format('YYYYMMDD'))
        day_start = arrow.get(
            event['start']['dateTime']).replace(hour=START_TIME, minute=0)
        stored_event_day = int(arrow.get(
            stored_event['start']['dateTime']).format('YYYYMMDD'))
        stored_event_end = stored_event['end']['dateTime']

        if start_time == 900 and end_time == 1700:
            stored_event = event
        elif start_time == 900 and end_time < 1700:
            if not is_first:
                if stored_event_day < event_day:
                    prev_day_end = arrow.get(
                        stored_event['end']['dateTime']).replace(hour=END_TIME,
                                                                 minute=0)
                    free_times.append((stored_event_end,
                                       prev_day_end.isoformat()))
                    print('1 {} - {}'.format(stored_event_end,
                                             prev_day_end.isoformat()))
            else:
                is_first = False
            stored_event = event
        elif start_time > 900 and end_time <= 1700:
            if not is_first:
                if stored_event_day < event_day:
                    prev_day_end = arrow.get(
                        stored_event['end']['dateTime']).replace(hour=END_TIME,
                                                                 minute=0)
                    free_times.append((stored_event_end,
                                       prev_day_end.isoformat()))
                    print('2 {} - {}'.format(stored_event_end,
                                             prev_day_end.isoformat()))
                if event_day != stored_event_day:
                    free_times.append((day_start.isoformat(),
                                       event_start.isoformat()))
                    print('3 {} - {}'.format(day_start.isoformat(),
                                             event_start.isoformat()))
                elif event_day == stored_event_day:
                    free_times.append((stored_event_end,
                                       event_start.isoformat()))
                    print('4 {} - {}'.format(stored_event_end,
                                             event_start.isoformat()))
            else:
                is_first = False
            stored_event = event

    print()

    return free_times
