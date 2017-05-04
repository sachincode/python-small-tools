# -*- coding: utf-8 -*-
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

url = 'http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201703/t20170310_1471429.html'


def read_lines():
    """
    文件内容复制自以上url页面，并替换显示为空格样式的非空格字符为空格字符
    :return:
    """
    f = open('/home/shichengzhang/citycode.txt')
    lines = f.readlines()
    lines = [one.rstrip() for one in lines]
    f.close()
    return lines


def process():
    """
    三级结果，跳过台湾、香港、澳门
    :return: [['110000', '北京市', '110100', '市辖区', '110101', '东城区']...]
    """
    lines = read_lines()
    print 'lines: ', len(lines)
    result = []
    context = []
    for line in lines:
        if not line:
            continue
        sc = start_space_count(line)
        parts = split_omit_space(line)
        c = len(parts)
        if c != 2:
            print line
            raise
        if sc == 0:
            if len(context) == 2:
                context.pop()
                context.pop()
            elif len(context) == 1:
                context.pop()
            context.append(parts)
        elif sc == 1:
            if len(context) == 2:
                context.pop()
            context.append(parts)
        elif sc == 2:
            result.append(join_parts(context, parts))
        else:
            print line
            raise
    print 'count: ', len(result)
    return result


def join_parts(context, parts):
    result = []
    for one in context:
        result.extend(one)
    if parts:
        result.extend(parts)
    return result


def split_omit_space(line):
    result = []
    parts = line.split(' ')
    for one in parts:
        if one:
            result.append(one)
    return result


def start_space_count(line):
    l = len(line)
    i = 0
    c = 0
    while i < l:
        if line[i] == ' ':
            c += 1
        else:
            break
        i += 1
    return c


if __name__ == '__main__':
    result = process()
    lens = set()
    for one in result:
        lens.add(len(one))
    print lens
