import datetime
import xlrd
import zipfile,string,sys,os,re,csv
import xml.parsers.expat
from Date import *
from xml.dom import minidom
from optparse import OptionParser
from bs4 import BeautifulSoup

StartDate=datetime.date(1899,12,31).toordinal()-1
FORMATS={
			'general' : 'float',
			'0' : 'float',
			'0.00' : 'float',
			'#,##0' : 'float',
			'#,##0.00' : 'float',
			'0%' : 'percentage',
			'0.00%' : 'percentage',
			'0.00e+00' : 'float',
			'mm-dd-yy' : 'date',
			'd-mmm-yy' : 'date',
			'd-mmm' : 'date',
			'mmm-yy' : 'date',
			'h:mm am/pm' : 'date',
			'h:mm:ss am/pm' : 'date',
			'h:mm' : 'time',
			'h:mm:ss' : 'time',
			'm/d/yy h:mm' : 'date',
			'#,##0 ;(#,##0)' : 'float',
			'#,##0 ;[red](#,##0)' : 'float',
			'#,##0.00;(#,##0.00)' : 'float',
			'#,##0.00;[red](#,##0.00)' : 'float',
			'mm:ss' : 'time',
			'[h]:mm:ss' : 'time',
			'mmss.0' : 'time',
			'##0.0e+0' : 'float',
			'@' : 'float',
			'yyyy\\-mm\\-dd' : 'date',
			'dd/mm/yy' : 'date',
			'hh:mm:ss' : 'time',
			"dd/mm/yy\\ hh:mm" : 'date',
			'dd/mm/yyyy hh:mm:ss' : 'date',
			'yy-mm-dd' : 'date',
			'd-mmm-yyyy' : 'date',
			'm/d/yy' : 'date',
			'm/d/yyyy' : 'date',
			'dd-mmm-yyyy' : 'date',
			'dd/mm/yyyy' : 'date',
			'mm/dd/yy hh:mm am/pm' : 'date',
			'mm/dd/yyyy hh:mm:ss' : 'date',
			'yyyy-mm-dd hh:mm:ss' : 'date'
		}
STANDARD_FORMATS={
					0 : 'general',
					1 : '0',
					2 : '0.00',
					3 : '#,##0',
					4 : '#,##0.00',
					9 : '0%',
					10 : '0.00%',
					11 : '0.00e+00',
					12 : '# ?/?',
					13 : '# ??/??',
					14 : 'mm-dd-yy',
					15 : 'd-mmm-yy',
					16 : 'd-mmm',
					17 : 'mmm-yy',
					18 : 'h:mm am/pm',
					19 : 'h:mm:ss am/pm',
					20 : 'h:mm',
					21 : 'h:mm:ss',
					22 : 'm/d/yy h:mm',
					37 : '#,##0 ;(#,##0)',
					38 : '#,##0 ;[red](#,##0)',
					39 : '#,##0.00;(#,##0.00)',
					40 : '#,##0.00;[red](#,##0.00)',
					45 : 'mm:ss',
					46 : '[h]:mm:ss',
					47 : 'mmss.0',
					48 : '##0.0e+0',
					49 : '@'
				}
AddSheetHead='"Fund_name","Fund_ticker","Download_date","Data_date",'

def Affix(FileContentList,ETFName,Ticker,DownloadDate,DataDate):
	ToAdd='"'+ETFName+'","'+Ticker+'","'+Today()+'","'+DataDate+'",'
	FileContentList[0]=AddSheetHead+FileContentList[0]
	for i in range(1,len(FileContentList)):
		FileContentList[i]=ToAdd+FileContentList[i]
	return FileContentList


def DropHeadTail(Content,Head,Tail):
	ContentText=Content
	Content=Content.split('\n')
	if Head>len(Content) or Tail>len(Content):
		return ContentText,-1
	NewContent=[]
	for i in range(Head,0-Tail):
		NewContent.append(Content[i])
	ReturnContent=''
	for NewContentItem in NewContent:
		ReturnContent=NewContentItem+'\n'
	return ReturnContent,1



