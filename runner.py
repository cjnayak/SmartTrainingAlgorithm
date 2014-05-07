import matplotlib.pyplot as plt
import project_functions as pf
import project_algorthims as pa
import monty
from cluster2d import cluster_svm as cluster
import numpy as np
import plottings

#test gating algorthim
if __name__ == "__main__":
	print "Reading Data..."
	users, batch_score, users_time, batch_time = pf.readData('data/Getty_Training1.json')

	#run calculate_avg_score_per_batch on the global user scores
	global_batch = pf.calculate_avg_score_per_batch(batch_score)
	global_time = pf.calculate_avg_score_per_batch(batch_time)

	scores = {}
	#this is the test parameter for a particular batch/project we are looking at so we exclude it from their aggregate score
	current_batch = 892
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
	
	#Prep for creation of beta weights
	print "Working on Beta weights..."
	regressionData = pf.regressionDataPrep(global_time,global_batch, users, users_time)
	beta_time, beta_scores, dummies = pf.weightRegressions(regressionData)
	

	#Create a matrix from Scores Dictionary that has UserID, Past Performance, Time Performance, and Current Score for each user
	perfMat = pf.create_perf_arrays(scores)
	#print perfMat

	#Calculate Centroids
	initial_centroids = np.array(([-1,1],[0,0],[1,-1]))
	initial_centroids2 = np.array(([-0.25,0.25],[0.25,-0.25]))
	centroids = cluster(perfMat[:,1],perfMat[:,2], initial_centroids, "Past Score (Normalized)", "Average Time (Normalized)", False)
	centroids2 = cluster(perfMat[:,1],perfMat[:,2], initial_centroids2, "Past Score (Normalized)", "Average Time (Normalized)", False)
	print "3 Cluster Centroids"
	print centroids
	print "2 Cluster Centroids"
	print centroids2

	#With Centroids as thresholds run each alogithm with the test parameters per users
	questions = np.zeros((len(perfMat[:,1]),6))
	base = 200
	weights = {"Current":1}
	weights["Time"], weights["Past"], newdummy = pf.weightRegressions(regressionData)
	for u in range(len(perfMat[:,1])):
		alg_params = [perfMat[u,1], perfMat[u,3], perfMat[u,2], .98, centroids, weights, base]
		questions[u,0] = pa.StepWise(*alg_params)
		questions[u,1] = pa.StepWisePenalty(perfMat[u,1], perfMat[u,3], perfMat[u,2], .98, centroids, weights, 200, 0.5)
		questions[u,2] = pa.Attenuated(*alg_params)
		questions[u,3] = pa.AttenuatedContinous(*alg_params)
		questions[u,4] = pa.centroidThreshold(*alg_params)
		questions[u,5] = pa.centroidThreshold(perfMat[u,1], perfMat[u,3], perfMat[u,2], .98, centroids2, weights, base)
	
	print "simple change"
	changeMatrix = questions - 200
	print changeMatrix

	average = np.mean(changeMatrix, axis=0)
	print "Average Change in number of tasks before gold"
	print average

	#Plot the results of the algorthim
	plottings.scatterOfClusterResults(perfMat[:,1], perfMat[:,2], perfMat[:,3], questions, 'Scores', 'Times', 'Questions before Gold')








