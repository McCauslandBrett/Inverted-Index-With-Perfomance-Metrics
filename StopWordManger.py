#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 14:15:51 2019

@author: Brettmccausland
"""
import glob
class StopWordManger:
    
   def __init__(self,spath):
      self.path = spath + "/*.txt"
      self.list_stopwords=[]
      self.load_stops()
#precondition:
#postcondition:  
   def load_stops(self):
       files = glob.glob(self.path)
       for fname in files:
           with open(fname) as f: #file
            for line in f:
                self.load_line(line.strip().split(' '))
#precondition:
#postcondition:  
   def load_line(self,l_line):
        for word in l_line:
            self.list_stopwords.insert(0,word.lower())
            
            
