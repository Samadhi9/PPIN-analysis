filtered = open('filtered_data.txt', 'r')
output_file = open('replaced_data.txt', 'w')

rows = filtered.readline()[0:]
output_file.write(rows)

names = open("4530.protein.info.v11.0.txt", 'r')
rows = names.readline()[0:]

dictionary = {}
for line in names:
    di = line.split()
    dictionary[di[0]] = di[1].lower()
names.close()

for line in filtered:
    row = line.split()
    row[0] = dictionary[row[0]]
    row[1] = dictionary[row[1]]
    row1 = ' '.join(row)
    output_file.write("%s\n" % row1)

output_file.close()
filtered.close()


