import hashlib

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
