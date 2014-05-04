import matplotlib.pyplot as plt
import scipy.stats as stats
import project_functions as pf
import project_algorthims as pa
import monty
from cluster2d import cluster_svm as cluster
import numpy as np

#test gating algorthim
if __name__ == "__main__":
	users, batch_score, users_time, batch_time = pf.readData('data/Getty_Training1.json')

	#run calculate_avg_score_per_batch on the global user scores
	global_batch = pf.calculate_avg_score_per_batch(batch_score)
	global_time = pf.calculate_avg_score_per_batch(batch_time)
	scores = {}
	#this is the test parameter for a particular batch/project we are looking at so we exclude it from their aggregate score
	exclude_batch = 903
	user_ten = []
	for user in users:
		if exclude_batch in users[user]["batch"]:
			if user != 368:
				if user != 369:
					user_ten.append(users[user]["tenure"])
					scores[user] = {}
					scores[user]["currentScore"] = pf.batch_avg(users[user]["batch"][exclude_batch])
					scores[user]["batch"], scores[user]["av"] = pf.calc_user_performance(users[user]["batch"], global_batch, exclude_batch)
					scores[user]["t_batch"], scores[user]["t_av"] = pf.calc_user_performance(users_time[user]["batch"], global_time, exclude_batch)
	score_array = []
	time_array = []
	curr_array = []
	outliers = []
	for score in scores:
		curr_array.append(scores[score]["currentScore"][0])
		score_array.append(scores[score]["av"])
		time_array.append(scores[score]["t_av"])
		if scores[score]["av"] > 3.0:
			outliers.append(scores[score]["av"])
		if scores[score]["av"] < -3.0:
			outliers.append(scores[score]["av"])
			print score
	centroids = cluster(score_array,time_array, 3, "Past Score (Normalized)", "Average Time (Normalized)", False)
	centroids2 = cluster(score_array,time_array, 2, "Past Score (Normalized)", "Average Time (Normalized)", False)
	#score_array.sort()
	print "Outliers:"
	print outliers
	#print centroids

	# dist = {'low':[],'med-low':[],'med-high':[], 'high':[]}
	# for i in range(len(score_array)):
	# 	if score_array[i] < centroids[0,0]:
	# 		dist['low'].append(score_array[i])
	# 	elif score_array[i] < centroids[1,0]:
	# 		dist['med-low'].append(score_array[i])
	# 	elif score_array[i] < centroids[2,0]:
	# 		dist['med-high'].append(score_array[i])
	# 	elif score_array[i] > centroids[2,0]:
	# 		dist['high'].append(score_array[i])
	# for level in dist:
	# 	print level +':'+str(len(dist[level]))

	# dist2= {'low':[], 'med':[], 'high':[]}
	# for i in range(len(score_array)):
	# 	if score_array[i] < centroids2[0,0]:
	# 		dist2['low'].append(score_array[i])
	# 	elif score_array[i] < centroids2[1,0]:
	# 		dist2['med'].append(score_array[i])
	# 	else:
	# 		dist2['high'].append(score_array[i])
	# for level in dist2:
	# 	print level +':'+str(len(dist2[level]))
	# plt.hist(time_array, 100)
	# plt.ylabel('Frequency')
	# plt.xlabel('Average Score Distribution')
	# plt.title('Histogram of Performance Scores')
	# plt.vlines(centroids[0,1],0,3)
	# plt.vlines(centroids[1,1],0,3)
	# plt.vlines(centroids[2,1],0,3)
	# plt.vlines(centroids2[0,1],0,3, colors='g')
	# plt.vlines(centroids2[1,1],0,3, colors='g')
	# plt.show()

	questions = np.zeros((len(score_array),6))

	for u in range(len(score_array)):
		test_params = [score_array[u], curr_array[u], time_array[u], centroids[1,0], .97, centroids[1,1], 0.01, 200]
		questions[u,0] = pa.gatingFrequencyStepWise(*test_params)
		questions[u,1] = pa.gatingFrequencyStepWisePenalty(score_array[u], curr_array[u], time_array[u], centroids[1,0], .97, centroids[1,1], 0.01, 200, 0.5)
		questions[u,2] = pa.gatingFrequencyAttenuated(*test_params)
		questions[u,3] = pa.gatingFrequencyAttenuatedContinous(*test_params)
		questions[u,4] = pa.centroidThresholdGating(score_array[u], curr_array[u], time_array[u], 0.97 , centroids, 0.1, 200)
		questions[u,5] = pa.centroidThresholdGating(score_array[u], curr_array[u], time_array[u], 0.97 , centroids2, 0.1, 200)
	print questions[:,5]
	print questions[:,4]
#questions.sort(axis=0)


# plt.figure()
# plt.plot(questions[:,0], label="Step Wise")
# plt.plot(questions[:,1], label="Step Wise with Penalty")
# plt.plot(questions[:,2], label="Freq Attenutate")
# plt.plot(questions[:,3], label="Continous Attenous")
# plt.legend()
# plt.ylabel('Number of questions')
# plt.xlabel('User')
# plt.title('Number of Questions')
# plt.show()

fig = plt.figure()

at = fig.add_subplot(121, projection='3d')
sc = at.scatter(score_array,time_array, questions[:,4], c=curr_array, marker='o', s=50)
at.set_xlabel('Scores')
at.set_ylabel('Times')
at.set_zlabel('Questions before gold')
ax = fig.add_subplot(122, projection='3d')
ax.set_xlabel('Scores')
ax.set_ylabel('Times')
ax.set_zlabel('Questions before gold')
ax.scatter(score_array,time_array, questions[:,5], c=curr_array, marker='o', s= 50)
fig.colorbar(sc)
plt.show()





