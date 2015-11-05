import requests
import sys
try:
    import cPickle as pickle
except:
    import pickle

Method=['POS','GET']
#Enviroment={'Windows':'%Temp%','Linux':'/tmp'}

def Parse_Fiddler(FiddlerString):
    FiddlerList=FiddlerString.split('\n')
    One=FiddlerList.pop(0)
    OneList=One.split(' ')
    Method=OneList[0]
    if OneList[1][0]!='h':
        Two=FiddlerList.pop(0)
        Url=''.join['http://',Two.split(': ')[-1],OneList[1]]
    else:
        Url=OneList[1]
        FiddlerList.pop(0)
    Header={}
    for Line in FiddlerList:
        if Line!='':
            LinePart=Line.split(': ')
            Header[LinePart[0]]=LinePart[1]
        else:
            continue
    return {'Method':Method,'Header':Header,'Url':Url}

def MakeRequest(RequestObject):
    Session=requests.Session()
    if RequestObject['Method']=='GET':
        Response=Session.get(RequestObject['Url'],headers=RequestObject['Header'])
    else:
        Response=Session.post(RequestObject['Url'],headers=RequestObject['Header'])
    return Session,Response

#need rewrite
def Initialize(FiddlerObject):
    if type(FiddlerObject)==str:
        if FiddlerObject[:3] in Method:
            return Parse_Fiddler(FiddlerObject)
        else:
            sys.stderr.write(''.join(['Error: Input "',FiddlerObject[:16],'" has no correct format.\n']))
    else:
        try:
            FiddlerString=FiddlerObject.read()
            FiddlerObject.close()
        except:
            sys.stderr.write(''.join(['Error: Input object is not a "File" object.\n']))
            FiddlerObject.close()
            return -1
        if FiddlerString[:3] in Method:
            return Parse_Fiddler(FiddlerString)
        else:
            sys.stderr.write(''.join(['Error: Input "',FiddlerString[:16],'" has no correct format.\n']))

if __name__=='__main__':
    Flag_Debug=False
    Flag_Quite=False
    if len(sys.argv)==1:
        sys.stdout.write('You should import it as a library or use "Fiddler2requests RequestContent.File"\n')
    else:
        for arg in sys.argv:
            if arg.lower()=='-d':
                Flag_Debug=True
            if arg[0]!='-':
                FileName=arg
            if arg.lower()=='-q':
                Flag_Quite=True
        try:
            FileHandle=open(sys.argv[1])
            Session,Response=MakeRequest(Initialize(FileHandle))
            FileHandle.close()
            if not Flag_Quite:
                print Response
            else:
                pass
            if Flag_Debug==True:
                FileHandle_Debug=open(FileName+'.rdump','wb')
                FileHandle_Debug.write(pickle.dumps([Session,Response]))
                FileHandle_Debug.close()
        except:
            sys.stderr.write(''.join(['Error: Input object is not a "File" object.\n']))
