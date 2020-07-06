import regex as re
from tabulate import tabulate

class IdSystem():
  # Constructor
  def __init__(self,regex=None,
               idIndicatorRegex=None,idSeparatorRegex=None,idSeparator=None):
    if regex is not None:
      self.idRegex=regex
      self.idIndicatorRegex=None
      self.idSeparatorRegex=None
      self.idSeparator=None
    elif idIndicatorRegex is not None and idSeparatorRegex is not None and idSeparator is not None:
      self.idRegex=idIndicatorRegex+'(?:'+idSeparatorRegex+'{1}'+idIndicatorRegex+'+)+'
      self.idIndicatorRegex=idIndicatorRegex
      self.idSeparatorRegex=idSeparatorRegex
      self.idSeparator=idSeparator
    else:
      self.idRegex=None
      self.idIndicatorRegex=None
      self.idSeparatorRegex=None
      self.idSeparator=None
      pass
    pass
  # Method: Get id level
  def getLevel(self,id):
    return len(list(filter(lambda item:item,re.split(self.idSeparatorRegex,id))))-1
  # Method: Get real id
  def getId(self,id):
    levels=re.split(self.idSeparatorRegex,id)
    levels=list(filter(lambda item: item, levels))
    levels=list(map(int,levels))
    newId=''
    for level in levels:
      newId=newId+'{:03}'.format(level)+self.idSeparator
      pass
    return newId
  pass

class NameSystem():
  # Constructor
  def __init__(self,regex=None):
    if regex is not None:
      self.nameRegex=regex
      pass
    pass
  # Method: Get real name
  def getName(self,name):
    if name is None:
      return None
    else:
      newName=name
      newName=re.sub('\n','',newName)
      newName=re.sub('\t','',newName)
      return newName
  pass

class SeparatorSystem():
  # Constructor
  def __init__(self,regex=None):
    if regex is not None:
      self.separatorRegex=regex
      pass
    pass
  pass

class LocationSystem():
  # Constructor
  def __init__(self,regex=None,gapTocReal=0):
    if regex is not None:
      self.locationRegex=regex
      self.gap=gapTocReal
      pass
    pass
  # Method: Get real page
  def getPage(self,page,gapActivation=False):
    if page is None:
      return None
    else:
      if gapActivation==True:
        return int(page)+self.gap
      else:
        return int(page)
      pass
    pass
  pass

class ReferenceSystem(IdSystem,NameSystem,SeparatorSystem,LocationSystem):
  # Constructor
  def __init__(self,idSys=None,namSys=None,sepSys=None,locSys=None,nomatterRegex=None):
    if (idSys is not None and isinstance(idSys,IdSystem),
        namSys is not None and isinstance(namSys,NameSystem),
        sepSys is not None and isinstance(sepSys,SeparatorSystem),
        locSys is not None and isinstance(locSys,LocationSystem)):
      IdSystem.__init__(self,idIndicatorRegex=idSys.idIndicatorRegex,
                        idSeparatorRegex=idSys.idSeparatorRegex,
                        idSeparator=idSys.idSeparator)
      NameSystem.__init__(self,regex=namSys.nameRegex)
      SeparatorSystem.__init__(self,regex=sepSys.separatorRegex)
      LocationSystem.__init__(self,regex=locSys.locationRegex,
                              gapTocReal=locSys.gap)
      self.nomatterRegex=nomatterRegex
      self.referenceRegex=(idSys.idRegex+nomatterRegex+
                           namSys.nameRegex+nomatterRegex+
                           sepSys.separatorRegex+nomatterRegex+
                           locSys.locationRegex)
    pass
  # Method: Is reference
  def isReference(self,ref):
    if ref is None:
      return False
    elif re.match(self.referenceRegex,ref) is not None:
      return True
    else:
      return False
  # Method: Print
  def print(self):
    print('idRegex: {0}'.format(self.idRegex))
    print('idIndicatorRegex: {0}'.format(self.idIndicatorRegex))
    print('idSeparatorRegex: {0}'.format(self.idSeparatorRegex))
    print('referenceRegex: {0}'.format(self.referenceRegex))
  pass

