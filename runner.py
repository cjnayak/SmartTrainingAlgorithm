import matplotlib.pyplot as plt
import project_functions as pf
import project_algorthims as pa

#test gating algorthim
if __name__ == "__main__":
	pf.tenure("2013-01-22")
	users, batch_score = pf.readData('data/Getty_Gold.json')

	#run calculate_avg_score_per_batch on the global user scores
	global_batch = pf.calculate_avg_score_per_batch(batch_score)

	scores = {}
	#this is the test parameter for a particular batch/project we are looking at so we exclude it from their aggregate score
	exclude_batch = 892

	for user in users:
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
	score_array.sort()
	print "Outliers:"
	print outliers


	plt.hist(score_array, 100)
	plt.ylabel('Frequency')
	plt.xlabel('Average Score Distribution')
	plt.title('Histogram of Performance Scores')
	#plt.plot(bins, y, 'r--')
	plt.show()


	stw = pa.gatingFrequencyStepWise(score_array[104], 0.25612226458999177, -0.4, 0, 0, 0, 0.9, 10 )
	stwpen = pa.gatingFrequencyStepWisePenalty(score_array[104], 0.25612226458999177, -0.4, 0, 0, 0, 0.9, 10, 0.5 )
	atten = pa.gatingFrequencyAttenuated(score_array[104], 0.25612226458999177, -0.4, 0, 0, 0, 0.9, 10 )
	attenCont = pa.gatingFrequencyAttenuatedContinous(score_array[104], 0.25612226458999177, -0.4, 0, 0, 0, 0.9, 10 )

	print score_array[104]
	print stw
	print stwpen
	print atten
	print attenCont

###OLD CODE
#test out calculate_avg_score_per_batch on user 105
#test_def = calculate_avg_score_per_batch(users[105]["batch"])

#Testing it out on user 105
#one_o_five_perf, aveg_oofive = calc_user_performance(test_def, global_batch, exclude_batch)
#print one_o_five_perf
#print aveg_oofive

#Implement as a loop
#print users



