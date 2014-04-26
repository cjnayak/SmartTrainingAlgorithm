import json
import numpy as np
import matplotlib.pyplot as plt
from ddate_diff import tenure as tenure

tenure("2013-01-22")


def readData(json_file):
	with open(json_file) as data_file:    
	    data = json.load(data_file)
	users = {}
	batch_score = {}
	for i in range(len(data)):
		#exclude Sama Source HQ tests
		if data[i]["delivery_centers.id"] != "1":
			batchID = data[i]["gold_metrics.batch_id"]
			c_batchID = int(str(batchID))
			if data[i]["gold_metrics.is_correct"] == "Yes":
				corr = 1
			else:
				corr = 0
			uid = int(str(data[i]["users.id"]))
			if uid not in users:
				users[uid] = {"tasks": 0, "batch": {} }
				
				#users[uid]["batch"].append(c_batchID)
				#users[uid]["score"].append(corr)
			users[uid]["tasks"] += 1

			if batchID in batch_score:
				batch_score[c_batchID].append(corr)
			else:
				batch_score.setdefault(c_batchID, [])
				batch_score[c_batchID].append(corr)
			
			if batchID in users[uid]["batch"]:
				users[uid]["batch"][c_batchID].append(corr)
			else:
				users[uid]["batch"].setdefault(c_batchID, [])
				users[uid]["batch"][c_batchID].append(corr)
	return users, batch_score

users, batch_score = readData('data/Getty_Gold.json')

def calculate_avg_score_per_batch(batch_dict):
	average_batch_score = {}
	# Calc average number, standard deviation of batch, number of jobs, 
	for batch in batch_dict:
		average_batch_score[batch] = [float(sum(batch_dict[batch]))/float(len(batch_dict[batch])), np.std(batch_dict[batch]), float(len(batch_dict[batch]))]
	return average_batch_score

#run calculate_avg_score_per_batch on the global user scores
global_batch = calculate_avg_score_per_batch(batch_score)

#calucuates z score for each batch then averages them to generate an average performance metric
def calc_user_performance(user_btch_avgs, global_batch_averages, exld):
	user_performance = {}
	for ubatch in user_btch_avgs:
	 	for project in global_batch_averages:
	 		if ubatch == project:
		 		if project != exclude_batch:
		 			#Calculate a z-score for the user's performance = (user's batch % - project avg)/std. for the project
		 			user_performance[ubatch] = (user_btch_avgs[ubatch][0] - global_batch_averages[project][0])/global_batch_averages[project][1]
	tot_z = 0
	len_z = 0
	for b in user_performance:
		tot_z += user_performance[b]
		len_z +=1
	avg_z = tot_z/len(user_performance)
	return user_performance, avg_z

#test out calculate_avg_score_per_batch on user 105
test_def = calculate_avg_score_per_batch(users[105]["batch"])

#this is the test parameter for a particular batch/project we are looking at so we exclude it from their aggregate score
exclude_batch = 892

#Testing it out on user 105
one_o_five_perf, aveg_oofive = calc_user_performance(test_def, global_batch, exclude_batch)
#print one_o_five_perf
#print aveg_oofive

#Implement as a loop
#print users

scores = {}
for user in users:
	scores[user] = {}
	scores[user]["batch"], scores[user]["av"] = calc_user_performance(users[user]["batch"], global_batch, exclude_batch)

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



#stepwise frequency gating
def gatingFrequencyStepWise(user_past_score, current_batch_score, average_time_score, past_threshold, current_threshold, time_threshold, reduction_rate, base):
	number_of_questions_before_gold = base
	if user_past_score > past_threshold:
		number_of_questions_before_gold += number_of_questions_before_gold*reduction_rate
	if current_batch_score > current_threshold:
		number_of_questions_before_gold += number_of_questions_before_gold*reduction_rate
	if average_time_score < time_threshold:
		number_of_questions_before_gold += number_of_questions_before_gold*reduction_rate
	
	return number_of_questions_before_gold

#stepwise frequency gating with Penalty (in terms of z)
def gatingFrequencyStepWisePenalty(user_past_score, current_batch_score, average_time_score, past_threshold, current_threshold, time_threshold, reduction_rate, base, penalty):
	number_of_questions_before_gold = base
	if user_past_score > past_threshold:
		number_of_questions_before_gold += number_of_questions_before_gold*reduction_rate
	if user_past_score < (past_threshold - penalty):
		number_of_questions_before_gold -= number_of_questions_before_gold*reduction_rate

	if current_batch_score > current_threshold:
		number_of_questions_before_gold += number_of_questions_before_gold*reduction_rate
	if current_batch_score < (current_threshold - penalty):
		number_of_questions_before_gold -= number_of_questions_before_gold*reduction_rate

	if average_time_score < time_threshold:
		number_of_questions_before_gold += number_of_questions_before_gold*reduction_rate
	if average_time_score > (time_threshold - penalty):
		number_of_questions_before_gold -= number_of_questions_before_gold*reduction_rate
	
	return number_of_questions_before_gold

#attenuated frequency algorthim
def gatingFrequencyAttenuated(user_past_score, current_batch_score, average_time_score, past_threshold, current_threshold, time_threshold, reduction_rate, base):
	number_of_questions_before_gold = base
	if user_past_score > past_threshold:
		number_of_questions_before_gold += number_of_questions_before_gold*reduction_rate*(user_past_score-past_threshold)
	if current_batch_score > current_threshold:
		number_of_questions_before_gold += number_of_questions_before_gold*reduction_rate*(current_batch_score - current_threshold)

	#time would need a weighting constant
	if average_time_score < time_threshold:
		number_of_questions_before_gold += number_of_questions_before_gold*reduction_rate*(average_time_score - time_threshold)
	
	return number_of_questions_before_gold	

def gatingFrequencyAttenuatedContinous(user_past_score, current_batch_score, average_time_score, past_threshold, current_threshold, time_threshold, reduction_rate, base):
	number_of_questions_before_gold = base
	number_of_questions_before_gold += number_of_questions_before_gold*reduction_rate*(user_past_score-past_threshold) + number_of_questions_before_gold*reduction_rate*(current_batch_score - current_threshold) + number_of_questions_before_gold*reduction_rate*(average_time_score - time_threshold)
	return number_of_questions_before_gold	



#print scores

#test gating algorthim
stw = gatingFrequencyStepWise(score_array[104], 0.25612226458999177, -0.4, 0, 0, 0, 0.9, 10 )
stwpen = gatingFrequencyStepWisePenalty(score_array[104], 0.25612226458999177, -0.4, 0, 0, 0, 0.9, 10, 0.5 )
atten = gatingFrequencyAttenuated(score_array[104], 0.25612226458999177, -0.4, 0, 0, 0, 0.9, 10 )
attenCont = gatingFrequencyAttenuatedContinous(score_array[104], 0.25612226458999177, -0.4, 0, 0, 0, 0.9, 10 )

print score_array[104]
print stw
print stwpen
print atten
print attenCont



