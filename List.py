def OpenUpList(List):
	Flag_NoOpenUpAction=0
	NewList=[]
	while Flag_NoOpenUpAction!=1:
		NewList=[]
		Flag_NoOpenUpAction=1
		for ListItem in List:
			if type(ListItem)!=list:
				NewList.append(ListItem)
			else:
				Flag_NoOpenUpAction=0
				for ListItem_0 in ListItem:
					NewList.append(ListItem_0)
		List=NewList
	return NewList
#I often use this method in C, but it is not the best method.The best method is recursion =3=.

def FillUpList(List,TargetLength,Filler=''):
	if len(List)<TargetLength:
		#for i in range(TargetLength-len(List)):
		FillerList=[Filler]*(TargetLength-len(List))
		return List+FillerList
	else:
		return List