def GetDomain(Url):
	Pattern=re.compile(r'https://.*?/')
	Pattern0=re.compile(r'http://.*?/')
	Match=Pattern.match(Url)
	if Match:
		Domain=Match.group()
		Domain=Domain.replace('https://','')
		Domain=Domain.replace('http://','')
		Domain=Domain.replace('/','')
		return Domain
	Match=Pattern0.match(Url)
	if Match:
		Domain=Match.group()
		Domain=Domain.replace('https://','')
		Domain=Domain.replace('http://','')
		Domain=Domain.replace('/','')
		return Domain
	else:
		return 'NULL'

def timestamp2date(Date):
	if isinstance(Date,float) and Date>1:
		Date=int(Date)
		d=datetime.date.fromordinal(StartDate+Date)
		return d.strftime("%Y%m%d")
	else:
		return '00000000'

def xls2csv(XLSFile,CSVFile,SheetName):
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')
	XLS=xlrd.open_workbook(XLSFile)
	Sheet=XLS.sheet_by_name(SheetName)
	CSVFile=open(CSVFile,'wb')
	WriteRow=csv.writer(CSVFile, quoting=csv.QUOTE_ALL)
	for rownum in xrange(Sheet.nrows):
		WriteRow.writerow(Sheet.row_values(rownum))
	CSVFile.close()

def xlsx2csv(infilepath, outfile, outfilename, sheetid=1, dateformat=None, delimiter=",", sheetdelimiter="--------", skip_empty_lines=False):
		try:
			ziphandle=zipfile.ZipFile(infilepath)
		except zipfile.BadZipfile:
			sys.stderr.write("Invalid xlsx file: " + infilepath + os.linesep)
			return
		try:
				shared_strings=parse(ziphandle, SharedStrings, "xl/sharedStrings.xml")
				styles=parse(ziphandle, Styles, "xl/styles.xml")
				workbook=parse(ziphandle, Workbook, "xl/workbook.xml")

				if sheetid > 0:
						outfile=outfilename and open(outfilename, 'w+b') or outfile
						try:
								writer=csv.writer(outfile, quoting=csv.QUOTE_MINIMAL, delimiter=delimiter, lineterminator=os.linesep)
								sheet=None
								for s in workbook.sheets:
										if s['id']==sheetid:
												sheetfile=ziphandle.open("xl/worksheets/sheet%i.xml" %s['id'], "r")
												sheet=Sheet(workbook, shared_strings, styles, sheetfile)
												break
								if not sheet:
										raise Exception("Sheet %i Not Found" %sheetid)
								sheet.set_dateformat(dateformat)
								sheet.set_skip_empty_lines(skip_empty_lines)
								sheet.to_csv(writer)
								sheetfile.close()
						finally:
								if outfilename:
										outfile.close()
				else:
						if outfilename:
								if not os.path.exists(outfilename):
										os.makedirs(outfilename)
								elif os.path.isfile(outfilename):
										sys.stderr.write("File " + outfilename + " already exists!" + os.linesep)
										sys.exit(1)
						for s in workbook.sheets:
								sheetname=s['name'].encode('utf-8')
								outfile=outfilename and open(os.path.join(outfilename, sheetname + '.csv'), 'w+b') or outfile
								try:
										writer=csv.writer(outfile, quoting=csv.QUOTE_MINIMAL, delimiter=delimiter, lineterminator=os.linesep)
										if not outfilename and sheetdelimiter !="":
												outfile.write(sheetdelimiter + " " + str(s['id']) + " - " + s['name'].encode('utf-8') + os.linesep)
										sheetfile=ziphandle.open("xl/worksheets/sheet%i.xml" %s['id'], "r")
										sheet=Sheet(workbook, shared_strings, styles, sheetfile)
										sheet.set_dateformat(dateformat)
										sheet.set_skip_empty_lines(skip_empty_lines)
										sheet.to_csv(writer)
										sheetfile.close()
								finally:
										if outfilename:
												outfile.close()
		finally:
				ziphandle.close()

def parse(ziphandle, klass, filename):
		instance=klass()
		if not filename in ziphandle.namelist():
				filename=filter(lambda f: f.lower()==filename.lower(), ziphandle.namelist())[0]
		if filename:
				f=ziphandle.open(filename, "r")
				instance.parse(f)
				f.close()
		return instance

