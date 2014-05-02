	# user_ten.sort()
	# plt.ylabel('Frequency')
	# plt.xlabel('User Tenure')
	# plt.title('Number of days since first Sama Source task')
	# plt.hist(user_ten, 100)
	# plt.show()

	# perftoscore = []
	# for i in range(len(user_ten)):
	# 	perftoscore.append(score_array[i]/user_ten[i])

	# perftoscore.sort()
	# plt.ylabel('Frequency')
	# plt.xlabel('User Tenure to Performance Ratio')
	# plt.title('Number of days since first Sama Source task')
	# plt.hist(perftoscore, 100)
	# plt.show()
	slope, intercept, r_value, p_value, std_err = stats.linregress(user_ten,score_array)
	print slope
	print r_value
	plt.scatter(user_ten,score_array)
	plt.show()

	plt.hist(score_array, 100)
	plt.ylabel('Frequency')
	plt.xlabel('Average Score Distribution')
	plt.title('Histogram of Performance Scores')
	# #plt.plot(bins, y, 'r--')
	plt.show()
