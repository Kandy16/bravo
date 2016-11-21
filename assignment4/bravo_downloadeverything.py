# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 22:05:14 2016

@author: Shriharsh Ambhore
@author: Kandhasamy Rajasekaran
@author: Daniel Akbari
"""

from assign4_p1 import extractHeaderAndResource
from assign4_p1 import getResource
import urllib

import os
import socket
import re



def extractImageUrl(fileLocation):
    urllist=[]
    pattern=re.compile('src="([^"]+)"') # regex for extracting the value of src attribute
    with  open(fileLocation) as f:
        for l in f:
            if "<img" in l:
                matches = re.findall(pattern,l)
                urllist.append(matches[0])

    return urllist

#fileLocation=input("Enter the html file location of the downloaded file:")
fileLoc="C:\\Users\\ShreeH\\resource"
#url=input("Enter the url from which the file was downloaded:")
inputurl='http://west.uni-koblenz.de'

listOfURL=extractImageUrl(fileLoc)

print("List of URLs",listOfURL)

# call the function from another file to download the resource


def savingResources(data,iname):
    if (data):
        header,resource = extractHeaderAndResource(data)
        if header is not None:
            print("saving header",header)          
            header = header.decode('utf-8')
            if(header):
                fopen = open(iname+'.resource.header','wb')
                fopen.write(data)
                fopen.flush()
                fopen.close()
            else:
                print('Header Extract failed')
            
        #Check the format of resource and based on that
        # the serialization will be different
        if resource is not None:
            print("saving resource",resource)
            if(resource):
                with open(os.getcwd()+"\\"+iname,'wb') as fopen:
                    fopen.write(fopen)
                    #fopen.flush()

                    fopen.close()
            else:
                print('Resource content Extract failed')

            


# iterate over the url to download the image 
for url in listOfURL:
    socClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    path=urllib.parse.urlparse(url).path
    imageName=(path[path.rfind("/")+1:])
    if url.find(inputurl)== -1:
        #append the input url to construct the absolute path for the image
        url=inputurl+url;
        data = getResource(socClient,url)
        savingResources(data,imageName)
    else:
        data=getResource(socClient,url)
        savingResources(data,imageName)
    url=None
    data=None            
socClient.close()
            
    


