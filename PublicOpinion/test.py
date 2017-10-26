# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.10.20
# Goal: 测试
# Other:
# '''
import csv
csvfile = file("out/out2017-10-25.15-33-05.727000.csv", 'rb')
reader = csv.reader(csvfile)

for line in reader:
    print ','.join(line)