import numpy as np
import sys

def rangeGen(max):
    ctr = 0
    while ctr < max:
        yield ctr
        ctr += 1



def findallcombs(N, M):
    # define a base-6 number
    newM = M-N
    allcombs = []
    for i in rangeGen(pow(6,N)):
        num = []
        prefix = 0
        for j in range(N-1, -1, -1):
            num.append((i-prefix) / pow(6,j))
            prefix += num[-1] * pow(6,j)
        #sys.stdout.write("\x1b[2K")
        #print '\r%s' % num
        if sum(num) == newM:
            print '\r%s' % num
            yield([n+1 for n in num])

    
         
         
prodlist = []
for result in findallcombs(3,9):
    prodlist.append(float(np.prod(result)))

print "There are %d combinations" % len(prodlist)
prodlist = np.array(prodlist)


#print result
#print prodlist.dtype
print "Average is %.10f" % np.mean(prodlist)
print "St. Dev. is %.10f" % np.std(prodlist)