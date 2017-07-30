import numpy as np
import pickle as pk
import sys

camp = sys.argv[1]

with open('./train/weight_lr_'+camp+'.pk', 'rb') as fp:
    weight = pk.load(fp)

def sigmoid(x):
    return 1/(1+np.exp(-x))

pctr = []
with open('./train/feature_'+camp+'.txt') as fp:
    for f in fp:
        a = list(map(int, f.strip('\n').split('\t')[:-1]))[3:]
        p=0
        for k in a:
            p+=weight[k]
        pctr.append(sigmoid(p))

with open('./train/pctr_'+camp+'.txt', 'w') as fw:
    for k in pctr:
        fw.write(str(k)+'\n')

pctr = []
with open('./test/feature_'+camp+'.txt') as fp:
    for f in fp:
        a = list(map(int, f.strip('\n').split('\t')[:-1]))[3:]
        p=0
        for k in a:
            p+=weight[k]
        pctr.append(sigmoid(p))

with open('./test/pctr_'+camp+'.txt', 'w') as fw:
    for k in pctr:
        fw.write(str(k)+'\n')

