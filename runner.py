import sys
import matplotlib.pyplot as plt
import project_functions as pf
import project_algorthims as pa
import monty
from cluster2d import cluster_svm as cluster
import numpy as np
import plottings

#test gating algorthim
if __name__ == "__main__":
	averagesum_2 = 0
	averagesum_3 = 0	
	profit_sum2 = 0
	profit_sum3 = 0 
	for i in xrange(30):
		print "Reading Data..."
		sys_arguments = sys.argv
		users, batch_score, users_time, batch_time = pf.readData(sys_arguments[1])

		#run calculate_avg_score_per_batch on the global user scores
		global_batch = pf.calculate_avg_score_per_batch(batch_score)
		global_time = pf.calculate_avg_score_per_batch(batch_time)

		#Prep for creation of beta weights
		print "Working on prepping data for regression weights..."
		regressionData = pf.regressionDataPrep(global_time,global_batch, users, users_time)

		#this is the test parameter for a particular batch/project we are looking at so we exclude it from their aggregate score
		#this will default to the largest batch in the file, but can be set at the command line by using the word batch and then putting the batch number
		if len(sys_arguments) > 2:
			if sys_arguments[2] == "batch":
				mxBatch = int(sys_arguments[3])
				if mxBatch not in global_batch:
					print "there are no tasks in this batch, reverting to longest batch"
					mxBatch = pf.chooseBatch(batch_score)
		else:
			mxBatch = pf.chooseBatch(batch_score)
		print '\033[1m' + "Current Batch: " +str(mxBatch) + '\033[0m'
		
		#Create a user dictionary based of of individual users and global scores
		scores, user_ten = pf.scoresLoop(users, users_time, mxBatch, global_batch, global_time)

		#Create a matrix from Scores Dictionary that has UserID, Past Performance, Time Performance, and Current Score for each user
		perfMat = pf.create_perf_arrays(scores)

		#Calculate Centroids
		#initial_centroids = np.array(([-0.5,0.5],[0,0],[0.5,-0.5]))
		#initial_centroids2 = np.array(([-0.25,0.25],[0.25,-0.25]))
		centroids = cluster(perfMat[:,1],perfMat[:,2], 3, "Past Score (Normalized)", "Average Time (Normalized)", False)
		centroids2 = cluster(perfMat[:,1],perfMat[:,2], 2, "Past Score (Normalized)", "Average Time (Normalized)", False)
		print " "
		print '\033[1m' + "Centroid Cutoffs" '\033[0m'
		print "3 Cluster Centroids"
		print centroids
		print "2 Cluster Centroids"
		print centroids2

		#With Centroids as thresholds run each alogithm with the test parameters per users
		base = 200
		weights = {"Current":1}
		weights["Time"], weights["Past"] = pf.weightRegressions(regressionData)
		print " "
		print '\033[1m' + "Algorthim weights:" + '\033[0m'
		print "Time Weight:" + str(weights["Time"])
		print "Past Score Weight:" + str(weights["Past"])

		#With our weights and centroids compute every user's estimated number of questions before 
		#gold using each of our 6 algorthims
		questions = np.zeros((len(perfMat[:,1]),6))
		for u in range(len(perfMat[:,1])):
			alg_params = [perfMat[u,1], perfMat[u,3], perfMat[u,2], .98, centroids, weights, base]
			#Old Algorthims
			questions[u,0] = pa.StepWise(*alg_params)
			questions[u,1] = pa.StepWisePenalty(perfMat[u,1], perfMat[u,3], perfMat[u,2], .98, centroids, weights, 200, 0.5)
			questions[u,2] = pa.Attenuated(*alg_params)
			questions[u,3] = pa.AttenuatedContinous(*alg_params)

			#Attenuated Cluster Algorthims of Insterest
			questions[u,4] = pa.centroidThreshold(*alg_params)
			questions[u,5] = pa.centroidThreshold(perfMat[u,1], perfMat[u,3], perfMat[u,2], .98, centroids2, weights, base)
		
		#Now that we have questions before gold, this parameter calculates the profits from the first batch of work based on Samasource profit measurements. 
		questions_norm = [200]*len(questions[:,:])

		profit_3 = 0
		profit_2 = 0
		profit_norm = 0
		for i in range(len(questions[:,:])):
			profit_3 += (0.0348*questions[i,4])-((.0008*(questions[i,4])*22) + (.000225*questions[i,4])+(.0000066*questions[i,4]))
			profit_2 += (0.0348*questions[i,5])-((.0008*(questions[i,5])*22) + (.000225*questions[i,5])+(.0000066*questions[i,5]))
			profit_norm += (0.0348*questions_norm[i])-((.0008*(questions_norm[i])*22) + (.00045*questions_norm[i])+(.0000132*questions_norm[i]))
		
		profit_sum3 += profit_2
		profit_sum2 += profit_3
		
		print "Profit for 3 Clusters"
		print profit_3
		
		print "Profit for 2 Clusters"
		print profit_2
		
		print "Profit for Base Gating Algorithm"
		print profit_norm
		
		print " "
		print '\033[1m' + "How many questions have been added or subtracted"+ '\033[0m'
		print "StepWise StepWisePenalty Attenuated AttenuatedContinous 2Cluster 3Cluster"
		changeMatrix = questions - 200
		print changeMatrix

		average = np.mean(changeMatrix, axis=0)
		averagesum_2 += average[4]
		averagesum_3 += average[5]
		
		print " "
		print '\033[1m' + "Average Change in number of tasks before gold" + '\033[0m'
		print "StepWise StepWisePenalty Attenuated AttenuatedContinous 2Cluster 3Cluster"
		print average

		#Plot the results of the algorthim
		#plottings.score_centroid_distributions(perfMat[:,1], centroids, centroids2)
		#plottings.tenure_to_performance_plot(perfMat[:,1],user_ten, "Tenure", "Scores")
		#plottings.scatterOfClusterResults(perfMat[:,1], perfMat[:,2], perfMat[:,3], questions, 'Scores', 'Times', 'Questions before Gold')

		## For a given project, once implemented the file would run the following function after the 
		#questionsCap = [50, 400]
		#secondRoundOutput = pf.secondRound(perfMat[:,1], newScores, questions[:,4:], centroids, centroids2, weights, questionsCap, perfMat)
	print profit_sum3
	print profit_sum2
	print profit_norm *30
	
	print "Average Change before gold 2 centroids"
	print averagesum_2
	print "Average Change before gold 3 centroids"
	print averagesum_3
	
	print "Less Gold"
	lessGold = ((20/(averagesum_3+200))*300000)-((20/(200))*300000)
	print lessGold
	
	print "Gold Savings"
	goldSavings = lessGold*.03
	print goldSavings

	




