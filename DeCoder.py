import PyPDF2
import regex as re

from DeCoder_Auxiliary import *

# Open PDF File
pdfFile=open('../Codes&Standards/EC 1993.1.8.2005-1.pdf','rb')
pdfReader=PyPDF2.PdfFileReader(pdfFile)
numPages=pdfReader.numPages
print('number of pages in the PDF document: {0}'.format(numPages))

# Pages content
pages={}
for pageNum in range(0,numPages):
  pdfPage=pdfReader.getPage(pageNum)
  pages[pageNum]=pdfPage.extractText()
  pass

# Toc settings
tocIdentifiers=['contents','Contents',
                 'table of contents','Table of contents','Table Of Contents']
noMatterRegex='[\s]*'
noMatter=' '
# Reference settings
refidRegex='\d'
refsepRegex='\.'
refsep='.'
# Name settings
namRegex='[\s\w]*'
# Location settings
locRegex='\d+'
# Separator settings
sepRegex='\.{2,}'
sep='.'

numberDotRef=ReferenceSystem(refidRegex, refsepRegex, refsep)
simpleNam=NameSystem(namRegex)
pageStringLoc=LocationSystem(locRegex)
dotSep=SeparatorSystem(sepRegex)
ECTocSys=TocSystem(numberDotRef,simpleNam,pageStringLoc,dotSep,noMatterRegex,noMatter)
# ECToc=Toc(numberDotRef,simpleNam,pageStringLoc,dotSep)

# Searching TOC by Identifiers
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
maxTocTotalCoincidences = max(tocTotalCoincidences.values())
print('Number of Max TOC indentifiers in One Page: {0}'.format(maxTocTotalCoincidences))
maxTocTotalCoincidencesPages = [key  for (key, value) in tocTotalCoincidences.items() if value == maxTocTotalCoincidences]
print('Pages with Max TOC indentifiers in One Page: {0}'.format(maxTocTotalCoincidencesPages))

# Searching TOC by tocRegex
tocCoincidences={}
for pageNum, pageContent in pages.items():
  tocCoincidences[pageNum]=len(re.findall(ECTocSys.tocRegex,pages[pageNum]))
  pass
noNullTocCoincidencesPages = [key  for (key, value) in tocCoincidences.items() if value != 0]
print('Pages with toc Regex: {0}'.format(noNullTocCoincidencesPages))

# TOC pages
tocPages=noNullTocCoincidencesPages

# toc's in TOC
pattern = re.compile(ECTocSys.tocRegex)
for page in tocPages:
  for match in pattern.finditer(pages[page]):
    [split1,split2]=re.split(ECTocSys.sepSys.sepRegex,match.group())
    ref=Reference(numberDotRef,re.search(ECTocSys.refSys.refRegex,split1).group())
    split1=re.sub(ECTocSys.refSys.refRegex,'',split1)
    nam=Name(simpleNam,re.search(ECTocSys.namSys.namRegex,split1).group())
    split1=re.sub(ECTocSys.namSys.namRegex,'',split1)
    locPage=re.search(ECTocSys.locSys.locRegex,split2).group()
    beginLocation=Location(pageStringLoc,locPage,begin=None,end=None)
    separator=Separator(dotSep, sep)
    ECTocUnit=TocUnit(ref,nam,beginLocation,separator)
    TOC_EC3.addToc(ECTocUnit)
    pass
  pass
TOC_EC3.tocList.sort(key=lambda x: x.ref, reverse=False)
TOC_EC3.printTOC()

# Search Missing toc's in TOC
refMissing=[]
for toc in TOC_EC3.tocList:
  levels=re.split(TOC_EC3.refsepRegex,toc.ref)
  levels=list(filter(lambda item: item, levels))
  levels=list(map(int,levels))
  for level in range(toc.level+1):
    numLevel=levels[level]
    #if numLevel=1 there is no previous ref in this level
    if numLevel!=1:
      #find the first part of the ref at the levels>0
      if level!=0:
        prevref=''
        for i in range(level):
          prevref=prevref+str(levels[i])+TOC_EC3.refsep
          pass
      else:
        prevref=''
        pass
      #add to refMissing the lefts references
      for i in range(1,numLevel+1):
        refMissing.append(prevref+str(i)+TOC_EC3.refsep)
        pass
      pass
    pass
  pass
refMissing=list(set(refMissing))
refMissing.sort()
print(refMissing)
len(refMissing)

# Add Missing toc's in TOC
for ref in refMissing:
  refsep=TOC_EC3.refsep
  beginLocation=DeCoderAux.PDFlocation(-1)
  toc_EC3=DeCoderAux.toc(ref,refsep,'',beginLocation)
  TOC_EC3.addToc(toc_EC3)
  pass
TOC_EC3.tocList.sort(key=lambda x: x.ref, reverse=False)
TOC_EC3.printTOC()

# Search Missing toc's in Main text
pattern = re.compile(TOC_EC3.refRegex)
refMissing=[]
refTOC=[]
for toc in TOC_EC3.tocList:
  refTOC.append(toc.ref)
  pass
for page in pages:
  for match in pattern.finditer(pages[page]):
    if match.group() not in refTOC:
      refMissing.append(match.group())
      pass
    pass
  pass

refMissing=list(set(refMissing))
refMissing.sort()
print(refMissing)
len(refMissing)


pdfFile.close()