import matplotlib.pyplot as plt
import scipy.stats as stats
import project_functions as pf
import project_algorthims as pa

#test gating algorthim
if __name__ == "__main__":
	users, batch_score = pf.readData('data/Getty_Training1.json')

	#run calculate_avg_score_per_batch on the global user scores
	global_batch = pf.calculate_avg_score_per_batch(batch_score)

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

	score_array = []
	outliers = []
	for score in scores:
		score_array.append(scores[score]["av"])
		if scores[score]["av"] > 3.0:
			outliers.append(scores[score]["av"])
		if scores[score]["av"] < -3.0:
			outliers.append(scores[score]["av"])
			print score

	score_array.sort()
	print "Outliers:"
	print outliers

	test_params = [score_array[10], 0.25612226458999177, -0.4, 0, 0, 0, 0.9, 10]
	print pa.gatingFrequencyStepWise(*test_params)
	print pa.gatingFrequencyStepWisePenalty(score_array[104], 0.25612226458999177, -0.4, 0, 0, 0, 0.9, 10, 0.5)
	print pa.gatingFrequencyAttenuated(*test_params)
	print pa.gatingFrequencyAttenuatedContinous(*test_params)





