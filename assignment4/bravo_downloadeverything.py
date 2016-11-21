# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 22:05:14 2016

@author: Shriharsh Ambhore
@author: Kandhasamy Rajasekaran
@author: Daniel Akbari
"""

#from assignment4_bravo_Q1_http import downloadResource
import urllib

import os
import socket
import re
import time

import sys
import urllib
from assignment4_bravo_functions import *

def getResource(socClient, urlInput):
    
    try: 
        urlObj = urllib.parse.urlparse(urlInput)
        print(urlObj)
    except:
        print('Invalid URL')
        return None
    
    urlScheme = urlObj[0] #http
    urlDomain = urlObj[1] #full domain name
    urlPath = urlObj[2]
    resourceName = (urlPath[urlPath.rfind("/")+1:])

    
    
    # Form the http GET request. Two \r\n at the end is very important
    httpRequest = 'GET ' + urlPath + ' ' + urlScheme+'/1.0\r\n'
    httpRequest += 'Host: '+urlDomain+ '\r\n\r\n'
    
    # Send and Receive the data. Keep the data as bytes
    # Header needs to be extracted with UTF-8 encoding and if the resource content is TEXT
    # then the body can be encoded to UTF and saved in file
    # Otherwise it should be retained the same and saved
    
    print('Inside get resource !!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(httpRequest)
    socClient.send(httpRequest.encode('utf-8'))
    temp = socClient.recv(4096)
    data = bytearray()
    while (temp != b''):
        print('looping in !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        #print(temp)
        # Tried a lot to append in bulk
        # RIght now appending char by char
        for char in temp :
            data.append(char)
        temp = socClient.recv(4096)
    return [resourceName, data]
    
def extractHeaderAndResource(data):
    #The header and resource will be separated  by two \r\n's
    try:
        splitData = data.split(b'\r\n\r\n')
        #print(splitData)
    except:
        splitData = [None, None]
    return splitData

def checkForRequest200(header):
    splittedHeader = header.split(b' ')
    print('Inside check for request 200')
    #print(splittedHeader)
    if(splittedHeader):
        return splittedHeader[1] == b'200'
    return False
    
def saveResource(data,iname):
    fopen = open(iname,'wb')
    fopen.write(data)
    fopen.flush()
    fopen.close()           
    
def downloadResource(socClient, urlInput):
    [name, data] = getResource(socClient, urlInput)
    if(name == ''):
        name = 'index.html'
    if (data):
        #try:
            header,resource = extractHeaderAndResource(data)
            if (header):
                if(checkForRequest200(header)) :
                    saveResource(header,name+'.header')
                    saveResource(resource,name)
                    print('Resource is downloaded successfully !!!')
                else:
                    print('Invalid Http response !!!!')
            else:
                print('Header and Resource extraction is invalid')


def extractImageUrl(fileLocation):
    urllist=[]
    pattern=re.compile('src="([^"]+)"') # regex for extracting the value of src attribute
    hrefPattern=re.compile('href="([^"]+)"')
    with  open(fileLocation) as f:
        for l in f:
            #print("**** currently reading::",l)
            if "<img" in l:
                matches = re.findall(pattern,l)
                urllist.append(matches[0])
                #print("****** found an img tab:")
            #elif "<link" in l:
            #    found=re.findall(hrefPattern,l)
            #    urllist.append(found[0])
                

    return urllist

#fileLoc=input("Enter the html file location of the downloaded file:")
fileLoc = 'index.html'
#fileLoc="C:\\Users\\ShreeH\\resource"
#inputurl=input("Enter the url from which the file was downloaded:")
inputurl='http://west.uni-koblenz.de'

listOfURL=extractImageUrl(fileLoc)

print("List of URLs",listOfURL)
  
socClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try: 
    urlObj = urllib.parse.urlparse(inputurl)
except:
    print('Invalid URL')

urlScheme = urlObj[0] #http
urlDomain = urlObj[1] #full domain name
urlPath = urlObj[2]
try:
    socClient.connect((urlDomain, 80))
except socket.error as e:
   print('Connection Invalid. Input proper URL !!!',e)
except:
    print('Connection Invalid. Input proper URL !!!')

# iterate over the url to download the image 
for url in listOfURL:
    
    path=urllib.parse.urlparse(url).path
    imageName=(path[path.rfind("/")+1:])
    tempUrl = url
    if url.find(inputurl)== -1:
        #append the input url to construct the absolute path for the image
        tempUrl=inputurl+url
  
    downloadResource(socClient,tempUrl)
    time.sleep(5)
url=None
data=None 
           
socClient.close()
            
    


