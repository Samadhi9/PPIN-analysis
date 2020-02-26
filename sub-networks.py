input_file = open('duplicate_removed_data.txt', 'r')
output_file = open('4004_in_sub_network75.txt', 'w')

rows = input_file.readline()[0:]
output_file.write(rows)

seeds = open('gene.txt', 'r')
#contents = seeds.read()

# defining a list named contents
contents =[]

for gene in seeds:
    gene1 = gene.strip().lower()
    contents.append(gene1)
#print(contents)
seeds.close()

for line in input_file:
    row = line.split()
    if row[0] in contents and row[1] in contents:
        output_file.write("%s" % line)

output_file.close()
input_file.close()





