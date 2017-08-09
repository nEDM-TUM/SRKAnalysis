
# coding: utf-8

# In[1]:

import sys
sys.path.insert(0, '/mnt/data/Eva/Simulation/SRKAnalysis/SRKAnalysis')
sys.path.insert(1, '/usr/lib64/root')
import srkdata 
import srkmisc 
import srkmultiprocessing 
import srkanalysis 
import sqlite3 
import numpy as np 
from datetime import date 
import time 
import srkglobal


# In[ ]:

start_time = time.time()
today = date.today()

s = srkdata.default_srk_settings("g2")
r = srkdata.default_run_settings("g2")
srkglobal.set_computer("work_desktop")

# SRK settings and run settings
r['Title'] = "g-2 full measurement period"
r['SRKVersion'] = '268424df43f9d7c8f200b60c39ad28676e006854'
r['Date'] = today.strftime('%m/%d/%y')
r['NumTracks'] = 1

titles = ["Baseline", "OscillationX", "OscillationZ", "Spiral"]
startPos = [(0,0), (0.041804007,0), (0,0.01665608), (0.041804007,0.01665608)]
BFields = [(0,0), (-0.81838,0), (0,-0.018459), (-0.81838,-0.018459)]

for i in range(4):
    r['RunType'] = 'g-2_'+titles[i]
    s['DefaultPos'] = str(startPos[i][0])+' 0 '+str(startPos[i][1])
    for j in range(4):
        s['BQuadFieldStrength'] = BFields[j][0]
        s['BSextFieldStrength'] = BFields[j][1]

# Create runs for different wall depolarization probabilities
#wall_depol=srkmisc.even_sample_over_log(0.000001, 0.00001, 4)
#for x in wall_depol:
#    s['DepolAtWallProb'] = x
    # Adds the run to the database, makes the macro, 
    # syncs it to Optima server, and runs it on Optima
#    srkdata.make_and_run(s,r,"optima") 
#    time.sleep(2) # To ensure random seeds will be different

        srkdata.make_and_run(s,r)
#        time.sleep(2) # To make time for results file update


# In[ ]:



