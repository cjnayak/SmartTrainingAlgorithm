import matplotlib.pyplot as plt
import project_functions as pf
import project_algorthims as pa
import monty
from cluster2d import cluster_svm as cluster
import numpy as np
import plottings

#test gating algorthim
if __name__ == "__main__":
	users, batch_score, users_time, batch_time = pf.readData('data/Getty_Training1.json')

	#run calculate_avg_score_per_batch on the global user scores
	global_batch = pf.calculate_avg_score_per_batch(batch_score)
	global_time = pf.calculate_avg_score_per_batch(batch_time)
	scores = {}
	#this is the test parameter for a particular batch/project we are looking at so we exclude it from their aggregate score
	current_batch = 903
	user_ten = []
	for user in users:
		if current_batch in users[user]["batch"]:
			if user != 368:
				if user != 369:
					user_ten.append(users[user]["tenure"])
					scores[user] = {}
					scores[user]["currentScore"] = pf.batch_avg(users[user]["batch"][current_batch])
					scores[user]["batch"], scores[user]["av"] = pf.calc_user_performance(users[user]["batch"], global_batch, current_batch)
					scores[user]["t_batch"], scores[user]["t_av"] = pf.calc_user_performance(users_time[user]["batch"], global_time, current_batch)

	#Create a matrix from Scores Dictionary that has UserID, Past Performance, Time Performance, and Current Score for each user
	perfMat = pf.create_perf_arrays(scores)
	#print perfMat

	#Calculate Centroids
	centroids = cluster(perfMat[:,1],perfMat[:,2], 3, "Past Score (Normalized)", "Average Time (Normalized)", False)
	centroids2 = cluster(perfMat[:,1],perfMat[:,2], 2, "Past Score (Normalized)", "Average Time (Normalized)", False)
	print centroids
	print centroids2

	#With Centroids as thresholds run each alogithm with the test parameters per users
	questions = np.zeros((len(perfMat[:,1]),6))

	for u in range(len(perfMat[:,1])):
		test_params = [perfMat[u,1], perfMat[u,3], perfMat[u,2], centroids[1,0], .98, centroids[1,1], 1, 200]
		questions[u,0] = pa.gatingFrequencyStepWise(*test_params)
		questions[u,1] = pa.gatingFrequencyStepWisePenalty(perfMat[u,1], perfMat[u,3], perfMat[u,2], centroids[1,0], .98, centroids[1,1], 1, 200, 0.5)
		questions[u,2] = pa.gatingFrequencyAttenuated(*test_params)
		questions[u,3] = pa.gatingFrequencyAttenuatedContinous(*test_params)
		questions[u,4] = pa.centroidThresholdGating(perfMat[u,1], perfMat[u,3], perfMat[u,2], 0.98 , centroids, 1, 200)
		questions[u,5] = pa.centroidThresholdGating(perfMat[u,1], perfMat[u,3], perfMat[u,2], 0.98 , centroids2, 1, 200)


	#Plot the results of the algorthim
	plottings.scatterOfClusterResults(perfMat[:,1], perfMat[:,2], perfMat[:,3], questions, 'Scores', 'Times', 'Questions before Gold')








