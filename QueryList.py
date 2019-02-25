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

from nltk.stem import PorterStemmer
import numpy as np
ps = PorterStemmer()
from operator import itemgetter, attrgetter
import operator
from sklearn.metrics.pairwise import cosine_similarity
class Query:

    def __init__(self,str_words,list_stopwords,query_num):
     self.docScores={}
     self.Ranks=[]
     self.Identifier=str_words
     self.idnum=query_num
     self.dict_querywords = {}
     self.numwords=0
     self.tfwieghts=[]
     self.load_query(list_stopwords)


    def load_query(self,list_stopwords):
       words = ps.stem(self.Identifier).lower().strip().split(' ')
       for w in words:
          if( w not in list_stopwords and w in self.dict_querywords ):
              self.dict_querywords[w]+= 1
              self.numwords+=1
          else:
              self.dict_querywords[w] = 1
              self.numwords+=1
       self.setlist_tfwieghts()

    def getTF(self,word):
         return self.dict_querywords[word]/self.numwords

    def setlist_tfwieghts(self):
         for word in self.dict_querywords:
             self.tfwieghts.append(self.getTF(word))
         self.tfwieghts = np.array(self.tfwieghts)

#precondition:
  #  Query contains dict of words
  #  dict terms contains the terms in vec space

#postcondition:
  #  Query Scores Key: fname , Value: Cosine Similarity is added for all Querys
  #  Document space is built on the same vector space as the query
    def setdocScores(self,fname,dict_terms,dict_docs):
     doc_space=[] # document space
     for word in self.dict_querywords: # check every word in the query
       if word in dict_terms:     # if word is a dictionary word
          curterm = dict_terms[word] # get term from dictionary
          if curterm.existposting(fname): # check if file has term from the postings in the term
           doc_space.append(curterm.get_IDF_TF(fname,dict_docs)) # add wieghting to document space
          else:
            doc_space.append(0) # add wieght of 0 if term is not in doc
       else:
            doc_space.append(0) # add wieght of 0 if term is not in dict aka not in postings
     self.docScores[fname]= self.cosineSimilarity(doc_space)

    def setRanks(self):
        Sortedscores = sorted(self.docScores.items(), key=operator.itemgetter(1),reverse=True)
        rank=1
        for items in Sortedscores:
            #   (rank, doc_no , score )
            tup=(rank,items[0],items[1])
            self.Ranks.append(tup)
            rank+=1

    #precondition:
    #postcondition:
    def cosineSimilarity(self,arr_doc):
      dot = np.dot(arr_doc,self.tfwieghts)
      normarr_doc = np.linalg.norm(arr_doc)
      normtfwieghts = np.linalg.norm(self.tfwieghts)
      return dot / ((normarr_doc * normtfwieghts) + 1)


    #precondition:
    #postcondition:
    def saveQuerytofile(self,path):
        # <query−number> Q0 <docno> <rank> <score> Exp
        file = open(path+".txt", 'a+')
        querynumber= str(self.idnum)
        for tups in self.Ranks:
            rank=str(tups[0])
            docno=str(tups[1])
            score=str(tups[2])
            file.writelines(querynumber +' Q0 ' + docno +' ' + rank +' '+ score + ' Exp ' + "\n")
        file.close()
      


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

               
            
             
             