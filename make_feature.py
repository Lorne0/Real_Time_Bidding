import numpy as np
import pickle as pk
import sys

# ['clk', 'marketprice', 'floorprice', 'bidid', 'timestep', 'weekday', 'hour', 'ipinyouid', 'device', 'os', 'browser', 'ip', 'region', 'city', 'adexchange', 'domain', 'url', 'anonymousurl', 'adslotid', 'adslotwidth', 'adslotheight', 'adslotvisibility', 'adslotformat', 'adslotfloorprice', 'creativeid', 'bidprice', 'keypageurl', 'adid', 'usetags']

select_feature = [5, 6, 8, 9, 10, 12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 24, 25, 28]
dic = {}
idx = 0
camp = sys.argv[1]
cnt=0

with open("./train/train_"+camp+".txt") as fp:
    for f in fp:
        a = np.array(f.strip('\n').split('\t'))[select_feature]
        for i in range(len(select_feature)):
            if select_feature[i]==28: #tags
                s = a[i].split(',')
                for ss in s:
                    if (str(select_feature[i])+":"+ss) not in dic:
                        dic[str(select_feature[i])+":"+ss] = idx
                        idx+=1
            else:
                if str(select_feature[i])+":"+a[i] not in dic:
                    dic[ str(select_feature[i])+":"+a[i] ] = idx
                    idx+=1
        cnt+=1
        #if cnt%100000==0:
        #    print(cnt)
print("Make dict done.")
print(idx)

if sys.argv[2] == 'train':
    with open("./train/feature_"+camp+".txt", "w") as fw:
        with open("./train/train_"+camp+".txt") as fp:
            for f in fp:
                a = np.array(f.strip('\n').split('\t'))
                clk = a[0]
                marketprice = a[1]
                floorprice = a[2]
                line = str(clk)+'\t'+str(marketprice)+'\t'+str(floorprice)+'\t'
                a = a[select_feature]
                for i in range(len(select_feature)):
                    if select_feature[i]==28:
                        s = a[i].split(",")
                        for ss in s:
                            line += str(dic[str(select_feature[i])+":"+ss])+'\t'
                    else:
                        line += str(dic[str(select_feature[i])+":"+a[i]])+'\t'
                line+='\n'
                fw.write(line)
    print("Train done.")

if sys.argv[2] == 'test':
    test_dic = {} # key: timestep, value: line
    with open("./test/test_"+camp+".txt") as fp:
        for f in fp:
            a = np.array(f.strip('\n').split('\t'))
            clk = a[0]
            marketprice = a[1]
            floorprice = a[2]
            line = str(clk)+'\t'+str(marketprice)+'\t'+str(floorprice)+'\t'
            ts = int(a[4])
            a = a[select_feature]
            for i in range(len(select_feature)):
                if select_feature[i]==28:
                    s = a[i].split(",")
                    for ss in s:
                        if (str(select_feature[i])+":"+ss) in dic:
                            line += str(dic[str(select_feature[i])+":"+ss])+'\t'
                else:
                    if (str(select_feature[i])+":"+a[i]) in dic:
                        line += str(dic[str(select_feature[i])+":"+a[i]])+'\t'
            line+='\n'
            while ts in test_dic:
                ts+=1
            test_dic[ts] = line
    # sort test_dic
    print("Read done, sorting...")
    keys = sorted(list(test_dic.keys()))
    print(len(keys))
    with open("./test/feature_"+camp+".txt", "w") as fw:
        for k in keys:
            fw.write(test_dic[k])
    print("Test done.")





            
    


