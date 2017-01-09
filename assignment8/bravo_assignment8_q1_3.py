
# coding: utf-8

import pandas as pd
import numpy as np
import sys
from collections import  Counter
import math

#import bravo_assignment8_q1_1 as q1

store=pd.HDFStore("C:\\Users\\ShreeH\\Desktop\\store2.h5")
text_df = store['df1']
out_link_df=store['df2']

text_df = text_df.iloc[0:10]
#print(text_df.head)
out_link_df = out_link_df.iloc[0:10]


# following code creates a word set for each and every article
text_df['wordset']=text_df.text.map(lambda x: set(x.lower().split()))


def calcJaccardSimilarity(wordset1, wordset2):
    wordset1=set(wordset1)
    wordset2=set(wordset2)
    inter=wordset1.intersection(wordset2)
    union=wordset1.union(wordset2)
    jc=(len(inter)/len(union))
    return jc
    

text_df['termfrequency']=text_df.text.map(lambda x: Counter(x.lower().split()).items())

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

docFreqDict=temp_docfreq_function(text_df['wordset'])

d=len(text_df['name']) # row size

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

## creating a coulum tfidf for each word in an article
text_df['tfidf']=text_df.termfrequency.map(temp_tfidf_function)

def calculateCosineSimilarity(dict1, dict2):
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
    
print('---------------------------------------------------------------------')

#print(text_df['name'])
#print(out_link_df['name'])

germanJackardListRank = []
germanCosineSimilarityListRank = []
germanRow = text_df[text_df['name']=='German']
j = 0
rows_count = text_df.shape[0]

while (j < rows_count):
    row = text_df.iloc[j]
    germanCosineSimilarityListRank.append(calculateCosineSimilarity(row['tfidf'], germanRow['tfidf'].iloc[0]))
    germanJackardListRank.append(calcJaccardSimilarity(row['wordset'], germanRow['wordset'].iloc[0]))
    j = j + 1
   
    
print(germanCosineSimilarityListRank)
print(germanJackardListRank)

'''    
for row in text_iterate:
    #print(row[0])
    #print(row[1].tfidf)
    print(type(germanRow['tfidf']))
    print(type(row[1]['tfidf']))
    germanListRank.append(calculateCosineSimilarity(germanRow['tfidf'], row[1]['tfidf']))
    #print(type(row))
    break
'''