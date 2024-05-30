#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 08:21:13 2024

@author: stejan
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.image as mpimg
import os
from datetime import datetime

path = os.path.dirname(__file__)
os.chdir(path)
#plt.style.use("dark_background")
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (10, 8),
         'axes.labelsize': 'x-large',
         'axes.titlesize': 'xx-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

# PTU
ptu_path = path + "/ptu/ptu_20240320_data.txt"
ptu = pd.read_csv(ptu_path, delimiter="\t")#, usecols=ptu_header)
ptu.columns = ["time", "P", "alt", "T", "rh"]

# ETAG
etag_path = path + "/etag/2024-03-20_LTU22_GPW.log"
# Read the data from the file using read_csv function
# etag = pd.read_csv(etag_path, header=None, delimiter=',', 
#                 names=['date', 'time', 'latitude_deg', 'latitude_min', 'latitude_sec', 
#                        'longitude_deg', 'longitude_min', 'longitude_sec', 'latitude_dir', 
#                        'longitude_dir', 'altitude', 'speed', 'course', 'horizontal_dilution', 
#                        'altitude_dilution', 'geoidal_separation', 'age_of_differential_data'],
#                 parse_dates=[['date', 'time']], 
#                 date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S.%f;$PRBEPOS,GPW,,,'))
names=['date', 'time', 'latitude_deg', 'latitude_min', 'latitude_sec', 
                        'longitude_deg', 'longitude_min', 'longitude_sec', 'latitude_dir', 
                        'longitude_dir', 'altitude', 'speed', 'course', 'horizontal_dilution', 
                        'altitude_dilution', 'geoidal_separation', 'age_of_differential_data', 'test'],
etag_raw = pd.concat([
    pd.read_csv(etag_path, sep=sep, names=range(19)) for sep in [',', ';'] ],
    ignore_index=True ).fillna(0)
etag_raw = etag_raw.iloc[214:5853]

# calculate the speed of the balloon
speed = etag_raw[10].diff()
#del speed[3856]

# TEMPERATURE
t_path = path + "/temperatures/thermistor_py.txt"
t_headers = ["date", "time", "T0", "T1", "T2", "T0_2", "T1_2", "T2_2", "T3_2", "volt0", "volt1", "volt2", "VDD", "volt0_2", "volt1_2", "volt2_2", "VDD2"]
temperature = pd.read_csv(t_path, header=None, delimiter=" ", skiprows=1, names=t_headers)
def convert_time(time_str):
    return datetime.strptime(time_str, "%H:%M:%S").time()
#temperature["time"] = temperature["time"].apply(convert_time)
temperature["time"] = pd.to_datetime(temperature["time"])
etag_time = etag_raw.iloc[:, 0].apply(lambda x: x[0:19])
#etag_time = etag_time.apply(convert_time)
etag_time = pd.to_datetime(etag_time)
#%%

# PLOT OUTSIDE TEMPERATURE
plt.figure()
plt.plot(ptu["T"], ptu["alt"],  linewidth=3)
plt.title("Outside temperature")#, fontsize=25)
plt.xlabel("Temperature C")
plt.ylabel("Altitude")
plt.savefig("outside_temperature.png", dpi=300)
#%%
#plt.close()

# INSIDE TEMPERATURE
plt.figure()
plt.plot(temperature["T0"], "white", label="inside", linewidth=3)
plt.plot(temperature["T1"], "orange", label="behind CCD", linewidth=3)
plt.plot(temperature["T2"], "blue", label="Before CCD", linewidth=3)
plt.plot(temperature["T0_2"], "purple", label = "Motor", linewidth=3)
plt.legend()
plt.ylabel("Temperature")
plt.title("Temperatures inside the instrument", fontsize=25)
plt.xticks([])

plt.savefig("inside temperatures.png", dpi=300)
#plt.close()

# BALLOON ALTITUDE
plt.figure()
plt.plot(etag_time, etag_raw[10], "white", linewidth=3)
plt.title("Balloon altitude", fontsize=20)
plt.savefig("altitude.png", dpi=300)
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=45)
#plt.tight_layout()
#plt.close()

#%% BALLOON SPEED
average_speed = [np.mean(speed[i:i+20]) for i in range(0, len(speed), 20)]
#del etag_time[3856]
plt.figure()
plt.plot(average_speed, "white", linewidth=3)
plt.title("Speed of the instrument", fontsize=20)
plt.savefig("etag_speed.png", dpi=300)
plt.ylabel("m/s")
plt.xticks(rotation=45)
#plt.tight_layout()
#plt.close()

#%% RH OVER ICE SATURATION
import typhon as tp
RHi = ptu["rh"] * tp.physics.e_eq_water_mk(ptu["T"] + 273.16) / tp.physics.e_eq_ice_mk(ptu["T"] + 273.16)
RH_at_icesat = 100 * tp.physics.e_eq_ice_mk(ptu["T"] + 273.16) / tp.physics.e_eq_water_mk(ptu["T"] + 273.16)

plt.figure(figsize=(10,8))
plt.plot(ptu["rh"] , ptu["alt"], label="RH")
plt.plot(RH_at_icesat, ptu["alt"], label="Ice saturation on T")
#plt.plot(RHi, ptu["alt"], label="rhi")
#plt.plot(ptu["rh"], ptu["alt"], label="rh")
plt.xlabel("RH%")
plt.ylabel("Altitude")
plt.title("RH over ice-saturation")
#plt.ylim([8500, 14000])
plt.legend()
plt.savefig("rh_icesat.png", dpi=300)
