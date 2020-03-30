import curve_plotter_single_function as cp
from collections import defaultdict

""" AUTHOR: PASAN FERNANDO

    Reads the dictionaries for ROC and PR curves and plots them
    """
# reading the dictionaries

def dictread(file_to_read, curve_type):

    # defining the multi dictionary
    multihash = defaultdict(list)
    for line in file_to_read:
        if line!='\n':
            split_el = line.strip().split('\t')
            multihash[split_el[2]].append(float(split_el[0]))
            multihash[split_el[2]].append(float(split_el[1]))

    cp.ROCplotter(multihash, 'root development', curve_type)

    return

# reading the file for ROC dictionary
rocdic = open('root_developmentroc_hash.txt', 'r')
dictread(rocdic,'roc')
rocdic.close()

# reading the file for PR dictionary
prdic = open('root_developmentprecision_hash.txt', 'r')
dictread(prdic,'precision_recall')
prdic.close()