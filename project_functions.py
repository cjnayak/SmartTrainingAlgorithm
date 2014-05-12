import json
import numpy as np
import datetime
from sklearn.naive_bayes import GaussianNB

def readData(json_file):
	with open(json_file) as data_file:    
	    data = json.load(data_file)
	users = {}
	batch_score = {}
	users_time = {}
	batch_time = {}

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
			ten = tenure(data[i]["gold_metrics.answered_date"])
			duration = int(str(data[i]["gold_metrics.duration"]))
			
			if uid not in users:
				users[uid] = {"tasks": 0, "batch": {}, "tenure" : ten, "dc":  float(data[i]["delivery_centers.id"])}	
				#users[uid]["batch"].append(c_batchID)
				#users[uid]["score"].append(corr)
			
			if uid not in users_time:
				users_time[uid] = {"tasks": 0, "batch": {}}
				users_time[uid]["tasks"] += 1
			
			else:
				if ten > users[uid]["tenure"]:
					users[uid]["tenure"] = ten
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

				
				if batchID in batch_time:
					batch_time[c_batchID].append(duration)
								
				else:
					batch_time.setdefault(c_batchID, [])
					batch_time[c_batchID].append(duration)
				
				if batchID in users_time[uid]["batch"]:
					users_time[uid]["batch"][c_batchID].append(duration)
				else:
					users_time[uid]["batch"].setdefault(c_batchID, [])
					users_time[uid]["batch"][c_batchID].append(duration)

	return users, batch_score, users_time, batch_time

def batch_avg(batch):
	return [float(sum(batch))/float(len(batch)), np.std(batch), float(len(batch))]

#def curr_threshold(accuracy_thres, meanScore, stdDev):
#	return (accuracy_thres - meanScore)
def zscore(x, xbar, stDev):
	return (x -xbar)/stDev

def calculate_avg_score_per_batch(batch_dict):
	average_batch_score = {}
	# Calc average number, standard deviation of batch, number of jobs, 
	for batch in batch_dict:
		average_batch_score[batch] = batch_avg(batch_dict[batch])
	return average_batch_score


#calucuates z score for each batch then averages them to generate an average performance metric
def calc_user_performance(user_btch_avgs, global_batch_averages, exld):
	user_performance = {}
	for ubatch in user_btch_avgs:
	 	for project in global_batch_averages:
	 		if ubatch == project:
		 		if project != exld:
		 			#Calculate a z-score for the user's performance = (user's batch % - project avg)/std. for the project
		 			if global_batch_averages[project][1] == 0:
		 				#Accounts for when there are uniform answers among all users for batch
		 				user_performance[ubatch] = 0
		 			else:		 				
		 				user_performance[ubatch] = zscore(user_btch_avgs[ubatch][0], global_batch_averages[project][0], global_batch_averages[project][1])
	tot_z = 0
	len_z = 0
	for b in user_performance:
		tot_z += user_performance[b]
		len_z +=1
	if len(user_performance) > 0:
		avg_z = round(tot_z/len(user_performance),9)
	else:
		avg_z = 0
	return user_performance, avg_z

#Run a loop to take global and batch averages into a functional user dictionary
def scoresLoop(users, users_time, current_batch, global_batch_scores, global_batch_time):
	scores = {}
	user_tenure = []
	for user in users:
		if current_batch in users[user]["batch"]:
			if user != 368:
				if user != 369:
					user_tenure.append(users[user]["tenure"])
					scores[user] = {}
					scores[user]["currentScore"] = batch_avg(users[user]["batch"][current_batch])
					scores[user]["batch"], scores[user]["av"] = calc_user_performance(users[user]["batch"], global_batch_scores, current_batch)
					scores[user]["t_batch"], scores[user]["t_av"] = calc_user_performance(users_time[user]["batch"], global_batch_time, current_batch)
	return scores, user_tenure

# Put the data in a format that weightRegressions can input
def regressionDataPrep(global_time,global_batch, users, users_time):
	observ = np.array(["Current","Time","Past","DC_Categorical", "batch", "tenure"])
	for batch in global_batch:
		for user in users:
			_, time = calc_user_performance(users_time[user]["batch"], global_time, "none")
			dc = users[user]["dc"]
			tenure = users[user]["tenure"]
			for ubatch in users[user]["batch"]:
				if ubatch == batch:
					newCurr = batch_avg(users[user]["batch"][batch])
					current = newCurr[0]
					_, past = calc_user_performance(users[user]["batch"], global_batch, batch)
					observ = np.vstack([observ, [current, time, past, dc, batch, tenure]])
	return observ

