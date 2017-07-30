import numpy as np
import pickle as pk
import sys
from random import seed, randint

camp = sys.argv[1]
algo = sys.argv[2]
algos = ['const', 'random', 'mcpc', 'lin']
seed(int(camp))
##################  Read data #######################

train_log = [] # (clk, market price, floor price)
with open('./train/'+camp+'/feature_'+camp+'.txt') as fp:
    for f in fp:
        a = f.strip('\n').split('\t')
        train_log.append( (int(a[0]), int(a[1]), int(a[2]) ))

test_log = [] # (clk, market price, floor price)
with open('./test/'+camp+'/feature_'+camp+'.txt') as fp:
    for f in fp:
        a = f.strip('\n').split('\t')
        test_log.append( (int(a[0]), int(a[1]), int(a[2]) ))
#test_log = test_log[:350000]

train_pctr = []
with open('./train/'+camp+'/pctr_'+camp+'.txt') as fp:
    for f in fp:
        a = float(f.strip('\n').split('\t')[0])
        train_pctr.append(a)

test_pctr = []
with open('./test/'+camp+'/pctr_'+camp+'.txt') as fp:
    for f in fp:
        a = float(f.strip('\n').split('\t')[0])
        test_pctr.append(a)
#test_pctr = test_pctr[:350000]

print("Read data done.")
###################################################
# bp: bid price, mp: market price, fp: floor price 
# b: budget, t: remaining time
def auction(bp, clk, mp, fp, budget, cost):
    bp = min(min(bp, 300), budget-cost)
    if bp>mp and bp>=fp: # win this auction
        return clk, cost+mp
    else: # lose this auction or < floor price
        return 0, cost

train_cost = 0
for i in range(len(train_log)):
    train_cost += train_log[i][1]
test_cost = 0
for i in range(len(test_log)):
    test_cost += test_log[i][1]
train_clk = 0
for i in range(len(train_log)):
    train_clk += train_log[i][0]

Budget = [2, 4, 8, 16, 32]
T = 1000
# Constant
with open('./test/'+camp+'/result_episode.txt', 'a') as fw:
    if algo == 'const':
        for B in Budget:
            budget = int(train_cost/len(train_log)*T/B)
            clist = list(range(0, 301, 2))
            # Training Tune parameter
            tune_list = []
            for b in clist:
                t = 0
                cost = 0
                clks = 0
                for i in range(len(train_log)):
                    c, cost = auction(b, train_log[i][0], train_log[i][1], train_log[i][2], budget, cost)
                    clks+=c
                    t+=1
                    if t>=T:
                        t=0
                        cost=0
                tune_list.append(clks)
            b = clist[np.argmax(tune_list)]
            # Testing
            t = 0
            cost = 0
            clks = 0
            for i in range(len(test_log)):
                c, cost = auction(b, test_log[i][0], test_log[i][1], test_log[i][2], budget, cost)
                clks+=c
                t+=1
                if t>=T:
                    t=0
                    cost=0
            line = algo+'\t'+str(B)+'\t'+str(clks)+'\n'
            print(line, end="")
            fw.write(line)
    elif algo=='random':
        for B in Budget:
            budget = int(train_cost/len(train_log)*T/B)
            rlist = list(range(20, 100, 10)) + list(range(100, 301, 30))
            # Training Tune parameter
            tune_list = []
            for r in rlist:
                t = 0
                cost = 0
                clks = 0
                for i in range(len(train_log)):
                    c, cost = auction(randint(0, r), train_log[i][0], train_log[i][1], train_log[i][2], budget, cost)
                    clks+=c
                    t+=1
                    if t>=T:
                        t=0
                        cost=0
                tune_list.append(clks)
            r = rlist[np.argmax(tune_list)]
            # Testing
            t = 0
            cost = 0
            clks = 0
            for i in range(len(test_log)):
                c, cost = auction(randint(0, r), test_log[i][0], test_log[i][1], test_log[i][2], budget, cost)
                clks+=c
                t+=1
                if t>=T:
                    t=0
                    cost=0
            line = algo+'\t'+str(B)+'\t'+str(clks)+'\n'
            print(line, end="")
            fw.write(line)

    elif algo=='mcpc':
        ecpc = train_cost/train_clk
        for B in Budget:
            # Testing
            budget = int(train_cost/len(train_log)*T/B)
            t = 0
            cost = 0
            clks = 0
            for i in range(len(test_log)):
                c, cost = auction(int(ecpc*test_pctr[i]), test_log[i][0], test_log[i][1], test_log[i][2], budget, cost)
                clks+=c
                t+=1
                if t>=T:
                    t=0
                    cost=0
            line = algo+'\t'+str(B)+'\t'+str(clks)+'\n'
            print(line, end="")
            fw.write(line)
    elif algo=='lin':
        avg_ctr = train_clk/len(train_log)
        for B in Budget:
            budget = int(train_cost/len(train_log)*T/B)
            B0 = list(range(2, 20, 2)) + list(range(20, 100, 5)) + list(range(100, 301, 10))
            # Training Tune parameter
            tune_list = []
            for b0 in B0:
                t = 0
                cost = 0
                clks = 0
                for i in range(len(train_log)):
                    c, cost = auction(b0*train_pctr[i]/avg_ctr, train_log[i][0], train_log[i][1], train_log[i][2], budget, cost)
                    clks+=c
                    t+=1
                    if t>=T:
                        t=0
                        cost=0
                tune_list.append(clks)
            b0 = B0[np.argmax(tune_list)]
            # Testing
            t = 0
            cost = 0
            clks = 0
            for i in range(len(test_log)):
                c, cost = auction(b0*test_pctr[i]/avg_ctr, test_log[i][0], test_log[i][1], test_log[i][2], budget, cost)
                clks+=c
                t+=1
                if t>=T:
                    t=0
                    cost=0
            line = algo+'\t'+str(B)+'\t'+str(clks)+'\n'
            print(line, end="")
            fw.write(line)




