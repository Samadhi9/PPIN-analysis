input_file = open('replaced_data.txt', 'r')
rows = input_file.readline()[0:]
output_file = open('protein_list1.txt', 'w')

for line in input_file:
    row = line.split()
    i = row[0:2]
    row1 = ' '.join(i)
    output_file.write("%s " % row1)

input_file1 = open('protein_list1.txt', 'r')
output_file1 = open('protein_list.txt', 'w')

for line in input_file1:
    row = line.split()
    li = list(dict.fromkeys(row))
    row1 = '\n'.join(li)
    output_file1.write("%s" % row1)




