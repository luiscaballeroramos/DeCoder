import numpy as np
import PyPDF2
import regex as re
# Classes import
from DeCoder_Auxiliary import (IdSystem,NameSystem,LocationSystem,SeparatorSystem,
                               ReferenceSystem,ObjectSystem,
                               Reference,Object,
                               ReferenceList,ObjectList,
                               Location)
# Functions import
from Regex_Auxiliary import (RegexInString,
                             RegexInDictionary,countRegexInDictionary)
# Open PDF File
pdfFile=open('../Codes&Standards/EC 1993.1.8.2005-1.pdf','rb')#EC 1993.1.8.2005-1.pdf #AWS .d1.1.2000.pdf
pdfReader=PyPDF2.PdfFileReader(pdfFile)
# % SETTING
print('-------------------------------------------------------')
# TOC settings
tocIdentifiers=['contents','Contents','CONTENTS',
                 'table of contents','Table of contents','Table Of Contents','TABLE OF CONTENTS']
ECTocSystem=ReferenceSystem(idSys=IdSystem(idIndicatorRegex='\d',
                                                     idSeparatorRegex='\.',
                                                     idSeparator='.'),
                                     namSys=NameSystem(regex='[\s\w]*'),
                                     locSys=LocationSystem(regex='\d+',
                                                gapTocReal=1),
                                     sepSys=SeparatorSystem(regex='\.{2,}'),
                                     nomatterRegex='[\s]*')
ECTocSystem.print()
# % LOCATION
print('-------------------------------------------------------')
# Number of pages in PDF
numPages=pdfReader.numPages
print('Number of pages in the PDF document: {0}'.format(numPages))
# % INTEGRATION
print('-------------------------------------------------------')
# Pages content
pages={}
for i in range(0,numPages):
  pdfPage=pdfReader.getPage(i)
  pages[i]=pdfPage.extractText()
  pass
# % COMPROBATION
print('-------------------------------------------------------')
# Delete \n and \t
for i in range(0,numPages):
  page=pages[i]
  page=re.sub('\n\t',' ',page)
  page=re.sub('\t',' ',page)
  pages[i]=page
  pass
auxDict=RegexInDictionary(pages, ['\n\t'])
print('Number of new lines or tabulations in the PDF document: {0}'.format(
  max(auxDict.values())))
print('Number of pages with new lines or tabulations: {0}'.format(
  [key  for (key, value) in auxDict.items() if value != 0]))
# %% REFERENCE LIST ID REGEX
ECIdList=ReferenceList(ECTocSystem)
for i in pages:
  page=pages[i]
  ids,idsBegin,idsEnd=RegexInString(page,[ECTocSystem.idRegex],beginend=True,show=False)
  for j in range(0,len(ids)):
    id=ids[j]
    begin=idsBegin[j]
    end=idsEnd[j]
    ECIdList.addReference(id=id,
                          beginPage=i,beginCharacter=begin,
                          endPage=i,endCharacter=end,repeated=True)
    pass
  pass
ECIdList.sort()
ECIdList.print()
ECIdList.percentageComplete()
# %% ID LIST
idList=list(set(ECIdList.getList('id')))
idList.sort()
print(idList)
# %% IDS VS PAGES
# Array counting ids in pages
idsVSpages=[[0 for y in range(numPages)] for x in range(len(idList))]
# ids in ECIdList
for i in ECIdList.list:
  id=0
  for j in range(len(idList)):
    if i.id==idList[j]:
      id=j
      pass
    pass
  idsVSpages[id][i.begin.page]+=1
  pass
print(len(idsVSpages))

# %% EXCEL
import xlsxwriter

xMax=len(idsVSpages)
yMax=len(idsVSpages[0])
headColums=1
headRows=1
# Array counting ids in pages
arrayToExcel=[[0 for y in range(0,yMax+headColums)] for x in range(0,xMax+headRows)]
# First Column: Ids
for x in range(0,xMax):
  arrayToExcel[x+headColums][0]=idList[x]
  pass
# First Row: pages
for y in range(0,yMax):
  arrayToExcel[0][y+headRows]=y
  pass
# ids in ECIdList
for i in ECIdList.list:
  id=0
  for j in range(xMax):
    if i.id==idList[j]:
      id=j
      pass
    pass
  arrayToExcel[id+headRows][i.begin.page+headColums]+=1
  pass

workbook=xlsxwriter.Workbook('EC.xlsx')
worksheet=workbook.add_worksheet('idsInPages')

col=0
for row,data in enumerate(arrayToExcel):
  worksheet.write_row(row,col,data)
  pass
workbook.close()
# %%




# %%
# ID LIST SORTED
idList=[]
auxList=[]
for num,page in pages.items():
  auxList=auxList+RegexInString(page,[ECTocSystem.idRegex])
  pass
for i in auxList:
  idList.append(ECTocSystem.getId(i))
  pass
idList=list(set(idList))
idList.sort()
for i in idList:
  print(i)
  pass