import hashlib
import os,sys

def GetFileMd5(FilePath):
	if not os.path.isfile(FilePath):
		return
	Hash=hashlib.md5()
	File=file(FilePath,'rb')
	while True:
		Bin=File.read(8096)
		if not Bin :
			break
		Hash.update(Bin)
	File.close()
	return Hash.hexdigest()

def Hasher(HashFile,Aim):
	Hasher=open(HashFile,'a')
	Contect=GetFileMd5(Aim)+'\n'
	Hasher.write(Contect)
	Hasher.close()
	Hasher=open(HashFile,'r')
	HasherList=[]
	while 1:
		Line=Hasher.readline()
		if not Line:
			break
		HasherList.append(Line)
	Counter=0
	for HasherItem in HasherList:
		if HasherItem.replace('\n','')==GetFileMd5(Aim):
			Counter=Counter+1
		else:
			continue
	return Counter
