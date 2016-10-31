import os
import csv
import numpy as np
import sys
import math
from geopy.distance import great_circle
import datetime



def readallfiles():
    fl = []
    for filename in os.listdir('data'):
        if filename.endswith('.csv'):
            fl.append(filename)
                
    return fl
    
    
def part_one(fl):
    bike_duration = []
    for fn in fl:
        with open('data/'+fn, 'r') as csvfn:
            csvreader = csv.reader(csvfn)
            for row in csvreader:
                
                print '\r%s' % row[0],
                sys.stdout.write("\x1b[2K")
                try:
                    bike_duration.append(int(row[0]))
                except ValueError:
                    continue
                    
    print np.median(bike_duration)

def part_two(fl):

    bikelist = []
    for fn in fl:

        with open('data/'+fn, 'r') as csvfn:
            firstline = True
            csvreader = csv.reader(csvfn)
            for row in csvreader:
                if firstline:
                    print "reading file %s" % fn
                    firstline = False
                    continue
                
                foundbike = None
                for bike in bikelist:
                    if bike[0] == row[11]:

                        foundbike = bike
                        break
                
                # if this bike is not in the record
                if foundbike == None:
                    bikerow = []
                    bikerow.append(row[11])
                    bikerow.append(row[3])
                    bikerow.append(row[7])
                    bikelist.append(bikerow)
                # or else...
                else:
                    bikerow = foundbike
                    bikerow.append(row[3])
                    bikerow.append(row[7])
                    
                
                
                print '\r%s' % row[0],
                sys.stdout.write("\x1b[2K")
    
    bss = [len(set(bike)) -1 for bike in bikelist]
    
    
    print np.std(bss)

def part_three(fl):

    months = [0] * 12
    monthctr = [0] * 12
    for fn in fl:
        with open('data/'+fn, 'r') as csvfn:
            firstline = True
            csvreader = csv.reader(csvfn)
            for row in csvreader:
                if firstline:
                    firstline = False
                    continue
                
                # the month = 1st number in the date string
                mth = int(row[1].split('/')[0])
                months[mth-1] += int(row[0])
                monthctr[mth-1] += 1
                
                
                
                print '\r%s' % row[1],
                sys.stdout.write("\x1b[2K")


    avgarray = [mth/float(ctr) for mth, ctr in zip(months, monthctr)]
    print avgarray
    print max(avgarray) - min(avgarray)
    
    
    
    
def part_four(fl):
    totalctr = 0
    expirectr = 0
    for fn in fl:
        with open('data/'+fn, 'r') as csvfn:
            firstline = True
            csvreader = csv.reader(csvfn)
            for row in csvreader:
                if firstline:
                    firstline = False
                    continue
                
                totalctr += 1
                
                if row[12] == 'Subscriber' and int(row[0]) > 45 * 60:
                    expirectr += 1
                elif row[12] == 'Customer' and int(row[0]) > 30 * 60:
                    expirectr += 1
                print '\r%s' % row[0],
                sys.stdout.write("\x1b[2K")

    print float(expirectr)/totalctr
    
  
def part_five(fl):


    ctr = 0
    samestopctr = 0
    for fn in fl:
        with open('data/'+fn, 'r') as csvfn:
            firstline = True
            csvreader = csv.reader(csvfn)
            for row in csvreader:
                if firstline:
                    firstline = False
                    continue
                ctr += 1
                
                if row[3] == row[7]:
                   samestopctr += 1 
                
                    
                
                
                
                print '\r%s' % row[0],
                sys.stdout.write("\x1b[2K")

    print ctr/float(samestopctr)

    
    
def part_six(fl):

    distances = []
    for fn in fl:
        with open('data/'+fn, 'r') as csvfn:
            firstline = True
            csvreader = csv.reader(csvfn)
            for row in csvreader:
                if firstline:
                    print "reading file %s" % fn
                    firstline = False
                    continue
                
                if row[3] == row[7]:
                   continue
                else:
                    start = (row[5], row[6])
                    end = (row[9], row[10])
                    rowdist = float(great_circle(start, end).kilometers)
                    if rowdist / int(row[0]) < 0.00555555555:
                        # if the speed doesn't exceed 20km/h
                        distances.append(float(rowdist))
                    
                
                
                
                print '\r%s' % row[0],
                sys.stdout.write("\x1b[2K")

    print np.mean(distances)

def part_seven(fl):

    stlist = []
    firstfile = True
    for fn in fl:

        with open('data/'+fn, 'r') as csvfn:
            if firstfile == True:
                firstfile = False
            else:
                break
            firstline = True
            csvreader = csv.reader(csvfn)
            for row in csvreader:
                if firstline:
                    print "reading file %s" % fn
                    firstline = False
                    continue
                
                foundst = None
                for st in stlist:
                    if st[0] == row[3]:

                        foundst = st
                        break
                
                # if this station is not in the record
                if foundst == None:
                    strow = []
                    strow.append(row[3])
                    strow.extend([0] * 24)
                    
                    #print strow
                    
                    hour = int(row[1].split(' ')[1].split(':')[0]          )
                    strow[hour+1] += 1
                    stlist.append(strow)
                # or else...
                else:
                    strow = foundst
                    hour = int(row[1].split(' ')[1].split(':')[0])
                                        
                    strow[hour+1] += 1
                
                
                print '\r%s' % row[0],
                sys.stdout.write("\x1b[2K")
    
    
            #print stlist
    systat = [0] * 24
    for st in stlist:
        st.append(float(sum(st[1:])))
        #print st
        systat = [syst + stitem for syst, stitem in zip(systat, st[1:-1])]
        st[1:-1] = [stitem / st[-1] for stitem in st[1:-1]]
    
    totsys = float(sum(systat))
    print systat
    systat[0:-1] = [syst / totsys for syst in systat[0:-1]]
    
    huf = 0
    for st in stlist:
        newhuf = max([sthr / syst for sthr, syst in zip(st[1:-1], systat[:-1])])
        if newhuf > huf:
            huf = newhuf
    
    
    print huf

def part_eight(fl):

    bikelist = []
    for fn in fl:

        with open('data/'+fn, 'r') as csvfn:
            firstline = True
            csvreader = csv.reader(csvfn)
            for row in csvreader:
                if firstline:
                    print "reading file %s" % fn
                    firstline = False
                    continue
                
                foundbike = None
                for bike in bikelist:
                    if bike[0] == row[11]:

                        foundbike = bike
                        break
                
                # if this bike is not in the record
                if foundbike == None:
                    bikerow = []
                    bikerow.append(row[11])
                    # store the end station here
                    bikerow.append(row[7])
                    bikerow.append(0)
                    bikelist.append(bikerow)
                # or else...
                else:
                    bikerow = foundbike
                    if bikerow[1] != row[3]:
                        bikerow[-1] += 1
                    bikerow[1] = row[7]
                    
                
                
                print '\r%s' % row[0],
                sys.stdout.write("\x1b[2K")
    
    moves = [bike[-1] for bike in bikelist]
    
    
    
    print np.mean(moves)
  
filelist = readallfiles()
#part_one(filelist)
#part_two(filelist)
#part_three(filelist)
#part_four(filelist)
#part_five(filelist)
#part_six(filelist)
#part_seven(filelist)
part_eight(filelist)
