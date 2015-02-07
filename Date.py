import time
import datetime

def Today():
	Today=time.strftime('%Y%m%d')
	return Today

def IntervalTimer(Interval='Y'):
	if Interval=='Y':
		return time.strftime('%Y')
	if Interval=='M':
		return time.strftime('%Y%m')
	if Interval=='D':
		return time.strftime('%Y%m%d')

def ConversionDate(DayPast):
	DayStart=datetime.date(1899,12,30)
	DayPast=datetime.timedelta(days=DayPast)
	TrueDate=DayStart+DayPast
	return TrueDate.strftime('%Y%m%d')