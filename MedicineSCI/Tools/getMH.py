from gensim import models

with open("D:\\Kuangyichen\\PythonRepository\\MedicineSCI\\d2017.bin", "r") as readMH:
    w =open('C:\\Users\\xmu\\Desktop\\MH.txt','w')
    MH_List = []
    cor1 = set()
    for line in readMH:
        term = str(line).strip().split(" = ")
        if term[0] == "MH":
            cor1.add(term[1])
            MH_List.append(term[1])
            w.write(term[1]+'\n')
readMH.close()
print(MH_List)
print("------------------------------------------------")
#---------------------------------------------------------------
lda1 = models.LdaModel.load('D:/Kuangyichen/PythonRepository/Test/temp/_2004-2005lda_moedel')
show = lda1.show_topics(num_words=400,formatted=False)
dict_show = dict(show)
#dict_show[i]
list = []
cor2 = set()
for i in dict(dict_show[1]).iterkeys():
    list.append(str(i).split(' [')[0])
    cor2.add(str(i).split(' [')[0])
    print i

#----------------------------------------------------------------
# path = 'D:\\Kuangyichen\\PythonRepository\\Test\\item_list.txt'
# path = "D:\\Kuangyichen\\JavaRepository\\LDAGibbsSampling-master\\data\\LdaResults\\termList.txt"
# with open(path,"r") as readWord:
#     Word_List = []
#     cor2 = set()
#     for line in readWord:
#         term = str(line).split()[0]
#         cor2.add(term)
#         Word_List.append(term)
# print(Word_List)
# print("------------------------------------------------")
cor3 = cor1 & cor2
print(cor3)
with open("C:\\Users\\xmu\\Desktop\\test2.txt","w") as write:
    for word in cor3:
        write.write(word+"\n")

