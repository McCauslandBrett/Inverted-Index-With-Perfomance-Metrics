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

    def insertposting(self,fname):
        self.postings[fname]=1
        self.numdocs+=1

    def incrdocfreq(self,fname):
        self.postings[fname]+=1

    def existposting(self,fname):
      if fname in self.postings:
          return True
      return False
  
    
    def get_Doc_tf(self,doc,dict_docs):
         postnum=self.postings[doc]
         num_word_in_doc=dict_docs[doc]
         return postnum/num_word_in_doc
    
    def get_Doc_idf(self,doc,dict_docs):
          tot_numdocs=len(dict_docs)
          df= tot_numdocs/self.numdocs+1
          idf = math.log(2, df)
          return idf
       
     
    def get_IDF_TF(self,doc,dict_docs):
          idf = self.get_Doc_idf(doc,dict_docs)
          tf  = self.get_Doc_tf(doc,dict_docs)
          return  tf * idf


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
                        
             