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

from ObjectFiles import *
import numpy as np

import pandas as pd

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


#precondition:
#postcondition:  
def load_stops(stopwords,path):

 spath = path + "/*.txt"
 files = glob.glob(spath)
 for fname in files:
     with open(fname) as f: #file
         for line in f:
             load_line(line.strip().split(' '), stopwords)


#precondition:
#postcondition:  
def load_line(l_line, stopwords):
   for word in l_line:
       stopwords.insert(0,word.lower())



#precondition:
#postcondition:
#Summary:
 # makes all word in line lowercase
 # implements stemming
 # Updates word count in fname for every word
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
               
#precondition:
#postcondition:  
def loadInvertedIndex(dict_terms,dict_docs,path,filetype,stopwords):
      if(filetype=="trec"):
         #print(' trec ')
         soup = BeautifulSoup(open(path),"lxml")
         #print(soup)
         for doc in soup.find_all('doc'):
            for eachdoc in doc.find_all('docno'):
                s=eachdoc.text.strip().split(' ')
                filename=s[0]
                dict_docs[filename] = 0
                for txt in doc.find('text'):
                  line_proc(txt.strip().split(' '),dict_terms,dict_docs, filename,stopwords)
                        
             
#precondition:
#postcondition:  
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
       term.display_wieghtings(dict_docs)
   else:
       print('not in the inverted file')

#precondition:
#postcondition:  
def cosineSimilarity(arr_query, arr_doc):
	dot_product = np.dot(arr_query,arr_doc)
	norm_query = np.linalg.norm(arr_query)
	norm_doc = np.linalg.norm(arr_doc)
	return dot_product / (norm_query * norm_doc )


#precondition:
#postcondition:           
def documentRelavanceScore(fname,Query,dict_terms,stopwords,dict_docs):
    # Use the vector space model to compute scores
    # Use cosine Similarity to compute score between 
    # Query and document
    
    #qi is the tf-idf weight of term i in the query
    #di is the tf_idf term i in the document
    d=[]
    #print(fname)
    for word in Query.dict_words: #check every word in the query
       #print(word) 
       if word in dict_terms: # if word is a dictionary word
          #print(word,"in dictionary")
          curterm = dict_terms[word] # get term from dictionary
          if curterm.existposting(fname):
           # print("match")
            d.append(curterm.get_IDF_TF(fname,dict_docs))
          else:
            d.append(0)
       else:
            d.append(0)
    #print(d)
    #print(cosineSimilarity(d, Query.tf_wieghts))
    Query.Scores[fname]=cosineSimilarity(d, Query.tf_wieghts)    
    

#Part 2 - Query Execution
#run the queries in the file results file.txt


#precondition:
#postcondition:  
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
    Prompt(dict_terms,dict_docs)

#precondition:
#postcondition:  
def DriverParserUpdate(stopwords,dict_terms,dict_docs):
     # load stop words
    path1="stopwords"
    load_stops(stopwords,path1)
    path2="data/ap98_collection.html"
    filetype="trec"
    loadInvertedIndex(dict_terms,dict_docs,path2,filetype,stopwords)

#precondition:
#postcondition:  
def loadquerys(list_querys,path):
 files = glob.glob(path)
 num=0
 for fname in files:
     with open(fname) as f: #file
         for line in f:
             num+=1
             i=line.index("Document")
             line=line[i+13:]
             print(line)
             query=Query(line,stopwords, num)
             list_querys.append(query)

# precondition:
# postcondition:
 # Summary:            
 # for each query in list of querys
 #  compare it with each doc everydoc
 # rank all the documents
 # save results for each query to a file
def RunQuerylist(list_querys,dict_terms,stopwords,dict_docs):
    query_num=0
    for each_query in list_querys:
        query_num+=1
        for each_doc in dict_docs:
            documentRelavanceScore(each_doc,each_query,dict_terms,stopwords,dict_docs)
        each_query.generateRank()
        each_query.saveQuerytofile()
  

#precondition:
#postcondition:  
def RankQuerylist(list_querys):
    for query in list_querys:
        query.Ranks = sorted(query.Scores.items(), key=operator.itemgetter(1))
       
def main():
 # display some lines
 stopwords=[]
 dict_terms={}
 dict_docs={}
 path1="stopwords"
 load_stops(stopwords,path1)
 path2="data/ap89_collection.html"
 filetype="trec"
 loadInvertedIndex(dict_terms,dict_docs,path2,filetype,stopwords)
 query_str = " A fast-spreading fire swept through a home "
 query=Query(query_str,stopwords,1)
 print(query.dict_words)
 print(query.tf_wieghts)
# ----------------------- driver document Relavance Score ------------------------
 list_querys=[]
 path_querys="querys/query_list.txt"
 loadquerys(list_querys,path_querys)
 RunQuerylist(list_querys,dict_terms,stopwords,dict_docs)
if __name__ == "__main__":
    main()     
        




