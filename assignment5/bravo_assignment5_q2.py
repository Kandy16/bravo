# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 19:28:21 2016

@author: Shriharsh Ambhore
@author: Kandhasamy Rajasekaran
@author: Daniel Akbari
web crawler

Assumptions
links = number of internal & external links per page
webpage= a page which is physically downloaded

"""

import logging
import urllib
import socket
import re
import os
import collections
from urllib import parse
from functions import *


logging.basicConfig(filename="info.log",level=logging.INFO)


counter=0
# total number of wepages encountered till the end
totalWebPageList=[]

#dict data structure containing  parentWebPage and ListofLinks in parentWebPage
linksPerWebPage={}

#this list containes the webpages that needs to be crawled
#toCrawlLinks=collections.deque()
toCrawlLinks=[]
#dict  where key= Parent Webpage, value = list[2]  list[0]=internalLinks,list[1]=externalLinks
intExtWebPageCounter={}

invalidHttpResponseCounter=[]
webpageCounter=0


    

def getResource(socClient, urlInput):
    
    try: 
        urlObj = urllib.parse.urlparse(urlInput)
        #print(urlObj)
        logging.info(urlObj)
    except:
        print('Invalid URL',urlInput)
        return None
    try:
            
        urlScheme = urlObj[0] #http
        urlDomain = urlObj[1] #full domain name
        urlPath = urlObj[2]
        #resourceName = (urlPath[urlPath.rfind("/")+1:])
        
        # Form the http GET request. Two \r\n at the end is very important
        httpRequest = 'GET ' + urlPath + ' ' + urlScheme+'/1.0\r\n'
        httpRequest += 'Host: '+urlDomain+ '\r\n\r\n'
        
        socClient.send(httpRequest.encode('utf-8'))
        temp = socClient.recv(4096)
        data = bytearray()
        while (temp != b''):
            #print(temp)
            # Tried a lot to append in bulk
            # RIght now appending char by char
            for char in temp :
                data.append(char)
            temp = socClient.recv(4096)
        
        return [urlPath, data]
    except socket.error as msg:
        print("Error in creating a socket connection",msg)


    
def extractHeaderAndResource(data):
    #The header and resource will be separated  by two \r\n's
    try:
        splitData = data.split(b'\r\n\r\n') #for actual testing
        #splitData = data.split(b'\n\n',1) # for local instance
        #print(len(splitData))
    except:
        print("exception")
        splitData = [None, None]
    return splitData

def checkForRequest200(header):
    splittedHeader = header.split(b' ')
    if(splittedHeader):
        return splittedHeader[1] == b'200'
    return False
    
def saveResource(data,iname):
    global webpageCounter
    try:
        #print("iname==",iname)
        directoryPath=iname[:iname.rfind("\\")]
        #print("Directory Path====",directoryPath)
        if not os.path.exists(directoryPath):
            #print("creating directory")
            os.makedirs(directoryPath,exist_ok=True)
            
        fopen = open(iname,'wb')
        fopen.write(data)
        fopen.flush()
        fopen.close()
        webpageCounter=webpageCounter+1
    except IOError as io:
         pass
           
    
def downloadResource(socClient,receivedurl):
#    global invalidHttpResponseCounter
    #print("urlInput===========",receivedurl)
    [name, data] = getResource(socClient,receivedurl)
    name=parse.unquote(name)
    #print("name",name)


    localPath=os.getcwd()+name
    localPath=os.path.normpath(localPath)
    
                    
    if(name == ''):
        name = 'index.html'
    if (data):
        try:
            #print("data is available!!!",data)
            header,resource = extractHeaderAndResource(data)
            #print("Resource====",len(resource))
            if (header):
                #print("header is available")
                if(checkForRequest200(header)) :
                    #print("sending this location for file===",localPath)
                    saveResource(resource,localPath)
                    #print('Resource is downloaded successfully !!!')
#                else:
#                    #print('Invalid Http response !!!!')
#                    invalidHttpResponseCounter.append(name)
                    
            else:
                print('Header and Resource extraction is invalid for url',urlInput)
        except:
            print('Error in downloading the resource !!!')
    return localPath


    
def extractLinkInformationUrl(path):
    #print("fileLocation",fileLocation)
    
    try:
        hrefPattern=re.compile(r'<a [^>]*href="([^"]+)')
        
        #print("file path received==",path)
        if os.path.isfile(path):
            #print("yes it is a file!!!")
            with  open(path,"r",encoding='utf8') as file:
                con=file.read()
                linkList=(hrefPattern.findall(con))
                #filers out other domain links e.g wikitionary
                internalLinks=list(filter(lambda x: x.find('articles')!=-1 ,linkList))
                externalLinks=list(filter(lambda y: y.find('http')!=-1 or y.find('https')!=-1 or y.find('www')!=-1 ,linkList))
                return [internalLinks,externalLinks]

        else:
            #print("invalid file path")
            return[None,None]
            pass
    except IOError as e:
        print("Error in file handling",e)


def createFullUrl(orgUrl,loc):
    url = urllib.parse.urlparse(orgUrl)
    #print(url)
    path = url.path
    hostname = "http://"+url[1]
    if path == "":
        path = "/"

    # absolut path
    if loc[0]=="/":
        url = hostname + loc
    #fully qualified domain name
    elif len(loc) > 7 and loc[0:7]=="http://":
        url = loc
    # relative path
    else:
        parentfolders = 0
        while len(loc)>3 and loc[0:3]=="../":
            loc = loc[3:]
            parentfolders= parentfolders + 1
            url = hostname + "/".join(path.split("/")[0:-(1+parentfolders)])+"/"+loc
    return url            
    
    
    ## starting point of the prog



try :
    
    socClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    urlInput='http://141.26.208.82/articles/g/e/r/Germany.html'
    #urlInput = 'http://localhost/articles/g/e/r/Germany.html'
    urlInputObj = urllib.parse.urlparse(urlInput)
    socClient.connect((urlInputObj[1], 80))
    #print("Sending this url====>>",urlInput)
    url=urlInput
    file=downloadResource(socClient,url)
    inLinks,outLinks=extractLinkInformationUrl(file)
    toCrawlLinks=list(set(toCrawlLinks+inLinks))
    
    #print("toCrawlList====",toCrawlLinks)
    counter=len(inLinks)
    linksPerWebPage[file]=len(inLinks)
    #print(linksPerWebPage)            
    inoutList=[None]*2
    inoutList[0]=len(inLinks)
    #toCrawlLinks=toCrawlLinks.append(inLinks)
    inoutList[1]=len(outLinks)
    intExtWebPageCounter[file]=inoutList
    inoutList= None
    #print("Internal links and External Links counter per web page",intExtWebPageCounter)
    crawledLinks=collections.deque()
    
    
    toCrawlLinks=list(set(toCrawlLinks))
    #print("length=========",len(toCrawlLinks))
    
    
    
    intj=0
    while len(toCrawlLinks)>0:
        if intj>150:
            print("breaking now!!!")
            break
    
        #print("Length of links==",len(toCrawlLinks))
        i=toCrawlLinks.pop(0)
        #logging.info("popped",i)
        try:
                
            tempClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            completeUrl=createFullUrl(url,i)
            tempClient.connect((urlInputObj[1], 80))
            tempFile=downloadResource(tempClient,completeUrl)
            if (tempFile):
                tempInLinks,tempOutLinks=extractLinkInformationUrl(tempFile)
                if (tempInLinks or tempOutLinks):
                    
                    #print("tempInLinks===",len(list(set(tempInLinks))))
                    #add the in links to the toCrawlLinks   list
                    toCrawlLinks=toCrawlLinks+list(set(tempInLinks))
                    
                    tempInOutList=[None]*2
            #        # keep an record of links found per page
                    linksPerWebPage[tempFile]=(len(tempInLinks)+len(tempOutLinks))
            #        # keep an record of number of internalLinks and externalLinks per page
                    tempInOutList[0]=len(tempInLinks)
                    tempInOutList[1]=len(tempOutLinks)
                    intExtWebPageCounter[tempFile]=tempInOutList
            #        print("intExtWebPageCounter",intExtWebPageCounter)
                    tempInOutList= None
            #        print("currently popped=====",i)
                    crawledLinks.append(i)
                   # toCrawlLinks.remove(i)
                    counter=counter+(len(tempInLinks)+len(tempOutLinks))
                tempClient.close()
        except socket.error as e:
            pass
        intj=intj+1
        if intj%100==0:
            print("Counter:::",intj)
            #print("Invalid Response Counter:::",len(invalidHttpResponseCounter))
            print("toCrawlLinks length",len(toCrawlLinks))
        
        
            
    print("-----****printing the stats****-----")    
    
    #print("length=========",len(toCrawlLinks))
    #logging.info(len(toCrawlLinks))
    #print("Invalid links==",invalidHttpResponseCounter)
    print("Total number of Links found===",counter)
    print("***************************")
    #logging.info("Total number of Links found===",counter)
    print("Total number of WebPages found===",len(crawledLinks))
    print("***************************")
    #logging.info("Total number of WebPages found===",len(crawledLinks))
    print("Internal and External Links per Webpage",intExtWebPageCounter)
    #logging.info("Internal and External Links per Webpage",intExtWebPageCounter)
    #print("Crawled Links====",crawledLinks)
    print("***************************")
    print("Links per web Page====",linksPerWebPage)
    #logging.info("Links per web Page====",linksPerWebPage)
    
    print ('Average is:', Average(linksPerWebPage))
    print ('Median is:',Median(linksPerWebPage))
    print (Histogram(linksPerWebPage))
    print(Plot(intExtWebPageCounter))
    
    
    
    
    socClient.close()
except socket.error as msg:
    print('Error in socket connection',msg)
finally:
    socClient = None
    logging.shutdown()
    



