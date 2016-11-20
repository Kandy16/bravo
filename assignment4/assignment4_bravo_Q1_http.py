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

    try:
        socClient.connect((urlDomain, 80))
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
    return data
    
def extractHeaderAndResource(data):
    #The header and resource will be separated  by two \r\n's
    try:
        splitData = data.split(b'\r\n\r\n')
    except:
        splitData = [None, None]
    return splitData
    
    
    
    

try :
    socClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #urlInput = input('Input the URL : ')
    urlInput = 'http://west.uni-koblenz.de/en/mws/dates'
    #urlInput = 'invalid input'
    
    data = getResource(socClient, urlInput)
    
    if (data):
        header,resource = extractHeaderAndResource(data)
        header = header.decode('utf-8')
        if(header):
            fopen = open('resource.header','w')
            fopen.write(header)
            fopen.close()
        else:
            print('Header Extract failed')
            
        #Check the format of resource and based on that
        # the serialization will be different
        
        resource = resource.decode('utf-8')
        if(resource):
            fopen = open('resource','w')
            fopen.write(resource)
            fopen.close()
        else:
            print('Resource content Extract failed')

               
    socClient.close()
finally:
    socClient = None
    
#print(urlInput)

