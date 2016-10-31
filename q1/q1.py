import numpy as np
import random
import sys


def die(N, M, sample):
    ctr = 0
    product = []

    while ctr <= sample:
        dice = [random.randint(1,6) for i in range(N)]
        sys.stdout.write("\x1b[2K")
        print '\r%s: %d' % (dice, sum(dice)),
        
        if sum(dice) == M:
            ctr += 1
            print True, np.prod(dice), ctr
            product.append(np.prod(dice))
            
            
    return product
            
            
            
N = 8
M = 24
sample = 1000*100


result = die(N, M, sample)
print "Average: %d" % float(np.average(result))
print "STD: %d" % float(np.std(result))