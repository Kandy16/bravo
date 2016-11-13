# -*- coding: utf-8 -*-
"""
server side code

Created on Mon Nov  7 03:36:00 2016

@author: Shriharsh Ambhore
@author: Kandhasamy Rajasekaran
@author: Daniel Akbari

url="http://www.example.com:80/path/to/myfile.html?key1=value1&key2=value2#InTheDocument"

"""

import socket
import sys
    

    
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


try:
    server_socket.bind(('localhost',8080))
except socket.error as msg:
    print ('Bind to socket failed.'+' Message ' + msg[1])
    sys.exit()
    
server_socket.listen(5)


while True:
    conn,address=server_socket.accept()
    dataFromClient=conn.recv(4096)
    url=dataFromClient.decode()
    print('Data from client:',dataFromClient)
    pos=url.find(":")

    if pos>0:
        tempvar=url[:pos]
        if url[pos:].find("//")> 0:
            protocol=tempvar
            print("protocol---",protocol)
            url=url[pos+3:] ## ignoring : and //
        if ":" in url:
            domain,url=url.split(":")
            print("domain---",domain)
            subdomain= domain[:(domain.rfind(".",1))]
            print("subdomain---",subdomain)
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
        
    else:
        domain=tempvar
        print("domain:",domain)
        if ":" in url:
            domain,url=url.split(":")
            print("domain---",domain)
            subdomain= domain[:(domain.rfind(".",1))]
            print("subdomain---",subdomain)
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
    
