# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 03:36:00 2016

@author: Shriharsh Ambhore
@author: Kandhasamy Rajasekaran
@author: Daniel Akbari
"""


import socket
import json

dict={'Name':'','Age':'','Matrikelnummer':''}

dict['Name']=input('Enter Name:')
dict['Age']=input('Enter Age:')
dict['Martrikelnumber']=input('Enter Matrikelnummber:')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8080))
s.send(json.dumps(dict).encode())
data = s.recv(4096)
s.close()
print('server response:\n',data.decode('utf-8'))

