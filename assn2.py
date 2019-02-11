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

import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import operator
from operator import itemgetter, attrgetter
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import train_test_split
import bs4 as bs
import urllib.request
import urllib

import pandas as pd
from collections import namedtuple
import pandas as pd

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
# Assnment 2
from bs4  import BeautifulSoup
ps = PorterStemmer()

class Query:
    def __init__(self,str_words,stopwords):
     self.rank=0
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
     #self.vectorSpace()
     for word in self.dict_words:
             self.tf_wieghts.append(self.dict_words[word]/self.numwords)
              
     def getTF(self,word):
         return self.dict_words[word]/self.numwords
     
     def vectorSpace(self):
         for word in self.dict_words:
             self.tf_wieghts.append(self.getTF(word))
   
  
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
              #tf, idf, and tf-idf i
         #print(post,self.postings[post])



def load_stops(stopwords,path):

 spath = path + "/*.txt"
 files = glob.glob(spath)
 for fname in files:
     with open(fname) as f: #file
         for line in f:
             load_line(line.strip().split(' '), stopwords)


def load_line(l_line, stopwords):
   for word in l_line:
       stopwords.insert(0,word.lower())


# makes all word in line lowercase
# implements stemming
# Updates word count in fname for every word
#
def line_proc(line, dict_terms,dict_docs,fname,stopwords):
   for word in line:
       w=word.lower()
       w=ps.stem(w)
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

def loadInvertedIndex(dict_terms,dict_docs,path,filetype,stopwords):
      if(filetype=="trec"):
         print(' trec ')
         soup = BeautifulSoup(open(path),"lxml")
         #print(soup)
         for doc in soup.find_all('doc'):
            for eachdoc in doc.find_all('docno'):
                s=eachdoc.text.strip().split(' ')
                filename=s[0]
                dict_docs[filename] = 0
                for txt in doc.find('text'):
                  line_proc(txt.strip().split(' '),dict_terms,dict_docs, filename,stopwords)
                        
             

def Prompt(dict_terms,dict_docs):
 run=True
 while run:
   x=input('enter the term of interest.')
   x=x.lower()
   x=ps.stem(x)
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
#Part 1 -
def cosineSimilarity(arr_query, arr_doc):
	dot_product = np.dot(arr_query,arr_doc)
	norm_query = np.linalg.norm(arr_query)
	norm_doc = np.linalg.norm(arr_doc)
	return dot_product / (norm_query * norm_doc )

"""def preprocessQuery(str_Query,stopwords):
    w=[]
    l=[]
    words = ps.stem(str_Query).lower().strip().split(' ')
    for w in words:
        if w not in stopwords:
            l.append(w)
    return l
"""           
def documentRelavanceScore(fname,Query,dict_terms,stopwords,dict_docs):
    # Use the vector space model to compute scores
    # Use cosine Similarity to compute score between 
    # Query and document
    
    #qi is the tf-idf weight of term i in the query
    #di is the tf_idf term i in the document
    d=[]
    print(fname)
    for word in Query.dict_words: #check every word in the query
       print(word) 
       if word in dict_terms: # if word is a dictionary word
          print(word,"in dictionary")
          curterm = dict_terms[word] # get term from dictionary
          #curterm.printPostings()    
          # curterm.get_Doc_tf(fname,dict_docs) # access the posting in the term for doc
          d.append(curterm.get_IDF_TF(fname,dict_docs))
          """ if curterm.existposting(fname):
            print("match")
            post = curterm.getPostings()
            print(post)
            print("match")"""
       
        
    

#Part 2 - Query Execution
#run the queries in the file results file.txt
"""def RunQuerylist(path,stopwords):
 spath = path + "/*.txt"
 files = glob.glob(spath)
 for fname in files:
     with open(fname) as f: #file
         for line in f:
             line_proc(line, dict_terms,dict_docs,fname,stopwords)
             line_proc(line.strip().split(' '),dict_terms,dict_docs, filename,stopwords)
"""
def DriverAssnment1():
    # load stop words
    stopwords=[]
    path1="stopwords"
    load_stops(stopwords,path1)

    # load distionary with counts
    dict_terms={}
    dict_docs={}
    path2="data"
    loadWcountWDoc(dict_terms,dict_docs,path2)
    t=dict_terms['system']
    #t.display_wieghtings(dict_docs)
    Prompt(dict_terms,dict_docs)

def DriverParserUpdate(stopwords,dict_terms,dict_docs):
     # load stop words

    path1="stopwords"
    load_stops(stopwords,path1)

    path2="data/ap98_collection.html"
    filetype="trec"


    loadInvertedIndex(dict_terms,dict_docs,path2,filetype,stopwords)
#  soup.get_text()



stopwords=[]
dict_terms={}
dict_docs={}
path1="stopwords"
load_stops(stopwords,path1)
path2="data/ap89_collection.html"

filetype="trec"
loadInvertedIndex(dict_terms,dict_docs,path2,filetype,stopwords)
"""
#DriverParserUpdate(stopwords,dict_terms,dict_docs)
"""
# ----------------------- driver documentRelavanceScore ------------------------

fname= 'AP890101-0003'
query_str = " A fast-spreading fire swept through a home "
query=Query(query_str,stopwords)
documentRelavanceScore(fname,query,dict_terms,stopwords,dict_docs)






