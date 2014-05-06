import matplotlib.pyplot as plt
import scipy.stats as stats

def plot_hist(array, ylab, xlab, titl, bins):
	plt.hist(array, bins)
	plt.ylabel(ylab)
	plt.xlabel(xlab)
	plt.title(titl)
	# #plt.plot(bins, y, 'r--')
	plt.show()

def tenure_to_performance_plot(scores,tenure, xlab, ylab):
	slope, intercept, r_value, p_value, std_err = stats.linregress(tenure,scores)
	print slope
	print r_value
	plt.scatter(tenure,scores)
	plt.show()

def score_centroid_distributions(array, cent3, cent2):
	dist = {'low':[],'med-low':[],'med-high':[], 'high':[]}
	for i in range(len(array)):
		if array[i] < cent3[0,0]:
			dist['low'].append(array[i])
		elif array[i] < cent3[1,0]:
			dist['med-low'].append(array[i])
		elif array[i] < cent3[2,0]:
			dist['med-high'].append(array[i])
		elif array[i] > cent3[2,0]:
			dist['high'].append(array[i])
	for level in dist:
		print level +':'+str(len(dist[level]))

	dist2= {'low':[], 'med':[], 'high':[]}
	for i in range(len(array)):
		if array[i] < cent2[0,0]:
			dist2['low'].append(array[i])
		elif array[i] < cent2[1,0]:
			dist2['med'].append(array[i])
		else:
			dist2['high'].append(array[i])
	for level in dist2:
		print level +':'+str(len(dist2[level]))
	plt.hist(array, 100)
	plt.ylabel('Frequency')
	plt.xlabel('Average Score Distribution')
	plt.title('Histogram of Performance Scores')
	plt.vlines(cent3[0,1],0,3)
	plt.vlines(cent3[1,1],0,3)
	plt.vlines(cent3[2,1],0,3)
	plt.vlines(cent2[0,1],0,3, colors='g')
	plt.vlines(cent2[1,1],0,3, colors='g')
	plt.show()

def questionLine(resultsMatrix):
	plt.figure()
	plt.plot(resultsMatrix[:,0], label="Step Wise")
	plt.plot(resultsMatrix[:,1], label="Step Wise with Penalty")
	plt.plot(resultsMatrix[:,2], label="Freq Attenutate")
	plt.plot(resultsMatrix[:,3], label="Continous Attenous")
	plt.legend()
	plt.ylabel('Number of questions')
	plt.xlabel('User')
	plt.title('Number of Questions')
	plt.show()

def scatterOfClusterResults(paramX, paramY, colorArray, resultsMatrix, xlab, ylab, zlab):
	fig = plt.figure()
	at = fig.add_subplot(121, projection='3d')
	sc = at.scatter(paramX,paramY, resultsMatrix[:,4], c=colorArray, marker='o', s=50)
	sc.set_clim(vmin=0.97,vmax=0.999)
	at.set_xlabel(xlab)
	at.set_ylabel(ylab)
	at.set_zlabel(zlab)
	at.set_zlim(100, 300)
	ax = fig.add_subplot(122, projection='3d')
	sc2 = ax.scatter(paramX,paramY, resultsMatrix[:,5], c=colorArray, marker='o', s= 50)
	sc2.set_clim(vmin=0.97,vmax=0.999)
	ax.set_xlabel(xlab)
	ax.set_ylabel(ylab)
	ax.set_zlim(100, 300)
	fig.colorbar(sc)
	plt.show()

#3d Scatter of Cluster Algorthim Results
#scatterOfClusterResults(score_array, time_array, curr_array, questions, 'Scores', 'Times', 'Questions before Gold')

# Score distribution
#plot_hist(score_array, 'Frequency', 'Average Score Distribution', 'Histogram of Performance Scores', 100)

#Tenure Distribution
#plot_hist(user_ten.sort(), 'Frequency', 'User Tenure', 'Number of days since first Sama Source task', 100)