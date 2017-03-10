# -*- coding: utf-8 -*-
"""
    《斗破苍穹》阅读器
    chapter_id: 2 - 1646
"""
from __future__ import unicode_literals
import requests
import sys
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from bs4.element import Tag

reload(sys)
sys.setdefaultencoding("utf-8")

base_chapter_id = 289
base_page_id = 1049704

url = 'http://www.xxbiquge.com/1_1413/{}.html'


def get_content(chapter_id):
    if chapter_id < 2 or chapter_id > 1646:
        print "章节ID, 从2开始, 1646截止"
        return
    diff = chapter_id - base_chapter_id
    page_id = base_page_id + diff
    print page_id
    resp = requests.get(url.format(page_id))
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = soup.title.string.split('-')[0].strip()
    print title
    tag = soup.find(id="content")
    contents = []
    for line in tag.contents:
        if isinstance(line, NavigableString):
            contents.append(line.string)
        elif isinstance(line, Tag):
            if line.text:
                contents.append(line.text)
    return contents


def open_chap(chapter_id):
    """
    第chapter_id章内容
    :param chapter_id: 章节ID, 从2开始, 1646截止
    :return:
    """
    contents = get_content(chapter_id)
    result = format_show(contents)
    for line in result:
        print line


def format_show(contents, char_num=20):
    """
    格式化展示
    :param contents: 内容， list
    :param char_num: 每行显示字数
    :return:
    """
    if not contents:
        return []
    result = []
    for line in contents:
        for i in xrange(0, len(line), char_num):
            result.append(line[i:i+char_num])
    return result


if __name__ == '__main__':
    open_chap(2)
