#! /usr/bin/python3

import pandas as pd
import gpxpy
import gpxpy.gpx
import os.path
import csv

##################################################
# Some book-keeping
#
km2mi = 0.621371
dir = '/home/freddy/insight/data/'
ext = 'gpx_data/'
conversion={'marathon'         : 26.219,
            'half_marathon'    : 13.109,
            'quarter_marathon' :  6.555,
            '6hours'           : -1.000,
            'ultra_marathon'   : -1.000
}

def cut_up_url(url):
    flag = 'meetingid='
    start = url.find(flag)+len(flag) 
    end   = url.find('&')
    substr = url[start:end]
    return int(substr)

def get_gpx_info(filename):
    name = dir+ext+filename
    elev = []
    try:
        gpx_file = open(name,'r')
        print('Analyzing %s' % name)
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    elev.append(point.elevation)
    except FileNotFoundError:
        print('%s not found, moving on...' % cut_up_url(url))
        
    sum_up, sum_down = 0.0, 0.0    
    for i in range(len(elev)-1):
        dy = elev[i+1] - elev[i]
        if dy > 0.0:
            sum_up += dy
        else:
            sum_down += dy
    features = [sum_up, sum_down]
    return features

################################################################################
gpx_info = dir + 'gpx_discover.csv'
df = pd.read_csv(gpx_info)
cols = list(df.columns)
ID, UP, DOWN = [], [], []
for index, row in df.iterrows():
    name = str(row[cols[3]])
    if 'no result' in name.lower():
        print('skipping row %d' % index)
        continue
    
    url   = row[cols[0]]
    meeting_id = cut_up_url(url)
    event = row[cols[1]]
    race  = str(row[cols[2]])
    gpx   = row[cols[3]]
    elevation = get_gpx_info(gpx)
    if elevation[0] == 0 and elevation[1] == 0:
        continue
    ID.append(meeting_id)
    UP.append(elevation[0])
    DOWN.append(elevation[1])

f = open("gpx_elevation_map.csv", "w")
for idx, val in enumerate(ID):
    f.write('%d,%1.3f,%1.3f\n' % (ID[idx], UP[idx], DOWN[idx]))
