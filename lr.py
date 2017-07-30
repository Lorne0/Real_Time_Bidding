import sys
import random
import numpy as np
import pickle as pk
from sklearn.metrics import roc_auc_score

camp = sys.argv[1]
camp_dim = {'1458': 63819, '2259': 40500, '2261': 28909, '2821': 39283, '2997': 2334, '3358': 46398, '3386': 68038, '3427': 64346, '3476': 51704}
camp_tnsize = {'1458': 3083056, '2259': 835556, '2261': 687617, '2821': 1322561, '2997': 312437, '3358': 1742104, '3386': 2847802, '3427': 2593765, '3476': 1970360}
camp_ttsize = {'1458': 614638, '2259': 417197, '2261': 343862, '2821': 661964, '2997': 156063, '3358': 300928, '3386': 545421, '3427': 536795, '3476': 523848}
dim = camp_dim[camp]
tnsize = camp_tnsize[camp]
ttsize = camp_ttsize[camp]
X_train = []
y_train = np.zeros(tnsize, dtype='int8')
X_test = []
y_test = np.zeros(ttsize, dtype='int8')

cnt=0
with open('./train/feature_'+camp+'.txt') as fp:
    for f in fp:
        a = list(map(int, f.strip('\n').split('\t')[:-1]))
        y_train[cnt] = 0 if a[0]==0 else 1
        X_train.append(a[3:])
        cnt+=1
cnt=0
with open('./test/feature_'+camp+'.txt') as fp:
    for f in fp:
        a = list(map(int, f.strip('\n').split('\t')[:-1]))
        y_test[cnt] = 0 if a[0]==0 else 1
        X_test.append(a[3:])
        cnt+=1

X_train = np.array(X_train)
X_test = np.array(X_test)
print("Read data done.")

#################################

weight = (np.random.random((dim, ))-0.5)*0.05

def sigmoid(x):
    return 1/(1+np.exp(-x))

alpha = 1e-2
lamb = 1e-6
epoch = 20
rlist = list(range(tnsize))
random.shuffle(rlist)
bestauc = 0

for e in range(epoch):
    X_train = X_train[rlist]
    y_train = y_train[rlist]

    for i in range(len(X_train)):
        grad = 0
        for k in X_train[i]:
            grad += weight[k]
        for k in X_train[i]:
            weight[k] -= alpha * (sigmoid(grad)-y_train[i] + lamb*weight[k])
        #for k in [x for x in range(dim) if x not in X_train[i]]:
        #    weight[k] -= alpha*lamb*weight[k]

    # test
    y_pred = []
    for i in range(len(X_test)):
        grad = 0
        for k in X_test[i]:
            grad += weight[k]
        y_pred.append(sigmoid(grad))
        
    auc = roc_auc_score(y_test, y_pred)

    # save model
    if auc>bestauc:
        bestauc = auc
        with open('./train/weight_lr_'+camp+'.pk', 'wb') as fp:
            pk.dump(weight, fp, protocol=pk.HIGHEST_PROTOCOL)

    print("episode: ", e+1, "AUC: ", auc, "Best AUC: ", bestauc)



