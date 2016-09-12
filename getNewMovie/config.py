#!/usr/bin/env python
# encoding: utf-8
# config.py created by Jesse
# 16/8/8 15:05

import urllib2
import re
from bs4 import BeautifulSoup


def get_page(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    page = response.read()
    return page


def get_nowplaying():
    """获取正在热映电影信息"""
    movie_url = 'https://movie.douban.com/nowplaying/shenzhen/'
    movie_item = {}
    movie_list = []

    main_page = get_page(movie_url)
    soup = BeautifulSoup(main_page, 'lxml')
    movie_info_list = soup.body.find(id='nowplaying').find_all('li', class_='list-item')

    for movie_info in movie_info_list:
        movie_name = movie_info.find_all('li', class_='stitle')[0].a['title']
        if movie_info['data-score'] == '':
            movie_info['data-score'] = u'暂无评分'
        else:
            movie_info['data-score'] = u'评分: ' + movie_info['data-score']
        movie_info['data-actors'] = u'演员: ' + movie_info['data-actors']
        movie_item['title'] = movie_name
        movie_item['subtitle'] = movie_info['data-score'] + '  ' + movie_info['data-actors']
        movie_item['arg'] = movie_info['data-subject']
        movie_list.append(movie_item.copy())

    return movie_list


def get_later():
    """获取即将上映电影信息"""
    movie_url = 'https://movie.douban.com/later/shenzhen/'
    movie_item = {}
    movie_list = []

    main_page = get_page(movie_url)
    soup = BeautifulSoup(main_page, 'lxml')

    movie_info_list = soup.body.find(id='showing-soon').find_all('div', class_='intro')
    for movie_info in movie_info_list:
        movie_item['title'] = movie_info.h3.a.string
        movie_intro = movie_info.ul.find_all('li')
        movie_item['subtitle'] = movie_intro[0].string + ' ' + movie_intro[2].string + '  ' + movie_intro[1].string
        movie_item['arg'] = re.search('\d{8}', movie_info.h3.a['href']).group()
        movie_list.append(movie_item.copy())

    return movie_list


def arg_switch(arg):
    """根据输入参数获取不同电影信息"""
    return {
        'now': get_nowplaying,
        'soon': get_later
    }.get(arg, get_nowplaying)


def main(wf):
    if len(wf.args) == 0:
        arg = 'soon'
    else:
        arg = wf.args[0]
    wf_items = arg_switch(arg)()
    for item in wf_items:
        wf.add_item(title=item['title'], subtitle=item['subtitle'], arg=item['arg'], valid=True)
    wf.send_feedback()
