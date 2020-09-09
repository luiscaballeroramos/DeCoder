import regex as re
from tabulate import tabulate

from Regex_Auxiliary import (RegexInString,RegexInDictionary)

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
      self.idRegex=idIndicatorRegex+'(?:'+idSeparatorRegex+'{1}'+idIndicatorRegex+'+)*'
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
    if id is None:
      return None
    else:
      return len(list(filter(lambda item:item,re.split(self.idSeparatorRegex,id))))-1
  # Method: Get id components
  def getComponents(self,id):
    components=re.split(self.idSeparatorRegex,id)
    components=list(filter(lambda item:item,components))
    components=list(map(int,components))
    return components
  # Method: Get real id
  def getId(self,id):
    if id is None:
      return None
    else:
      components=self.getComponents(id)
      newId=''
      for component in components:
        newId=newId+'{:03}'.format(component)+self.idSeparator
        pass
      return newId
  # Method: Get previous id
  def getPreviousId(self,id):
    if id is None:
      return None
    else:
      components=self.getComponents(id)
      level=self.getLevel(id)
      previous=[]
      newId=''
      # if level is 0 there´s no previous id
      if level==0:
        return None
      else:
        component=components[level]
        previous=components[:-1]
        # if component is 1 previous is upper level
        if component==1:
          return self.getUpId(id)
        else:
          previous=previous+[component-1]
          pass
        pass
      for prev in previous:
        newId=newId+str(prev)+self.idSeparator
        pass
      newId=self.getId(newId)
      return newId
    pass
  # Method: Get up id
  def getUpId(self,id):
    if id is None:
      return None
    else:
      components=self.getComponents(id)
      level=self.getLevel(id)
      previous=[]
      newId=''
      # if level is 0 there´s no previous id
      if level==0:
        return None
      else:
        previous=components[:-1]
        for prev in previous:
          newId=newId+str(prev)+self.idSeparator
          pass
        newId=self.getId(newId)
        return newId
    pass
  # Method: Get next id
  def getNextId(self,id):
    if id is None:
      return None
    else:
      components=self.getComponents(id)
      level=self.getLevel(id)
      previous=[]
      newId=''
      component=components[level]
      previous=components[:-1]
      previous=previous+[component+1]
      for prev in previous:
        newId=newId+str(prev)+self.idSeparator
        pass
      newId=self.getId(newId)
      return newId
    pass
  # Method: Get below id
  def getBelowId(self,id):
    if id is None:
      return None
    else:
      components=self.getComponents(id)
      newId=''
      previous=components
      previous=previous+[1]
      for prev in previous:
        newId=newId+str(prev)+self.idSeparator
        pass
      newId=self.getId(newId)
      return newId
    pass
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
    else:
      self.separatorRegex=''
      pass
    pass
  pass
class LocationSystem():
  # Constructor
  def __init__(self,regex=None,gapTocReal=0):
    if regex is not None:
      self.locationRegex=regex
      self.gap=gapTocReal
    else:
      self.locationRegex=''
      self.gap=0
      pass
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
  def __init__(self,idSys=None,namSys=None,sepSys=None,locSys=None,nomatterRegex=None,
               reverse=False):
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
      if reverse is True:
        self.referenceRegex=(namSys.nameRegex+nomatterRegex+
                             idSys.idRegex+nomatterRegex+
                             sepSys.separatorRegex+nomatterRegex+
                             locSys.locationRegex)
      else:
        self.referenceRegex=(idSys.idRegex+nomatterRegex+
                             namSys.nameRegex+nomatterRegex+
                             sepSys.separatorRegex+nomatterRegex+
                             locSys.locationRegex)
        pass
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
class ObjectSystem(IdSystem,NameSystem,SeparatorSystem,LocationSystem):
  # Constructor
  def __init__(self,idSys=None,namSys=None,locSys=None,nomatterRegex=None,
               reverse=False):
    if (idSys is not None and isinstance(idSys,IdSystem),
        namSys is not None and isinstance(namSys,NameSystem)):
      IdSystem.__init__(self,idIndicatorRegex=idSys.idIndicatorRegex,
                        idSeparatorRegex=idSys.idSeparatorRegex,
                        idSeparator=idSys.idSeparator)
      NameSystem.__init__(self,regex=namSys.nameRegex)
      LocationSystem.__init__(self,regex=locSys.locationRegex,
                              gapTocReal=locSys.gap)
      self.nomatterRegex=nomatterRegex
      if reverse is True:
        self.referenceRegex=(namSys.nameRegex+nomatterRegex+
                             idSys.idRegex+nomatterRegex)
      else:
        self.referenceRegex=(idSys.idRegex+nomatterRegex+
                             namSys.nameRegex+nomatterRegex)
        pass
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
    print('referenceRegex: {0}'.format(self.referenceRegex))
  pass
