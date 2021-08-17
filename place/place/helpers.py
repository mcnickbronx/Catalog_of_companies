import datetime
from django.db.models import Q
import re
import arrow


def week_of_number(i):
    week = {
        1: 'Montag',
        2: 'Dienstag',
        3: 'Mittwoch',
        4: 'Donnerstag',
        5: 'Freitag',
        6: 'Samstag',
        7: 'Sonntag'
    }
    return week[i]


def check_open(open_list):

    b_time = arrow.now('Europe/Berlin')
    b_time = b_time.replace(hour=12) # for test
    open_place = []
    for v in open_list:
        interval = v['open_interval']
        if interval == 'Geschlossen':
            continue
        if interval == '24 Stunden geöffnet':
            open_place.append(v['place'])
            continue
        time_list = re.findall(r'[0-2]?\d:[0-5]\d', interval)  # We get a list of hours from the line
        time2 = b_time
        # print(v['place'], interval)
        for i, v1 in enumerate(time_list):
            v1 = v1.split(':')
            time1 = time2
            time2 = b_time.replace(hour=int(v1[0]), minute=int(v1[1]), second=0, microsecond=0)
            if i % 2 != 0:
                # print(f'time1: {time1.format("HH:mm")}, time_now: {b_time.format("HH:mm")}, time2: {time2.format("HH:mm")}, chet: ', {i % 2})
                if time1 <= b_time <= time2:
                    # open now
                    open_place.append(v['place'])
                    break
                else:
                    pass
                    # close

            # 10:30–11:3011:45–12:4513:00–14:0014:15–15:1515:30–16:30



    return open_place


def split_list(my_list, field_name):
    new_list = []
    for el in my_list:
        st = str(el[field_name])
        st_list = re.split(', |\r\n|\n', st)
        for s in st_list:
            new_list.append(s)

    # unique
    new_list = list(set(new_list))
    return new_list


def to_list(my_list, field_name):
    new_list = []
    for el in my_list:
        new_list.append(el[field_name])
    return new_list


def q_filter(r_list, places, field):
    q = Q()
    for r in r_list:
        q |= Q(**{'%s' % field: r})
    places = places.filter(q)
    return places
