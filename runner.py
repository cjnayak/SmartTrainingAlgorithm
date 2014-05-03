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
	exclude_batch = 517
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
	cluster(score_array,time_array, 3, "Past Score (Normalized)", "Average Time (Normalized)", False)
	#score_array.sort()
	print "Outliers:"
	print outliers

	# plt.hist(time_array, 100)
	# plt.ylabel('Frequency')
	# plt.xlabel('Average Score Distribution')
	# plt.title('Histogram of Performance Scores')
	# # #plt.plot(bins, y, 'r--')
	# plt.show()

	questions = np.zeros((len(score_array),4))

	for u in range(len(score_array)):
		test_params = [score_array[u], curr_array[u], time_array[u], 0, .97, 0, 0.01, 200]
		questions[u,0] = pa.gatingFrequencyStepWise(*test_params)
		questions[u,1] = pa.gatingFrequencyStepWisePenalty(score_array[u], curr_array[u], time_array[u], 0, .97, 0, 0.01, 200, 0.5)
		questions[u,2] = pa.gatingFrequencyAttenuated(*test_params)
		questions[u,3] = pa.gatingFrequencyAttenuatedContinous(*test_params)
	print questions

questions.sort(axis=0)

plt.figure()
plt.plot(questions[:,0], label="Step Wise")
plt.plot(questions[:,1], label="Step Wise with Penalty")
plt.plot(questions[:,2], label="Freq Attenutate")
plt.plot(questions[:,3], label="Continous Attenous")
plt.legend()
plt.ylabel('Number of questions')
plt.xlabel('User')
plt.title('Number of Questions')
plt.show()





