
# coding: utf-8

# In[83]:

import pandas as pd
import numpy as np
import sys
from collections import  Counter


# In[84]:

store=pd.HDFStore("C:\\Users\\ShreeH\\Desktop\\store2.h5")
df1=store['df1']
df2=store['df2']


# In[85]:

#split on space for each and every article

splittedArticles=df1[:].text.str.split()   # returns a series of splitted text

len(splittedArticles)   # all articles are included
type(splittedArticles)


# In[86]:

# the logic is to create an additional coulumn in the df1 dataframe containing a dictionary of termFrequency of each word and
# write it to a csv file

copyDF=df1.copy()
copyDF['termfrequency']=copyDF.text.map(lambda x: Counter(x.lower().split()).items())
copyDF['splitData']=copyDF.text.map(lambda x: set(x.split()))

copyDF.head()


# In[87]:


def temp_map_function(wordHist):
    newList = []

    for word in wordHist:
        num = 0
        if(word[1] > 0):
            num = 1
        tempList = [word[0], num]
        newList.append(tuple(tempList))
        #break
    return newList

#temp_function(copyDF['termfrequency'])
#temp_map_function(copyDF['termfrequency'][0])

#creating a column documentfrequency of each word 
copyDF['docfrequency']=copyDF.termfrequency.map(temp_map_function)


# In[88]:

copyDF.head()


# In[89]:




# In[112]:

def temp_docfreq_function(wordHist):
    dictofwords = {}
    
    for row in wordHist:
        #print(row)
        for word in row:
            if len(dictofwords)==0:
                num = 1
            elif word in dictofwords:
                num=0
                num=dictofwords[word]+1
            dictofwords[word]=num

    return dictofwords

tempDict=temp_docfreq_function(copyDF['splitData'])

#copyDF['docfrequency']=copyDF.termfrequency.map(temp_docfreq_function)


# In[135]:

import math
d=len(copyDF['name'])

def temp_tfidf_function(wordHist):
    ##tf-idf= tf of word * (number of documents/df(word))
    numofdocs=d
    dictofwords = {}
    for word in wordHist:
        #print((word[0]))
        if word[0] in tempDict:
            #print(word)           
        
            df=tempDict[word[0]] # get the document frequency of that word
            idf=math.log((numofdocs/df),10) # calculate the idf
            tfidf=idf*word[1]  # calculate the tf-idf= tf(word)*idf(word)
            dictofwords[word[0]]=tfidf
                   
    return dictofwords

#tfidfDict=temp_tfidf_function(copyDF['termfrequency'][0],len(copyDF['name']))
## creating a coulum tfidf for each word in an article
copyDF['tfidf']=copyDF.termfrequency.map(temp_tfidf_function)


# In[136]:

copyDF.head()


# In[ ]:




# In[162]:

def calcJaccardSimilarity(wordset1, wordset2):
    wordset1=set(wordset1)
    wordset2=set(wordset2)
    inter=wordset1.intersection(wordset2)
    union=wordset1.union(wordset2)
    jc=(len(inter)/len(union))
    return jc

Germany=copyDF['splitData'][copyDF['name']=='Germany']
Europe=copyDF['splitData'][copyDF['name']=='Europe']

#print(Germany.tolist()[0])
print('*****words in article splitted on space*****')
print('Jaccard coefficent for articles Germany and Europe:',calcJaccardSimilarity(Germany.tolist()[0],Europe.tolist()[0]))


# In[256]:

def calculateCosineSimilarity(CSGermany, CSEurope):

    temp=CSGermany.iteritems()
    temp2=CSEurope.iteritems()
    dict1=None
    dict2=None
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
            
print('Cosine Similarity of articles Germany and Europe:',calculateCosineSimilarity(CSGermany,CSEurope))
    
    
    


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



