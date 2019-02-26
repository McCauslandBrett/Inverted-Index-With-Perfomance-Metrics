# IRassn1

Design:
DATA_STRUCTURE_1: term        := user defined class that contains DATA_STRUCTURE_2: postings and number of documents its in
DATA_STRUCTURE_2: postings    := python dictionary, Key is filename, Value is number of keyword occurances
DATA_STRUCTURE_3: dict_docs   := python dictionary, Key is filename, Value is number of words
DATA_STRUCTURE_4: dict_terms  := python dictionary, Key is term "string" , Value is DATA_STRUCTURE_1: term 
DATA_STRUCTURE_5: stop_words  := python list, conatians all stopwords

parseing and indexing
 - Done with the use of functions:
     load_stops(stopwords,path):
          opens the file in the designated path with the stopwods and populates a list with the stopwords
        
     loadWcountWDoc(dict_terms,dict_docs,path):
           opens all files and loads the dictionary of document using 
           there filename as an index to the number of there word count
           PASSES every line of text for each file split on spaces TO word_count
     
     word_count(line, dict_terms,dict_docs,fname):
            processes every word in the document
            
     line_process(line, stopwords),  processes every word in a line
       
Input Output
- Prompt(dict_terms,dict_docs): called After the terms and documents have already been indexed, type (quit or QUIT) to stop

To run
- Download the entire zip file and open in Spyder and simply press play button.If you have any problems running please feel 
free to email me at bmcca009@ucr.edu

References: https://stackabuse.com/read-a-file-line-by-line-in-python/

