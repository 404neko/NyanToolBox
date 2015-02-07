import time
from FileSystem import *

class LogMan(object):
	def __init__(self,Path):
		self.Path=Path

	def Logger(self,Message):
		NowTime=time.strftime('%H:%M:%S')
		CreatFolder(self.Path)
		LogPath=self.Path+'/log'+time.strftime('%Y%m%d')+'.txt'
		if not os.path.isfile(LogPath):
			File=open(LogPath,'w')
		else:
			File=open(LogPath,'a')
		Message=NowTime+' -> '+Message+'\n'
		File.write(Message)
		File.close()