#Regress current accuracy on time and past performance to be used in the threshold algorthims 
def weightRegressions(regressionData):
	print "Calculating regression weights..."
	#Generate Dummy Variables for each DC
	uniques = np.unique(regressionData[1:,3])
	newDummies = np.zeros((len(regressionData[:,3]),len(uniques)))
	for i in range(len(uniques)):
		for j in range (len(regressionData)):
			if regressionData[j,4] == i:
				newDummies[j,i] = 1
	regressionData = np.hstack((regressionData,newDummies))
	regressionDat = regressionData[1:,:].astype(np.float)
	timeX = np.transpose(regressionDat[:,1])
	pastX = np.transpose(regressionDat[:,2])
	tenX = np.transpose(regressionDat[:,5])
	#dc2 = np.transpose(regressionDat[:,6])
	#dc3 = np.transpose(regressionDat[:,7])
	#dc5 = np.transpose(regressionDat[:,8])
	#dc7 = np.transpose(regressionDat[:,9])
	A = np.vstack([timeX, pastX, tenX, np.ones(len(timeX))]).T
	y = np.transpose(regressionDat[:,0])
	linReg = np.linalg.lstsq(A, y)
	betas = linReg[0]
	betaTime = betas[0]
	betaScores = betas[1]
	rSquared = (1 -linReg[1])/(y.size * y.var())
	print "rSquared"
	print rSquared
	B = np.vstack([timeX, np.ones(len(timeX))]).T
	rSquared2 = (1 - np.linalg.lstsq(B, y)[1])/(y.size * y.var())
	print rSquared2

	#Run through each user and develop a category for them:
	# 0: Bad user based off of current accuracy
	# 1: Average performance users
	# 2: High performance on score
	userCat = []
	for i in range(len(regressionDat[:,1])):
		if regressionDat[i,1] < .95:
			userCat.append(0)
		elif regressionDat[i,1] < .98:
			userCat.append(1)
		else:
			userCat.append(2)
	#run Naive Bayes on Past Performance and Time
	gnb = GaussianNB()
	y_pred = gnb.fit(regressionDat[:,1:3], userCat).predict(regressionDat[:,1:3])
	precision = 1.0 - float((userCat != y_pred).sum())/float(len(userCat))
	print precision


	return betaTime, betaScores

def create_perf_arrays(userDict):
	score_array = []
	time_array = []
	curr_array = []
	users = []
	outliers = []
	for score in userDict:
		users.append(score)
		curr_array.append(userDict[score]["currentScore"][0])
		score_array.append(userDict[score]["av"])
		time_array.append(userDict[score]["t_av"])
		if userDict[score]["av"] > 3.0:
			outliers.append(userDict[score]["av"])
		if userDict[score]["av"] < -3.0:
			outliers.append(userDict[score]["av"])
	perfMat = np.hstack([np.vstack(users), np.vstack(score_array), np.vstack(time_array), np.vstack(curr_array)])
	return perfMat

def tenure(rawDate):
	today = datetime.date.today()
	y = int(rawDate[0:4])
	m = int(rawDate[5:7])
	d = int(rawDate[-2:])
	task_date = datetime.date(y,m,d)
	diff  = today - task_date
	return diff.days

def chooseBatch(batches):
	mxBatchlen = 0
	mxBatch = 0
	for batch in batches:
		if len(batches[batch]) > mxBatchlen:
			mxBatch = batch
			mxBatchlen = len(batches[batch])
	return mxBatch

def secondRound(last_score, current_score, new_base, cent3, cent2, betas, questions_cap, old_perf):
	secondRoundOutput = np.zeros((len(perfMat[:,1]),4))
	newRegXY = np.array(["change", "questions"])
	for i in len(last_score):
		secondRoundOutput[i,0] = current_score - last_score
		# If last score was perfect, keep weight at 1
		if last_score == 1.0:
			secondRoundOutput[i,1] = 1
		else:
			newRegXY = np.vstack([newRegXY, [current_score - last_score, new_base[i]]])
	X = np.transpose(newRegXY[:,0])
	A = np.vstack([X, np.ones(len(X))]).T
	Y = np.transpose(newRegXY[:,1])
	newWeight = np.linalg.lstsq(A, Y)[0][0]
	betas["Current"] = newWeight
	for u in range(len(secondRoundOutput[:,1])):
		#Attenuated Cluster Algorthims of Interest
		secondRoundOutput[u,2] = pa.centroidThreshold(*alg_params)
		secondRoundOutput[u,3] = pa.centroidThreshold(current_score[u], perfMat[u,3], perfMat[u,2], .98, centroids2, betas, new_base[u])
	#Adjust for Questions cap
	return secondRoundOutput

