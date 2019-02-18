#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 18:58:49 2019

@author: Brettmccausland
"""
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from operator import itemgetter, attrgetter
import operator
class Query:
    
    def __init__(self,str_words,list_stopwords,query_num):
     self.Scores={}
     self.Ranks=[]
     self.Identifier=str_words
     self.idnum=query_num
     self.dict_querywords = {}
     self.numwords=0
     self.list_tfwieghts=[]
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
             self.list_tfwieghts.append(self.getTF(word))
        
#precondition: 
  #  Query contains dict of words  
  #  dict terms contains the terms in vec space
     
#postcondition: 
  #  Query Scores Key: fname , Value: Cosine Similarity is added for all Querys
  #  Document space is built on the same vector space as the query        
    def setScores(self,fname,dict_terms,dict_docs):
     doc_space=[] # document space
     for word in self.dict_querywords: # check every word in the query
       if word in dict_terms:     # if word is a dictionary word
          curterm = dict_terms[word] # get term from dictionary
          if curterm.existposting(fname): # check if file has term from the postings in the term
           doc_space.append(curterm.set_IDF_TF(fname,dict_docs)) # add wieghting to document space
          else:
            doc_space.append(0) # add wieght of 0 if term is not in doc 
       else:
            doc_space.append(0) # add wieght of 0 if term is not in dict aka not in postings
     Query.Scores[fname]= cosineSimilarity(doc_space, self.list_tfwieghts)  # add cosine sim score for the file  

    def setRanks(self):
        for query in self.Scores:
         self.Ranks = sorted(self.Scores.items(), key=operator.itemgetter(1))
        '''self.Ranks= list(self.Scores.items())
        self.Ranks= sorted(self.Ranks, key=itemgetter(1),reverse=True)'''
        
    #precondition:
    #postcondition:  
    def cosineSimilarity(self,arr_query, arr_doc):
       """ dot_product = np.dot(arr_query,arr_doc)
        m_query = np.linalg.norm(arr_query)
        m_doc = np.linalg.norm(arr_doc)
        return  dot_product / (norm_query * norm_doc ) + 1"""


    #precondition:
    #postcondition:            
    def saveQuerytofile(self):
        # <query−number> Q0 <docno> <rank> <score> Exp
       print(self.idnum)
       """ file = open(self.idnum+".txt", 'w')
        res_list = [x[1] for x in self.Ranks]
        for lines in res_list:
            #print(lines)
            file.writelines(str(lines)+"\n")
        file.close()
        """
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        