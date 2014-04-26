import json	
import numpy as np
import matplotlib.pyplot as plt

def readData(json_file):
	with open(json_file) as data_file:    
	    data = json.load(data_file)
	users_proj = {}
	users_dur = {}
	batch_score = {}
	batch_time = {}
	dc_proj= {}
	dc_dur = {}
	users_dc = {}
	for i in range(len(data)):
		#exclude Sama Source HQ tests
		if data[i]["delivery_centers.id"] != "1":
			batchID = data[i]["gold_metrics.batch_id"]
			c_batchID = int(str(batchID))
				
			if data[i]["gold_metrics.is_correct"] == "Yes":
				corr = 1
			else:
				corr = 0
			#Creating list of all users
			uid = int(str(data[i]["users.id"]))
			duration = int(str(data[i]["gold_metrics.duration"]))
			dcid= int(str(data[i]["delivery_centers.id"]))
			
			if uid not in users_proj:
				users_proj[uid] = {"tasks": 0, "batch": {} }
			
			if uid not in users_dc:
				users_dc[uid] = dcid
				
			if uid not in users_dur	:
				users_dur[uid] = {"tasks": 0, "batch": {} }
				#users[uid]["batch"].append(c_batchID)
				#users[uid]["score"].append(corr)
			users_proj[uid]["tasks"] += 1
			users_dur[uid]["tasks"] += 1
			
			if dcid not in dc_proj:
				dc_proj[dcid] = {"batch": {}}
			
			if dcid not in dc_dur:
				dc_dur[dcid] = {"batch": {}}
				
			# Working towards Avg time by batch
				
			if batchID in batch_score:
				batch_score[c_batchID].append(corr)
			else:
				batch_score.setdefault(c_batchID, [])
				batch_score[c_batchID].append(corr)
				
			# Working towards Avg time by batch
			
			if batchID in batch_time:
				batch_time[c_batchID].append(duration)
				
			else:
				batch_time.setdefault(c_batchID, [])
				batch_time[c_batchID].append(duration)
			
			# Working towards user id: batch: score
			
			if batchID in users_proj[uid]["batch"]:
				users_proj[uid]["batch"][c_batchID].append(corr)
			else:
				users_proj[uid]["batch"].setdefault(c_batchID, [])
				users_proj[uid]["batch"][c_batchID].append(corr)
				
			# Working towards dc: batch: score
			
			if batchID in dc_proj[dcid]["batch"]:
				dc_proj[dcid]["batch"][c_batchID].append(corr)
					
			else:
				dc_proj[dcid]["batch"].setdefault(c_batchID, [])
				dc_proj[dcid]["batch"][c_batchID].append(corr)
				
			# Working towards user id: batch: duration 
					
			if batchID in users_dur[uid]["batch"]:
				users_dur[uid]["batch"][c_batchID].append(duration)
			else:
				users_dur[uid]["batch"].setdefault(c_batchID, [])
				users_dur[uid]["batch"][c_batchID].append(duration)
				
			# Working towards dc: batch: duration			
			if batchID in dc_dur[dcid]["batch"]:
				dc_dur[dcid]["batch"][c_batchID].append(duartion)
					
			else:
				dc_dur[dcid]["batch"].setdefault(c_batchID, [])
				dc_dur[dcid]["batch"][c_batchID].append(duration)
					
		# This function creates (1) UserID, Batch: Score (2) DC, Batch: Score; 	
	return users_proj, users_dur, batch_score, dc_proj, dc_dur, batch_time, users_dc
	
users_proj, users_dur, batch_score, dc_proj, dc_dur, batch_time, users_dc = readData('Getty_Gold_time.json') 

#print users_dc

def calculate_avg_score_per_batch(batch_dict):
	average_batch_score = {}
	# Calc average number, standard deviation of batch, number of jobs, 
	for batch in batch_dict:
		average_batch_score[batch] = [float(sum(batch_dict[batch]))/float(len(batch_dict[batch])), np.std(batch_dict[batch]), float(len(batch_dict[batch]))]
	return average_batch_score

global_batch = calculate_avg_score_per_batch(batch_score)
global_time = calculate_avg_score_per_batch(batch_score)

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



#calucuates z score for each batch then averages them to generate an average performance metric
def calc_user_performance_dc(user_btch_avgs, dc_batch_averages, exld):
	user_performance = {}
	for ubatch in user_btch_avgs:
		for dcid in usersdc:
	 		for project in dc_batch_averages:
	 			if ubatch == project:
					if dcid == dc:
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
test_def = calculate_avg_score_per_batch(users_proj[105]["batch"])
test_def2 = calculate_avg_score_per_batch(users_dur[105]["batch"])
test_def3 = calculate_avg_score_per_batch(dc_proj[2]["batch"])

print test_def3
#this is the test parameter for a particular batch/project we are looking at so we exclude it from their aggregate score
exclude_batch = 892

#Testing it out on user 105
one_o_five_perf, aveg_oofive = calc_user_performance(test_def, global_batch, exclude_batch)
one_o_five_time, aveg_oofive2 = calc_user_performance(test_def2, global_time, exclude_batch)
#print one_o_five_perf
#print aveg_oofive
print one_o_five_time
print aveg_oofive2

#Implement as a loop

scores = {}
for user in users_proj:
	scores[user] = {}
	scores[user]["batch"], scores[user]["av"] = calc_user_performance(users_proj[user]["batch"], global_batch, exclude_batch)

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


#plt.hist(score_array, 100)
#plt.ylabel('Frequency')
#plt.xlabel('Average Score Distribution')
#plt.title('Histogram of Performance Scores')
##plt.plot(bins, y, 'r--')
#plt.show()



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

