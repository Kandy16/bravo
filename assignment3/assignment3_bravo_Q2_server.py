# -*- coding: utf-8 -*-
"""
server side code

Created on Mon Nov  7 03:36:00 2016

@author: Shriharsh Ambhore
@author: Kandhasamy Rajasekaran
@author: Daniel Akbari


"""

import socket
import sys
    

    
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


try:
    server_socket.bind(('localhost',8080))
except socket.error as msg:
    print ('Bind to socket failed.'+' Message ' + msg[1])
    sys.exit()
    
server_socket.listen(1)


while True:
    conn,address=server_socket.accept()
    dataFromClient=conn.recv(4096)
    url=dataFromClient.decode()
    print('Data from client:',dataFromClient) # data received from client
    ## at any point of time  characters  :?#/[]@  are reserved as delimeters     

    pos=url.find(":")
    subdomainlist = []
    if pos>0:
        tempvar=url[:pos]
        if url[pos:].find("//")> 0: # if the url contains the protocol then execute this block i.e  https://www.google.com
            protocol=tempvar # 
            print("protocol---",protocol)
            url=url[pos+3:] ## ignoring : and //
        if ":" in url: ## check for : to get the domain 
            domain,url=url.split(":")
            print("domain---",domain)
            #subdomain= domain[:(domain.find(".",1))]
            
            subdomainlist.append(domain)
            gblsd = ""
            
            while domain.find(".")!=-1:  # find . in the domain for finding the  subdomain 
                remainingUrl,sd=domain.rsplit(".",1)    # split from right hand side which gives www.example, com
                sd="."+sd+gblsd 
                subdomainlist.append(sd.lstrip("."))    #add valid string to the list
                gblsd=sd                                # change the string from www.example.com to www.example
                domain=remainingUrl
            
            print("subdomain---",subdomainlist)
        if "#" in url:  ## split on # to get the fragment
            url,anchor=url.split("#",1)
            print("fragment---",anchor)
        if "?" in url: ## split on ? to get the query
            url,query=url.split("?",1)
            print("query---",query)
        if "/" in url:   ## split on / to get the port and the path
            port,path=url.split("/",1)
            if port.isdigit():
                print("port---",port)
            else:
                print("domain",port)
                subdomain= port[:(port.rfind(".",2))]
                print("subdomain---",subdomain)
            print("path---",path)
        
    else:       # if the url does not contain any protocol specified i.e www.google.com
        domain=tempvar  
        print("domain:",domain)
        if ":" in url:
            domain,url=url.split(":")
            print("domain---",domain)
            #subdomain= domain[:(domain.rfind(".",1))]
            gblsd = ""
            
            while domain.find(".")!=-1:
                remainingUrl,sd=domain.rsplit(".",1)
                sd="."+sd+gblsd
                subdomainlist.append(sd.lstrip("."))
                gblsd=sd
                domain=remainingUrl
            
            print("subdomain---",subdomainlist)
            
        if "#" in url:
            url,anchor=url.split("#",1)
            print("fragment---",anchor)
        if "?" in url:
            url,query=url.split("?",1)
            print("query---",query)
        if "/" in url:
            port,path=url.split("/",1)
            print("port---",port)
            print("path---",path)
   
    
    conn.close()
    
