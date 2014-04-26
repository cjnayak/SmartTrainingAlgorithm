import json
import numpy as np
import datetime

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

def calculate_avg_score_per_batch(batch_dict):
	average_batch_score = {}
	# Calc average number, standard deviation of batch, number of jobs, 
	for batch in batch_dict:
		average_batch_score[batch] = [float(sum(batch_dict[batch]))/float(len(batch_dict[batch])), np.std(batch_dict[batch]), float(len(batch_dict[batch]))]
	return average_batch_score


#calucuates z score for each batch then averages them to generate an average performance metric
def calc_user_performance(user_btch_avgs, global_batch_averages, exld):
	user_performance = {}
	for ubatch in user_btch_avgs:
	 	for project in global_batch_averages:
	 		if ubatch == project:
		 		if project != exld:
		 			#Calculate a z-score for the user's performance = (user's batch % - project avg)/std. for the project
		 			user_performance[ubatch] = (user_btch_avgs[ubatch][0] - global_batch_averages[project][0])/global_batch_averages[project][1]
	tot_z = 0
	len_z = 0
	for b in user_performance:
		tot_z += user_performance[b]
		len_z +=1
	avg_z = tot_z/len(user_performance)
	return user_performance, avg_z

def tenure(rawDate):
	today = datetime.date.today()
	y = int(rawDate[0:4])
	m = int(rawDate[5:7])
	d = int(rawDate[-2:])
	task_date = datetime.date(y,m,d)
	diff  = today - task_date
	return diff.days


