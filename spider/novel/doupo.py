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
import time
import random

reload(sys)
sys.setdefaultencoding("utf-8")

base_chapter_id = 289
base_page_id = 1049704
start_chapter_id = 2
end_chapter_id = 1646

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
    tag = soup.find(id="content")
    contents = []
    for line in tag.contents:
        if isinstance(line, NavigableString):
            contents.append(line.string)
        elif isinstance(line, Tag):
            if line.text:
                contents.append(line.text)
    return title, contents


def open_chap(chapter_id):
    """
    第chapter_id章内容
    :param chapter_id: 章节ID, 从2开始, 1646截止
    :return:
    """
    title, contents = get_content(chapter_id)
    print title
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


def save_chapter_novel(from_chapter_id, to_chapter_id, file_name):
    """
    保存小说内容到文件
    :param from_chapter_id: 开始章节id
    :param to_chapter_id: 结束章节id
    :param file_name: 文件名
    :return:
    """
    contents = []
    for chapter_id in range(from_chapter_id, to_chapter_id+1):
        chapter = get_content(chapter_id)
        contents.append(chapter)
        r = random.uniform(1, 2)
        time.sleep(r)
    lines = []
    for one in contents:
        lines.append(one[0])
        for c in one[1]:
            lines.append(c)
        lines.append('\n\n')
    write_file(file_name, lines)


def save_novel(file_name):
    save_chapter_novel(start_chapter_id, end_chapter_id, file_name)


def write_file(file_name, lines):
    f = open(file_name, 'w')
    for line in lines:
        f.write(line)
        f.write('\n')
    f.close()

if __name__ == '__main__':
    open_chap(2)
