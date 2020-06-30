import regex as re
from tabulate import tabulate

class ReferenceSystem():
  def __init__(self,refidRegex,refsepRegex,refsep):
    self.refidRegex=str(refidRegex)
    self.refsepRegex=str(refsepRegex)
    self.refsep=str(refsep)
    self.refRegex=refidRegex+'(?:'+refsepRegex+'{1}'+refidRegex+'+)+'
    pass
  pass

class Reference(ReferenceSystem):
  def __init__(self,refSys,ref):
    if isinstance(refSys,ReferenceSystem):
      self.refSys=refSys
      if re.search(self.refSys.refRegex)!=None:
        self.ref=ref
        self.level = len(list(filter(lambda item: item, re.split(self.refSys.refsep+'*',ref))))-1
      else:
        self.ref=None
        self.level=None
        pass
      pass
    pass
  pass

class NameSystem():
  # Constructor
  def __init__(self,namRegex):
    self.namRegex=namRegex
    pass
  pass

class Name(NameSystem):
  def __init__(self,namSys,nam):
    if isinstance(namSys,NameSystem):
      NameSystem.__init__(self, namSys.namRegex)
      if re.search(self.namRegex)!=None:
        self.nam=nam
      else:
        self.nam=None
        pass
      pass
    pass
  pass

class LocationSystem():
  # Constructor
  def __init__(self,locRegex):
    self.locRegex=locRegex
    pass
  pass

class Location(LocationSystem):
  # Constructor
  def __init__(self,locSys,page,begin=None,end=None):
    if isinstance(locSys,LocationSystem):
      self.page=int(page)
      if begin is None:
        self.begin=None
        self.end =None
      else:
        self.begin=int(begin)
        if end is None:
          self.end=int(begin)
        else:
          self.end=end
          pass
        pass
      pass
    pass
  pass

class SeparatorSystem():
  # Constructor
  def __init__(self,sepRegex):
    self.sepRegex=sepRegex
    pass
  pass

class Separator(SeparatorSystem):
  def __init__(self,sepSys,sep):
    if isinstance(sepSys,SeparatorSystem):
      SeparatorSystem.__init__(self, sepSys.sepRegex)
      if re.search(self.sepRegex)!=None:
        self.sep=sep
      else:
        self.sep=None
        pass
      pass
    pass
  pass

class TocSystem(ReferenceSystem,NameSystem,LocationSystem,SeparatorSystem):
  def __init__(self,refSys,namSys,locSys,sepSys,noMatterRegex,noMatter):
    if isinstance(refSys,ReferenceSystem) and isinstance(namSys,NameSystem) and isinstance(locSys,LocationSystem):
      self.refSys=refSys
      self.namSys=namSys
      self.locSys=locSys
      self.sepSys=sepSys
      self.noMatterRegex=noMatterRegex
      self.noMatter=noMatter
      self.tocRegex=refSys.refRegex+noMatterRegex+namSys.namRegex+noMatterRegex+sepSys.sepRegex+noMatterRegex+locSys.locRegex
      pass
    pass
  pass

class TocUnit(TocSystem):
  # Contructor
  def __init__(self,reference,name,location,separator):
    if isinstance(reference,Reference) and isinstance(name,Name) and isinstance(location,Location) and isinstance(separator,Separator):
      self.reference=reference
      self.name=name
      self.location=location
      self.separator=separator
      pass
    pass
  pass

class Toc():
  # Constructor
  def __init__(self,refSys,namSys,locSys,sepSys):
    if isinstance(refSys,ReferenceSystem):
      self.refSys=refSys
    else:
      self.refSys=None
      pass
    if isinstance(namSys,NameSystem):
      self.namSys=namSys
    else:
      self.namSys=None
      pass
    if isinstance(locSys,LocationSystem):
      self.locSys=locSys
    else:
      self.locSys=None
      pass
    if isinstance(sepSys,SeparatorSystem):
      self.sepsys=sepSys
    else:
      self.sepsys=None
      pass
    self.tocList=[]
    pass
  # Method: Add toc to TOC.tocList
  def addToc(self,toc):
    if isinstance(toc,TocUnit):
      self.tocList.append(toc)
      pass
    pass
  # Method: Print TOC.tocList in a table
  def printToc(self,num=None):
    table=[]
    if num is None:
      for toc in self.tocList:
        table.append([toc.ref,toc.name,toc.begin.page,toc.level])
        pass
    else:
      toc=self.tocList[num]
      table.append([toc.ref,toc.name,toc.begin.page,toc.level])
      pass
    print(tabulate(table,headers=['Ref.','Name','Begin page','Level'], tablefmt='orgtbl'))
    pass
  pass
