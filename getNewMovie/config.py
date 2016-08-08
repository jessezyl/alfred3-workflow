#!/usr/bin/env python
# encoding: utf-8
# config.py created by Jesse
# 16/8/8 15:05

import urllib2
from bs4 import BeautifulSoup


def main(wf):
    movie_list = {}
    movie_url = 'https://movie.douban.com/nowplaying/shenzhen/'
    req = urllib2.Request(movie_url)
    response = urllib2.urlopen(req)
    main_page = response.read()

    soup = BeautifulSoup(main_page, 'lxml')

    movie_info_list = soup.body.find(id='nowplaying').find_all('li', class_='list-item')

    for movie_info in movie_info_list:
        movie_name = movie_info.find_all('li', class_='stitle')[0].a['title']
        if movie_info['data-score'] == '':
            movie_info['data-score'] = u'暂无评分'
        else:
            movie_info['data-score'] = u'评分: ' + movie_info['data-score']
        movie_info['data-actors'] = u'演员: ' + movie_info['data-actors']
        movie_list[movie_name] = (movie_info['data-score'], movie_info['data-actors'], movie_info['data-subject'])

    for name in movie_list:
        subtitle = movie_list[name][0]+'  '+movie_list[name][1]
        wf.add_item(title=name, subtitle=subtitle, arg=movie_list[name][2], valid=True)
    wf.send_feedback()
