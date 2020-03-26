#!/usr/bin/python
# Reads in parameter range file, generates directories and parameter file for
# each combination, and generates a job file

import sys
import os
import numpy
import math
import itertools

ranges = numpy.loadtxt("paramranges",numpy.float64)
numparams = numpy.size(ranges[:,0])

paramlists = []
for i in range(numparams):
    steps = math.floor((ranges[i,1] - ranges[i,0]) / ranges[i,2]) + 1
    paramlists.append(numpy.linspace(ranges[i,0],ranges[i,1],steps,numpy.float64).tolist())

combinations = itertools.product(paramlists[0],paramlists[1],paramlists[2],paramlists[3],paramlists[4],paramlists[5])

jobsfile = open("jobs","w")

for comb in combinations:
    dirname = "data/x0_%.1f_v0_%.1f_k_%.1f_b_%.1f_m_%.1f_tf_%.1f" % (comb[0],comb[1],comb[2],comb[3],comb[4],comb[5])
    paramstr = ""
    for j in comb:
        paramstr += (str(j)+"\n")
    os.system("mkdir %s" % dirname)
    paramfile = open(dirname+"/params","w")
    paramfile.write(paramstr)
    paramfile.close()
    jobsfile.write("cd '"+os.getcwd()+"/"+dirname+"'\n../../dampedOscillator\n")

jobsfile.close()
