# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 23:02:56 2017

@author: The Users
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import time
import scipy.stats
from math import erf
from PIL import Image

startTime = time.time()

#defining pixel grid to represent area of interest
uraniumGrid = np.zeros([100, 100])
print(uraniumGrid.shape)
rows = uraniumGrid.shape[0]
columns = uraniumGrid.shape[0]
euclid = 0
scattering = (0.5 * (1 + erf(-3 / np.sqrt(2)))*2)#three sigma gaussian
runTime = 10#how many seconds to measure detector
fastForward = 10#accelerating epochs of simulation
print('simulated runtime is', runTime*fastForward, 'seconds')
muonFlux = fastForward*10**-1#1/10cm/s^2 = 0.1 per unit area
#calculating the Z numbers of uranium and concrete
uraniumZ = 92
rhoUranium = 18950
rhoConcrete = 2350
concreteZ = (30*0.219)+(28*0.63)+(50*0.069)+(20*0.025)+(40*0.017)+(76*0.03)
#print(concreteZ)

for i in range(1, (runTime+1)):#number of seconds
    for x in range(0, rows):#pixels in x axis
        for y in range(0, columns):#pixels in y axis
            #print (grid[x,y])
            euclid = 2*(np.sqrt((0.5**2)-(np.absolute((y/100)-0.5))**2))#cylinder thickness
            if random.random() < (scattering*euclid*muonFlux):#likelihood for interaction
                uraniumGrid[x,y] = 1#changes pixel from black to white
            #print (grid[x,y])
#print(grid, grid[1,1].dtype)
plt.imsave('uraniumGrid.png', uraniumGrid, cmap=cm.gray)#saves image


concreteGrid = np.zeros([300, 300])
print(concreteGrid.shape)
rows = concreteGrid.shape[0]
columns = concreteGrid.shape[0]

ratio = (rhoConcrete/rhoUranium)*(concreteZ/uraniumZ)**2

for i in range(1, (runTime+1)):#number of seconds
    for x in range(0, rows):#pixels in x axis
        for y in range(0, columns):#pixels in y axis
            #print (grid[x,y])
            euclid = 2*(np.sqrt((1.5**2)-(np.absolute((y/300)-1.5))**2))#cylinder thickness
            if random.random() < (scattering*euclid*muonFlux*ratio):#likelihood for interaction
                concreteGrid[x,y] = 1#changes pixel from black to white
            #print (grid[x,y])
#print(grid, grid[1,1].dtype)
plt.imsave('concreteGrid.png', concreteGrid, cmap=cm.gray)#saves image


imgU = Image.open('uraniumGrid.png', 'r')
img_w, img_h = imgU.size
background = Image.open('concreteGrid.png', 'r')
bg_w, bg_h = background.size
offset = 100, 100#((bg_w - img_w) / 2, (bg_h - img_h) / 2)
background.paste(imgU, offset)
background.save('final.png')

print("--- %s seconds ---" % (time.time() - startTime))
