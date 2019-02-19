#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 13:25:58 2019

@author: Brettmccausland
"""
from ObjectFiles import *
from bs4  import BeautifulSoup
import numpy as np
import pandas as pd
import operator
from nltk.stem import PorterStemmer
ps = PorterStemmer()

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
                        
             