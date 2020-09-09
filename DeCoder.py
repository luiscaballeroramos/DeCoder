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
ECFigureSystem=ObjectSystem(idSys=IdSystem(idIndicatorRegex='\d',
                                                     idSeparatorRegex='\.',
                                                     idSeparator='.'),
                                     namSys=NameSystem(regex='((?:Figure|figure))'),
                                     locSys=LocationSystem(regex='\d+',
                                                gapTocReal=1),
                                     nomatterRegex='[\s]*',
                                     reverse=True)
ECFigureSystem.print()
ECTableSystem=ObjectSystem(idSys=IdSystem(idIndicatorRegex='\d',
                                                     idSeparatorRegex='\.',
                                                     idSeparator='.'),
                                     namSys=NameSystem(regex='((?:Table|table))'),
                                     locSys=LocationSystem(regex='\d+',
                                                gapTocReal=1),
                                     nomatterRegex='[\s]*',
                                     reverse=True)
ECTableSystem.print()
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
# % LOCATION
print('-------------------------------------------------------')
# Figure pages
# searching Figure's pages by reference system
auxDict=countRegexInDictionary(pages,[ECFigureSystem.referenceRegex])
print('Number of Figure references in PDF file: {0}'.format(sum(auxDict.values())))
numFigurePages = [key  for (key, value) in auxDict.items() if value != 0]
print('Number of pages with Figure references: {0}'.format(len(numFigurePages)))
print('Pages with Figure references: {0}'.format(numFigurePages))
figurePages={}
for i in numFigurePages:
  figurePages[i]=pages[i]
  pass
# % INTEGRATION
print('-------------------------------------------------------')
# Figure objects with begin and end
auxDict,auxBegin,auxEnd=RegexInDictionary(figurePages,[ECFigureSystem.referenceRegex],
                                          beginend=True,show=False)
ECFigureList=ObjectList(ECFigureSystem)
for i in range(min(figurePages),max(figurePages)+1):
  if i in auxDict.keys():
    j=0
    for aux in auxDict[i]:
      ECFigureList.addObject(aux,beginPage=i,beginCharacter=auxBegin[i][j],
                            endPage=i,endCharacter=auxEnd[i][j])
      j+=1
      pass
    pass
  pass
ECFigureList.sort('id')
ECFigureList.print()
ECFigureList.percentageComplete()
# % LOCATION
print('-------------------------------------------------------')
# Table pages
# searching Table's pages by reference system
auxDict=countRegexInDictionary(pages,[ECTableSystem.referenceRegex])
print('Number of Table references in PDF file: {0}'.format(sum(auxDict.values())))
numTablePages = [key  for (key, value) in auxDict.items() if value != 0]
print('Number of pages with Table references: {0}'.format(len(numTablePages)))
print('Pages with Table references: {0}'.format(numTablePages))
tablePages={}
for i in numTablePages:
  tablePages[i]=pages[i]
  pass
# % INTEGRATION
print('-------------------------------------------------------')
# Table objects with begin and end
auxDict,auxBegin,auxEnd=RegexInDictionary(tablePages,[ECTableSystem.referenceRegex],
                                          beginend=True,show=False)
ECTableList=ObjectList(ECTableSystem)
for i in range(min(tablePages),max(tablePages)+1):
  if i in auxDict.keys():
    j=0
    for aux in auxDict[i]:
      ECTableList.addObject(aux,beginPage=i,beginCharacter=auxBegin[i][j],
                            endPage=i,endCharacter=auxEnd[i][j])
      j+=1
      pass
    pass
  pass
ECTableList.sort('id')
ECTableList.print()
ECTableList.percentageComplete()
# % LOCATION
print('-------------------------------------------------------')
# TOC pages

# searching TOC's beginning by identifiers
auxDict=countRegexInDictionary(pages,tocIdentifiers)
print('Number of TOC indentifiers in PDF file: {0}'.format(sum(auxDict.values())))
print('Number of Max TOC indentifiers in One Page: {0}'.format(max(auxDict.values())))
print('Pages with Max TOC indentifiers in One Page: {0}'.format(
  [key  for (key, value) in auxDict.items() if value == max(auxDict.values())]))

