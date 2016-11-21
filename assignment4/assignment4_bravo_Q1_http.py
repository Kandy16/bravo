#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 11:05:14 2016

@author: kandy
"""

import socket
import sys
import urllib

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

    try:
        socClient.connect((urlDomain, 80))
    except socket.error as e:
       print('Connection Invalid. Input proper URL !!!',e)
       return None
    except:
        print('Connection Invalid. Input proper URL !!!')
        return None
    
    # Form the http GET request. Two \r\n at the end is very important
    httpRequest = 'GET ' + urlPath + ' ' + urlScheme+'/1.0\r\n'
    httpRequest += 'Host: '+urlDomain+ '\r\n\r\n'
    
    # Send and Receive the data. Keep the data as bytes
    # Header needs to be extracted with UTF-8 encoding and if the resource content is TEXT
    # then the body can be encoded to UTF and saved in file
    # Otherwise it should be retained the same and saved
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
    
def extractHeaderAndResource(data):
    #The header and resource will be separated  by two \r\n's
    try:
        splitData = data.split(b'\r\n\r\n')
    except:
        splitData = [None, None]
    return splitData

def checkForRequest200(header):
    splittedHeader = header.split(b' ')
    #print('Inside check for request 200')
    #print(splittedHeader)
    if(splittedHeader):
        return splittedHeader[1] == b'200'
    return False
    
def saveResource(data,iname):
    fopen = open(iname,'wb')
    fopen.write(data)
    fopen.flush()
    fopen.close()           
    

try :
    socClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    urlInput = input('Input the URL : ')
    #urlInput = 'http://west.uni-koblenz.de/en/mws/dates/index.html'
    #urlInput = 'https://www.uni-koblenz-landau.de/de/koblenz/index.html'
    #urlInput = 'http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science'
    #urlInput = 'http://blog.ifimbschool.com/wp-content/uploads/2014/12/Hindi-Quote-on-overcoming-obstacles-with-unity-by-Atal-Bihar-Vajpayee-624x467.jpg'
    #urlInput = 'http://www.w3schools.com/tags/tag_link.asp'
    #urlInput = 'http://west.uni-koblenz.de/sites/default/files/styles/front-slider/public/fslide_1_0.jpg'
    
    [name, data] = getResource(socClient, urlInput)
    if (data):
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
    socClient.close()
finally:
    socClient = None
    
#print(urlInput)

