#! /usr/bin/python3

import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt

file = open('gpx_data/Centurion_December.gpx','r')
file = open('gpx_data/Cannonball_Christmas_Cracker_.gpx','r')
gpx = gpxpy.parse(file)

dist, elev = [],[]
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            #print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
            elev.append(point.elevation)
dx = 4 / len(elev)
for i, val in enumerate(elev):
    dist.append(i*dx)

plt.plot(dist,elev,alpha=0.75)
plt.xlabel('Distance (Mi)')
plt.ylabel('Elevation (ft)')
plt.show()
