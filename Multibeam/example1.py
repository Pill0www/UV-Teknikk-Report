from pyall import pyall
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
#import Pillow
import pyvista as pv
from os import listdir
from os.path import isfile, join


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
            depth_df = depth_df.append(d_df)
            counter = counter + 1

        if TypeOfDatagram == 'P':
            datagram.read()
            d = {"time" : datagram.Time, "lat" : datagram.Latitude, "lon" : datagram.Longitude, "yaw" : datagram.Heading}
            p_df = pd.DataFrame(data=d, index=[0])
            pos_df = pos_df.append(p_df)


    df = pd.concat([depth_df,pos_df],join="outer")
    df.sort_values(by="time", inplace=True)
    df.interpolate(limit_direction="both", inplace=True)
    df.dropna(inplace=True)

    print("final df size: ", df.shape)
    print("Read Duration: %.3f seconds" % (time.time() - start_time)) # print the processing time. It is handy to keep an eye on processing performance.

    r.rewind()
    print("Complete reading ALL file :-)")
    r.close()
    # see the test code in main() at the end of pyall for more details.  Have Fun
    return df


########### Your Path/Code here ###################################################
mypath  = "/home/tore/tokt/tmr4120/MBES/Vessel_MBES05032020/"
processedfilepath = "/home/tore/tokt/tmr4120/MBES/Vessel_MBES05032020/processed/"

files = [f for f in listdir(mypath) if isfile(join(mypath,f))]
first = True
counter = 0


for f in files:

    df = read_all_file(mypath+f)
    print(df.columns)

    pointcloud = pd.DataFrame(columns=["x","y","z","t"])
    if first:
        first = False
        lat_0 = df["lat"].values[0]
        lon_0 = df["lon"].values[0]
    meterPerDeg = 111319.444 #Circumference of the earth divided by 360 degrees

    rows,cols = df.shape
    for i in range(0,rows-1):
        across = df["across"].values[i]
        along = df["along"].values[i]
        depth = df["depth"].values[i]
        lat = df["lat"].values[i]
        lon = df["lon"].values[i]
        yaw = df["yaw"].values[i]
        ttime = df["time"].values[i]

        along = np.asarray(along)
        across = np.asarray(across)
        depth = np.asarray(depth)

        x = meterPerDeg*(lat-lat_0) - across*np.sin(np.deg2rad(yaw)) + along*np.cos(np.deg2rad(yaw))
        y = meterPerDeg*np.cos(np.deg2rad(lat_0))*(lon-lon_0) + across*np.cos(np.deg2rad(yaw)) + along*np.sin(np.deg2rad(yaw))
        z = depth

        d = {"x" : x, "y" : y, "z" : z, "t" : ttime}
        d_df = pd.DataFrame(data=d)
        pointcloud = pointcloud.append(d_df)

    print(pointcloud.shape)
    # CSV-exporter
    df.to_csv(processedfilepath + f[:-4]+ "RAW.csv", index=True)
    pointcloud.to_csv(processedfilepath +  f[:-4]+ "XYZ.csv", index=True)
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
