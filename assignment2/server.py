# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 03:36:00 2016

@author: Shriharsh Ambhore
@author: Kandhasamy Rajasekaran
@author: Daniel Akbari
"""

import socket
import json
    
server_details=('localhost',8080)
    
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(server_details)
server_socket.listen(5)

conn,address=server_socket.accept()
print ("connected on",address)
while True:
    print('listening')
    dataFromClient=conn.recv(4096)
    print('Data from client:',dataFromClient.decode())
    
    recvdDict=json.loads(dataFromClient.decode())
    
    returnString="Name:"+recvdDict['Name']+";\n"+"Age:"+recvdDict['Age']+";\n"+"Matrikelnummer:"+recvdDict['Martrikelnumber']+";"
    
    conn.send(returnString.encode())
    conn.close()
    
