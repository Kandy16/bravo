# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 17:42:14 2016

@author: Daniel
"""
import codecs
import matplotlib.pyplot as plt
import pandas
from collections import Counter
#import numpy as np

filename = "simple-20160801-1-article-per-line"

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

num_lines = 0
num_words = 0
num_Enchars = 0
num_Othchars =0
i=0
x= list()
y= list()


with codecs.open(filename , encoding='utf-8') as file:
#with codecs.open(filename) as file:
    text = file.read()
    
    for line in text:
        words = line.split()
        num_words += len(words)
        if line in alphabet and not "":
           
            num_Enchars += len(line)
            x.append(line.lower())
            
        else:
            num_Othchars +=len(line)
            y.append(line)
x.sort() 
           
def Plot(x,y):
    # Create a figure of size 8x6 inches, 80 dots per inch
    plt.figure(figsize=(8, 6), dpi=80)
    # Create a new subplot from a grid of 1x1
    plt.subplot(1, 1, 1)
        
    plt.title('Internal & External Links')
    plt.xlabel('Internal Links')
    plt.ylabel('External Links')
    plt.grid(True)
     
    plt.scatter(x,y,color="red")
    #plt.scatter(list,y, color="blue", label="External")
    plt.legend()
     
    plt.show()

def Histogram(x):
    letter_counts = Counter(x)
    df = pandas.DataFrame.from_dict(letter_counts, orient='index')
    df.plot(kind='bar')
   
    #plt.hist(len(letter_counts),bins=5)
    plt.title('Histogram')
    plt.xlim(-2,30)
    plt.xlabel("Alphabet")
    plt.ylabel("Frequencey")
    plt.show()
    
def Bar(x) :
    
    performance = [9000,4500,0]
    plt.bar(x, performance, align='center', alpha=0.5)
    #plt.xticks(y_pos, objects)
    plt.ylabel('Chars No')
    plt.title('Language')
    #plt.xticks(index ('English', 'Other''))
    plt.show()
        
TotalChar= num_Enchars + num_Othchars 
percent =  100 * float(num_Enchars)/float(TotalChar )   

print ("Words  ", num_words)
print ("Number of English Chars  ", num_Enchars)
print ("Number of Non English Chars  ", num_Othchars)
print ("Total Chars  ", TotalChar)
print("Percentage",percent)

print(Histogram(x))
print(Histogram(y))
#print(Bar(x))
#print("Percentage",y)

