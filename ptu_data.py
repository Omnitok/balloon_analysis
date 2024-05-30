#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 09:29:11 2024

@author: stejan
"""
import numpy as n
import os
from matplotlib import pyplot as plt
import pandas as pd

path = os.path.dirname(__file__)
os.chdir(path)

# Open the file #1
with open('ptu_20240320_data.txt', 'r') as file:
    # Read the lines of the file
    lines = file.readlines()
    # Initialize an empty list to store the data
    data = []
    # Loop through the lines and split them by tabs
    for line in lines:
        row = line.strip().split('\t')
        data.append(row)
        
header = ["time", "pressure", "altitude", "temp", "rh" ]

df1 = pd.DataFrame(data)
ptu = pd.DataFrame(
    n.row_stack([df1.columns, df1.values]),
    columns=header
    )
ptu = ptu.iloc[1:] # remove first and last row fro the dataframe
ptu["pressure"] = ptu["pressure"].astype(float)
ptu["altitude"] = ptu["altitude"].astype(float)
ptu["temp"] = ptu["temp"].astype(float)
ptu["rh"] = ptu["rh"].astype(float)

plt.plot(ptu["temp"], ptu["altitude"])
#plt.gca().invert_yaxis() # Invert y-axis
