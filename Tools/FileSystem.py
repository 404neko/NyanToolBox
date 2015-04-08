import os
import imghdr

def PictureNameFormater(Path,Filer='/'):
	SourcePath=Path
	if os.path.isfile(Path):
		Type=imghdr.what(Path)
		if Type==None:
			pass
			print 'Nothing happend.'
		else:
			PathList=Path.split(Filer)
			FileName=PathList[-1]
			FileNameList=FileName.split('.')
			if len(FileNameList)!=1:
				FileNameList[-1]=Type
			else:
				FileNameList.append(Type)
			FileName='.'.join(FileNameList)
			PathList[-1]=FileName
			Path=Filer.join(PathList)
			try:
				os.renames(SourcePath,Path)
			except WindowsError:
				PathList=Path.split('.')
				PathList[-2]=PathList[-2]+'_0'
				Path='.'.join(PathList)
				os.renames(SourcePath,Path)