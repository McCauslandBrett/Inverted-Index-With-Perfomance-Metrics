# Custom Inverted Index w Querying and Performance Evaluation

Design:
DATA_STRUCTURE_1: term        := user defined class that contains DATA_STRUCTURE_2: postings and number of documents its in <br/>
DATA_STRUCTURE_2: postings    := python dictionary, Key is filename, Value is number of keyword occurances <br/>
DATA_STRUCTURE_3: dict_docs   := python dictionary, Key is filename, Value is number of words <br/>
DATA_STRUCTURE_4: dict_terms  := python dictionary, Key is term "string" , Value is DATA_STRUCTURE_1: term <br/>
DATA_STRUCTURE_5: stop_words  := python list, conatians all stopwords <br/>
DATA_STRUCTURE_6: InvertedIndex   := user defined class, Decorater of DATA_STRUCTURE_4 <br/>
DATA_STRUCTURE_7: StopWordManger  := user defined class <br/>
DATA_STRUCTURE_8: QueryList       := user defined class , Contains list of DATA_STRUCTURE_9 <br/>
DATA_STRUCTURE_9: Query           := user defined class <br/>

parseing and indexing <br/>
 - Done with the use of functions: <br/>
     load_stops(stopwords,path): <br/>
          opens the file in the designated path with the stopwods and populates a list with the stopwords <br/>
        
     loadWcountWDoc(dict_terms,dict_docs,path): <br/>
           opens all files and loads the dictionary of document using <br/>
           there filename as an index to the number of there word count <br/>
           PASSES every line of text for each file split on spaces TO word_count <br/>
     
     word_count(line, dict_terms,dict_docs,fname): <br/>
            processes every word in the document <br/>
            
     line_process(line, stopwords),  processes every word in a line <br/>
       
To run <br/>
- Download the entire zip file and open in Spyder and simply press play button. 

References: https://stackabuse.com/read-a-file-line-by-line-in-python/