class Reference():
  # Constructor
  def __init__(self,refSys,ref,id=None,name=None,separator=None,
               beginPage=None,beginCharacter=None,endPage=None,endCharacter=None,
               gapActivation=False):
    if isinstance(refSys,ReferenceSystem):
      self.refSys=refSys
      if refSys.isReference(ref):
        self.reference=ref
        # id
        self.id=self.refSys.getId(re.match(refSys.idRegex,ref).group())
        ref=re.sub(refSys.idRegex,'',ref,count=1)
        # level
        self.level=refSys.getLevel(self.id)
        # nomatter
        ref=re.sub(refSys.nomatterRegex,'',ref,count=1)
        # name
        self.name=refSys.getName(re.match(refSys.nameRegex,ref).group())
        ref=re.sub(refSys.nameRegex,'',ref,count=1)
        # nomatter
        ref=re.sub(refSys.nomatterRegex,'',ref,count=1)
        # separator
        self.separator=re.match(refSys.separatorRegex,ref).group()
        ref=re.sub(refSys.separatorRegex,'',ref,count=1)
        # nomatter
        ref=re.sub(refSys.nomatterRegex,'',ref,count=1)
        # beginPage
        self.beginPage=refSys.getPage(re.match(refSys.locationRegex,ref).group(),gapActivation=gapActivation)
        ref=re.sub(refSys.locationRegex,'',ref,count=1)
      else:
        self.id=self.refSys.getId(id)
        self.level=refSys.getLevel(self.id)
        self.name=self.refSys.getName(name)
        self.separator=separator
        self.beginPage=self.refSys.getPage(beginPage,gapActivation=gapActivation)
        self.beginCharacter=beginCharacter
        self.endPage=self.refSys.getPage(endPage,gapActivation=gapActivation)
        self.endCharacter=endCharacter
        pass
      pass
    pass
  # Method: Is complete
  def isComplete(self):
    if (self.id is not None and
        self.level is not None and
        self.name is not None and
        self.separator is not None and
        self.beginPage is not None and
        self.beginCharactern is not None and
        self.endPage is not None and
        self.endCharacter is not None):
      return True
    else:
      return False
    pass
  # Method: Is in page
  def isInPage(self,pageToSearch,pagesReferences):
    if self.id in [x[0] for x in pagesReferences[pageToSearch]]:
      return True
    else:
      return False
    pass
  # Method: Set begin character
  def setBeginCharacter(self,pages):
    self.beginCharacter=pages[self.beginPage].find(self.id)
    pass

  # Method: Delete Begin
  def deleteBegin(self):
    self.beginPage=None
    self.beginCharacter=None
    pass
  # Method: Delete End
  def deleteEnd(self):
    self.endPage=None
    self.endCharacter=None
    pass
  # Method: Print
  def print(self):
    table=[]
    table.append([self.level,self.id,self.beginPage,self.beginCharacter,self.endPage,self.endCharacter])
    print(tabulate(table,headers=['level','id','beginPage','beginCharacter','endPage','endCharacter'], tablefmt='orgtbl'))
    pass
  pass

class ReferenceList():
  # Constructor
  def __init__(self,refSys):
    if isinstance(refSys,ReferenceSystem):
      self.refSys=refSys
      self.list=[]
      pass
    pass
  # Method: Add Reference
  def addReference(self,ref=None,id=None,name=None,separator=None,beginPage=None,
                   beginCharacter=None,endPage=None,endCharacter=None,
                   gapActivation=False):
    refToAdd=Reference(self.refSys,ref,id=id,name=name,separator=separator,
                       beginPage=beginPage,beginCharacter=beginCharacter,endPage=endPage,endCharacter=endCharacter
                       ,gapActivation=gapActivation)
    if refToAdd.id not in self.getList('id'):
      self.list.append(refToAdd)
      pass
    pass
  # Method: Sort List
  def sort(self,by='id'):
    if by=='id':
      self.list.sort(key=lambda x: x.id, reverse=False)
    elif by=='level':
      self.list.sort(key=lambda x: x.level, reverse=False)
    elif by=='name':
      self.list.sort(key=lambda x: x.name, reverse=False)
    elif by=='separator':
      self.list.sort(key=lambda x: x.separator, reverse=False)
    elif by=='beginPage':
      self.list.sort(key=lambda x: x.beginPage, reverse=False)
    elif by=='beginCharacter':
      self.list.sort(key=lambda x: x.beginCharacter, reverse=False)
    elif by=='endPage':
      self.list.sort(key=lambda x: x.endPage, reverse=False)
    elif by=='endCharacter':
      self.list.sort(key=lambda x: x.endCharacter, reverse=False)
      pass
    pass
  # Method: Get list of references attribute
  def getList(self,attribute=None):
    attributeList=[]
    if attribute=='id':
      attributeList=(ref.id for ref in self.list)
    elif attribute=='level':
      attributeList=(ref.level for ref in self.list)
    elif attribute=='name':
      attributeList=(ref.name for ref in self.list)
    elif attribute=='separator':
      attributeList=(ref.separator for ref in self.list)
    elif attribute=='beginPage':
      attributeList=(ref.beginPage for ref in self.list)
    elif attribute=='beginCharacter':
      attributeList=(ref.beginCharacter for ref in self.list)
    elif attribute=='endPage':
      attributeList=(ref.endPage for ref in self.list)
    elif attribute=='endCharacter':
      attributeList=(ref.endCharacter for ref in self.list)
      pass
    return attributeList
  # Method: Print
  def print(self,first=None,last=None):
    table=[]
    if first is None and last is None:
      for reference in self.list:
        table.append([reference.level,reference.id,
                      reference.beginPage])#,reference.beginCharacter
        pass
    else:
      if last is None:
        last=first
        pass
      for i in range(first,last+1):
        reference=self.list[i]
        table.append([reference.level,reference.id,
                      reference.beginPage,reference.beginCharacter])
        pass
      pass
    print(tabulate(table,headers=['level','id','begPag','begChar'], tablefmt='github'))#tablefmt='orgtbl'))
    pass
  pass
