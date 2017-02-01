
# coding: utf-8

# In[9]:

import pandas as pd
import math
from collections import Counter
import pylab as plt



# In[2]:

#data=pd.read_excel("C:\\Users\\ShreeH\\Desktop\\WebScience\\Introduction to web science\\assignment10_itws\\Assignment10_itws\\onlyhash.data\\onlyhash.xlsx")
data=pd.read_excel("onlyhash.xlsx")


# In[24]:

# calculates the average user entropy for a date
#input date
#output average user entropy for that date

def UserEntropyDateWise(date):
    tempData=data[data['date']==date] # gives subset of data for that date
    singleUserEntropy={}
    userData=set(tempData.user) 
    for user in userData:
        hashtagData=tempData['hashtag'][tempData['user']==user]
        #print((hashtagData),user)
        hashtagList=[]
        for hashtag in hashtagData:
            hashtag=str(hashtag)
            # if the hashtag contains multiple hashtags then split it on space
            if hashtag.count('#') > 1:
                hashtagList=hashtagList+hashtag.split(' ')
            else:
                hashtagList.append(hashtag)
        # gives the count of the hashtags in for a user
        c=Counter((hashtagList))
        #print(c)
        n=(sum(c.values()))
        userEntropy=0
        # calculates the user entropy
        for item,value in c.items():
            proportion=value/n
            userEntropy=userEntropy-(proportion*math.log2(proportion))
            #print("ent",userEntropy)
        singleUserEntropy[user]=(userEntropy)
        
    return (sum(singleUserEntropy.values())/len(singleUserEntropy))    

        


# In[25]:

# calculates the system entropy for a date
#input date
#output system entropy for that date


def systemEntropy(date):
    #systemEntropyForDay={}
    hashtagData=data['hashtag'][data['date']==date]
    hashtagList=[]
    for hashtag in hashtagData:
        hashtag=str(hashtag)
        if hashtag.count('#') > 1:
            hashtagList=hashtagList+hashtag.split(' ')
        else:
            hashtagList.append(hashtag)
    c=Counter((hashtagList))
    n=(sum(c.values()))
    systemEntropy=0
    for item,value in c.items():
        prop=value/n
        systemEntropy=systemEntropy-(prop*math.log2(prop))
    #systemEntropyForDay[str(date)]=systemEntropy
    return systemEntropy


    


# In[33]:

#prepare 2 dictionary for datewise systemEntropy and userEntropy

systemEntropyMap={}
userEntropyMap={}
uniqueDates=set(data.date)# get all the unique dates in the dataset
for date in uniqueDates:  # iterating over the unique date to find the average user entropy and the system entropy
    dayWiseSystemEntropy=systemEntropy(date)
    stringDate=str(date)
    userEntropyMap[stringDate]=UserEntropyDateWise(date)
    systemEntropyMap[stringDate]=dayWiseSystemEntropy



        


# In[70]:

# dump the hashmap data to json file for further data processing

import json
with open ('C:\\Users\\ShreeH\\Desktop\\singleuserentropy.json', 'w') as fp:
    json.dump(userEntropyMap,fp)
    
with open ('C:\\Users\\ShreeH\\Desktop\\systementropy.json', 'w') as fp:
    json.dump(systemEntropyMap,fp)


# In[80]:

##loading the json data to the dictionary
with open('C:\\Users\\ShreeH\\Desktop\\systementropy.json') as data_file:    
    systemEntropyMap = json.load(data_file)

with open('C:\\Users\\ShreeH\\Desktop\\singleuserentropy.json') as data_file:    
    userEntropyMap = json.load(data_file)



# In[81]:

#prepare the data for plotting
# sort the user entropy and the system entropy on the basis of the date

sortedUserEntropyList=[]
xpoint=[]
i=0
for key in sorted(userEntropyMap):
    xpoint.append(i)
    i=i+1

    sortedUserEntropyList.append(userEntropyMap[key])

sortedSystemEntropyList=[]

for key in sorted(systemEntropyMap):
    sortedSystemEntropyList.append(systemEntropyMap[key])


# In[87]:

plt.xlabel("Day(0-384): 0 being the lowest system entropy and 384 the highest.")
plt.ylabel("Entropy")
systemEntropyPlot = plt.scatter(xpoint, sortedSystemEntropyList, color='b', marker='o', label='System entropy', alpha=0.5)
userEntropyPlot = plt.scatter(xpoint, sortedUserEntropyList, color='k', marker='+', label='User entropy', alpha=0.5)
plt.legend(handles=[systemEntropyPlot, userEntropyPlot],bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()


# In[ ]:

## as seen in the scatter plot the user entropy remains at constant level irrespective of the variations in the system entropy.
## which can  be interpreted as the average breadth of user's attention remains constant irrespective of the diversity in 
## the system
## this observed behavour is compatible with the findings of the author,which also represents that even
## though the system is made up of diverse memes, the users attention is confined to very few of them.

