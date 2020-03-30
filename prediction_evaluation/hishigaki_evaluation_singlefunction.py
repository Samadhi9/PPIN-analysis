import networkx as nx
from collections import defaultdict
from operator import itemgetter
from collections import OrderedDict
import numpy as np

import curve_plotter_single_function as cp

#import matplotlib.pyplot as plt

""" AUTHOR: PASAN FERNANDO

    This script predicts the score for each gene in the network for the given function
    Employs leave-one-out method for all the network genes
    Generates ROC, Precision-recall curves and some other metric curves
    """

############################################################################# ###########

# Check the name of the function here
func_name = 'root_development'


#methods for calculating evaluation metrics

def evaluation_metrics(p,n,tp,tn,fp,fn):

    # calculating the accuracy
    try:
        accuracy = (tp+tn)/float(p+n)
    except ZeroDivisionError:
        accuracy = 0
    #print 'Accuracy is:',accuracy

    #error rate
    try:
        error_rate = (fp+fn)/float(p+n)
    except ZeroDivisionError:
        error_rate = 0
    #print 'Error rate is:', error_rate

    #sensitivity/ same as recall
    try:
        sensitivity = tp/float(p)
    except ZeroDivisionError:
        sensitivity = 0
    #print 'sensitivity:', sensitivity

    #specificity1
    try:
        specificity = tn/float(n)
    except ZeroDivisionError:
        specificity = 0
    #print 'specificity:', specificity

    #precision
    try:
        precision = tp/float(tp+fp)
    except ZeroDivisionError:
        precision=0
    #print 'precision:', precision

    #true positive rate
    try:
        tpr = tp/float(p)
    except ZeroDivisionError:
        tpr=0

    # false positive rate
    try:
        fpr = fp/float(n)
    except ZeroDivisionError:
        fpr=0

    # false positive rate

    return accuracy,error_rate,sensitivity,specificity,precision,tpr,fpr


########################################################################################

# reading gene list for the given function

genelist = open('seedlist.txt', 'r')


# a list to store the genes
glist =[]

# reading the gene file
for line in genelist:
    if line != '\n':
        
        glist.append(line.strip().lower())  # convert to lower case and append to the list


#print glist
print 'Number of genes in the gene list:',len(glist)

### reading the network file########################################################
in1 = open('duplicate_removed_data.txt', 'r')
G = nx.Graph()
for line in in1:
    if line != '\n':
        #print line
        if 'combined_score' not in line:
            line = line.strip('\n')
            a = line.split()
            G.add_edge(a[0].lower(),a[1].lower(), weight = a[2])


######### calculate the function frequency or phi #########
# total proteins in the network
totps = nx.number_of_nodes(G)


genes_in_network = nx.nodes(G)
print 'Number of genes in the network:',len(genes_in_network)


print ('predicting the chi score for each network gene.....')

chigenes={}

for gene in genes_in_network:
    #print 'gene is:',gene

    #dictionaries to store total and function counts, chi square value
    total={}
    ccount={}
    chisq = {}

    #counting the genes with given function in immediate neighborhood of gene in consideration of leave one out method

    # going through the different functions in the function list

    genelist = glist

    # making sure the gene in question is removed from the gene list because we are assuming it does not have any function
    if gene in genelist:
        # removing the gene by list comprehension; otherwise it will mutate the original dictionary
        genelist = [x for x in genelist if x != gene]


    # making sure all the genes in the input data file are in the network

    notfound = set(genelist) - set(genes_in_network)  # genes that are not found in the network

    found = set(genelist) & set(genes_in_network)  # genes that are found in the network
    #print 'genes that are found in the network:', found


    funps = len(found)

    fracps = float(funps) / totps

    #print fracps

    # counting the genes with given function in immediate neighborhood of gene in consideration in leave one out method
    totalc =0 # initially, total count is zero
    ccountc=0 # initially, neighborhood count is zero
    
    # getting the neighbors
    nb = nx.all_neighbors(G, gene)

    for j in nb:
        #print j
        totalc=totalc+1 # counting the total neighbors; could have done this using len(j) as well
        if j in genelist: # if the neighbor is in the gene list that neghbor has the function
            ccountc=ccountc+1

    # storing the above calculated values in designated dictionaries
    total[func_name]=totalc
    ccount[func_name]=ccountc

    #calculate expected frequency values
    ef = fracps*totalc
    # calculating the chi-square value
    try: # this error handling is required to avoid zero division when ef=0
        chi = ((ccountc-ef)**2)/ef
    except ZeroDivisionError:
        chi = 0
    chisq[func_name] = chi


    chigenes[gene]=chisq
        
print 'genes that are not found in the network:', notfound
# ordering each dictionary based on the highest function

for i in chigenes:
    chigenes[i]= OrderedDict(sorted(chigenes[i].items(),key=lambda t:t[1], reverse=True))
    #print chigenes[i]

