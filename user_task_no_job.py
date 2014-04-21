import json
import numpy as np
import matplotlib.pyplot as plt

with open('Getty_Gold.json') as data_file:    
    data = json.load(data_file)

users = {}
batch_score = {}
for i in range(len(data)):
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
#one_o_five_perf, aveg_oofive = calc_user_performance(test_def, global_batch, exclude_batch)
#print one_o_five_perf
#print aveg_oofive

#Implement as a loop
#print users

scores = {}
for user in users:
	scores[user] = {}
	scores[user]["batch"], scores[user]["av"] = calc_user_performance(users[user]["batch"], global_batch, exclude_batch)

score_array = []
for score in scores:
	score_array.append(scores[score]["av"])
score_array.sort()

plt.hist(score_array, 50)
plt.ylabel('Average Score Distribution')
plt.show()

	

#print scores

