# -*- coding:utf-8 -*-
# ！usr/bin/python2.7

import math
import operator
from MedicineSCI.InterfaceSQL import MSSQL
# python3 之后 reduce不在内建的函数中的，需要用以下语句来import
#from functools import reduce

# 余弦相似度的计算,传入的参数为向量a,b
def sim(a,b):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for x, y in zip(a, b):
        dot_product+=x*y
        normA += x**2
        normB += y**2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product/((normA*normB)**0.5)

# 取集合的并集，用于计算总的集合
def buildlex(corpus):
    lexicon = set()
    for doc in corpus:
        lexicon=lexicon| set(doc)
    return list(lexicon)

# 得到简化的词向量（实质上与总的向量计算是一致的。）
def buildVec(vocabList,inputword):
    returnVec = [0]*len(vocabList)
    for word in inputword:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:
            pass
    return returnVec

#入口词的相似度
#参数 t1 主题1的 词列表 t2 主题2的 词列表 dic 对照表
def S_infor(t1,t2,dic):
    lis=[]
    for x in t1:
        for y in t2:
            if len(dic[x])>0:
                Xdic = dic[x]
            else:
                Xdic = [x]
            if len(dic[y])>0:
                Ydic = dic[y]
            else:
                Ydic = [y]
            # Xdic=dic[x]
            # Ydic=dic[y]
            p1 = [i.split(';') for i in Xdic]
            q1 = []
            for i in p1:
                if i != '':
                    q1.extend(i)
            p2 = [i.split(';') for i in Ydic]
            q2 = []
            for i in p2:
                if i != '':
                    q2.extend(i)
            cor=[q1,q2]
            # cor=[Xdic,Ydic]
            vo = buildlex(cor)
            v1 = buildVec(vo,cor[0])
            v2 = buildVec(vo,cor[1])
            p = sim(v1,v2)
            # print cor,v1,v2,p
            # print cor
            if p != None:
                lis.append(p)
    return sum(lis)/len(lis)

#注释的相似度
#参数 t1 主题1的 词列表 t2 主题2的 词列表 dic 对照表
def S_annotation(t1,t2,dic):
    lis=[]
    for x in t1:
        for y in t2:
            if len(dic[x])>0:
                Xdic = dic[x]
            else:
                Xdic = [x]
            if len(dic[y])>0:
                Ydic = dic[y]
            else:
                Ydic = [y]
            # Xdic=dic[x]
            # Ydic=dic[y]
            p1 = [i.split() for i in Xdic]
            q1 = []
            for i in p1:
                if i != '':
                    q1.extend(i)
            p2 = [i.split() for i in Ydic]
            q2 = []
            for i in p2:
                if i != '':
                    q2.extend(i)
            cor=[q1,q2]
            # cor=[Xdic,Ydic]
            vo = buildlex(cor)
            v1 = buildVec(vo,cor[0])
            v2 = buildVec(vo,cor[1])
            p = sim(v1,v2)
            #print cor,v1,v2,p
            # print "p1----------------"
            # print p1
            # print "p2----------------"
            # print p2
            # print "cor----------------"
            # print cor
            if p != None:
                lis.append(p)
    return sum(lis)/len(lis)


#主题间的语义距离
#传入的参数S1，S2为MN字段
def mn_depth(s1,s2):
    #防止出现MN为空的情况
    if s1 == '' or s2 == '':
        return 0
    if s1[0]==s2[0]:
        s1=s1.split('.')
        s2=s2.split('.')
        if len(s1)>len(s2):
            s2+=[0]*(len(s1)-len(s2))
        elif len(s1)<len(s2):
            s1+=[0]*(len(s2)-len(s1))
        i=zip(s1,s2)
        dd=[]
        for j in zip(s1,s2):
            if j[0]==j[1]:
                dd.append(j)
            elif j[0]!=j[1]:
                break
        if len(dd)>1:
            x=float(2*(len(dd)+2))
            sim=x/(len(s1)+len(s2)-len(dd)+x-s1.count(0)-s2.count(0))
            return sim
        elif len(dd)==1 and len(dd[0])>1:
            x=4.0
            sim=x/(len(s1)+len(s2)-2+x-s1.count(0)-s2.count(0))
            return sim
        elif len(dd)==1 and len(dd[0])==1:
            x=2.0
            sim=x/(len(s1)+len(s2)+x-s1.count(0)-s2.count(0))
            return sim
        elif len(dd)<1:
            x=4.0
            sim=x/(len(s1)+len(s2)+x-s1.count(0)-s2.count(0))
            return sim
    else:
        s1 = s1.split('.')
        s2 = s2.split('.')
        sim = 2.0/(len(s1)+len(s2)+4-s1.count(0)-s2.count(0))
        return sim

