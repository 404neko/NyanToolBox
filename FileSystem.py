import os

def CreatFolder(Path):
	if Path.find('/')==-1:
		if not os.path.exists(Path):
			os.mkdir(Path)
	else:
		Path=Path.split('/')
		Path0=''
		for PathItem in Path:
			Path0=Path0+PathItem+'/'
			if not os.path.exists(Path0):
				os.mkdir(Path0)

def ReadForLine(FileHandle,SwitchForClose=1):
	List=[]
	while 1:
		Line=FileHandle.readline()
		if not Line:
			break
		List.append(Line)
	if SwitchForClose==1:
		FileHandle.close()
	else:
		pass
	return List

def FileNameFiler(String,Replacment=''):
	List=['/','\\','*',':','?','"','<','>','|']
	New=''
	for i in String:
		if i not in List:
			New+=i
		else:
			New+=String,Replacment
	return New