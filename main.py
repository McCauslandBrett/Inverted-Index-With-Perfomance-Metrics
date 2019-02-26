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


from StopWordManger import *
from InvertedIndex import *
from QueryList import *
import numpy as np

import pandas as pd




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
def driverInvertedobject():
   
   #load stopwords
   stopwords = StopWordManger("stopwords")
   
   #load data
   Invertobj = InvertedIndex("data/ap89_collection.html",stopwords.list_stopwords)
   
   #load QuerysList
   Qlist= QueryList("querys/query_list.txt",stopwords.list_stopwords,'results_file')
   
   # Run querys
   Qlist.runQuerylist(Invertobj.dict_terms,Invertobj.dict_docs)


def main():
    
 driverInvertedobject()
 
if __name__ == "__main__":
    main()     
        




