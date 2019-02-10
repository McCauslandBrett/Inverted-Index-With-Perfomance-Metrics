#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 17:12:00 2019

@author: Brettmccausland
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:29:44 2019
References: https://stackabuse.com/read-a-file-line-by-line-in-python/
@author: Brettmccausland
"""

import math
import glob
import errno
import os
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import operator
from operator import itemgetter, attrgetter
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import train_test_split

import pandas as pd
from collections import namedtuple
import pandas as pd


class term:
    def __init__(self,numdocs,postings):
        self.numdocs=numdocs
        self.postings=postings

    def insertposting(self,fname):
        self.postings[fname]=1
        self.numdocs+=1

    def incrdocfreq(self,fname):
        self.postings[fname]+=1

    def existposting(self,fname):
      if fname in self.postings:
          return True
      return False

    def display_wieghtings(self,dict_docs):
       for post in self.postings:
          #print(post)
          numwords_in_post=dict_docs[post]
          #print( numwords_in_post)
          term_freq = self.postings[post]
          #print (term_freq)
          tf= term_freq/numwords_in_post
          numdicts=len(dict_docs)
          #print(numdicts)
          numdoc_term_in= len(self.postings)
          df= numdicts/numdoc_term_in+1
          idf = math.log(2, df)
          #print(idf)
          print(post,',',round(tf,4),',',round(idf,4),',',round(tf*idf,4))
              #tf, idf, and tf-idf i
         #print(post,self.postings[post])



def load_stops(stopwords,path):

 spath = path + "/*.txt"
 files = glob.glob(spath)
 for fname in files:
     with open(fname) as f: #file
         cnt = 0
         for line in f:
             line_process(line.strip().split(' '), stopwords)
             cnt += 1

def line_process(line, stopwords):
   for word in line:
       stopwords.insert(0,word.lower())

# dict_term={term,#docs,postings{fname,docFreq}}

def word_count(line, dict_terms,dict_docs,fname):
   for word in line:
       w=word.lower()
       if w not in stopwords:
           dict_docs[fname] += 1
           if w in dict_terms:
               curterm= dict_terms[w]
               if curterm.existposting(fname):
                   curterm.incrdocfreq(fname)
               else:
                   curterm.insertposting(fname)
           else:
               postings={}
               postings[fname]=1
               t =term(1,postings)
               dict_terms[w] = t

def loadWcountWDoc(dict_terms,dict_docs,path):
 spath = path + "/*.txt"
 files = glob.glob(spath)
 for fname in files:
     filename=fname[5:]
     dict_docs[filename] = 0
     with open(fname) as f: #file
         for line in f:
             word_count(line.strip().split(' '),dict_terms,dict_docs, filename)

def Prompt(dict_terms,dict_docs):
 run=True

 while run:
   x=input('enter the term of interest.')
   x=x.lower()
   if x =='quit':
       run=False
       continue
   if x in dict_terms:
       term=dict_terms[x]
       print("list of the postings for that term:")
       #print(t.postings)
       term.display_wieghtings(dict_docs)

   else:
       print('not in the inverted file')





# load stop words
stopwords=[]
path1="s"
load_stops(stopwords,path1)
ps = PorterStemmer()
# load distionary with counts

dict_terms={}
dict_docs={}
path2="data"
loadWcountWDoc(dict_terms,dict_docs,path2)
t=dict_terms['system']
#t.display_wieghtings(dict_docs)
Prompt(dict_terms,dict_docs)