class Reference():
  # Constructor
  def __init__(self,refSys,ref=None,id=None,name=None,separator=None,
               beginPage=None,beginCharacter=None,endPage=None,endCharacter=None,
               gapActivation=False):
    if isinstance(refSys,ReferenceSystem):
      self.refSys=refSys
      if refSys.isReference(ref):
        # reference
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
        # begin
        self.begin=Location(refSys.getPage(re.match(refSys.locationRegex,ref).group(),gapActivation=gapActivation),
                                           character=beginCharacter)
        # end
        self.end=Location(self.refSys.getPage(endPage,gapActivation=gapActivation),character=endCharacter)
      else:
        self.id=self.refSys.getId(id)
        self.level=refSys.getLevel(self.id)
        self.name=self.refSys.getName(name)
        self.separator=separator
        self.begin=Location(self.refSys.getPage(beginPage,gapActivation=gapActivation),beginCharacter)
        self.end=Location(self.refSys.getPage(endPage,gapActivation=gapActivation),endCharacter)
        pass
      pass
    pass
  # Method: Set begin character in pages
  def setBeginCharacterInPages(self,pages,exceptions=[]):
    found=0
    loc=Location(0,0)
    # if has begin page
    if self.begin.page is not None:
      page=pages[self.begin.page]
      # idRegex in Page
      auxList,auxBegin,auxEnd=RegexInString(page,[self.refSys.idRegex],beginend=True,show=False)
      # each idRegex
      for j in range(0,len(auxList)):
        # regex
        auxReg=auxList[j]
        # begin
        auxBeg=Location(self.begin.page,auxBegin[j])
        # if id==self.id and idRegex is in (begin,end)
        if self.refSys.getId(auxReg)==self.id:
          # if exceptions
          if exceptions==[]:
            found+=1
            loc=auxBeg
          # if no exceptions
          else:
            inexception=False
            for exception in exceptions:
              for item in exception:
                if auxBeg.isBetweenLocations(item.begin,item.end)==True:
                  inexception=True
                  print('{} begin({},{}) Regex({},{}) end({},{})'.format(item.name+' '+item.id,
                                                 item.begin.page,item.begin.character,
                                                 auxBeg.page,auxBeg.character,
                                                 item.end.page,item.end.character))
                  pass
                pass
              pass
            # if no in exception
            if inexception==False:
              found+=1
              loc=auxBeg
              pass
            pass
          pass
        pass
      pass
    print(found,loc.page,loc.character)
    if found==1:
      self.begin=loc
      pass
    pass
# Method: Set begin character between locations
  def setBeginBetweenLocations(self,pages,begin,end,exceptions=[]):
    found=0
    loc=Location(0,0)
    # pages between locations
    for i in range(begin.page,end.page+1):
      page=pages[i]
      # idRegex in Page
      auxList,auxBegin,auxEnd=RegexInString(page,[self.refSys.idRegex],beginend=True,show=False)
      # each idRegex
      for j in range(0,len(auxList)):
        # regex
        auxReg=auxList[j]
        # begin
        auxBeg=Location(i,auxBegin[j])
        # if id==self.id and idRegex is in (begin,end)
        if self.refSys.getId(auxReg)==self.id and auxBeg.isBetweenLocations(begin,end):
          # if exceptions
          if exceptions==[]:
            found+=1
            loc=auxBeg
          # if no exceptions
          else:
            inexception=False
            for exception in exceptions:
              for item in exception:
                if auxBeg.isBetweenLocations(item.begin,item.end)==True:
                  inexception=True
                  print('{} begin({},{}) Regex({},{}) end({},{})'.format(item.name+' '+item.id,
                                                 item.begin.page,item.begin.character,
                                                 auxBeg.page,auxBeg.character,
                                                 item.end.page,item.end.character))
                  pass
                pass
              pass
            # if no in exception
            if inexception==False:
              found+=1
              loc=auxBeg
              pass
            pass
          pass
        pass
      pass
    print(self.id,found,loc.page,loc.character,begin.page,begin.character,end.page,end.character)
    if found==1:
      self.begin=loc
      pass
    pass
  # Method: Count in string
  def countInString(self,string):
    count=0
    # idRegex coincidences
    refIds=RegexInString(string,[self.refSys.idRegex])
    for refId in refIds:
      if self.refSys.getId(refId)==self.id:
        count+=1
        pass
      pass
    return count
  # Delete begin
  def deleteBegin(self):
    self.begin=Location(None)
    pass
  # Method: Print
  def print(self):
    table=[]
    table.append([self.level,self.id,self.beginPage,self.beginCharacter,self.endPage,self.endCharacter])
    print(tabulate(table,headers=['level','id','beginPage','beginCharacter','endPage','endCharacter'], tablefmt='orgtbl'))
    pass
  pass
