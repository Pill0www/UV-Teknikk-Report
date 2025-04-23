#Changes made by me
#Imported pyall by accessing correct py file from directory using absolute path, sys and os had to be imported as well
#df = read_all_file(os.path.join(mypath, f)) This line is new since the original joining wasn't correct for finding the directory
#df.append() is depreceated so this function had to be changed to the new .concat function for all three instances

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join("pyall", "pyall")))
import pyall  # refers to pyall.py inside the inner pyall folder
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
#import Pillow
import pyvista as pv
from os import listdir
from os.path import isfile, join
import ast



def read_all_file(filename):
    r = pyall.ALLReader(filename)
    start_time = time.time() # time the process
    pos_df = pd.DataFrame(columns=["time", "lat", "lon", "yaw"])
    depth_df = pd.DataFrame(columns=["time", "across", "along", "depth", "pingnumber"])
    counter = 0

    while r.moreData():
        # read a datagram.  If we support it, return the datagram type and aclass for that datagram
        # The user then needs to call the read() method for the class to undertake a fileread and binary decode.  This keeps the read super quick.
        TypeOfDatagram, datagram = r.readDatagram()

        if TypeOfDatagram == 'D':
            datagram.read()

            dtime =  datagram.Time
            tdepth = datagram.TransducerDepth
            print("On ping number",counter+1)
            d = {"time": dtime, "across": [datagram.AcrossTrackDistance], "along": [datagram.AlongTrackDistance],
                 "depth": [datagram.Depth], "pingnumber": counter}
            d_df = pd.DataFrame(data=d)
            depth_df = pd.concat([depth_df, d_df], ignore_index=True)
            counter = counter + 1

        if TypeOfDatagram == 'P':
            datagram.read()
            d = {"time" : datagram.Time, "lat" : datagram.Latitude, "lon" : datagram.Longitude, "yaw" : datagram.Heading}
            p_df = pd.DataFrame(data=d, index=[0])
            pos_df = pd.concat([pos_df, p_df], ignore_index=True)



    df = pd.concat([depth_df,pos_df],join="outer")
    df.sort_values(by="time", inplace=True)
    df.interpolate(limit_direction="both", inplace=True)
    df.dropna(inplace=True)

    print("final df size: ", df.shape)
    print("Read Duration: %.3f seconds" % (time.time() - start_time)) # print the processing time. It is handy to keep an eye on processing performance.

    r.rewind()
    print("Complete reading ALL file 🙂")
    r.close()
    # see the test code in main() at the end of pyall for more details.  Have Fun
    return df


########### Your Path/Code here ###################################################
mypath = "Multibeam/Data/Raw"
processedfilepath = "Multibeam/Data/Processed/Processed.csv"
processeddict = "Multibeam/Data/Processed"

files = [f for f in listdir(mypath) if isfile(join(mypath,f))]
first = True
counter = 0

df = pd.read_csv("Multibeam/Data/Raw/0000_20240229_191034_RVGunnerusRAW.csv")

for f in files:

 
    pointcloud = pd.DataFrame(columns=["x","y","z","t"])

    if first:
        first = False
        lat_0 = float(df["lat"].values[0])
        lon_0 = float(df["lon"].values[0])
    meterPerDeg = 111319.444 #Circumference of the earth divided by 360 degrees

    rows,cols = df.shape
    for i in range(0,rows-1):
        across = [float(a) for a in ast.literal_eval(df["across"].values[i])]
        along = [float(a) for a in ast.literal_eval(df["along"].values[i])]
        depth = [float(d) for d in ast.literal_eval(df["depth"].values[i])]


        lat = float(df["lat"].values[i])
        lon = float(df["lon"].values[i])
        yaw = float(df["yaw"].values[i])
        ttime = df["time"].values[i]  # Denne kan være string hvis det er timestamp, så det er kanskje OK


        along = np.asarray(along)
        across = np.asarray(across)
        depth = np.asarray(depth)

        x = meterPerDeg*(lat-lat_0) - across*np.sin(np.deg2rad(yaw)) + along*np.cos(np.deg2rad(yaw))
        y = meterPerDeg*np.cos(np.deg2rad(lat_0))*(lon-lon_0) + across*np.cos(np.deg2rad(yaw)) + along*np.sin(np.deg2rad(yaw))
        z =depth

        d = {"x" : x, "y" : y, "z" : z, "t" : ttime}
        d_df = pd.DataFrame(data=d)
        pointcloud = pd.concat([pointcloud, d_df], ignore_index=True)


    print(pointcloud.shape)
    # CSV-exporter
    df.to_csv(os.path.join(processeddict, f[:-4] + "RAW.csv"), index=True)
    pointcloud.to_csv(os.path.join(processeddict, f[:-4] + "XYZ.csv"), index=True)

    counter += 1

x = pointcloud["x"].values
y = pointcloud["y"].values
z = pointcloud["z"].values



points = []
for i in range(0,len(x)-1):
    points.append([x[i],y[i],z[i]])

points = np.asarray(points)

point_cloud = pv.PolyData(points)
if not np.allclose(points,point_cloud.points):
    print("The data points are not generated properly. ")
# Make data array using z-component of points array
data = points[:,-1]
#print(nameOfFile)
# Add that data to the mesh with the name "uniform dist"
point_cloud["Depth"] = data

point_cloud.plot(render_points_as_spheres=True)