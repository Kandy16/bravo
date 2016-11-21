#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 11:05:14 2016

@author: kandy
"""

from assignment4_bravo_functions import *

try :
    socClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    urlInput = input('Input the URL : ')
    #urlInput = 'http://west.uni-koblenz.de/en/mws/dates/index.html'
    #urlInput = 'https://www.uni-koblenz-landau.de/de/koblenz/index.html'
    #urlInput = 'http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science'
    #urlInput = 'http://blog.ifimbschool.com/wp-content/uploads/2014/12/Hindi-Quote-on-overcoming-obstacles-with-unity-by-Atal-Bihar-Vajpayee-624x467.jpg'
    #urlInput = 'http://www.w3schools.com/tags/tag_link.asp'
    #urlInput = 'http://west.uni-koblenz.de/sites/default/files/styles/front-slider/public/fslide_1_0.jpg'
    #urlInput = 'http://west.uni-koblenz.de/'
    
    try:
        socClient.connect((urlDomain, 80))
        downloadResource(socClient, urlInput)
        socClient.close()
    except socket.error as e:
       print('Connection Invalid. Input proper URL !!!',e)
    except:
        print('Connection Invalid. Input proper URL !!!')
  
finally:
    socClient = None

    
#print(urlInput)

