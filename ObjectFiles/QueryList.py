#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 13:56:50 2019

@author: Brettmccausland
"""
from ObjectFiles import *
import glob
from nltk.stem import PorterStemmer

ps = PorterStemmer()

class QueryList:
    
    def __init__(self,path_querys,list_stopwords,output_path):
     self.list_querys = []
     self.path= path_querys  
     self.loadquerylist(list_stopwords)
     self.outputfile= output_path
                 
   # precondition: dictionary terms, dictionary documents
   # postcondition:
   # Summary:            
      # for each query in list of querys
      #  compare it with each doc everydoc
      # rank all the documents
      # save results for each query to a file
    def runQuerylist(self,dict_terms,dict_docs):
         for each_query in self.list_querys:
           for each_doc in dict_docs:
            each_query.setdocScores(each_doc,dict_terms,dict_docs)
            each_query.setRanks()
            each_query.saveQuerytofile(self.outputfile)
            
     
    def loadquerylist(self,list_stopwords):
      files = glob.glob(self.path)
      for fname in files:
       with open(fname) as f: #file
         for line in f:
             i=line.index("Document")
             k=line.index('.')
             num= line[:k]
             line=line[i+13:]
             query=Query(line,list_stopwords, num)
             self.list_querys.append(query)  

               
            
             
             