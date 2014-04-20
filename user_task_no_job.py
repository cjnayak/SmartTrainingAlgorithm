import json
import numpy
from pprint import pprint

with open('Getty_Gold.json') as data_file:    
    data = json.load(data_file)

print len(data)
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
		average_batch_score[batch] = [float(sum(batch_dict[batch]))/float(len(batch_dict[batch])), numpy.std(batch_dict[batch]), float(len(batch_dict[batch]))]
	return average_batch_score

#test out calculate_avg_score_per_batch on user 105
test_def = calculate_avg_score_per_batch(users[105]["batch"])

#run calculate_avg_score_per_batch on the global user scores
global_batch = calculate_avg_score_per_batch(batch_score)

#this is the test parameter for a particular batch/project we are looking at so we exclude it from their aggregate score
exclude_batch = 892
def calc_user_performance(user_btch_avgs, global_batch_averages, exld):
	user_performance = {}
	for ubatch in user_btch_avgs:
	 	for project in global_batch_averages:
	 		if ubatch == project:
		 		if project != exclude_batch:
		 			#Calculate a z-score for the user's performance = (user's batch % - project avg)/std. for the project
		 			user_performance[ubatch] = (user_btch_avgs[ubatch][0] - global_batch_averages[project][0])/global_batch_averages[project][1]
	return user_performance

#We need to decide how we are aggregating the total score- we want to encourage higher score

#Testing it out on user 105
one_o_five_perf = calc_user_performance(test_def, global_batch, exclude_batch)
print one_o_five_perf

#print users
#print len(users)
#print average_batch_score
