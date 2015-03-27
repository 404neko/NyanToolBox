from Process import *

def Joiner(*args):
	ToReturn=''
	for Item in args:
		Type=type(Item)
		if Type==str:
			ToReturn=ToReturn+Item
		if Type==int or Type==float:
			ToReturn=ToReturn+str(Item)
		if Type==None:
			if CheckSet(LogMan0):
				LogMan0.Logger('Variable '+Item.__name__+' is NoneType!')
			else:
				ToReturn=ToReturn+'!NoneType'
	return ToReturn

def GetDomain(Url):
	Pattern=re.compile(r'https://.*?/')
	Pattern0=re.compile(r'http://.*?/')
	Match=Pattern.match(Url)
	if Match:
		Domain=Match.group()
		Domain=Domain.replace('https://','')
		Domain=Domain.replace('http://','')
		Domain=Domain.replace('/','')
		return Domain
	Match=Pattern0.match(Url)
	if Match:
		Domain=Match.group()
		Domain=Domain.replace('https://','')
		Domain=Domain.replace('http://','')
		Domain=Domain.replace('/','')
		return Domain
	else:
		return 'NULL'