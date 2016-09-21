#!/usr/bin/env python
# encoding: utf-8
# config.py created by Jesse
# 16/9/20 15:29


from workflow import web
import os
import datetime
import json

coming_soon_url = 'https://api.douban.com/v2/movie/coming_soon'
nowplaying_url = 'https://api.douban.com/v2/movie/in_theaters'


def get_data(arg):
    url = arg_switch(arg)
    data_filename = datetime.date.today().strftime('%Y_%m_%d') + '_%s.json' % arg
    if not os.path.exists(data_filename):
        web.get(url).save_to_path(data_filename)
    data_fd = open(data_filename, 'r')
    data = json.load(data_fd)
    data_fd.close()
    return data


def get_movies(arg):
    data = get_data(arg)
    movie_item = {}
    movie_list = []

    for movie_info in data['subjects']:
        movie_item['title'] = movie_info['title']
        icon = movie_info['id'] + '.jpg'
        if not os.path.exists(icon):
            web.get(movie_info['images']['small']).save_to_path(icon)
        directors_name = map(lambda x: x['name'], movie_info['directors'])
        actors_name = map(lambda x: x['name'], movie_info['casts'])

        if movie_info['rating']['average'] == 0:
            score = u'暂无评分'
        else:
            score = u'评分:' + str(movie_info['rating']['average'])
        movie_item['subtitle'] = score + u'  导演:' + ' / '.join(directors_name) + u'  演员:' + ' / '.join(actors_name)
        movie_item['arg'] = movie_info['id']
        movie_item['icon'] = icon
        movie_list.append(movie_item.copy())

    return movie_list


def arg_switch(arg):
    return {
        'now': nowplaying_url,
        'soon': coming_soon_url,
    }.get(arg, nowplaying_url)


def main(wf):
    if wf.args[0] == 'soon':
        arg = 'soon'
    else:
        arg = 'now'

    wf_items = get_movies(arg)

    for item in wf_items:
        wf.add_item(title=item['title'], subtitle=item['subtitle'], arg=item['arg'], icon=item['icon'], valid=True)
    wf.send_feedback()
