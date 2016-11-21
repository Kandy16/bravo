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
    pattern=re.compile(r'<img [^>]*src="([^"]+)') # regex for extracting the value of src attribute
    hrefPattern=re.compile(r'<link [^>]*href="([^"]+)')
    with  open(fileLocation) as f:
        con=f.read()
        
        urllist= pattern.findall(con)
        urlhref=(hrefPattern.findall(con))

    return urllist+urlhref

fileLoc=input("Enter the html file location of the downloaded file:")
#fileLoc="C:\\Users\\ShreeH\\resource"
url=input("Enter the url from which the file was downloaded:")
#nputurl='http://west.uni-koblenz.de'

listOfURL=extractImageUrl(fileLoc)

print("List of URLs:::::::",listOfURL)

# call the function from another file to download the resource


def savingResources(data,iname):
    if (data):
        header,resource = extractHeaderAndResource(data)
        if header is not None:
            if(header):
                fopen = open(iname+'.resource.header','wb')
                fopen.write(header)
                fopen.flush()
                fopen.close()
            else:
                print('Header Extract failed')
            
        #Check the format of resource and based on that
        # the serialization will be different
        if resource is not None:
            if(resource):
                fopen = open(os.getcwd()+"\\"+iname,'wb')
                #resource.strip(b"\r\n\r\n")
                fopen.write(resource)
                fopen.flush()
                fopen.close()
#               
            else:
                print('Resource content Extract failed')

#filters out list .css and non image files
imageList = list(filter(lambda x: x.find('.ico')!=-1 or x.find('.png')!=-1 or x.find('.jpg')!=-1 or x.find('.jpg')!=-1 ,listOfURL))

print("final image list::::",imageList)
# iterate over the url to download the image 
for url in imageList:
    
    socClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    path=urllib.parse.urlparse(url).path
    imageName=(path[path.rfind("/")+1:])
    if url.find(inputurl)== -1:
        #append the input url to construct the absolute path for the image
        
        url=inputurl+url;
        print("Calling this url:::::",url)
        data = getResource(socClient,url)
        savingResources(data,imageName)
    else:
        print("Calling this url:::::",url)
        data=getResource(socClient,url)
        savingResources(data,imageName)
    url=None
    data=None            
socClient.close()
            
    


