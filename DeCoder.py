import numpy as np
import PyPDF2
import regex as re

from DeCoder_Auxiliary import (IdSystem,NameSystem,LocationSystem,SeparatorSystem,
                               ReferenceSystem,
                               ReferenceList)
# Open PDF File
pdfFile=open('../Codes&Standards/EC 1993.1.8.2005-1.pdf','rb')#EC 1993.1.8.2005-1.pdf #AWS .d1.1.2000.pdf
pdfReader=PyPDF2.PdfFileReader(pdfFile)
numPages=pdfReader.numPages
print('number of pages in the PDF document: {0}'.format(numPages))


# ----------------------------------------------------------------------------
# SETTING
# ----------------------------------------------------------------------------
# TOC settings
tocIdentifiers=['contents','Contents','CONTENTS'
                 'table of contents','Table of contents','Table Of Contents','TABLE OF CONTENTS']
# Id settings
idIndicatorRegex='\d'
idSeparatorRegex='\.'
idSeparator='.'
# Name settings
nameRegex='[\s\w]*'
# Location settings
locationRegex='\d+'
gapTocReal=1
# Separator settings
separatorRegex='\.{2,}'
sep='.'
# No Matter settings
nomatterRegex='[\s]*'

numberDotRef=IdSystem(idIndicatorRegex=idIndicatorRegex,
                      idSeparatorRegex=idSeparatorRegex,
                      idSeparator=idSeparator)
simpleNam=NameSystem(nameRegex)
pageStringLoc=LocationSystem(locationRegex,gapTocReal=gapTocReal)
dotSep=SeparatorSystem(separatorRegex)
ECTocReferenceSystem=ReferenceSystem(idSys=numberDotRef,
                         namSys=simpleNam,
                         locSys=pageStringLoc,
                         sepSys=dotSep,
                         nomatterRegex=nomatterRegex)
ECTocReferenceSystem.print()
# ----------------------------------------------------------------------------
# CONTENT & CORRECTION
# ----------------------------------------------------------------------------
# Pages content
pages={}
for pageNum in range(0,numPages):
  pdfPage=pdfReader.getPage(pageNum)
  page=pdfPage.extractText()
  # delete \n and \t
  page=re.sub('\n',' ',page)
  page=re.sub('\t',' ',page)
  pages[pageNum]=page
  pass

# Pages references correction
pattern=re.compile(ECTocReferenceSystem.idRegex)
for pageNum in range(0,numPages):
  # look for reference, position
  pagesReferences=[]
  page=pages[pageNum]
  while re.search(pattern,page) is not None:
    reference=re.search(pattern,page).group()
    begin=re.search(pattern,page).start()
    pagesReferences.append([reference,
                            begin,
                            ECTocReferenceSystem.getId(reference)])
    page=re.sub(reference,'',page,count=1)
    pass
  # delete references
  pages[pageNum]=page
  # introduce real reference in position
  numReferences=len(pagesReferences)
  for refNum in range(0,numReferences):
    reference=pagesReferences[numReferences-refNum-1]
    page=(page[:reference[1]]+
          ECTocReferenceSystem.getId(reference[0])+
          page[reference[1]:])
    pass
  # update pages with real references
  pages[pageNum]=page
  pass
# ----------------------------------------------------------------------------
# LOCATION
# ----------------------------------------------------------------------------
# Searching TOC's beginning by identifiers
tocCoincidences={}
tocTotalCoincidences={}
for pageNum, pageContent in pages.items():
  auxList=[]
  for tocIdentifier in tocIdentifiers:
    auxList.append(pageContent.count(tocIdentifier))
    pass
  tocCoincidences[pageNum]=auxList
  tocTotalCoincidences[pageNum]=sum(auxList)
  pass
print('Number of TOC indentifiers in PDF file: {0}'.format(sum(tocTotalCoincidences.values())))
print('Number of Max TOC indentifiers in One Page: {0}'.format(max(tocTotalCoincidences.values())))
print('Pages with Max TOC indentifiers in One Page: {0}'.format(
  [key  for (key, value) in tocTotalCoincidences.items() if value == max(tocTotalCoincidences.values())]))

# Searching TOC's pages by reference system
tocCoincidences={}
for pageNum, pageContent in pages.items():
  tocCoincidences[pageNum]=len(re.findall(ECTocReferenceSystem.referenceRegex,pageContent))
  pass
