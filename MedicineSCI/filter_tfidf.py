# -*- encoding:utf-8 -*-

f1 = open('TFIDF.txt', 'r')
word_list = []
temp_words_list = []
temp_words_num = 0
for line in f1:
    if len(line.strip().split('\t')) == 1:
        word_list += temp_words_list[:temp_words_num/5]
        temp_words_list = []
        temp_words_num = 0
        continue
    else:
        temp_words_num += 1
        frequency = float(line.split('\t')[-1])
        key = " ".join(line.split('\t')[0:-1])
        temp_words_list.append(key)
f1.close()
new_list = list(set(word_list))
f2 = open('TFIDF_filtered.txt', 'w')
for w in new_list:
    f2.write(w+'\n')
f2.close()