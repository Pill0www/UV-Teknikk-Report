#Changes that have been done is commented in the code
import sys
import os
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
#import Pillow
import pyvista as pv
from os import listdir
from os.path import isfile, join
import ast

########### Your Path/Code here ###################################################
mypath = "Multibeam/Data/Raw"
processedfilepath = "Multibeam/Data/Processed/Processed.csv"
processeddict = "Multibeam/Data/Processed"

files = [f for f in listdir(mypath) if isfile(join(mypath,f))]
first = True
counter = 0

df = pd.read_csv("Multibeam/Data/Raw/0000_20240229_191034_RVGunnerusRAW.csv") # Instead of an .all file we got a fully processed csv file
                                                                              #Therefore we just read it directly from pandas

for f in files:

    pointcloud = pd.DataFrame(columns=["x","y","z","t"])

    if first:
        first = False                        # Here and downwards i need to make sure the numbers are in correct format
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
        ttime = df["time"].values[i]  


        along = np.asarray(along)
        across = np.asarray(across)
        depth = np.asarray(depth)

        x = meterPerDeg*(lat-lat_0) - across*np.sin(np.deg2rad(yaw)) + along*np.cos(np.deg2rad(yaw))
        y = meterPerDeg*np.cos(np.deg2rad(lat_0))*(lon-lon_0) + across*np.cos(np.deg2rad(yaw)) + along*np.sin(np.deg2rad(yaw))
        z =depth

        d = {"x" : x, "y" : y, "z" : z, "t" : ttime}
        d_df = pd.DataFrame(data=d)
        pointcloud = pd.concat([pointcloud, d_df], ignore_index=True) #df.append() is outdated so this function had to be changed to the new .concat function


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