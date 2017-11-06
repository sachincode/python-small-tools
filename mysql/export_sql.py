# -*- coding: utf-8 -*-
"""
    导出mysql表中数据为 insert sql 文件
    依据主键id进行分页查询，所以表必须有包含id的列
    example:
        mysql> select * from test_zsc;
        +----+-------------+
        | id | name        |
        +----+-------------+
        |  1 | 案例库      |
        |  2 | 日志        |
        |  3 | 按理哭      |
        |  4 | abc'ddd"eee |
        +----+-------------+

        INSERT INTO `test_zsc`(id,name) VALUES('1','案例库'),('2','日志'),('3','按理哭'),('4','abc\'ddd"eee');
"""
from __future__ import unicode_literals
import MySQLdb
import sys
from datetime import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

# 分页查询条数
limit = 1000


def get_connection():
    connection = MySQLdb.Connect(
        host='127.0.0.1',
        port=3306,
        user='sachin_w',
        passwd='sachin',
        db='simple',
        charset='utf8'
    )
    return connection


def get_table_sql(table_name):
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    sql = 'select * from {} where id > %s order by id limit {}'.format(table_name, limit)
    lines = []
    tid = 0
    count = 0
    while True:
        print 'next start id: {}'.format(tid)
        cursor.execute(sql, (tid, ))
        out = cursor.fetchall()
        tid = get_tid(out[-1])
        lines.append(build_insert_sql(table_name, out))
        count += len(out)
        if len(out) < limit:
            break
    cursor.close()
    connection.close()
    print 'table: {}, count: {}'.format(table_name, count)
    return lines


def get_table_sql_range(table_name, start_id, end_id, increment_id):
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    sql = 'select * from {} where {} >= %s and {} < %s order by {} limit {}'.format(table_name, increment_id, increment_id, increment_id, limit)
    lines = []
    tid = start_id
    count = 0
    while True:
        print 'next start id: {}'.format(tid)
        cursor.execute(sql, (tid, end_id))
        out = cursor.fetchall()
        if not out:
            break
        tid = out[-1].get(increment_id) + 1
        lines.append(build_insert_sql(table_name, out))
        count += len(out)
        if len(out) < limit:
            break
    cursor.close()
    connection.close()
    print 'table: {}, count: {}'.format(table_name, count)
    return lines


def get_tid(data):
    ids = {'id', 'ID', 'iD', 'Id'}
    for one in ids:
        if data.get(one):
            return data[one]


def build_insert_sql(table_name, data_list):
    columns = data_list[0].keys()
    sql = 'INSERT INTO `{}`({}) VALUES'.format(table_name, ','.join(columns))
    values = []
    for data in data_list:
        values.append(build_value(columns, data))
    return sql + ','.join(values) + ';'


def build_value(columns, data):
    values = []
    for name in columns:
        v = data.get(name)
        if (isinstance(v, str) or isinstance(v, unicode)) and v.find("'") >= 0:
            v = v.replace("'", "\\'")
        if isinstance(v, datetime):
            v = v.strftime("%Y-%m-%d %H:%M:%S")
        values.append('\'{}\''.format(v))
    return '(' + ','.join(values) + ')'


def write_file(file_name, lines):
    f = open(file_name, 'w')
    for line in lines:
        f.write(line)
        f.write('\n')
    f.close()


def export(table_name):
    """
    导出sql文件数据
    :param table_name: 表名，表必须包含主键id列
    :return:
    """
    out = get_table_sql(table_name)
    for one in out:
        print one
    print 'insert sql count: {}'.format(len(out))
    file_name = '/tmp/' + table_name + '.sql'
    write_file(file_name, out)
    print 'file name: {}'.format(file_name)

def export_range(table_name, start_id, end_id, increment_id="id"):
    """
    导出sql文件数据
    :param table_name: 表名
    :param start_id: 开始id
    :param end_id: 结束id
    :param increment_id: 主键列名
    :return:
    """
    out = get_table_sql_range(table_name, start_id, end_id, increment_id)
    for one in out:
        print one
    print 'insert sql count: {}'.format(len(out))
    file_name = '/tmp/' + table_name + '.sql'
    write_file(file_name, out)
    print 'file name: {}'.format(file_name)


if __name__ == '__main__':
    table_name = 'test_zsc'
    export(table_name)
