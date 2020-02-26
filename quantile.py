import numpy as np
import matplotlib.pyplot as plt

input_file = open('node_degree_75.txt', 'r')
rows = input_file.readline()[0:]
list1 = []
for line in input_file:
    row = line.split()
    row[1] = int(row[1])
    list1.append(row[1])
array = np.array(list1)
percentile = np.quantile(array, 0.90)
print(percentile)
