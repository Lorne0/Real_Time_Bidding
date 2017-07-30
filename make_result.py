# algo, B, clk
camps = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476']
s2 = ['1458', '3358', '3386', '3427', '3476']
s3 = ['2259', '2261', '2821', '2997']
filename = ['result_all.txt', 'result_episode.txt']
#filename = ['result_all.txt']
B = [2, 4, 8, 16, 32]
algos = ['const', 'random', 'mcpc', 'lin']

for fn in filename:
    result = {}
    for camp in camps:
        result[camp] = []
        with open('./test/'+camp+'/'+fn) as fp:
            for f in fp:
                result[camp].append(f.strip('\n').split('\t'))

    with open(fn, 'w') as fw:
        for b in B:
            fw.write('B: 1/'+str(b)+'\n')
            fw.write('camp\tcons\trand\tmcpc\tlin\n')
            algo_dic = {}
            for a in algos:
                algo_dic[a] = {}
                for camp in camps:
                    algo_dic[a][camp] = 0
            for camp in camps:
                line = ''+camp+'\t'
                for algo in algos:
                    for r in result[camp]:
                        if r[1]==str(b) and r[0]==algo:
                            line += r[2]+" "*(4-len(r[2]))+'\t'
                            algo_dic[algo][camp] = int(r[2])
                            break
                line+='\n'
                fw.write(line)
            line = 's2  \t'
            for a in algos:
                c=0
                for camp in s2:
                    c += algo_dic[a][camp]
                line += str(c)+' '*(4-len(str(c)))+'\t'
            line+='\n'
            fw.write(line)
            line = 's3  \t'
            for a in algos:
                c=0
                for camp in s3:
                    c += algo_dic[a][camp]
                line += str(c)+' '*(4-len(str(c)))+'\t'
            line+='\n'
            fw.write(line)
            line = 'Total\t'
            for a in algos:
                c=0
                for camp in camps:
                    c += algo_dic[a][camp]
                line += str(c)+' '*(4-len(str(c)))+'\t'
            line+='\n'
            fw.write(line)
            fw.write('\n')



