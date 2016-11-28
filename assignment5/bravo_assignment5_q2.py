# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 19:28:21 2016

@author: Shriharsh Ambhore
@author: Kandhasamy Rajasekaran
@author: Daniel Akbari
web crawler
"""


import urllib
import socket
import re
import os
import collections

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



    

def getResource(socClient, urlInput):
    
    try: 
        urlObj = urllib.parse.urlparse(urlInput)
        print(urlObj)
    except:
        print('Invalid URL',urlInput)
        return None
    try:
            
        urlScheme = urlObj[0] #http
        urlDomain = urlObj[1] #full domain name
        urlPath = urlObj[2]
        resourceName = (urlPath[urlPath.rfind("/")+1:])
        
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
        return [resourceName, data]
    except socket.error as msg:
        print("Error in creating a socket connection",msg)


    
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
    if(splittedHeader):
        return splittedHeader[1] == b'200'
    return False
    
def saveResource(data,iname):
    fopen = open(iname,'wb')
    fopen.write(data)
    fopen.flush()
    fopen.close()           
    
def downloadResource(socClient,receivedurl):
    print("urlInput===========",receivedurl)
    [name, data] = getResource(socClient,receivedurl)
    if(name == ''):
        name = 'index.html'
    if (data):
        try:
            header,resource = extractHeaderAndResource(data)
            if (header):
                if(checkForRequest200(header)) :
                    #saveResource(header,name+'.header')
                    print("Saving file !!!!",name)
                    saveResource(resource,name)
                    print('Resource is downloaded successfully !!!')
                else:
                    print('Invalid Http response !!!!')
            else:
                print('Header and Resource extraction is invalid for url',urlInput)
        except:
            print('Error in downloading the resource !!!')
    return name

## starting point of the prog

    
def extractLinkInformationUrl(fileLocation):
    print("fileLocation",fileLocation)
    
    try:
        hrefPattern=re.compile(r'<a [^>]*href="([^"]+)')
        path=os.getcwd()+"\\"+fileLocation
        print("file path generated==",path)
        if os.path.isfile(path):
            print("yes it is a file!!!")
            with  open(path,"r",encoding='utf8') as file:
                con=file.read()
                linkList=(hrefPattern.findall(con))
                #filers out other domain links e.g wikitionary
                internalLinks=list(filter(lambda x: x.find('articles')!=-1 ,linkList))
                externalLinks=list(filter(lambda y: y.find('http')!=-1 or y.find('https')!=-1 or y.find('www')!=-1 ,linkList))
                return [internalLinks,externalLinks]

        else:
            print("invalid file path")
            pass
    except IOError as e:
        print("Error in file handling",e)


def createFullUrl(orgUrl,loc):
    url = urllib.parse.urlparse(orgUrl)
    print(url)
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
    
    
    


try :
    
    socClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    urlInput = 'http://141.26.208.82/articles/g/e/r/Germany.html'
    urlInputObj = urllib.parse.urlparse(urlInput)
    socClient.connect((urlInputObj[1], 80))
    print("Sending this url====>>",urlInput)
    url=urlInput
    file=downloadResource(socClient,url)
    inLinks,outLinks=extractLinkInformationUrl(file)
    toCrawlLinks=toCrawlLinks+inLinks
    counter=len(inLinks)
    linksPerWebPage[file]=len(inLinks)
    #print(linksPerWebPage)            
    counter=len(outLinks)
    print("webpage counter",counter)
    inoutList=[None]*2
    inoutList[0]=len(inLinks)
    #toCrawlLinks=toCrawlLinks.append(inLinks)
    inoutList[1]=len(outLinks)
    intExtWebPageCounter[file]=inoutList
    inoutList= None
    #print("Internal links and External Links counter per web page",intExtWebPageCounter)
    crawledLinks=collections.deque()
    
    
    for i in toCrawlLinks:
        tempClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Calling url ===",i)
        completeUrl=createFullUrl(url,i)
        tempClient.connect((urlInputObj[1], 80))
        tempFile=downloadResource(tempClient,completeUrl)
        if not(tempFile):
            tempInLinks,tempOutLinks=extractLinkInformationUrl(tempFile)
                
            #add the in links to the toCrawlLinks   list
            toCrawlLinks.extend(tempInLinks)
            # keep an record of links found per page
            linksPerWebPage[tempFile]=len(tempInLinks)
            # keep an record of number of internalLinks and externalLinks per page
            tempInOutList=[None]*2
            tempInOutList[0]=len(tempInLinks)
            tempInOutList[1]=len(tempOutLinks)
            intExtWebPageCounter[tempFile]=tempInOutList
            #tempInOutList= None
            crawledLinks.append(i)
            toCrawlLinks.remove(i)
            counter=counter+len(tempInLinks)
            tempClient.close()

        
    
    print("Total Web Pages===",counter)
    print("Internal and External Links per Webpage",intExtWebPageCounter)
    print("Crawled Links====",crawledLinks)
    
    
    
    socClient.close()
except socket.error as msg:
    print('Error in socket connection',msg)
finally:
    socClient = None