tocPages = [key  for (key, value) in tocCoincidences.items() if value != 0]
print('Pages with toc Regex: {0}'.format(tocPages))

# left tocs in TOC
ECTocList=ReferenceList(ECTocReferenceSystem)
pattern = re.compile(ECTocReferenceSystem.referenceRegex)
for page in tocPages:
  for match in pattern.finditer(pages[page]):
    ECTocList.addReference(match.group(),gapActivation=True)
    pass
  pass
ECTocList.sort(by='id')

# Search Missing toc's in TOC
refMissing=[]
for reference in ECTocList.list:
  levels=re.split(ECTocReferenceSystem.idSeparatorRegex,reference.id)
  levels=list(filter(lambda item: item, levels))
  levels=list(map(int,levels))
  print(levels)
  for level in range(reference.level+1):
    numLevel=levels[level]
    #if numLevel=1 there is no previous ref in this level
    if numLevel!=1:
      #find the first part of the ref at the levels>0
      if level!=0:
        prevref=''
        for i in range(level):
          prevref=prevref+str(levels[i])+ECTocReferenceSystem.idSeparator
          pass
      else:
        prevref=''
        pass
      #add to refMissing the lefts references
      for i in range(1,numLevel+1):
        refMissing.append(prevref+str(i)+ECTocReferenceSystem.idSeparator)
        pass
      pass
    pass
  pass
refMissing=list(set(refMissing))
refMissing.sort()

ECTocList.print()


# Add Missing toc's in TOC
for refId in refMissing:
  ECTocList.addReference(id=refId,gapActivation=False)
  pass
ECTocList.sort('id')

# Pages References and their Levels
pagesReferences={}
pattern=re.compile(ECTocReferenceSystem.idRegex)
for pageNum in range(0,numPages):
  page=pages[pageNum]
  refList=[]
  newpage=page
  for match in pattern.finditer(page):
    refList.append([ECTocReferenceSystem.getId(match.group()),
                    ECTocReferenceSystem.getLevel(match.group())])
    pass
  pagesReferences[len(pagesReferences.keys())]=refList
  pass

# Delete incorrect references locations in TOC
for reference in ECTocList.list:
  if reference.beginPage:
    if reference.isInPage(reference.beginPage,pagesReferences) is False:
      reference.deleteBegin()
      pass
    pass
  pass






first=0
final=1

while final<len(ECTocList.list):
  found=False
  firstOfAll=first
  print('first of all: {}'.format(firstOfAll))
  # while not finding a missing page reference and till list end
  while found==False and final<len(ECTocList.list):
    firstReference=ECTocList.list[first]
    finalReference=ECTocList.list[final]
    if firstReference.beginPage is not None:
      first+=1
      final+=1
    elif finalReference.beginPage is not None:
      found=True
    else:
      final+=1
      pass
    pass
  # if final at the end set final to last page
  if final==len(ECTocList.list):
    final-=1
    finalReference=ECTocList.list[final]
    pass
  print('-----------------------------------------')
  print(first,final)

  # max between (last tocPages, firstReference TOC page)
  if firstReference.beginPage:
    firstPage=max(max(tocPages),firstReference.beginPage)
  else:
    firstPage=max(tocPages)
    pass
  # finalReference TOC page
  if finalReference.beginPage:
    lastPage=finalReference.beginPage
  else:
    lastPage=len(pages.keys())
    pass

  # Pages where references are
  newTOC=False
  # each reference between first and final
  for ref in range(first,final):
    reference=ECTocList.list[ref]
    # list pages where reference is (after TOC & before final page)
    pageList=[]
    for pageNum in range(0,numPages):
      if (reference.isInPage(pageNum,pagesReferences) and
          pageNum<=lastPage and
          pageNum>firstPage):
        pageList.append(pageNum)
        pass
      pass
    print(pageList)
    if len(pageList)==1:
      ECTocList.list[ref].beginPage=pageList[0]
      newTOC=True
      print('in {}  assign {}'.format(ref,pageList[0]))
      pass
    pass
  # Update first and last if newTOC
  if newTOC==True:
    # if newTOC back to the first
    first=firstOfAll
  else:
    # unless newTOC go forward
    first=final
    pass
  final=first+1
  pass

# Get begin character
for reference in ECTocList.list:
  if reference.beginPage is not None:
    reference.setBeginCharacter(pages)
    pass
  pass

ECTocList.print()



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