#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 13:25:58 2019

@author: Brettmccausland
"""

from bs4  import BeautifulSoup
import numpy as np
import pandas as pd
import operator
from nltk.stem import PorterStemmer
ps = PorterStemmer()



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 18:59:57 2019

@author: Brettmccausland
"""
import math
class term:
    def __init__(self,numdocs,postings):
        self.numdocs=numdocs
        self.postings=postings
        self.tf=0
        self.numDocTermIn = 0

    def insertposting(self,fname):
        self.postings[fname]=1
        self.numdocs+=1

    def incrdocfreq(self,fname):
        self.postings[fname]+=1

    def existposting(self,fname):
      if fname in self.postings:
          return True
      return False
  
    def printPostings(self):
        print(self.postings)
        
    def getPostings(self):
        return self.postings
    
    def get_Doc_tf(self,doc,dict_docs):
        if doc in self.postings:
         postnum=self.postings[doc]
         num_word_in_doc=dict_docs[doc]
         return postnum/num_word_in_doc
        else:
         return 0
     
    def get_IDF_TF(self,doc,dict_docs):
          tot_numdocs=len(dict_docs)
          df= tot_numdocs/self.numdocs+1
          idf = math.log(2, df)
          return self.get_Doc_tf(doc,dict_docs) * idf
        
    def display_wieghtings(self,dict_docs):
       for post in self.postings:
          numwords_in_post=dict_docs[post]
          #print( numwords_in_post)
          term_freq = self.postings[post]
          #print (term_freq)
          tf = term_freq/numwords_in_post
          numdicts=len(dict_docs)
          #print(numdicts)
          df= numdicts/self.numdocs
          idf = math.log(2, df)
          #print(idf)
          print(post,',',round(tf,4),',',round(idf,4),',',round(tf*idf,4))
  
    

class InvertedIndex:
    
    def __init__(self,_path,_stopwords):
        self.dict_terms={}
        self.dict_docs={}
        self.stopwords=_stopwords
        self.path=_path
        self.loadInvertedIndex(_path,_stopwords)
        
#precondition:
#postcondition: 
#Summary:
 # makes all word in line lowercase
 # implements stemming
 # Updates word count in fname for every word
    def line_proc(self,line,dict_docs,fname,stopwords):
      for word in line:
        w=ps.stem(word)
        if w not in stopwords:
           w=word.lower()
           dict_docs[fname] += 1
           if w in self.dict_terms:
               curterm= self.dict_terms[w]
               if curterm.existposting(fname):
                   curterm.incrdocfreq(fname)
               else:
                   curterm.insertposting(fname)
           else:
               postings={}
               postings[fname]=1
               t = term(1,postings)
               self.dict_terms[w] = t
               
#precondition:
#postcondition:  
    def loadInvertedIndex(self,path,stopwords):
         soup = BeautifulSoup(open(path),"lxml")
         for doc in soup.find_all('doc'):
            for eachdoc in doc.find_all('docno'):
                s=eachdoc.text.strip().split(' ')
                filename=s[0]
                self.dict_docs[filename] = 0
                for txt in doc.find('text'):
                  self.line_proc(txt.strip().split(' '),self.dict_docs, filename,stopwords)
                        
             