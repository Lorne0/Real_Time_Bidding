import numpy as np
import pickle as pk
import sys
from random import seed, randint

camp = sys.argv[1]
mode = sys.argv[2] # train or test
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
#Budget = [16]
T = 1000
# Constant
# make market price pdf, with Laplace Smoothing/Additive Smoothing
mp_counter = [0]*301
for i in range(len(train_log)):
    mp_counter[train_log[i][1]]+=1
m_pdf = [0]*301
laplace = 1
for i in range(301):
    m_pdf[i] = (mp_counter[i]+laplace)/(len(train_log)+301*laplace)

avg_ctr = train_clk/len(train_log)

for B in Budget:
    print(B)
    budget = int(train_cost/len(train_log)*T/B)
    # Training, build value table V(t, b)
    if mode=='train':
        V = np.zeros((T, budget+1))
        V_max = 0 # for early stop, since V[][b], V[][b+1] is similar when b is large enough
        for t in range(1, T):
            V_max = t*avg_ctr
            for b in range(1, budget+1):
                prev = -1000000000
                k = V[t-1][b]
                for delta in range(0, min(b, 301)):
                    k += m_pdf[delta]*(avg_ctr+V[t-1][b-delta]-V[t-1][b])
                    if k <= prev:
                        break
                    else:
                        prev = k
                V[t][b] = prev

                # early stop
                if abs(prev-V_max)<1e-10:
                    for bb in range(b+1, budget+1):
                        V[t][bb] = V_max
                    break

        # Save V
        with open('./train/'+camp+'/rlb_dp_v_'+str(B)+'.pk', 'wb') as fw:
            pk.dump(V, fw, protocol=pk.HIGHEST_PROTOCOL)

    # Testing, choose best a
    elif mode=='test':
        # Load value
        with open('./train/'+camp+'/rlb_dp_v_'+str(B)+'.pk', 'rb') as fp:
            V = pk.load(fp)
        t = 0
        cost = 0
        clks = 0
        with open('./test/'+camp+'/result_episode.txt', 'a') as fw:
            for i in range(len(test_log)):
                a = 0
                b = min(budget-cost, 300) #remain budget
                for delta in range(b+1):
                    if test_pctr[i]+V[T-t-1][budget-cost-delta]-V[T-t-1][budget-cost] >= 0:
                        a = delta
                    else:
                        break
                c, cost = auction(a, test_log[i][0], test_log[i][1], test_log[i][2], budget, cost)
                clks += c
                t += 1
                if t >= T:
                    t = 0
                    cost = 0
            line = 'rlb_dp\t'+str(B)+'\t'+str(clks)+'\n'
            print(line, end="")
            fw.write(line)