# searching TOC's pages by reference system
auxDict=countRegexInDictionary(pages,[ECTocSystem.referenceRegex])
print('Number of TOC references in PDF file: {0}'.format(sum(auxDict.values())))
numTocPages = [key  for (key, value) in auxDict.items() if value >= 5]
print('Number of pages with TOC references: {0}'.format(len(numTocPages)))
print('Pages with TOC references: {0}'.format(numTocPages))
tocPages={}
for i in numTocPages:
  tocPages[i]=pages[i]
  pass
# % INTEGRATION
print('-------------------------------------------------------')
# TOC references
auxDict=RegexInDictionary(tocPages,[ECTocSystem.referenceRegex])
ECTocList=ReferenceList(ECTocSystem)
for i in range(min(tocPages),max(tocPages)+1):
  for aux in auxDict[i]:
    ECTocList.addReference(aux,gapActivation=True)
    pass
  pass
ECTocList.sort('id')
# % COMPROBATION
print('-------------------------------------------------------')
# Delete non-unique references begin
for reference in ECTocList.list:
  if reference.countInString(pages[reference.begin.page])!=1:
    reference.deleteBegin()
  pass
# % COMPROBATION
print('-------------------------------------------------------')
# Delete references to TOC pages or before
for reference in ECTocList.list:
  if reference.begin.page in tocPages:
    reference.deleteBegin()
  elif reference.begin.page is not None:
    if int(reference.begin.page)<min(tocPages):
      reference.deleteBegin()
      pass
    pass
  pass
ECTocList.sort('id')
# % LOCATION
print('-------------------------------------------------------')
# Unique TOC references begin
for reference in ECTocList.list:
  if reference.begin.page is not None:
    reference.setBeginCharacterInPages(pages)
    pass
  pass
ECTocList.sort('id')
# % INTEGRATION
print('-------------------------------------------------------')
# Missing TOC references
reference=ECTocList.list[0]
refMissing=[]
for reference in ECTocList.list:
  refId=reference.id
  while ECTocSystem.getPreviousId(refId):
    refMissing.append(ECTocSystem.getPreviousId(refId))
    refId=ECTocSystem.getPreviousId(refId)
    pass
  pass
refMissing=list(set(refMissing))
refMissing.sort()
# Add Missing toc's in TOC
for refId in refMissing:
  ECTocList.addReference(id=refId,gapActivation=False)
  pass
ECTocList.sort('id')
ECTocList.print()
ECTocList.percentageComplete()
# %% LOOP
print('-------------------------------------------------------')
# Missing TOC references (between first and final loop)
minPag=max(tocPages)+1
maxPag=numPages-1

first=-1
final=first+1
interval=Reference(ECTocSystem,beginPage=minPag,beginCharacter=0,
                   endPage=0,endCharacter=0)
while final<len(ECTocList.list)-1:
  # Find final
  finalFound=False
  final=first
  while finalFound==False and final<len(ECTocList.list):
    final+=1
    # if no final, set absolute final
    if final==len(ECTocList.list):
      interval.end=Location(maxPag,len(pages[maxPag]))
    else:
      interval.end=ECTocList.list[final].begin
      pass
    finalFound=interval.end.isComplete()
    pass
  print('final: {}'.format(final))
  newTOC=False
  ECTocList.sort('id')
