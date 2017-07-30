import numpy as np
import pickle as pk
from datetime import date
from user_agents import parse
import sys

#['clk', 'marketprice', 'floorprice', 'bidid', 'timestep', 'weekday', 'hour', 'ipinyouid', 'device', 'os', 'browser', 'ip', 'region', 'city', 'adexchange', 'domain', 'url', 'anonymousurl', 'adslotid', 'adslotwidth', 'adslotheight', 'adslotvisibility', 'adslotformat', 'adslotfloorprice', 'creativeid', 'bidprice', 'keypageurl', 'adid', 'usetags']

camp = sys.argv[1]

clk = []
with open('./train/clk_all.txt') as fp:
    for f in fp:
        n = f.strip('\n').split('\t')[0]
        clk.append(n)
clk = list(set(clk))

cnt = 0
with open("./train/train_"+camp+".txt", "w") as fw:
    with open('./train/imp_all.txt') as fp:
        for f in fp:
            a = f.strip('\n').split('\t')
            if a[22] != camp:
                continue
            for i in range(len(a)):
                if len(a[i])==0:
                    a[i]=='null'

            s = ['null']*29
            ck = '1' if a[0] in clk else '0'
            mp = a[20]
            fpp = a[17]
            weekday = date(int(a[1][0:4]), int(a[1][4:6]), int(a[1][6:8])).strftime("%w")
            hour = a[1][8:10]
            ua = parse(a[3].lower())
            d = ua.device.family
            o = ua.os.family
            b = ua.browser.family
            fprice = int(a[17])
            rp = 0
            if fprice==0:
                rp = '0'
            elif fprice>=1 and fprice<=5:
                rp = '1-5'
            elif fprice>=6 and fprice<=49:
                rp = '6-49'
            elif fprice>=50 and fprice<=69:
                rp = '50-69'
            elif fprice>=70 and fprice<=79:
                rp = '70-79'
            elif fprice>=80 and fprice<=300:
                rp = '80-300'
            s[0:3] = [ck, mp, fpp]
            s[3:5] = a[0:2]
            s[5:11] = [weekday, hour, a[3], d, o, b]
            s[11:26] = a[5:20]
            s[26:29] = a[21:24]
            s[23] = rp

            fw.write('\t'.join(s)+'\n')
            cnt+=1
            if cnt % 100000 == 0:
                print(cnt)

print("Read imp done.")
print(cnt)

# Save file
#with open("./train/train_"+camp+".pk", "wb") as fp:
#    pk.dump(A, fp, protocol=pk.HIGHEST_PROTOCOL)
        

