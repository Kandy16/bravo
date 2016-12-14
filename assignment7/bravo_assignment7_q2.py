#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 14:42:55 2016

@author: kandy
"""

import random
from bisect import bisect
import matplotlib.pyplot as plt

import collections

def createCDF(pdf) :
    pdfCount = len(pdf)
    for i in range(1, pdfCount):
            pdf[i] = pdf[i] + pdf[i-1]

class SimpleLanguageModel:
    
    def __init__(self, filePath):
        self.filePath = filePath
        self.countAndCreateCDF()
        
    def countAndCreateCDF(self):
        fb = open(self.filePath, encoding="utf-8")
        content = fb.read()
        self.characterCount = len(content)
        contentList = collections.Counter(content.split()).most_common()
        self.freq = [frequency for (key, frequency) in contentList]
        total = sum(self.freq)
        self.cdf = [value/total for value in self.freq]
        
        createCDF(self.cdf)

        '''for i in range(0, 10) :
            print(self.cdf[i])
        cdfCount = len(self.cdf)  
        print("...")
        for i in range(cdfCount-10, cdfCount) :
            print(self.cdf[i])'''
    freq = []
    cdf = []
    characterCount = 0

zipf_probabilities = {' ': 0.17840450037213465, '1': 0.004478392057619917, '0': 0.003671824660673643, '3': 0.0011831834225755678, '2': 0.0026051307175779174, '5': 0.0011916662329062454, '4': 0.0011108979455528355, '7': 0.001079651630435706, '6': 0.0010859164582487295, '9': 0.0026071152282516083, '8': 0.0012921888323905763, '_': 2.3580656240324293e-05, 'a': 0.07264712490903191, 'c': 0.02563767289222365, 'b': 0.013368688579962115, 'e': 0.09688273452496411, 'd': 0.029857183586861923, 'g': 0.015076820473031856, 'f': 0.017232219565845877, 'i': 0.06007894642873102, 'h': 0.03934894249122837, 'k': 0.006067466280926215, 'j': 0.0018537015877810488, 'm': 0.022165129421030945, 'l': 0.03389465109649857, 'o': 0.05792847618595622, 'n': 0.058519445305660105, 'q': 0.0006185966212395744, 'p': 0.016245321110753712, 's': 0.055506530071283755, 'r': 0.05221605572640867, 'u': 0.020582942617121572, 't': 0.06805204881206219, 'w': 0.013964469813783246, 'v': 0.007927199224676324, 'y': 0.013084644140464391, 'x': 0.0014600810295164054, 'z': 0.001048859288348506}
uniform_probabilities = {' ': 0.1875, 'a': 0.03125, 'c': 0.03125, 'b': 0.03125, 'e': 0.03125, 'd': 0.03125, 'g': 0.03125, 'f': 0.03125, 'i': 0.03125, 'h': 0.03125, 'k': 0.03125, 'j': 0.03125, 'm': 0.03125, 'l': 0.03125, 'o': 0.03125, 'n': 0.03125, 'q': 0.03125, 'p': 0.03125, 's': 0.03125, 'r': 0.03125, 'u': 0.03125, 't': 0.03125, 'w': 0.03125, 'v': 0.03125, 'y': 0.03125, 'x': 0.03125, 'z': 0.03125}


# goes through a distribution fuction and calculates CDF
zipfCumDist = list(zipf_probabilities.values())
createCDF(zipfCumDist)
zipfCharacters = ''.join(list(zipf_probabilities.keys()))
#print(zipfCumDist)

uniformCumDist = list(uniform_probabilities.values())
createCDF(uniformCumDist)
uniformCharacters = ''.join(list(uniform_probabilities.keys()))

slm = SimpleLanguageModel("simple-wiki")
print('Simple Wiki character count ',slm.characterCount)

rand = random.Random()
zipRandlist = []

for i in range(0,slm.characterCount):
    zipRandlist.append(zipfCharacters[bisect(zipfCumDist, rand.random())])
    #print(characters[bisect(zipfCumDist, rand.random())],end='')    

print('zipf content generated')
zipfContent = ''.join(zipRandlist)

fp = open('zipf-generated-file','w')
fp.write(zipfContent)
fp.flush()
fp.close()

print('zipf content written')


uniformRandlist = []

for i in range(0,slm.characterCount):
    uniformRandlist.append(uniformCharacters[bisect(uniformCumDist, rand.random())])
    #print(characters[bisect(zipfCumDist, rand.random())],end='')    

print('uniform content generated')

uniformContent = ''.join(uniformRandlist)

fp = open('uniform-generated-file','w')
fp.write(uniformContent)
fp.flush()
fp.close()

print('uniform content written')



simpleWiki = SimpleLanguageModel('simple-wiki')
zipLangModel = SimpleLanguageModel('zipf-generated-file-bkp')
uniformLangModel = SimpleLanguageModel('uniform-generated-file-bkp')


plt.figure(1,figsize=(10,5))
plt.xscale('log')
plt.yscale('log')
plt.xlabel('rank')
plt.ylabel('frequency')
plt.plot(simpleWiki.freq, color='blue', linewidth=1.0, linestyle='-',label='Simple WIKI')
plt.plot(zipLangModel.freq, color='red', linewidth=1.0, linestyle='-', label='Zipf Generated')
plt.plot(uniformLangModel.freq, color='green', linewidth=1.0, linestyle='-', label='Uniform Generated')
plt.legend(loc='upper right')
plt.title('Rank Freq diagram for all 3 datasets')
plt.grid()

plt.show()


plt.figure(2,figsize=(10,5))
plt.xscale('log')
plt.xlabel('rank')
plt.ylabel('CDF')
plt.plot(simpleWiki.cdf, color='blue', linewidth=1.0, linestyle='-',label='Simple WIKI')
plt.plot(zipLangModel.cdf, color='red', linewidth=1.0, linestyle='-', label='Zipf Generated')
plt.plot(uniformLangModel.cdf, color='green', linewidth=1.0, linestyle='-', label='Uniform Generated')
plt.legend(loc='upper right')
plt.title('Cumulative Distribution for all 3 datasets')
plt.grid()


print(len(zipLangModel.cdf))
print(len(simpleWiki.cdf))
print(zipLangModel.characterCount)
print(simpleWiki.characterCount)
print(len(zipLangModel.freq))
print(len(simpleWiki.freq))

#kolmogorov smirnov test
#wikiZip =  zip(simpleWiki.cdf ,zipLangModel.cdf)
kolDisZip = max([abs(x-y) for (x,y) in zip(zipLangModel.cdf,simpleWiki.cdf)])

print('Kolmogorov smirnov test value for Simple wiki and Zipf generative model is ',kolDisZip)


#wikiUni =  zip(simpleWiki.cdf ,uniformLangModel.cdf)
kolDisUni = max([abs(x-y) for (x,y) in zip(simpleWiki.cdf ,uniformLangModel.cdf)])

print('Kolmogorov smirnov test value for Simple wiki and Uniform generative model is ',kolDisUni)