# % LOCATION and INTEGRATION
  print('-------------------------------------------------------')
  # begin (set begin between first and final)
  for i in range(first+1,final):
    ref=ECTocList.list[i]
    ref.setBeginBetweenLocations(pages,interval.begin,interval.end,exceptions=[])
    if ref.begin.isComplete():
      newTOC=True
      pass
    pass

  # begin with exceptions Figures and Tables
  for i in range(first+1,final):
    ref=ECTocList.list[i]
    ref.setBeginBetweenLocations(pages,interval.begin,interval.end,
                                  exceptions=[ECFigureList.list,ECTableList.list])
    if ref.begin.isComplete():
      newTOC=True
      pass
    pass

  # Another step
  print('-------------------------------------------------------')

  print(newTOC)
  # if TOC doesn't change
  if newTOC==False:
    first=final-1
    interval.begin=ECTocList.list[first].begin
    pass
  firstFound=(interval.begin.isComplete()==True and
              ECTocList.list[first+1].begin.isComplete()==False)
  while (firstFound==False and first<len(ECTocList.list)-2):
    first+=1
    interval.begin=ECTocList.list[first].begin
    firstFound=(interval.begin.isComplete()==True and
                ECTocList.list[first+1].begin.isComplete()==False)
  print('first: {}'.format(first))
  pass
ECTocList.sort('id')
ECTocList.print()
ECTocList.percentageComplete()
# %% LOCATION and INTEGRATION
print('-------------------------------------------------------')
# Missing Next TOC references
for reference in ECTocList.list:
  print('---------------------')
  print(reference.id)
  print('------')
  nextId=ECTocSystem.getNextId(reference.id)
  ref=Reference(ECTocSystem)
  foundNext=False
  foundNextUp=False
  # look for next in TOC
  for i in ECTocList.list:
    if i.id==nextId:
      ref=i
      foundNext=True
      print('found next id: {}'.format(nextId))
      pass
    pass
  # if don't find next in TOC and reference's level is not 0
  if foundNext is False and ECTocSystem.getLevel(reference.id)!=0:
    nextUpId=ECTocSystem.getNextId(ECTocSystem.getUpId(reference.id))
    # look for nextup Id in TOC
    for i in ECTocList.list:
      if i.id==nextUpId:
        print('found next up id: {}'.format(nextUpId))
        ref=i
        foundNextUp=True
        pass
      pass
    pass
  # if next or nextup Id's begin is complete
  if foundNextUp is True and reference.begin.isComplete() and ref.begin.isComplete():
    print('begin of {} found'.format(ref.id))
    foundNext=True
    first=reference.begin
    final=ref.begin
    auxRef=Reference(ECTocSystem,id=nextId)
    auxRef.setBeginBetweenLocations(pages,first,final,
                                    exceptions=[ECFigureList.list,ECTableList.list])
    if auxRef.begin.isComplete() and auxRef.begin.page!=0:
      ECTocList.addReference(id=auxRef.id,beginPage=auxRef.begin.page,beginCharacter=auxRef.begin.character)
      ECTocList.sort('id')
      print(auxRef.id)
      pass
  else:
    print('not begin of {}'.format(ref.id))
    pass
  pass
ECTocList.sort('id')
ECTocList.print()
ECTocList.percentageComplete()
# %% LOCATION and INTEGRATION
print('-------------------------------------------------------')
# Missing Below TOC references
for reference in ECTocList.list:
  print('---------------------')
  print(reference.id)
  print('------')
  nextId=ECTocSystem.getNextId(reference.id)
  ref=Reference(ECTocSystem)
  foundNext=False
  foundNextUp=False
  # look for next in TOC
  for i in ECTocList.list:
    if i.id==nextId:
      ref=i
      foundNext=True
      print('found next id: {}'.format(nextId))
      pass
    pass
  # if don't find next in TOC and reference's level is not 0
  if foundNext is False and ECTocSystem.getLevel(reference.id)!=0:
    nextUpId=ECTocSystem.getNextId(ECTocSystem.getUpId(reference.id))
    # look for nextup Id in TOC
    for i in ECTocList.list:
      if i.id==nextUpId:
        print('found next up id: {}'.format(nextUpId))
        ref=i
        foundNextUp=True
        pass
      pass
    pass
  # if next or nextup Id's begin is complete
  if (foundNext is True or foundNextUp is True) and reference.begin.isComplete() and ref.begin.isComplete():
    print('begin of {} found'.format(ref.id))
    foundNext=True
    first=reference.begin
    final=ref.begin
    auxRef=Reference(ECTocSystem,id=ECTocSystem.getBelowId(reference.id))
    auxRef.setBeginBetweenLocations(pages,first,final,
                                    exceptions=[ECFigureList.list,ECTableList.list])
    if auxRef.begin.isComplete() and auxRef.begin.page!=0:
      ECTocList.addReference(id=auxRef.id,beginPage=auxRef.begin.page,beginCharacter=auxRef.begin.character)
      ECTocList.sort('id')
      print(auxRef.id)
      pass
  else:
    print('not begin of {}'.format(ref.id))
    pass
  pass
