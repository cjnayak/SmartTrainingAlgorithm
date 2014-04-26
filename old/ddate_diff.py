import datetime

def tenure(rawDate):
	today = datetime.date.today()
	y = int(rawDate[0:4])
	m = int(rawDate[5:7])
	d = int(rawDate[-2:])
	task_date = datetime.date(y,m,d)
	diff  = today - task_date
	return diff.days