#主题词距离相似度，传入参数为主题t1与主题t2的词，dic为词对应MN的字段
def S_depth(t1, t2, dic):
    lis = []
    for x in t1:
        for y in t2:
            if len(dic[x]) > 0:
                Xdic = dic[x]
            else:
                Xdic = [x]
            if len(dic[y]) > 0:
                Ydic = dic[y]
            else:
                Ydic = [y]
            # Xdic=dic[x]
            # Ydic=dic[y]
            p1 = [i.split(';') for i in Xdic]
            q1 = []
            for i in p1:
                if i != '':
                    q1.extend(i)
            p2 = [i.split(';') for i in Ydic]
            q2 = []
            for i in p2:
                if i != '':
                    q2.extend(i)
            mn_d = 0.0
            for m in q1:
                for n in q2:
                    mn_d += mn_depth(m,n)
            mn_d /= (q1.__len__()*q2.__len__())

            if mn_d != None:
                lis.append(mn_d)
    return sum(lis) / len(lis)



#######################################################################
#KL距离 暂时不用考虑
def kl(p, q):
    return reduce(operator.add, map(lambda x, y: x*math.log(x/y), p, q))

def result(a,b):
    r1=abs(kl(a,b))
    r2=abs(kl(b,a))
    return (r1+r2)/2.0
#######################################################################

def inno(t1,t2,dic_MN,dic_AN,dic_EN):
    D = S_depth(t1, t2, dic_MN)
    A = S_annotation(t1, t2, dic_AN)
    I = S_infor(t1, t2, dic_EN)
    print "深度" + str(D), "注释" + str(A), "入口词" + str(I)
    S = 0.5 * I + 0.3 * D + 0.2 * A
    print S
    return S
########################################################################

# print  S_depth('J1.637.847.500','L01.143.230') #全部不同
# print  S_depth('J01.637.847.500','J01.143.230.500') #一个相同
# print  S_depth('J01.637.847.500','J01.637.230.500') #两个
# print  S_depth('J01.637.847.500','J01.637.847.400') #三个
# print  S_depth('J01.637.847.500','J01.637.847.500') #四个

#主题中的词选择20个
#######################################################################

