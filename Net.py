#-*- coding:utf-8 -*-

import os
from i233n import Chinese

#Define
CommandLineLang='GBK'

def PingTest(Aim,Total=10):
	OutPut=os.popen('ping -n '+str(Total)+' '+Aim)
	OutPut=OutPut.read()
	OutPut=OutPut.split('\n')[1:Total+2]
	Success=0
	Time=0
	for Item in OutPut:
		if Item[:4].decode(CommandLineLang)==Chinese.Lang['Success']:
			Success+=1
			Time+=int(Item.split(' ')[-2].replace('<','=').split('=')[-1][:-2])
	return [Time,Success,Total]