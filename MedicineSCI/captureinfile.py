with open("C:\\Users\\xmu\\Desktop\\1999_2000.txt" , "r") as file_reader:
    first = file_reader.readline()
    lines = file_reader.readlines()

for line in lines:
    line = line.replace(';   ','').split('\t')
    with open("C:\\Users\\xmu\\Desktop\\1999-2000\\"+line[0]+".txt","w") as file_writer:
        file_writer.write((line[1])+line[2])

