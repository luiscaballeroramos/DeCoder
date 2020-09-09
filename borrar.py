# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 11:43:22 2020

@author: lcr
"""


import nltk
from nltk.corpus import treebank
# nltk.download()
text=pages[9]
# %%
sent_detector=nltk.data.load('tokenizers/punkt/english.pickle')
aux=sent_detector.tokenize(text.strip())
i=2
for i in sent_detector.tokenize(text.strip()):
  print('\n---------------------------------\n')
  tokens=nltk.word_tokenize(i)
  # print('\n-----\n'.join(tokens))
  tagged=nltk.pos_tag(tokens)
  # entities=nltk.chunk.ne_chunk(tagged)
  # t=treebank.parsed_sents('wsj_0001.mrg')[0]
  # t.draw()
  ok=False
  for tag in tagged:
    if tag[1] in ['NNP','VB','VBD','VBG','VBN','VBP','VBZ']:
      ok=True
    else:
      pass
  if ok==True:
    print(i)
  else:
    print(tagged)

text='''Scope (1) This part
of EN 1993 gives design methods for the design of joints to predominantly static loading using steel grades S235, S355, S420,
S450 and S460 1.2 Normative references
This European Standard incorporates by dated or undated reference, provisions tiOln other publications.
'''




