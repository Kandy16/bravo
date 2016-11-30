# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 08:14:25 2016

@author: Daniel Akbari
@author: Shriharsh Ambhore
@author: Kandhasamy Rajasekaran
"""


import statistics 
import matplotlib.pyplot as plt
#import array

#list=input('dict with key as web page and number of links per webpage as value')
def Average(linksPerWebPage):
    
    valueList=list(linksPerWebPage.values())
    avg=(sum(valueList)/(len(valueList)))
    return avg
    
def Median(linksPerWebPage):
    valueList=list(linksPerWebPage.values())
    return statistics.median(valueList)

def Histogram(linksPerWebPage):
    plt.hist(list(linksPerWebPage.values()),bins=5)
    plt.title('Histogram')
    plt.xlim(0,150)
    plt.xlabel("Bins")
    plt.ylabel("Frequencey")
    plt.show()
    
def Plot(intExtWebPageCounter):
    # Create a figure of size 8x6 inches, 80 dots per inch
    plt.figure(figsize=(8, 6), dpi=80)
    # Create a new subplot from a grid of 1x1
    plt.subplot(1, 1, 1)
    
    data = intExtWebPageCounter
    
    for coord in data.items():
        data["x"].append(coord[0])
        data["y"].append(coord[1])
        
    plt.title('Internal & External Links')
    plt.xlabel('Internal Links')
    plt.ylabel('External Links')
    plt.grid(True)
     
    plt.scatter(data["x"],data["y"],color="red")
    #plt.scatter(list,y, color="blue", label="External")
    plt.legend()
     
    plt.show()
#    
#list=[1,2,3,5,11,75]
#x=[2,6,5,9,15,17]
#y=[4,1,5,9,18,7]
#print ('Average is:', Average(list))
#print ('Median is:',Median(list))
##print (Plot(x,y))
#print (Histogram(list))
