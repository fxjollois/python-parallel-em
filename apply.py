from parallelkmeans import *
import csv
import numpy

# Get data
y = numpy.genfromtxt('data/Iris.csv', 
						delimiter = ";", names = True, 
						dtype = None, autostrip = True) 
x = numpy.array([[round(yy[i], 1) for i in range(4)] for yy in y])

# Run parallel kmeans 
res = pkmeans(x, 3)
printResults(res)

