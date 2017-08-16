# -*- coding: utf-8 -*-
import Dao
import os
import re


def create_table():
    dao = Dao.Dao()
    dao.connect()
    sql = 'CREATE TABLE [dbo].[RawMedicine2](' \
            '[paperid][numeric](18, 0) IDENTITY(1, 1)NOT NULL, [PT][nvarchar](max)NULL,[AU][nvarchar](max)NULL,' \
            '[AF][nvarchar](max)NULL, [TI][nvarchar](max)NULL, [SO][nvarchar](max)NULL, [LA][nvarchar](max)NULL,' \
            '[DT][nvarchar](max)NULL, [DE][nvarchar](max)NULL,[ID][nvarchar](max)NULL, [AB][nvarchar](max)NULL,' \
            '[C1][nvarchar](max)NULL,[RP][nvarchar](max)NULL,[EM][nvarchar](max)NULL, [FU][nvarchar](max)NULL,' \
            '[FX][nvarchar](max)NULL,[CR][nvarchar](max)NULL,[NR][nvarchar](max)NULL, [TC][nvarchar](max)NULL,' \
            '[Z9][nvarchar](max)NULL,[U1][nvarchar](max)NULL,[U2][nvarchar](max)NULL, [PU][nvarchar](max)NULL,' \
            '[PI][nvarchar](max)NULL, [PA][nvarchar](max)NULL,[SN][nvarchar](max)NULL, [J9][nvarchar](max)NULL,' \
            '[JI][nvarchar](max)NULL, [PD][nvarchar](max)NULL,[PY][nvarchar](max)NULL, [VL][nvarchar](max)NULL,' \
            '[AR][nvarchar](max)NULL, [DI][nvarchar](max)NULL,[PG][nvarchar](max)NULL, [WC][nvarchar](max)NULL,' \
            '[EI][nvarchar](max)NULL,[IMPIS][nvarchar](max)NULL,[BP][nvarchar](max)NULL,[OI][nvarchar](max)NULL,' \
            '[EP][nvarchar](max)NULL,[RI][nvarchar](max)NULL,[CT][nvarchar](max)NULL,[CY][nvarchar](max)NULL,' \
            '[CL][nvarchar](max)NULL,[SP][nvarchar](max)NULL,[BE][nvarchar](max)NULL,[SE][nvarchar](max)NULL,' \
            '[BN][nvarchar](max)NULL,[SU][nvarchar](max)NULL,[SI][nvarchar](max)NULL, [PN][nvarchar](max)NULL,' \
            '[HO][nvarchar](max)NULL, [CA][nvarchar](max)NULL,' \
            '[SC][nvarchar](max)NULL, [GA][nvarchar](max)NULL,[UT][nvarchar](max)NULL, [PM][nvarchar](max)NULL,'\
            '[OA][nvarchar](max)NULL,[DA][nvarchar](max)NULL' \
          ')'

    dao.create(sql)
    dao.close()


def read_file(filename):
    dao = Dao.Dao()
    dao.connect()

    col_name = ''
    value = ''
    names = ''
    values = ''
    with open(filename, 'r') as file_reader:
        lines = file_reader.readlines()
        for i in lines[2:-1]:
            i = i.replace("'", "''")
            if i == '\n':
                pass
            if i == "ER\n":
                # ER标志一篇论文信息结束
                names += col_name
                if len(value.split(';')) == 2:
                    value = value.replace(';', '')
                values += value + "'"
                sql = 'insert into RawMedicine2 ' + " ( " + names + " ) " + \
                      "values " + " ( " + values.replace(';;', ';') + " ); "
                print(sql)

                dao.insert(sql)

                col_name = ''
                names = ''
                values = ''
            else:
                temp = i.split(' ')
                if temp[0] == "MA" or temp[0] == "D2" or temp[0] == "BA" or temp[0] == "BF"\
                        or temp[0] == "GP":
                    continue
                if not temp[0] == '' and not temp[0] == '\n' and not temp[0] == '\r':
                    if not col_name == '':
                        names += col_name + ","
                        if len(value.split(';')) == 2:
                            value = value.replace(';', '')
                        values += value + "',"
                    col_name = temp[0]
                    col_name = col_name.replace('IS', 'IMPIS')
                    value = "'"
                    value += i.replace(col_name, '').replace('\n', ';')
                else:
                    value += i.replace('\n', ';')


def find_files():
    # folder 为文件夹路径
    folder = 'C:\\Users\\xmu\\Desktop\\medicine\\'
    filename_list = []
    lists = sort_strings_with_embedded_numbers(os.listdir(folder))

    for filename in lists:
        filename_list.append(folder + filename)
    return filename_list


def embedded_numbers(s):
    re_digits = re.compile(r'(\d+)')
    pieces = re_digits.split(s)               # 切成数字与非数字
    pieces[1::2] = map(int, pieces[1::2])     # 将数字部分转成整数
    return pieces


def sort_strings_with_embedded_numbers(alist):
    return sorted(alist, key=embedded_numbers)


# def write_into_file():
#       dao = Dao.Dao()
#       dao.connect()
#       sql = "select paperid, TI from DATA1 where TI != 'None' order by paperid"
#       rs = dao.select(sql)

#       for row in rs:
#             with open("input_ti\\ti_" + str(row[0]) + ".txt", 'w', encoding='utf-8') as file_writer:
#                   file_writer.write(row[1] + "\n")


# 遍历所有文件名
files = find_files()
# 创建表格
#create_table()
# 遍历文件, 插入数据
for f in files:
    print(f)
    read_file(f)

# write_into_file()




