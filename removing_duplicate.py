input_file = open('replaced_data.txt', 'r')
output_file = open('duplicate_removed_data.txt', 'w')

dictionary = {}
for line in input_file:
    di = line.split()
    dictionary[di[0], di[1]] = di[2]
input_file.close()

input_file = open('replaced_data.txt', 'r')
for line in input_file:
    row = line.split()
    if (row[0], row[1]) in dictionary and (row[1], row[0]) in dictionary:
        output_file.write("%s" % line)
        del (dictionary[row[0], row[1]])
        del (dictionary[row[1], row[0]])
    elif (row[0], row[1]) in dictionary:
        output_file.write("%s" % line)
        del (dictionary[row[0], row[1]])
input_file.close()
