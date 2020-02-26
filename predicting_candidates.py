protein = open('protein_list.txt', 'r')
data = open('duplicate_removed_data.txt', 'r').readlines()
seeds = open('genes.txt', 'r').read()
output_file = open('prediction_score.txt', 'w')
output_file.write("protein prediction_score\n")

seed = []
for line in seeds:
    seed.append(line.strip())
#print(len(seed))

proteins = []
for line in protein:
    proteins.append(line.strip())
#print(len(proteins))
protein.close()

tot_f = len(seed)
tot_n = len(proteins)

protein = open('protein_list.txt', 'r')
for line in protein:
    row = line.split()
    if row[0] in seeds:
        continue

    else:
        count = 0
        count_nfu = 0
        for line1 in data:
            if row[0] in line1:
                count = count + 1

                row1 = line1.split()
                if row1[0] in seeds or row1[1] in seeds:
                    count_nfu = count_nfu + 1

    nu = count
    nfu = float(count_nfu)

    ef = (tot_f * nu) / float(tot_n)
    try:
        prediction_score = (nfu - ef) ** 2 / float(ef)
    except ZeroDivisionError:
        prediction_score = 0
    prediction_scores = str(prediction_score)
    #print(prediction_score)

    list1 = [row[0], prediction_scores]
    row1 = ' '.join(list1)
    output_file.write("%s\n" % row1)

