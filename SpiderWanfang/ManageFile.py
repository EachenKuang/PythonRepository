# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.9.27
# Goal: 文件管理
# Other:
# '''
import os

def zero_papernum():
    for i in range(1, 21):
        with open('data/'+str(i)+'/paper_num.txt','w') as write:
            write.write('0')
        print 'change' + 'data/'+str(i)+'/paper_num.txt'+'to 0'

def delete_csv(file):
    for i in range(1, 21):
        try:
            os.remove('data/'+str(i)+'/'+file)
            print 'os delete'+'data/'+str(i)+'/'+file
        except:
            print 'can\'t find' + 'data/' + str(i) + '/' + file
            continue


def main():
    zero_papernum()
    delete_csv('paper_num')

if __name__ == '__main__':
    main()
