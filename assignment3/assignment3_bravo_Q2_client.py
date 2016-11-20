# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 19:13:29 2016

@author: Shriharsh Ambhore
@author: Kandhasamy Rajasekaran
@author: Daniel Akbari

"""



import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8080))  ## connect to the server and send the data
s.send('https://www.example.com:80/path/to/myfile.html?key1=value1&key2=value2#InTheDocument'.encode())
s.close()

