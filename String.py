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