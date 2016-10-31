import numpy as np
import sys
import types
import math





def combs(N, M):
    #define 6 blocks, one for each number
    
    blist = []
    duplist= []
    blocks = []
    
    for i, rem1 in getnum(1, M):
        blocks.append(i)
        #print '%dth level with value %d %d' % (1, i, rem1)
        for j, rem2 in getnum(2, rem1):
            blocks.append(j)
            #print '%dth level with value %d %d' % (2, j, rem2)
            for k, rem3 in getnum(3, rem2):
                blocks.append(k)
                #print '%dth level with value %d %d' % (3, k, rem3)
                for l, rem4 in getnum(4, rem3):
                    blocks.append(l)
                    #print '%dth level with value %d %d' % (4, l, rem4)
                    for m, rem5 in getnum(5, rem4):
                        blocks.append(m)
                        #print '%dth level with value %d %d' % (5, m, rem5)
                        for n, rem6 in getnum(6, rem5):
                            if rem6 == 0 and sum(blocks) + n == N:
                                blocks.append(n)
                                print blocks
                                #dup = math.factorial(N)/np.prod([math.factorial(el) for el in blocks])
                                dup = math.factorial(N)
                                for el in blocks:
                                    dup = dup / math.factorial(el)
                                
                                
                                duplist.append(dup)
                                blist.append(blocks[:])
                                #print blocks, dup
                                blocks.pop()
                        blocks.pop()
                    blocks.pop()
                    
                blocks.pop()
                
            blocks.pop()
        blocks.pop()
    return blist, duplist

                                            
    #total = sum([blocks[i] * (i + 1) for i in range(6)])
    
    #Ncombs = factorial(N)/np.prod([factorial(el) for el in blocks])


def getnum(el, remainder):
    max = remainder / el
    for i in range(0, remainder/el + 1):
        yield (i, (remainder - i*el))


            
totlist, totdup = combs(50,150)
loglist = []
for row in totlist:
    loglist.append(sum([row[r] * math.log(r+1) for r in range(6)]))
#print loglist

#reformedlist = []
#for row in totlist:
#    reformedlist.append([pow(long(i+1), row[i]) for i in range(6)])
#print reformedlist
#prodlist = np.array([np.prod(el) for el in reformedlist])

#newlist = [[prod] * dup for prod, dup in zip(prodlist,totdup)]
#print newlist
#sumtot = float(sum(totdup))
#print sumtot
#meanarray = [tot/sumtot*prod for prod, tot in zip(prodlist, totdup)]
#print min(prodlist)
#print [math.exp(lg) for lg in loglist]
mean = sum([math.exp(lg)*dup for dup,lg in zip(totdup,loglist)])/sum(totdup)
print mean
#np.dot(prodlist, totdup)/sum(totdup)
#print prodlist
#print np.dot(prodlist - mean, totdup)

#print totdup
#print min(np.dot(prodlist, totdup))
prodlist = np.array([math.exp(lg) for lg in loglist])
tmp = [pow(el, 2)* dup  for el, dup in zip((prodlist-mean),totdup)]
#tmp = np.multiply(tmp, totdup)
std = math.sqrt(sum(tmp)/sum(totdup))

print "The average is %.10f" % mean
print "The St. Dev. is %.10f" % std
print "The ratio is %.10f" % (mean/std)