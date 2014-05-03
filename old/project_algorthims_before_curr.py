#stepwise frequency gating
def gatingFrequencyStepWise(user_past_score, current_batch_score, average_time_score, past_threshold, current_threshold, time_threshold, delta, base):
	num_bf_gold = base
	if user_past_score > past_threshold:
		num_bf_gold += base*delta
	if current_batch_score > current_threshold:
		num_bf_gold += base*delta
	if average_time_score < time_threshold:
		num_bf_gold += base*delta
	
	return num_bf_gold

#stepwise frequency gating with Penalty (in terms of z)
def gatingFrequencyStepWisePenalty(user_past_score, current_batch_score, average_time_score, past_threshold, current_threshold, time_threshold, delta, base, penalty):
	num_bf_gold = base
	if user_past_score > past_threshold:
		num_bf_gold += base*delta
	if user_past_score < (past_threshold - penalty):
		num_bf_gold -= base*delta

	if current_batch_score > current_threshold:
		num_bf_gold += base*delta
	if current_batch_score < (current_threshold - penalty):
		num_bf_gold -= base*delta

	if average_time_score < time_threshold:
		num_bf_gold += base*delta
	if average_time_score > (time_threshold + penalty):
		num_bf_gold -= base*delta
	
	return num_bf_gold

#attenuated frequency algorthim
def gatingFrequencyAttenuated(user_past_score, current_batch_score, average_time_score, past_threshold, current_threshold, time_threshold, delta, base):
	num_bf_gold = base
	if user_past_score > past_threshold:
		num_bf_gold += base*delta*(user_past_score-past_threshold)
		print "above score"
	if current_batch_score > current_threshold:
		num_bf_gold += base*delta*(current_batch_score - current_threshold)
		print "above current"

	#time would need a weighting constant
	if average_time_score < time_threshold:
		num_bf_gold += -1*base*delta*(average_time_score - time_threshold)
		print "fast"
	
	return num_bf_gold	

def gatingFrequencyAttenuatedContinous(user_past_score, current_batch_score, average_time_score, past_threshold, current_threshold, time_threshold, delta, base):
	num_bf_gold = base
	num_bf_gold += num_bf_gold*delta*(user_past_score-past_threshold) + num_bf_gold*delta*(current_batch_score - current_threshold) + (-1*num_bf_gold*delta*(average_time_score - time_threshold))
	return num_bf_gold	
