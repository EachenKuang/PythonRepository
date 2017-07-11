#-*- coding:utf-8 -*-
import Dao
import os


def create_table():

      dao = Dao.Dao()
      dao.connect()
      sql = 'CREATE TABLE [dbo].[DATA2] (' \
            '[paperid][numeric](18, 0) IDENTITY(1, 1)NOT NULL, [PN][nvarchar](max)NULL,[SU][nvarchar](max)NULL,' \
            '[BE][nvarchar](max)NULL, [BN][nvarchar](max)NULL,[D2][nvarchar](max)NULL,' \
            '[U1][nvarchar](max)NULL, [U2][nvarchar](max)NULL,[PM][nvarchar](max)NULL, [MA][nvarchar](max)NULL,' \
            '[AU][nvarchar](max)NULL,[AF][nvarchar](max)NULL,[CA][nvarchar](max)NULL, [SI][nvarchar](max)NULL,' \
            '[SO][nvarchar](max)NULL,[DT][nvarchar](max)NULL,[DE][nvarchar](max)NULL, [CY][nvarchar](max)NULL,' \
            '[CL][nvarchar](max)NULL,[ID][nvarchar](max)NULL,[C1][nvarchar](max)NULL, [EM][nvarchar](max)NULL,' \
            '[OI][nvarchar](max)NULL, [CR][nvarchar](max)NULL,[TC][nvarchar](max)NULL, [Z9][nvarchar](max)NULL,' \
            '[PU][nvarchar](max)NULL, [PI][nvarchar](max)NULL,[PA][nvarchar](max)NULL, [JI][nvarchar](max)NULL,' \
            '[VL][nvarchar](max)NULL, [EP][nvarchar](max)NULL,[DI][nvarchar](max)NULL, [WC][nvarchar](max)NULL,' \
            '[SC][nvarchar](max)NULL, [UT][nvarchar](max)NULL,[PT][nvarchar](max)NULL, [GP][nvarchar](max)NULL,' \
            '[TI][nvarchar](max)NULL, [SE][nvarchar](max)NULL,[LA][nvarchar](max)NULL, [CT][nvarchar](max)NULL,' \
            '[SP][nvarchar](max)NULL, [HO][nvarchar](max)NULL,[AB][nvarchar](max)NULL, [RP][nvarchar](max)NULL,' \
            '[RI][nvarchar](max)NULL, [FU][nvarchar](max)NULL,[FX][nvarchar](max)NULL, [NR][nvarchar](max)NULL,' \
            '[SN][nvarchar](max)NULL, [J9][nvarchar](max)NULL,[PD][nvarchar](max)NULL, [PY][nvarchar](max)NULL,' \
            '[IMPIS][nvarchar](max)NULL, [BP][nvarchar](max)NULL, [PG][nvarchar](max)NULL, [GA][nvarchar](max)NULL, ' \
            '[AR][nvarchar](max)NULL, [EI][nvarchar](max)NULL, [BATCH][numeric](18, 0)NULL, [SID][numeric](18, 0)NULL)'

      dao.create(sql)
      dao.close()


def read_file(filename):
      dao = Dao.Dao()
      dao.connect()

      col_name = ''
      value = ''
      names=''
      values=''
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
                        sql = 'insert DATA2 ' + " ( " + names + " ) " + \
                              "values " + " ( " + values.replace(';;', ';') + " ); "
                        # print(sql)
                        try:
                              dao.insert(sql)
                        except:
                              print(sql)

                        col_name = ''
                        names = ''
                        values = ''
                  else:
                        temp = i.split(' ')
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
      folder = 'C:\\Users\\xmu\\Desktop\\1\\'
      filename_list = []
      for filename in os.listdir(r'C:\Users\xmu\Desktop\1'):
            filename_list.append(folder + filename)
      return filename_list


# 遍历所有文件名
files = find_files()
# 创建表格
#create_table()
# 遍历文件, 插入数据
for f in files:
      print(f)
      read_file(f)






