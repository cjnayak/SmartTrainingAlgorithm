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
