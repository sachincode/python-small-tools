# -*- coding: utf-8 -*-

"""

Usage:
  main generate <config_file>
  main (-h | --help)
  main --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
# 根据数据表创建语句生成java对象类
# 在数据库 show create table table_name;
# 复制创建表语句并保存进文本文件， 如：
#
# CREATE TABLE `tbl_test` (
#  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
#  `accept_order` int(11) NOT NULL DEFAULT '0' COMMENT '接受订单数',
#  `reject_order` int(11) NOT NULL DEFAULT '0' COMMENT '拒绝订单数',
#  `occur_date` date NOT NULL DEFAULT '1990-01-01' COMMENT '发生日期',
#  PRIMARY KEY (`id`),
#  KEY `idx_occur_date` (`occur_date`)
# ) ENGINE=InnoDB AUTO_INCREMENT=433 DEFAULT CHARSET=utf8mb4 COMMENT='扣款前请求阶段拒绝统计表'
#
# 然后执行本脚本，如：
# python -m java.model generate /home/shichengzhang/test.txt
# 或
# python model.py generate /home/shichengzhang/test.txt
#
# 将生成如下java类:
# import java.util.Date;
#
# public class TblTest {
#     /** 主键 **/
#     private Long id;
#     /** 接受订单数 **/
#     private Integer acceptOrder;
#     /** 拒绝订单数 **/
#     private Integer rejectOrder;
#     /** 发生日期 **/
#     private Date occurDate;
# }
from docopt import docopt


java_import = {
    'timestamp': 'import java.util.Date;',
    'datetime': 'import java.util.Date;',
    'date': 'import java.util.Date;',
}

number_types = {'int', 'bigint', 'tinyint'}


def get_upper_camel_case(param):
    """将user_id格式的参数生成大写驼峰命名格式
    :param param: 如user_id
    :return: 如UserId
    """
    parts = param.split('_')
    for i in range(0, len(parts)):
        parts[i] = parts[i].capitalize()
    return ''.join(parts)


def get_lower_camel_case(param):
    """将user_id格式的参数生成小写驼峰命名格式
    :param param: 如user_id
    :return: 如userId
    """
    parts = param.split('_')
    if len(parts) == 1:
        return param
    for i in range(1, len(parts)):
        parts[i] = parts[i].capitalize()
    return ''.join(parts)


def read_create_table_sql(sql_filename):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    result = []
    start = False
    for line in lines:
        line = line.strip()
        if line.startswith("CREATE TABLE"):
            start = True
        if not start or not line:
            continue
        result.append(line)
    return result


def write_to_java_file(java_file_name, java_codes):
    f = open(java_file_name, 'w')
    for line in java_codes:
        f.write(line + '\n')
    f.close()


def generate_from_sql(sql_filename):
    java_codes = ['']
    lines = read_create_table_sql(sql_filename)
    class_name = get_upper_camel_case(lines[0].split(' ')[2].replace('`', ''))
    head = 'public class {} '.format(class_name) + '{'
    java_codes.append(head)
    date_type = False
    decimal_type = False
    lines = lines[1:-1]
    for line in lines:
        if line.startswith('PRIMARY KEY') or line.startswith('UNIQUE KEY') or line.startswith('KEY'):
            continue
        parts = line.split(' ')
        for i in range(1, len(parts)):
            parts[i] = parts[i].lower()
        if 'comment' in parts:
            index = parts.index('comment')
            tmp = ''.join(parts[index+1:]).strip()
            java_codes.append('    /** {} **/'.format(tmp[1:-2]))
        prop_name = get_lower_camel_case(parts[0].replace('`', ''))
        prop_type = parts[1].split('(')[0]
        if prop_type == 'bigint':
            java_codes.append('    private Long {};'.format(prop_name))
        elif prop_type in {'tinyint', 'smallint', 'mediumint'}:
            java_codes.append('    private Integer {};'.format(prop_name))
        elif prop_type == 'int':
            if 'unsigned' in parts:
                java_codes.append('    private Long {};'.format(prop_name))
            else:
                java_codes.append('    private Integer {};'.format(prop_name))
        elif prop_type in {'varchar', 'char', 'text', 'varbinary', 'blob'}:
            java_codes.append('    private String {};'.format(prop_name))
        elif prop_type in {'timestamp', 'datetime', 'date'}:
            date_type = True
            java_codes.append('    private Date {};'.format(prop_name))
        elif prop_type == 'decimal':
            decimal_type = True
            java_codes.append('    private BigDecimal {};'.format(prop_name))
    java_codes.append('}')
    if date_type:
        java_codes.insert(0, 'import java.util.Date;')
    if decimal_type:
        java_codes.insert(0, 'import java.math.BigDecimal;')
    for code in java_codes:
        print code
    java_file_name = '/tmp/{}.java'.format(class_name)
    write_to_java_file(java_file_name, java_codes)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0')
    if arguments['generate']:
        file_name = arguments['<config_file>']
        print(file_name)
        generate_from_sql(file_name)