class Workbook:
		def __init__(self):
				self.sheets=[]
				self.date1904=False

		def parse(self, filehandle):
				workbookDoc=minidom.parseString(filehandle.read())
				if len(workbookDoc.firstChild.getElementsByTagName("fileVersion"))==0:
						self.appName='unknown'
				else:
						self.appName=workbookDoc.firstChild.getElementsByTagName("fileVersion")[0]._attrs['appName'].value
				try:
						self.date1904=workbookDoc.firstChild.getElementsByTagName("workbookPr")[0]._attrs['date1904'].value.lower().strip() !="false"
				except:
						pass

				sheets=workbookDoc.firstChild.getElementsByTagName("sheets")[0]
				for sheetNode in sheets.getElementsByTagName("sheet"):
						attrs=sheetNode._attrs
						name=attrs["name"].value
						if self.appName=='xl':
								if attrs.has_key('r:id'): id=int(attrs["r:id"].value[3:])
								else: id=int(attrs['sheetId'].value)
						else:
								if attrs.has_key('sheetId'): id=int(attrs["sheetId"].value)
								else: id=int(attrs['r:id'].value[3:])
						self.sheets.append({'name': name, 'id': id})

class Styles:
		def __init__(self):
				self.numFmts={}
				self.cellXfs=[]

		def parse(self, filehandle):
				styles=minidom.parseString(filehandle.read()).firstChild
				numFmtsElement=styles.getElementsByTagName("numFmts")
				if len(numFmtsElement)==1:
						for numFmt in numFmtsElement[0].childNodes:
								if numFmt.nodeType==minidom.Node.ELEMENT_NODE:
										numFmtId=int(numFmt._attrs['numFmtId'].value)
										formatCode=numFmt._attrs['formatCode'].value.lower().replace('\\', '')
										self.numFmts[numFmtId]=formatCode
				cellXfsElement=styles.getElementsByTagName("cellXfs")
				if len(cellXfsElement)==1:
						for cellXfs in cellXfsElement[0].childNodes:
								if cellXfs.nodeType !=minidom.Node.ELEMENT_NODE or cellXfs.nodeName !="xf":
										continue
								if cellXfs._attrs.has_key('numFmtId'):
										numFmtId=int(cellXfs._attrs['numFmtId'].value)
										self.cellXfs.append(numFmtId)
								else:
										self.cellXfs.append(None)

class SharedStrings:
		def __init__(self):
				self.parser=None
				self.strings=[]
				self.si=False
				self.t=False
				self.rPh=False
				self.value=""

		def parse(self, filehandle):
				self.parser=xml.parsers.expat.ParserCreate()
				self.parser.CharacterDataHandler=self.handleCharData
				self.parser.StartElementHandler=self.handleStartElement
				self.parser.EndElementHandler=self.handleEndElement
				self.parser.ParseFile(filehandle)

		def handleCharData(self, data):
				if self.t:
						self.value+=data

		def handleStartElement(self, name, attrs):
				if name=='si':
						self.si=True
						self.value=""
				elif name=='t' and self.rPh:
						self.t=False
				elif name=='t' and self.si:
						self.t=True
				elif name=='rPh':
						self.rPh=True

		def handleEndElement(self, name):
				if name=='si':
						self.si=False
						self.strings.append(self.value)
				elif name=='t':
						self.t=False
				elif name=='rPh':
						self.rPh=False

