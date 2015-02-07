import requests

def GetContent(Address):
	Requests=requests.get(Address)
	return Requests.content

def GetFile(Address,FilePath):
	Requests=requests.get(Address)
	File=open(FilePath,'wb')
	File.write(Requests.content)
	File.close()