import regex as re

def countRegexInDictionary(dictionary,listOfRegex):
  # Searching substrings coincidences
  coincidences={}
  for key, value in dictionary.items():
    auxList=[]
    # Look for each toc identifier
    for regex in listOfRegex:
      auxList.append(len(re.findall(regex,value)))
      pass
    coincidences[key]=sum(auxList)
    pass
  return coincidences

def RegexInString(string,listOfRegex,beginend=False,show=False):
  # Searching toc identifieers coincidences
  coincidences=[]
  begin=[]
  end=[]
  # Look for each toc identifier
  for regex in listOfRegex:
    for find in re.finditer(regex,string):
      coincidences.append(find.group())
      begin.append(find.start())
      end.append(find.end())
      pass
    if show is True:
      for find in re.finditer(regex,string):
        print(find.group())
        pass
      pass
    pass
  if beginend is True:
    return coincidences,begin,end
  else:
    return coincidences
  pass

def RegexInDictionary(dictionary,listOfRegex,beginend=False,show=False):
  # Searching toc identifieers coincidences
  coincidences={}
  begin={}
  end={}
  for key, value in dictionary.items():
    coinList=[]
    begList=[]
    endList=[]
    # Look for each toc identifier
    for regex in listOfRegex:
      for find in re.finditer(regex,value):
        coinList.append(find.group())
        begList.append(find.start())
        endList.append(find.end())
        pass
      if show is True:
        print('key: {}'.format(key))
        for find in re.finditer(regex,value):
          print(find.group())
          pass
        pass
      pass
    coincidences[key]=coinList
    begin[key]=begList
    end[key]=endList
    pass
  if beginend is True:
    return coincidences,begin,end
  else:
    return coincidences
  pass




