# parallel version of k-means algorithm
import numpy
import multiprocessing as mp

def randomPoints(k, length):
	# return k different numbers of objects (between 0 and length-1)
	return numpy.floor(numpy.random.random(k)*length)

def randomPartition(k, length):
	# return a vector of given length with k random clusters
	return (numpy.floor(numpy.random.random(length)*k+1)).astype(int)

def clusterCenters(data, z):
	# compute the centers for each cluster
	g = []
	for k in numpy.unique(z):
		if g == []:
			g = numpy.nanmean(data, 0)
		else:
			g = numpy.vstack((g, numpy.nanmean(data[z == k,], 0)))
	return g

def clusterAssignement(data, g):
	# assign each object to the nearest cluster
	z = []
	for x in data:
		d = []
		for k in range(len(g)):
			d.append(sum((x - g[k])**2))
		z.append(d.index(min(d))+1)
	return z

def pclusterAssignement(data, g):
	# assign each object to the nearest cluster
	z = []
	p = mp.Pool(len(g))
	for x in data:
		d = []
		def dist(x, g):
			return sum((x - g[k])**2)
		
# A FAIRE !!!!		d = p.map(dist,  
		z.append(d.index(min(d))+1)
	return z

def W(data, g, z):
	# compute the W criteria
	w = 0
	for i in range(len(data)):
		w += sum((data[i] - g[z[i]-1])**2)
	return w

def pkmeans(data, k):
	# compute k-means
	z = randomPartition(k, len(data))
	while len(numpy.unique(z)) < k:
		z = randomPartition(k, len(data))
	g = clusterCenters(data, z)
	w = W(data, g, z)
	wlist = w
	iter = 0
	wold = w
	error = 0
	msg = ""
	cont = True
	while cont:
		z = clusterAssignement(data, g)
		if len(numpy.unique(z)) < k:
			msg = "Error: empty cluster"
			error = -1
			cont = False
		else:
			g = clusterCenters(data, z)
			w = W(data, g, z)
			if abs(w - wold) < 0.001:
				cont = False
			wold = w
			wlist = numpy.append(wlist, w)
		iter += 1
	return {"centers": g, "partition": z, "criteria": w, "convergence": wlist, "error": error, "message": msg, "k": k}

def printResults(res):
	# smart print of pkmeans function
	print "k-means Result :"
	print "\tinitial number of clusters :", res["k"]
	if res["error"] < 0:
		print "\t", res["message"]
	else:
		print "\tFinal criteria :", res["criteria"]
		print "\tClusters size :", [sum(res["partition"] == k) for k in numpy.unique(res["partition"])]