class Sheet:
		def __init__(self, workbook, sharedString, styles, filehandle):
				self.parser=None
				self.writer=None
				self.sharedString=None
				self.styles=None

				self.in_sheet=False
				self.in_row=False
				self.in_cell=False
				self.in_cell_value=False
				self.in_cell_formula=False

				self.columns={}
				self.rowNum=None
				self.colType=None
				self.s_attr=None
				self.data=None

				self.dateformat=None
				self.skip_empty_lines=False

				self.filehandle=filehandle
				self.workbook=workbook
				self.sharedStrings=sharedString.strings
				self.styles=styles

		def set_dateformat(self, dateformat):
				self.dateformat=dateformat

		def set_skip_empty_lines(self, skip):
				self.skip_empty_lines=skip

		def to_csv(self, writer):
				self.writer=writer
				self.parser=xml.parsers.expat.ParserCreate()
				self.parser.CharacterDataHandler=self.handleCharData
				self.parser.StartElementHandler=self.handleStartElement
				self.parser.EndElementHandler=self.handleEndElement
				self.parser.ParseFile(self.filehandle)

		def handleCharData(self, data):
				if self.in_cell_value:
						self.collected_string+=data
						self.data=self.collected_string
						if self.colType=="s":
								self.data=self.sharedStrings[int(self.data)]
						elif self.colType=="b":
								self.data=(int(data)==1 and "TRUE") or (int(data)==0 and "FALSE") or data
						elif self.s_attr:
								s=int(self.s_attr)
								format=None
								xfs_numfmt=self.styles.cellXfs[s]
								if self.styles.numFmts.has_key(xfs_numfmt):
										format=self.styles.numFmts[xfs_numfmt]
								elif STANDARD_FORMATS.has_key(xfs_numfmt):
										format=STANDARD_FORMATS[xfs_numfmt]
								if format and FORMATS.has_key(format):
										format_type=FORMATS[format]
										try:
												if format_type=='date':
														if self.workbook.date1904:
																date=datetime.datetime(1904, 01, 01) + datetime.timedelta(float(self.data))
														else:
																date=datetime.datetime(1899, 12, 30) + datetime.timedelta(float(self.data))
														if self.dateformat:
																self.data=date.strftime(str(self.dateformat))
														else:
																dateformat=format.replace("yyyy", "%Y").replace("yy", "%y"). \
																	replace("hh:mm", "%H:%M").replace("h", "%H").replace("%H%H", "%H").replace("ss", "%S"). \
																	replace("d", "%e").replace("%e%e", "%d"). \
																	replace("mmmm", "%B").replace("mmm", "%b").replace(":mm", ":%M").replace("m", "%m").replace("%m%m", "%m"). \
																	replace("am/pm", "%p")
																self.data=date.strftime(str(dateformat)).strip()
												elif format_type=='time':
														self.data=str(float(self.data) * 24*60*60)
												elif format_type=='float' and ('E' in self.data or 'e' in self.data):
														self.data=("%f" %(float(self.data))).rstrip('0').rstrip('.')
										except (ValueError, OverflowError):
												pass
		def handleStartElement(self, name, attrs):
				if self.in_row and name=='c':
						self.colType=attrs.get("t")
						self.s_attr=attrs.get("s")
						cellId=attrs.get("r")
						if cellId:
								self.colNum=cellId[:len(cellId)-len(self.rowNum)]
								self.colIndex=0
						else:
								self.colIndex+=1
						self.data=""
						self.in_cell=True
				elif self.in_cell and (name=='v' or name=='is'):
						self.in_cell_value=True
						self.collected_string=""
				elif self.in_sheet and name=='row' and attrs.has_key('r'):
						self.rowNum=attrs['r']
						self.in_row=True
						self.columns={}
						self.spans=None
						if attrs.has_key('spans'):
								self.spans=[int(i) for i in attrs['spans'].split(":")]
				elif name=='sheetData':
						self.in_sheet=True

		def handleEndElement(self, name):
				if self.in_cell and name=='v':
						self.in_cell_value=False
				elif self.in_cell and name=='c':
						t=0
						for i in self.colNum: t=t*26 + ord(i) - 64
						self.columns[t - 1 + self.colIndex]=self.data
						self.in_cell=False
				if self.in_row and name=='row':
						if len(self.columns.keys()) > 0:
								d=[""] * (max(self.columns.keys()) + 1)
								for k in self.columns.keys():
										d[k]=self.columns[k].encode("utf-8")
								if self.spans:
										l=self.spans[0] + self.spans[1] - 1
										if len(d) < l:
												d+=(l - len(d)) * ['']
								if not self.skip_empty_lines or d.count('') !=len(d):
										self.writer.writerow(d)
						self.in_row=False
				elif self.in_sheet and name=='sheetData':
						self.in_sheet=False

def convert_recursive(path, kwargs):
		for name in os.listdir(path):
				fullpath=os.path.join(path, name)
				if os.path.isdir(fullpath):
						convert_recursive(fullpath, kwargs)
				else:
						if fullpath.lower().endswith(".xlsx"):
								outfilepath=fullpath[:-4] + 'csv'
								print("Converting %s to %s" %(fullpath, outfilepath))
								try:
										xlsx2csv(fullpath, None, outfilepath, **kwargs)
								except zipfile.BadZipfile:
										print("File is not a zip file")