class Object():
  # Constructor
  def __init__(self,objSys,obj=None,id=None,name=None,
               beginPage=None,beginCharacter=None,endPage=None,endCharacter=None,
               gapActivation=False):
    if isinstance(objSys,ObjectSystem):
      self.objSys=objSys
      if objSys.isReference(obj):
        # reference
        self.object=obj
        # name
        self.name=objSys.getName(re.match(objSys.nameRegex,obj).group())
        obj=re.sub(objSys.nameRegex,'',obj,count=1)
        # nomatter
        obj=re.sub(objSys.nomatterRegex,'',obj,count=1)
        obj=re.sub(objSys.nomatterRegex,'',obj,count=1)
        # id
        self.id=self.objSys.getId(re.match(objSys.idRegex,obj).group())
        obj=re.sub(objSys.idRegex,'',obj,count=1)
        # level
        self.level=objSys.getLevel(self.id)
        # begin
        self.begin=Location(self.objSys.getPage(beginPage,gapActivation=gapActivation),beginCharacter)
        # end
        self.end=Location(self.objSys.getPage(endPage,gapActivation=gapActivation),endCharacter)
      else:
        self.id=self.objSys.getId(id)
        self.level=objSys.getLevel(self.id)
        self.name=self.objSys.getName(name)
        self.begin=Location(self.objSys.getPage(beginPage,gapActivation=gapActivation),beginCharacter)
        self.end=Location(self.objSys.getPage(endPage,gapActivation=gapActivation),endCharacter)
        pass
      pass
    pass
  # Method: Set begin character in pages
  def setBeginCharacterInPages(self,pages):
    # if has begin page
    if self.begin.page is not None:
      page=pages[self.begin.page]
      # if is only once in begin.page
      if self.countInString(page)==1:
        # search idRegex in page
        refIds=self.refSys.RegexInString(page,self.refSys.idRegex)
        ref=''
        for refId in refIds:
          if self.refSys.getId(refId)==self.id:
            ref=refId
            pass
          pass
        self.begin.character=re.search(ref,page).start()
        pass
      pass
    pass
  # Method: Set begin character between locations
  def setBeginBetweenLocations(self,pages,begin,end):
    found=0
    pag=0
    char=0
    for i in range(begin.page,end.page+1):
      page=pages[i]
      # if is more than once in page
      if self.countInString(page)>=1:
        # search idRegex in page
        refIds=self.refSys.RegexInString(page,self.refSys.idRegex)
        ref=''
        for refId in refIds:
          if self.refSys.getId(refId)==self.id:
            ref=refId
            found+=1
            pass
          pass
        pag=i
        char=re.search(ref,page).start()
        pass
      pass
    print(found,pag,char)
    if found==1:
      self.begin=Location(pag,char)
      pass
    pass
  # Method: Count in string
  def countInString(self,string):
    count=0
    # idRegex coincidences
    refIds=self.refSys.getIdsInString(string)
    for refId in refIds:
      if self.refSys.getId(refId)==self.id:
        count+=1
        pass
      pass
    return count
  # Delete begin
  def deleteBegin(self):
    self.begin=Location(None)
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
  def addReference(self,ref=None,id=None,name=None,separator=None,
                   beginPage=None,beginCharacter=None,endPage=None,endCharacter=None,
                   gapActivation=False,repeated=False):
    refToAdd=Reference(self.refSys,ref,id=id,name=name,separator=separator,
                       beginPage=beginPage,beginCharacter=beginCharacter,endPage=endPage,endCharacter=endCharacter
                       ,gapActivation=gapActivation)
    if refToAdd.id not in self.getList('id'):
      self.list.append(refToAdd)
    elif repeated is True:
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
    return list(attributeList)
  # Method: percentage complete
  def percentageComplete(self):
    k=0
    l=0
    for i in self.list:
      if i.begin.isComplete():
        k+=1
      else:
        l+=1
        pass
      pass
    print('{}/{} {}%'.format(k,l,round(k/(k+l)*100,2)))
    pass
  # Method: Print
  def print(self,first=None,last=None):
    table=[]
    if first is None and last is None:
      for reference in self.list:
        auxList=[]
        try:
          auxList.append(reference.level)
        except:
          pass
        try:
          auxList.append(reference.id)
        except:
          pass
        try:
          auxList.append(reference.begin.page)
        except:
          pass
        try:
          auxList.append(reference.begin.character)
        except:
          pass
        try:
          auxList.append(reference.end.page)
        except:
          pass
        try:
          auxList.append(reference.end.character)
        except:
          pass
        table.append(auxList)
        pass
    else:
      if last is None:
        last=first
        pass
      for i in range(first,last+1):
        reference=self.list[i]
        table.append([reference.level,reference.id,
                      reference.begin.page,reference.begin.character,
                      reference.end.page,reference.end.character])
        pass
      pass
    print(tabulate(table,headers=['level','id','begPag','begChar','endPag','endChar'], tablefmt='github'))#tablefmt='orgtbl'))
    pass
  pass
