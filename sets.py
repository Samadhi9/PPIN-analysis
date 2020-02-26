seeds = open('gene.txt', 'r').readlines()
input_file = open('protein1.txt', 'r').readlines()
output_file = open('count_data1.txt', 'w')

seed = []
for line in seeds:
    seed.append(line.strip())
set1 = set(seed)
print(set1)


p = []
for line in input_file:
    p.append(line.strip())
set2 = set(p)
print(set2)


nf = (set1.intersection(set2))
print(nf)
output_file.write("%s\n" % nf)
nfu = len(set1.intersection(set2))
print(nfu)
