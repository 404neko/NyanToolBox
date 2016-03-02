import hashlib
import os

def GetFileMD5(FilePath):
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

def GetMD5(Data):
    Hash=hashlib.md5()
    Hash.update(Data)
    return Hash.hexdigest()