#print chigenes

# a list to store chivalues; used to get the maximum chi value
chivalues = []

############################################################################################
# writing the predicted gene functions in an output file in sorted order
out = open('predicted_functions.txt', 'wb+')
out.write('genes\tpredicted_functions\n')



for i in chigenes:
    out.write('%s\t'%(i))
    func_chi = chigenes[i]
    lastelement = list(func_chi.keys())
    #print lastelement[-1]
    for j in func_chi:
        #print j
        chivalues.append(float(func_chi[j]))# appending chi values
        if j == lastelement[-1]:# this avoids printing a comma after the last element
            out.write('%s:%s' % (j, func_chi[j]))
        else:
            out.write('%s:%s,'%(j,func_chi[j]))

    out.write('\n')
out.close()



###########################################################################################
# module to calculate FP,TP,TN, FN

# defining dictionaries to store evaluation metrics for each threshold value
accuhash ={}
errorhash ={}
sensehash ={}
specifichash ={}
precisionhash ={}

# one multi dictionary to store fpr and tpr for thresholods
# the key should be the threshold
rochash = defaultdict(list)

# another hash for prescision recall curve
precision_recall_hash = defaultdict(list)


# then, for the given function, we need to move through different threshold values
# numpy is used to iterate through float values like 0.5


print 'Maximum chi value score:',max(chivalues)

print 'Iterating through thresholds......'

for threshold in np.arange(0,(max(chivalues)+0.2),0.01):
    print 'the threshold is:',threshold
    #threshold use as the cutoff to draw the roc curve
    #threshold = 0

    # defining the variables
    pcountfinal =0
    ncountfinal =0
    tpcountfinal =0
    tncountfinal =0
    fpcountfinal =0
    fncountfinal =0

    # calculating the confusion matrix: tp,fp,tn,fn
    # Iterating through each gene in the network
    for i in chigenes:
        pred_functions =[] # list to store functions higher than the threshold
        genefunctions = chigenes[i]

        # if the gene is in seed list it is a actual positive
        if i in glist:
            pcountfinal = pcountfinal + 1
            # positive can be a true positive if it is predicted or false negative if else
            if float(genefunctions[func_name]) >= threshold: # if the score is higher than the threshold it is predicted
                tpcountfinal = tpcountfinal + 1

            # In this case, this would be a false negative not a false postive
            else:
                fncountfinal = fncountfinal + 1


        # if the gene is not in the seed list it is a actual negative
        else:
            ncountfinal = ncountfinal + 1
            # negative can be a true negative if it is not predicted or false positive otherwise
            if float(genefunctions[func_name]) >= threshold:
                # here, it is predicted as a positive but actually it is a negative
                fpcountfinal = fpcountfinal + 1

            else:
                tncountfinal = tncountfinal + 1


    # print 'P:', pcountfinal
    # print 'N:',ncountfinal
    # print 'TP:',tpcountfinal
    # print 'TN:',tncountfinal
    # print 'FP:',fpcountfinal
    # print 'FN:',fncountfinal

    # getting all the evaluation metrics including the tpr and fpr
    accuracy,error_rate,sensitivity,specificity,precision,tpr,fpr= evaluation_metrics(pcountfinal,ncountfinal,tpcountfinal,tncountfinal,fpcountfinal,fncountfinal)

    # storing metrics in defined dictionaries
    accuhash[threshold]=accuracy
    errorhash[threshold]=error_rate
    sensehash[threshold]=sensitivity
    specifichash[threshold]=specificity
    precisionhash[threshold]=precision

    rochash[threshold].append(fpr)
    rochash[threshold].append(tpr)

    precision_recall_hash[threshold].append(sensitivity)
    precision_recall_hash[threshold].append(precision)

# writing the curve values in a file
preciout = open(func_name + 'precision_hash.txt', 'wb+')
rocout = open(func_name + 'roc_hash.txt', 'wb+')

for i in rochash:
    a = rochash[i]
    rocout.write('%s\t%s\t%s\n' % (a[0], a[1], i))

for i in precision_recall_hash:
    a = precision_recall_hash[i]
    preciout.write('%s\t%s\t%s\n' % (a[0], a[1], i))

preciout.close()
rocout.close()

print 'Number of positives:',pcountfinal
print 'Number of negatives:',ncountfinal


cp.ROCplotter(rochash,func_name,'roc')

# plotting the precision-recall curve for given function
cp.ROCplotter(precision_recall_hash, func_name, 'precision_recall')
#print accuhash
cp.metric_plotter(accuhash,'Accuracy',func_name)
cp.metric_plotter(errorhash,'Error_rate',func_name)
cp.metric_plotter(sensehash,'Sensitivity',func_name)
cp.metric_plotter(specifichash,'Specificity',func_name)
cp.metric_plotter(precisionhash,'Precision',func_name)



