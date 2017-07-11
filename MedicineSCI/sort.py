# -*- encoding:utf-8 -*-

f1 = open('TFIDF.txt', 'r')
item_dict = {}
article_id = ''
for line in f1:
    if len(line.strip().split('\t')) == 1:
        article_id = line.strip().split('\\')[-1]
    else:
        frequency = float(line.split('\t')[-1])
        key = " ".join(line.split(' ')[0:-1])
        item_dict[article_id + ' ' + key] = frequency
f1.close()
# print item_dict
item_dict = sorted(item_dict.items(), key=lambda item: item[1])
# print item_dict
# print item_dict
f2 = open('TFIDF_sorted.txt', 'w')
for (key, value) in item_dict:
    f2.write(key+','+str(value)+'\n')
f2.close()