import random as rand
import numpy as np
from project_algorthims import AttenuatedContinous as algoCont
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import csv, codecs, cStringIO

users_test = [[-0.518539030945, 0.25612226458999177, -0.4],[0.618539030945, -0.25612226458999177, 0.2]]

def rand_float(a,b):
	return round((rand.uniform(a, b)),2)

def monty(users, numtimes, deltas, base,thres_range, show_graph):
	curr_thres = []
	past_thres = []
	time_thres = []
	gold_matrix = np.zeros([len(users),numtimes, numtimes, numtimes])
	for b in range(numtimes):
		curr_thres.append(rand_float(*thres_range))
		past_thres.append(rand_float(*thres_range))
		time_thres.append(rand_float(*thres_range))

	curr_thres.sort()
	past_thres.sort()
	time_thres.sort()
	for u in range(len(users)):
		user_past = users[u][0]
		user_curr = users[u][1]
		time = users[u][2]
		for i in range(numtimes):
			for j in range(numtimes):
				for k in range(numtimes):
					gold_matrix[u,i,j,k] = algoCont(user_past, user_curr, time, past_thres[j], curr_thres[i], time_thres[k], deltas, base)
					
					#gold_matrix[i,j,k] = algoCont(user_past, user_curr, time, -0.46, -0.44, -0.25, delta, base)
	user_avg= np.mean(gold_matrix,axis=0)

	if show_graph == True:
		#Create a Figure of 5 subplots for each quintile of time
		fig = plt.figure()
		iInt = 9
		subnum = 151
		for i in range(5):
			ax = fig.add_subplot(subnum, projection='3d')
			X = curr_thres
			Y = past_thres
			X, Y = np.meshgrid(X, Y)
			surf = ax.plot_surface(X, Y, user_avg[:,:,iInt], rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0, antialiased=False)
			ax.set_zlim(175, 250)
			iInt += 20
			subnum +=1
		fig.subplots_adjust(right=0.8)
		fig.colorbar(surf, shrink=0.5, aspect=5)
		plt.show()
	return curr_thres, past_thres, time_thres, gold_matrix, user_avg


