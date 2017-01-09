
# coding: utf-8

import pandas as pd
import numpy as np
import sys
from collections import  Counter
import math


store=pd.HDFStore("store2.h5")
df1=store['df1']

#split on space for each and every article

splittedArticles=df1[:].text.str.split()   # returns a series of splitted text


# following code creates a word set for each and every article
copyDF=df1.copy()
copyDF['wordset']=copyDF.text.map(lambda x: set(x.split()))


def calcJaccardSimilarity(wordset1, wordset2):
    wordset1=set(wordset1)
    wordset2=set(wordset2)
    inter=wordset1.intersection(wordset2)
    union=wordset1.union(wordset2)
    jc=(len(inter)/len(union))
    return jc

Germany=copyDF['wordset'][copyDF['name']=='Germany']
Europe=copyDF['wordset'][copyDF['name']=='Europe']

#print(Germany.tolist()[0])
#print('*****words in article splitted on space*****')
print('Jaccard coefficent for articles Germany and Europe:',calcJaccardSimilarity(Germany.tolist()[0],Europe.tolist()[0]))


# In order to find cosine similarity - we need term frequency, document frequency (inverse of it)
# tf-idf score
# following creates term frequency
copyDF['termfrequency']=copyDF.text.map(lambda x: Counter(x.lower().split()).items())


# it goes through each article's wordset and find the document freq
def temp_docfreq_function(rows):
    dictofwords = {}
    
    for row in rows:
        #print(row)
        for word in row:
            if word in dictofwords:
                num=dictofwords[word]+1
            else:
                num=1
            dictofwords[word]=num

    return dictofwords

docFreqDict=temp_docfreq_function(copyDF['wordset'])

d=len(copyDF['name']) # row size

def temp_tfidf_function(wordHist):
    ##tf-idf= tf of word * (number of documents/df(word))
    numofdocs=d
    dictofwords = {}
    for word in wordHist:
        #word[0] - is the word (key)
        #word[1] - is the term freq value
        if word[0] in docFreqDict:
            #print(word)           
        
            df=docFreqDict[word[0]] # get the document frequency of that word
            idf=math.log((numofdocs/df),10) # calculate the idf
            tfidf=idf*word[1]  # calculate the tf-idf= tf(word)*idf(word)
            dictofwords[word[0]]=tfidf
                   
    return dictofwords

#tfidfDict=temp_tfidf_function(copyDF['termfrequency'][0],len(copyDF['name']))
## creating a coulum tfidf for each word in an article
copyDF['tfidf']=copyDF.termfrequency.map(temp_tfidf_function)

def calculateCosineSimilarity(doc1, doc2):

    temp=doc1.iteritems()
    temp2=doc2.iteritems()
    dict1=None
    dict2=None
    # the data structure is a list with two elements and second element is the dictonary
    # that we wanted
    for t2 in temp2:
        dict2=t2[1]
    for t in temp:
        dict1=(t[1])    
    dotprod=0
    for k1 in dict1:
        if k1 in dict2.keys():
            dotprod=dotprod+(dict1[k1]*dict2[k1])
    
    dict1dot=0
    dict2dot=0
    
    for key1 in dict1:
        dict1dot=dict1dot+(dict1[key1]*dict1[key1])

    for key2 in dict2:
        dict2dot=dict2dot+(dict2[key2]*dict2[key2])
        
    cosinesimilarity=dotprod/((math.sqrt(dict1dot))*(math.sqrt(dict2dot)))    
    
    return cosinesimilarity
    
  
  
CSGermany=copyDF['tfidf'][copyDF['name']=='Germany']
CSEurope=copyDF['tfidf'][copyDF['name']=='Europe']

#print(CSEurope)
            
print('Cosine Similarity of articles Germany and Europe:',calculateCosineSimilarity(CSGermany,CSEurope))