class ObjectList():
  # Constructor
  def __init__(self,objSys):
    if isinstance(objSys,ObjectSystem):
      self.objSys=objSys
      self.list=[]
      pass
    pass
  # Method: Add Reference
  def addObject(self,obj=None,id=None,name=None,
                   beginPage=None,beginCharacter=None,endPage=None,endCharacter=None,
                   gapActivation=False):
    objToAdd=Object(self.objSys,obj,id=id,name=name,
                       beginPage=beginPage,beginCharacter=beginCharacter,endPage=endPage,endCharacter=endCharacter,
                       gapActivation=gapActivation)
    # if objToAdd.id not in self.getList('id'):
    self.list.append(objToAdd)
      # pass
    pass
  # Method: Sort List
  def sort(self,by='id'):
    if by=='id':
      self.list.sort(key=lambda x: x.id, reverse=False)
    elif by=='level':
      self.list.sort(key=lambda x: x.level, reverse=False)
    elif by=='name':
      self.list.sort(key=lambda x: x.name, reverse=False)
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
  # Method: percentage complete
  def percentageComplete(self):
    k=0
    l=0
    for i in self.list:
      if i.begin.isComplete():
        k+=1
      else:
        l+=1
        pass
      pass
    print('{}/{} {}%'.format(k,l,round(k/(k+l)*100,2)))
    pass
  # Method: Print
  def print(self,first=None,last=None):
    table=[]
    if first is None and last is None:
      for reference in self.list:
        auxList=[]
        try:
          auxList.append(reference.level)
        except:
          pass
        try:
          auxList.append(reference.id)
        except:
          pass
        try:
          auxList.append(reference.begin.page)
        except:
          pass
        try:
          auxList.append(reference.begin.character)
        except:
          pass
        try:
          auxList.append(reference.end.page)
        except:
          pass
        try:
          auxList.append(reference.end.character)
        except:
          pass
        table.append(auxList)
        pass
    else:
      if last is None:
        last=first
        pass
      for i in range(first,last+1):
        reference=self.list[i]
        table.append([reference.level,reference.id,
                      reference.begin.page,reference.begin.character,
                      reference.end.page,reference.end.character])
        pass
      pass
    print(tabulate(table,headers=['level','id','begPag','begChar','endPag','endChar'], tablefmt='github'))
    pass
  pass
class Location():
  # Constructor
  def __init__(self,page,character=None):
    self.page=page
    self.character=character
    self.character=character
    pass
  # Method: Is between locations
  def isBetweenLocations(self,begin,end):
    if (isinstance(self,Location) and
        isinstance(begin,Location) and
        isinstance(end,Location)):
      # begin and end in same page
      if (begin.page==end.page):
        if (self.page==begin.page and self.character>=begin.character and self.character<=end.character):
          return True
        else:
          return False
        pass
      # begin and end in different pages
      else:
        if (self.page>begin.page and
            self.page<end.page):
          return True
        elif (self.page==begin.page and
              self.character>=begin.character):
          return True
        elif (self.page==end.page and
              self.character<=end.character):
          return True
        else:
          return False
        pass
      pass
    pass
  #Method: Is complete
  def isComplete(self):
    if (self.page is not None) and (self.character is not None):
      return True
    else:
      return False
    pass
  pass
pass
