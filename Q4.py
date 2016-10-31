# -*- coding: utf-8 -*-
"""
Team Bravo
Daniyal Akbari (akbari@uni-koblenz.de)
Shriharsh Ambhore (ashriharsh@uni-koblenz.de)
Kandhasamy Rajasekaran (kandhasamy@uni-koblenz.de)
"""

import random , numpy as np, matplotlib.pyplot as plt

list=[]
sin=[]
cosin=[]
for i in range(0,10):
    x = random.randint(0,90)
    list.append(x)
    sin.append(np.sin(x))
    cosin.append(np.cos(x))

# Create a figure of size 8x6 inches, 80 dots per inch
plt.figure(figsize=(8, 6), dpi=80)
# Create a new subplot from a grid of 1x1
plt.subplot(1, 1, 1)
 
plt.title('Sine & Cosine')
plt.xlabel('t (radians)')
plt.ylabel('red: sin (t), blue: cos (t)')
plt.grid(True)
 
plt.scatter(list,sin, color="red", label="sine")
plt.scatter(list,cosin, color="blue", label="cosine")
plt.legend()
 
plt.show()
