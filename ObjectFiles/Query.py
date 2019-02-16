#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 18:58:49 2019

@author: Brettmccausland
"""

class Query:
    
    def __init__(self,str_words,stopwords,query_num):
     self.Scores={}
     self.Ranks=[]
     self.Identifier=str_words
     self.idnum=query_num
     self.dict_words={}
     self.numwords=0
     self.tf_wieghts=[]
     
     words = ps.stem(str_words).lower().strip().split(' ')
     for w in words:
        if w not in stopwords:
            if w in self.dict_words:
              self.dict_words[w]+= 1
              self.numwords+=1
            else:
              self.dict_words[w] = 1
              self.numwords+=1
 
     for word in self.dict_words:
             self.tf_wieghts.append(self.dict_words[word]/self.numwords)
              
     def getTF(self,word):
         return self.dict_words[word]/self.numwords
     
     def vectorSpace(self):
         for word in self.dict_words:
             self.tf_wieghts.append(self.getTF(word))
    
    def generateRank(self):
        print('genrerateRank Scores before',self.Scores)
        
        
    def saveQuerytofile(self):
        file=open(str(self.idnum)+".txt", "a+")
        print(self.Ranks)
        print(self.idnum)