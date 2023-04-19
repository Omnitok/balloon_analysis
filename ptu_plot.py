#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 09:33:31 2023

@author: Stenszky János
Relative Humidity in respect ti ICE calculation
"""
from datetime import date, datetime
import typhon as ty
import os
#from os import chdir, getcwd

#wd = getcwd()
path = os.path.dirname(__file__)
os.chdir(path)

# IMPORT THE FILES OF DIFFERENT MEASUREMENTS
file = '/home/stejan/Desktop/ballon/20211116_LTU18/ptu/ptu_20211116_data.txt'
stime = datetime(2021,11,16,9,16,25)
date = date( int(file[-17:-13]), int(file[-13:-11]), int(file[-11:-9]) )

# file = '/home/stejan/Desktop/ballon/20211120_LTU19/ptu_20211120_data.txt'
# stime = datetime(2021,11,20,5,00,53)
# date = date( int(file[-17:-13]), int(file[-13:-11]), int(file[-11:-9]) )

# file = '/home/stejan/Desktop/ballon/20211210_LTU20/ptu_20211210_data.txt'
# stime = datetime(2021,12,10,7,49,28)
# date = date( int(file[-17:-13]), int(file[-13:-11]), int(file[-11:-9]) )

# file = '/home/stejan/Desktop/ballon/20220309_LTU21/ptu_20220309_data.txt'
# stime = datetime(2022,3,9,3,29,29)
# date = date( int(file[-17:-13]), int(file[-13:-11]), int(file[-11:-9]) )


# IMPORT data as pandas dataframe
import pandas as pd
columns = ['time', 'P', 'altitude', 'T', 'RH']
data = pd.read_csv(file, 
                   delimiter='\t',
                   names=columns
                   )

RHi = data['RH'] * ty.physics.e_eq_water_mk(data['T']+273.16) / ty.physics.e_eq_ice_mk(data['T']+273.16) 
RH_at_icesat = 100 * ty.physics.e_eq_ice_mk(data['T']+273.16) / ty.physics.e_eq_water_mk(data['T']+273.16)

# PLOT IT
import matplotlib.pyplot as plt
fig = plt.figure(facecolor='none')
plt.plot(data['RH'], data['altitude'], linewidth=2, label='Relative humidity')
plt.plot(RH_at_icesat, data['altitude'], linewidth=2, label='RH at ice-sat' )
plt.xlabel('RH')
plt.ylabel('Altitude')
plt.title(f'{date}')
plt.legend()
fig.savefig(f'rh_{date}.png', transparent='True', dpi=300)

plt.show()
