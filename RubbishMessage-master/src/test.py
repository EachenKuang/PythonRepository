
import random
random.randint(1,2)
with open('../data/evaluation_public.tsv','r')as fr, open('../data/out_test.csv', 'w') as fw:
    for line in fr:
        line = line.strip()
        line = line.split('\t')
        if random.randint(1, 3) == 2:
            fw.write(line[0] + ',' + 'POSITIVE'+'\n')
        else:
            fw.write(line[0] + ',' + 'NEGATIVE' + '\n')