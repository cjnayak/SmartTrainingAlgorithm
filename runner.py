import matplotlib.pyplot as plt
import scipy.stats as stats
import project_functions as pf
import project_algorthims as pa
import monty
from cluster2d import cluster_svm as cluster

#test gating algorthim
if __name__ == "__main__":
	users, batch_score, users_time, batch_time = pf.readData('data/Getty_Training1.json')

	#run calculate_avg_score_per_batch on the global user scores
	global_batch = pf.calculate_avg_score_per_batch(batch_score)
	global_time = pf.calculate_avg_score_per_batch(batch_time)

	scores = {}
	#this is the test parameter for a particular batch/project we are looking at so we exclude it from their aggregate score
	exclude_batch = 517

	user_ten = []
	for user in users:
		if user != 368:
			if user != 369:
				user_ten.append(users[user]["tenure"])
				scores[user] = {}
				scores[user]["batch"], scores[user]["av"] = pf.calc_user_performance(users[user]["batch"], global_batch, exclude_batch)
				scores[user]["t_batch"], scores[user]["t_av"] = pf.calc_user_performance(users_time[user]["batch"], global_time, exclude_batch)

	score_array = []
	time_array = []
	outliers = []
	for score in scores:
		score_array.append(scores[score]["av"])
		time_array.append(scores[score]["t_av"])
		if scores[score]["av"] > 3.0:
			outliers.append(scores[score]["av"])
		if scores[score]["av"] < -3.0:
			outliers.append(scores[score]["av"])
			print score
	cluster(score_array,time_array, 3, "Past Score (Normalized)", "Average Time (Normalized)")
	score_array.sort()
	print "Outliers:"
	print outliers

	# plt.hist(time_array, 100)
	# plt.ylabel('Frequency')
	# plt.xlabel('Average Score Distribution')
	# plt.title('Histogram of Performance Scores')
	# # #plt.plot(bins, y, 'r--')
	# plt.show()


	
	print score_array[10]
	test_params = [score_array[10], 0.25612226458999177, time_array[10], 0, 0, 0, 0.01, 200]
	print pa.gatingFrequencyStepWise(*test_params)
	print pa.gatingFrequencyStepWisePenalty(score_array[104], 0.25612226458999177, time_array[10], 0, 0, 0, 0.01, 10, 0.5)
	print pa.gatingFrequencyAttenuated(*test_params)
	print pa.gatingFrequencyAttenuatedContinous(*test_params)





