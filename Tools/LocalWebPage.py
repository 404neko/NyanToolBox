import re,requests,os

Folder='./Picture/'
NoPic=Folder+'None.png'

def FileNameFiler(String):
	List=['/','\\','*',':','?','"','<','>','|']
	New=''
	for i in String:
		if i not in List:
			New+=i
		else:
			pass
	return New

def Filer(String):
	if String.split('.')[-1]!='html':
		return False
	else:
		return True

def OpenDir(Path='.',Filer=None):
	if Filer==None:
		return os.listdir(Path)
	else:
		Filer_=[]
		for Item in os.listdir(Path):
			if Filer(Item):
				Filer_.append(Item)
			else:
				pass
		return Filer_

def AzPage(String):
	List=re.findall('''(src=('|").*?("|'))''',String)
	return String,List


for Item in OpenDir(Filer=Filer):
	with open(Item,'r') as File:
		String,Content=AzPage(File.read())
	for Picture in Content:
		Url=Picture[0][5:-1]
		try:
			print Url
			Repson=requests.get(Url)
			Name=FileNameFiler(Url.split('/')[-1])
			with open(Folder+Name,'wb') as File:
				File.write(Repson.content)
			print String.find(Picture[0])
			String=String.replace(Picture[0],'src="'+Folder+Name+'" ')
		except:
			String=String.replace(Url,NoPic)
	with open(Item,'w') as File:
		File.write(String)