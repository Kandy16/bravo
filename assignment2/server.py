# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 03:36:00 2016

@author: Shriharsh Ambhore
@author: Kandhasamy Rajasekaran
@author: Daniel Akbari
"""

import socket
import json
import sys
    

    
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    server_socket.bind(('localhost',8080))
except socket.error as msg:
    print ('Bind to socket failed.'+' Message ' + msg[1])
    sys.exit()
    
server_socket.listen(5)

while True:
    print('listening')
    conn,address=server_socket.accept()
    print ("connected on",address[1])
    dataFromClient=conn.recv(4096)
    print('Data from client:',dataFromClient.decode())
    
    recvdDict=json.loads(dataFromClient.decode())
    
    returnString="Name:"+recvdDict['Name']+";\n"+"Age:"+recvdDict['Age']+";\n"+"Matrikelnummer:"+recvdDict['Martrikelnumber']+";"
    
    conn.send(returnString.encode())
    conn.close()
    
