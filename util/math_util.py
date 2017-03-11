# -*- coding: utf-8 -*-
import math
import hashlib


def get_log2_part_nums(num):
    """将一个整数按2的次方分解, 如输入7,则返回[4, 2, 1]
    :param num: 待处理整数
    :return: 一个list, 如输入7,则返回[4, 2, 1]
    """
    result = []
    while num > 0:
        re = pow(2, math.floor(math.log(num, 2)))
        num -= re
        result.append(int(re))
    return result


def get_gps_distance(lat1, lng1, lat2, lng2):
    """计算两个gps点之间的距离，单位米
    :param lat1: 纬度，如39.81625
    :param lng1: 经度，如109.99309
    :param lat2: 纬度，如39.81595
    :param lng2: 经度，如109.99456
    :return: 两个gps点之间的距离，单位米（保留小数点后一位），如 130.1
    """
    r = 6378.137
    lat1 = math.radians(lat1)
    lng1 = math.radians(lng1)
    lat2 = math.radians(lat2)
    lng2 = math.radians(lng2)
    d1 = abs(lat1 - lat2)
    d2 = abs(lng1 - lng2)
    p = math.pow(math.sin(d1 / 2), 2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(d2 / 2), 2)
    dis = r * 2 * math.asin(math.sqrt(p))
    return round(dis * 1000, 1)


def md5(string):
    """计算输入参数的md5值
    :param string: 字符串类型, 如: 'qunar'
    :return: md5字符串，如: 'ed8e212a114c18dda84ab5c14b42bfc7'
    """
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()


if __name__ == '__main__':
    print get_gps_distance(39.81625, 109.99309, 39.81595, 109.99456)
    print get_gps_distance(31.980298, 117.107277, 31.888227, 117.524757)
    print md5('china')
