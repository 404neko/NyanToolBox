import requests
from String import *
'''
def HaveAntiHotlink(ResourceLink,SourceDomain='http://www.example.com'):
 DirectResult=''
 ViaDomain=''
 ViaPictureServer=''
 Mode=3
 if SourceDomain=='http://www.example.com':
  Mode=2
 else:
  if GetDomain(ResourceLink)=GetDomain(SourceDomain):
   Mode=2
  else:
   Mode=3
 try:
  Request0=requests.get(ResourceLink)
 except:
  print 'An error happend when request resource from the server.'
  return -1
 else:
  DirectResult=Request0.content
 try:
  Request1=requests.get(ResourceLink)
'''

def LoadCookieLite(Json):
	import json
	try:
		JsonObject=json.loads(Json)
		Dict={}
		for Data in JsonObject:
			Dict[Data['name']]=Data['value']
		return True,Dict
	except:
		return False,None