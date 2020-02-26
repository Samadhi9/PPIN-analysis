input_file = open('4530.protein.links.v11.0.txt', 'r')
output_file = open('filtered_data.txt', 'w')

rows = input_file.readline()[0:]
output_file.write(rows)

for line in input_file:
    row = line.split()
    row[2] = int(row[2])
    if row[2] > 400:
        output_file.write("%s" % line)

output_file.close()
input_file.close()