#将数据库中数据放入dic中
def main():

    #用于存放MH-EN，MN，AN的字典
    dic_EN = {}
    dic_MN = {}
    dic_AN = {}

    #用于测试、真实数据
    t = []

    topic1 = ['Occupational Exposure', 'Viremia', 'Radiology', 'Magnetic Resonance Angiography', 'Epithelium',
              'Science', 'Biliary Fistula', 'Environment', 'Microdissection', 'Safety', 'Maintenance', 'Body Weight',
              'Acupuncture', 'Hepatitis B, Chronic', 'Transfection', 'Chromosomes', 'Risk Assessment',
              'Genetic Engineering', 'Attention', 'Intraabdominal Infections', 'Microbubbles', 'Anatomy',
              'Histiocytosis, Langerhans-Cell', 'Goals', 'Light', 'Hormone Replacement Therapy', 'Blood Coagulation',
              'Mice', 'Pacific Islands', 'Retrospective Studies', 'Biomarkers', 'DNA Damage', 'Multicenter Study',
              'Virology', 'Adrenal Cortex', 'Relaxation', 'Alaska', 'X Chromosome', 'Dilatation', 'Solvents',
              'Capsules', 'General Practice', 'Drinking', 'Digestion', 'End Stage Liver Disease', 'Addresses',
              'Prospective Studies', 'Sex Workers', 'Epidemiologic Studies', 'Cholangiocarcinoma', 'Patient Care',
              'Histology', 'Water Pollution', 'Age Distribution', 'Cholangiography']
    topic2 = ['Acceleration', 'Controlled Clinical Trial', 'Mediterranean Region', 'Rats, Wistar', 'Liver Regeneration',
              'Seoul', 'HIV', 'Control Groups', 'Alcoholics', 'Mutagens', 'Gastric Mucosa', 'Patients', 'Art',
              'Methods', 'Electrodes', 'Steroids', 'RNA', 'Parasites', 'Enzyme-Linked Immunosorbent Assay',
              'Liver Diseases', 'Schistosomiasis', 'Porphyrias, Hepatic']
    topic3 = ['Medical Records', 'Awareness', 'Arteries', 'Biochemistry', 'Cholestasis', 'Radiation', 'Hormones',
              'Policy', 'Hope', 'Elements', 'Apoptosis', 'Endoplasmic Reticulum', 'Oxidative Stress', 'Blood',
              'Hepatocytes', 'Gene Expression', 'Cells', 'Work', 'GB virus C', 'Compliance', 'Animals',
              'Immune Tolerance', 'DNA Mismatch Repair', 'Hawaii', 'Laparotomy', 'Liposomes', 'Water Quality',
              'Endothelial Cells', 'Terminology', 'Chemoprevention', 'Lipid Peroxidation',
              'Elective Surgical Procedures', 'Hypertension, Portal', 'Rats', 'Gap Junctions', 'Family', 'Hemodynamics',
              'Rats, Sprague-Dawley', 'Linkage Disequilibrium', 'Lysosomes', 'Densitometry', 'Pathology']
    topic4 = ['Mallory Bodies', 'Genes', 'Dialysis', 'Loss of Heterozygosity', 'Schistosoma japonicum', 'Cell Cycle',
              'Mutation', 'Comparative Genomic Hybridization', 'Metabolism', 'Gastrointestinal Neoplasms',
              'Comet Assay', 'Transplant Recipients', 'Extracellular Matrix', 'Existentialism', 'Signal Transduction',
              'Diet', 'Allelic Imbalance', 'Alcohol Drinking', 'Brachytherapy', 'Cooking', 'Comparative Study',
              'Neuroendocrine Tumors', 'Methylation', 'Carcinogenesis', 'Mitochondria', 'Kinetics', 'Literature',
              'Nucleotides', 'Aflatoxins', 'Oncogenes', 'Adenomatous Polyposis Coli', 'Alleles',
              'Kaplan-Meier Estimate', 'Codon', 'Rest', 'Archives', 'Culture', 'Antibiotic Prophylaxis',
              'Iron Overload', 'Protective Factors', 'Environmental Exposure', 'Geographic Locations']
    topic5 = ['Schistosoma', 'Qualitative Research', 'Genotype', 'Survivors', 'Pedigree',
              'Cholangiopancreatography, Magnetic Resonance', 'Students', 'Angiomyolipoma', 'Common Bile Duct',
              'Flaviviridae', 'Platelet Count', 'Outpatients', 'Cell Membrane', 'Drive', 'Peptides', 'Seroconversion',
              'Coinfection', 'Hepatitis C', 'Health Resources', 'Phlebotomy', 'Follow-Up Studies', 'Tattooing',
              'Viral Load', 'Confidence Intervals', 'Immunization Programs', 'Odds Ratio', 'Attitude', 'Graft Survival',
              'Skin', 'Geography']
    topic6 = ['Africa, Northern', 'Hemangioendothelioma', 'Men', 'Copyright', 'Africa', 'Public Health',
              'Chemical Industry', 'Morphogenesis', 'Charts', 'Gases', 'Death Certificates', 'Health', 'Genome',
              'Motor Vehicles', 'Immune System', 'Interview', 'Veterans', 'Exercise', 'Europe',
              'Liver Cirrhosis, Experimental', 'Coffee', 'Siderosis', 'Persons', 'Food', 'Beverages', 'Lakes',
              'Telomere', 'Epidemiology', 'Cholangitis, Sclerosing', 'Contraceptives, Oral', 'Serum Albumin',
              'Developing Countries', 'Association', 'Diffusion', 'Deamination', 'Watchful Waiting', 'Gestational Age',
              'Swine', 'Smoke', 'Accounting', 'Hepatic Insufficiency', 'History', 'Asia, Western', 'Plastics', 'Aged',
              'Central America', 'Cytoplasm', 'Tissues', 'Humans', 'Sex', 'Paper', 'Case Reports', 'Education']
    topic7 = ['Postoperative Complications', 'Hepatectomy', 'Mitotic Index', 'Adenocarcinoma, Papillary',
              'Telomere Shortening', 'Patient Selection', 'Cystic Duct', 'American Cancer Society', 'Mortality',
              'Disease-Free Survival', 'Cell Differentiation', 'Postoperative Period', 'Life Expectancy', 'Morbidity',
              'Chronic Disease', 'Sound', 'Lithiasis', 'Regression Analysis', 'DNA, Viral', 'Pathologists',
              'General Practitioners', 'Rupture', 'Chromosome Aberrations', 'Chronology']
    topic8 = ['Pharmacoepidemiology', 'Parity', 'Dairy Products', 'Microvilli', 'Cystadenoma', 'Cell Proliferation',
              'Carcinogens, Environmental', 'Asia', 'Research', 'Laparoscopy', 'Porphyrias', 'Habits',
              'Chromosomes, Human', 'Gastroenterology', 'Clonal Evolution', 'Hospital Mortality', 'Risk Factors',
              'Probability']
    topic9 = ['Meta-Analysis', 'Syndrome', 'Serology', 'Artifacts', 'Early Diagnosis', 'Paint', 'Phenotype',
              'Thoracic Surgery', 'Hepatitis Viruses', 'Gastroenterologists', 'Life', 'Palliative Care',
              'Operative Time', 'Ligation', 'Survival', 'Alcoholic Beverages', 'Treatment Outcome', 'Survival Analysis',
              'Clinical Decision-Making', 'Tokyo', 'Uncertainty', 'Heating', 'Transplantation', 'Pathology, Clinical',
              'Inpatients', 'Survival Rate', 'Population Surveillance', 'Longevity', 'Natural History',
              'Liver Transplantation', 'Clonal Deletion', 'Employment', 'Ultrasonography']
    topic10 = ['Genetics', 'Knowledge', 'Microcirculation', 'DNA Repair', 'Diagnosis, Differential',
               'Immunohistochemistry', 'Pathology, Surgical', 'Contracts', 'Cell Communication', 'Efficiency',
               'Catheterization', 'Colectomy', 'Affect', 'Bile Reflux', 'Mass Screening', 'MEDLINE',
               'Diagnostic Imaging', 'Programs', 'Chromatin', 'Radioimmunoassay', 'Cohort Effect', 'Classification',
               'Focal Nodular Hyperplasia', 'Macroglossia', 'Sepsis', 'Lipid Droplets', 'Sex Ratio', 'Touch',
               'Technology', 'Cytogenetic Analysis', 'Bile Ducts, Extrahepatic']

    t.append(topic1)
    t.append(topic2)
    t.append(topic3)
    t.append(topic4)
    t.append(topic5)
    t.append(topic6)
    t.append(topic7)
    t.append(topic8)
    t.append(topic9)
    t.append(topic10)


    ms = MSSQL(host="localhost:59318", user="eachen", pwd="123456", db="mydata")
    resultList = ms.ExecQuery("SELECT MH,EN,MN,AN FROM MeshStructure")

    for (MH,EN,MN,AN) in resultList:
        dic_EN[MH] = EN
        dic_MN[MH] = MN
        dic_AN[MH] = AN
    out = [[] for i in range(10)]
    for i in range(0, 10):
        for j in range(0, 10):
            print "topic"+str(i)+" and topic "+str(j)
            s = inno(t[i], t[j], dic_MN, dic_AN, dic_EN)
            if i == j:
                s = 1
            out[i].append(s)
    for i in range(10):
       print str(out[i])+"\n"


if __name__ == '__main__':
    main()