ECTocList.sort('id')
ECTocList.print()
ECTocList.percentageComplete()
# %%
print(RegexInDictionary(pages,['Table','Figure']))


for reference in ECTocList.list:

  pass









# %%
auxDict=len(RegexInDictionary(pages,[ECTocSystem.idRegex]))
for i in range(0,len(ECTocList.list)):
  ref=ECTocList.list[i]
  print(ref.id)
  print(auxDict[ref.begin.page])

# %%
auxDict=RegexInDictionary(pages,[ECTocSystem.idRegex])
for i,aux in auxDict.items():
  for j in range(0,len(aux)):
    aux[j]=ECTocSystem.getId(aux[j])
    pass
  auxDict[i]=aux
  pass
# %%
# Pages references
pagesReferencesMatrix=np.zeros((numPages,len(ECTocList.list)))
i=0
while i<numPages:
  j=0
  while j<len(ECTocList.list):
    print(i,j)
    print(pages[i].count(ECTocList.list[j].id))
    pagesReferencesMatrix[i,j]=pages[i].count(ECTocList.list[j].id)
    j+=1
    pass
  pagesReferencesMatrix[i]=auxList
  i+=1
  pass


# Pages References and their Levels
pagesReferences={}
pattern=re.compile(ECTocSystem.idRegex)
for pageNum in range(0,numPages):
  page=pages[pageNum]
  refList=[]
  newpage=page
  for match in pattern.finditer(page):
    refList.append([ECTocSystem.getId(match.group()),
                    ECTocSystem.getLevel(match.group())])
    pass
  pagesReferences[len(pagesReferences.keys())]=refList
  pass




# # Pages references correction
# pattern=re.compile(ECTocSystem.idRegex)
# for pageNum in range(0,numPages):
#   # look for reference, position
#   pagesReferences=[]
#   page=pages[pageNum]
#   while re.search(pattern,page) is not None:
#     reference=re.search(pattern,page).group()
#     begin=re.search(pattern,page).start()
#     pagesReferences.append([reference,
#                             begin,
#                             ECTocSystem.getId(reference)])
#     page=re.sub(reference,'',page,count=1)
#     pass
#   # delete references
#   pages[pageNum]=page
#   # introduce real reference in position
#   numReferences=len(pagesReferences)
#   for refNum in range(0,numReferences):
#     reference=pagesReferences[numReferences-refNum-1]
#     page=(page[:reference[1]]+
#           ECTocSystem.getId(reference[0])+
#           page[reference[1]:])
#     pass
#   # update pages with real references
#   pages[pageNum]=page
#   pass


# # Search complete references
# i=0
# found=False
# while found==False:
#   reference=ECTocList.list[i]
#   if reference.isComplete():
#     reference.print()
#     locationPage=pages[int(reference.location)]
#     locationPage.find(reference.id)
#     found=True
#     pass
#   i+=1
#   pass

# # Search Missing toc's in Main text
# pattern = re.compile(TOC_EC3.refRegex)
# refMissing=[]
# refTOC=[]
# for toc in TOC_EC3.tocList:
#   refTOC.append(toc.ref)
#   pass
# for page in pages:
#   for match in pattern.finditer(pages[page]):
#     if match.group() not in refTOC:
#       refMissing.append(match.group())
#       pass
#     pass
#   pass

# refMissing=list(set(refMissing))
# refMissing.sort()
# print(refMissing)
# len(refMissing)


pdfFile.close()