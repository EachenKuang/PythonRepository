#-*- coding:utf-8 -*-
#读取d2017.bin 用于对创新度的计算，将数据存入数据库中。
#需要三个关键字 ENTRY(入口词)、MN(树形路径)、AN(注释)
#ENTRY每个都有、MN（XXX.XXX.XXX）可能有几个、AN有些没有
import Dao

dao = Dao.Dao()
dao.connect()

#col_name = ''
MH_value = ''
MN_value = ''
ENTRY_value = ''
AN_value =''
#names=''
values=''
count = 0
wrong = 0
with open("d2017.bin", "r") as readMesh:
    for line in readMesh:
        line = line.strip()
        if line == '':
            # 到了结尾
            # if AN_value == '':
            #     AN_value = 'null'
            values = "'" + MH_value + "','" + ENTRY_value + "','" + MN_value + "','" + AN_value +"'"
            sql = 'insert  MeshStructure ' + " (MH , EN , MN , AN) " + \
                  "values " + " ( " + values + " ); "
            try:
                dao.insert(sql)
                count += 1
                print count

            except:
                wrong += 1
                print(wrong, sql)

            MH_value = ''
            MN_value = ''
            ENTRY_value = ''
            AN_value = ''
            values = ''
        else:
            if line == "*NEWRECORD":
                continue
            newline = line.split(" = ")
            if newline[0] == "MH":
                # col_name = "MH"
                MH_value = newline[1]
            elif newline[0] == "ENTRY":
                # 需要处理有多个ENTRY的情况，多个ENTRY用分号分隔开
                # col_name = "ENTRY"
                ENTRY_line = newline[1].split('|')[0]
                ENTRY_value += ENTRY_line + ";"
            elif newline[0] == "MN":
                # 需要处理有多个MN的情况，多个MN用分号分隔开
                #col_name = "MN"
                MN_value += newline[1] + ";"
            elif newline[0] == "AN":
                #col_name = "AN"
                AN_value = newline[1]
            else:
                continue



#insert into Data("","") values("","")