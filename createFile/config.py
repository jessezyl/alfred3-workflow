#!/usr/bin/env python
# encoding: utf-8
# config.py.py created by Jesse
# 16/9/19 11:25


def main(wf):
    file_exts = ['', '.py', '.js', '.txt', '.md', '.json', '.log', '.cfg', '.html']
    file_name = ''

    if len(wf.args) != 0:
        file_name = ' '.join(wf.args)

    for ext in file_exts:
        title = file_name + ext
        subtitle = u'在"文稿"文件夹创建"' + title + u'"文件'
        arg = title
        wf.add_item(title=title, subtitle=subtitle, arg=arg, icon='file.png', valid=True)

    wf.send_feedback()
