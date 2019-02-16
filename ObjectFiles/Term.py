#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 18:59:57 2019

@author: Brettmccausland
"""

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
  
    def printPostings(self):
        print(self.postings)
        
    def getPostings(self):
        return self.postings
    
    def get_Doc_tf(self,doc,dict_docs):
        if fname in self.postings:
         postnum=self.postings[doc]
         num_word_in_doc=dict_docs[doc]
         return postnum/num_word_in_doc
        else:
         return 0
     
    def get_IDF_TF(self,doc,dict_docs):
          tot_numdocs=len(dict_docs)
          numdoc_term_in= len(self.postings)
          df= tot_numdocs/numdoc_term_in+1
          idf = math.log(2, df)
          return self.get_Doc_tf(doc,dict_docs) * idf
        
    def display_wieghtings(self,dict_docs):
       for post in self.postings:
          #print(post)
          numwords_in_post=dict_docs[post]
          #print( numwords_in_post)
          term_freq = self.postings[post]
          #print (term_freq)
          tf = term_freq/numwords_in_post
          numdicts=len(dict_docs)
          #print(numdicts)
          numdoc_term_in= len(self.postings)
          df= numdicts/numdoc_term_in+1
          idf = math.log(2, df)
          #print(idf)
          print(post,',',round(tf,4),',',round(idf,4),',',round(tf*idf,4))
  
    