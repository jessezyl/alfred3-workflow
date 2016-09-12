#!/usr/bin/env python
# encoding: utf-8
# config.py created by Jesse
# 16/9/12 16:24

import time
import json
from workflow import web


def save_calendar(data):
    cal_file = open('cal.json', 'w')
    cal_file.write(json.dumps(data))


def get_cal_data_from_file():
    cal_file = open('cal.json', 'r')
    data = cal_file.read()
    cal_file.close()
    return json.loads(data)


def get_cal_data_from_web(year, month):
    cal_url = 'http://api.tuijs.com/calendar'
    return web.get(cal_url+'?year=%s&month=%s' % (year, month)).json()


def get_chinese_calendar():
    time_tuple = time.localtime()
    year = time_tuple.tm_year
    month = time_tuple.tm_mon
    day = time_tuple.tm_mday
    data = get_cal_data_from_web(year, month)
    save_calendar(data)
    # if day == 1:
    #     data = get_cal_data_from_web(year, month)
    # else:
    #     data = get_cal_data_from_file()
    return data


def get_today_info():
    data = get_chinese_calendar()
    day = time.localtime().tm_mday
    today_info = data['monthData'][day-1]
    return today_info


def main(wf):
    today_data = get_today_info()
    title = u'%s年%s月%s日' % (today_data['year'], today_data['month'], today_data['day'])
    subtitle = today_data['lunarMonthName'] + today_data['lunarDayName']
    if 'solarFestival' in today_data:
        subtitle = subtitle + ' ' + today_data['solarFestival']
    # print today
    wf.add_item(title=title, subtitle=subtitle, arg=subtitle)
    wf.send_feedback()


# data = get_today_info()
# print data
# main()