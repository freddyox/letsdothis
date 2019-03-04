#! /usr/bin/python3

import pandas as pd
import gpxpy
import gpxpy.gpx
import os.path
import csv
import math

#################################################################
# Obrecht - 1/20/2019 - Insight Data Science
# Goal: Read a CSV table, find/open GPS files, and extract physical
# quantities for each file.  We also want to map each GPS file to
# runbritain's unique indentifier.
#################################################################

# This variable does not change in the code; all
# important outputs go here for subsequent analysis
FGLOBAL = open("all_elevations.csv", "w")

##################################################
# Some book-keeping
dir = '/home/freddy/insight/data/'
ext = 'gpx_data/'
km2mi = 0.621371
conversion = {'marathon'         : 26.219,
              'half_marathon'    : 13.109,
              'quarter_marathon' :  6.555,
              '6hours'           : -1.000, # ignore
              'ultra_marathon'   : -1.000  # ignore
}

##################################################
# Accepts a URL, cuts it up to find an identifier
# that is unique to runbritain.com (where I'm scraping)
def cut_up_url(url):
    """ 
    Input:  A URL string consistent w/ runbritain.com. Here is an ex)
    https://www.runbritainrankings.com/results/results.aspx?meetingid=201320&pagenum=1
    
    Output: Unique ID int for a particular race, which is how
    I cross-reference GPS info with race info
    """ 
    flag = 'meetingid='
    start = url.find(flag) + len(flag) 
    end   = url.find('&')
    substr = url[start:end]
    return int(substr) 

##################################################
# Open the GPS file, calculate some quantities,
# and spit out the result to a text file which is
# used in subsequent analyses.
def get_gpx_info(filename, meeting_id):
    """ 
    Input:  GPS filename (string) and it's corresponding unique
    identifier (int), which is labeled as meeting_id
    
    Output: A list of important features for each GPS file, all floats
    """ 
    name = dir + ext + filename
    elev = []
    try:
        gpx_file = open(name,'r')
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    elev.append(point.elevation)
    except FileNotFoundError:
        print('%s not found, moving on...' % cut_up_url(url))
        return [0] # return garbage, filter this below
    
    print('Analyzing %s, %d data points' % (name,len(elev)))   
    sum_up, sum_down = 0.0, 0.0 # Should only be looking @ N-1 pts
    sum = 0.0                   # Need all N pts
    for i in range(len(elev)-1):
        sum += elev[i]
        dy = elev[i+1] - elev[i]
        if dy > 0.0:
            sum_up += dy
        else:
            sum_down += dy
    sum += elev[len(elev)-1]         # Here is last point
    mean_elevation = sum / len(elev) # Normalize

    # Let's find the Standard Deviation and write the results:
    sum2=0.0
    bin=0
    for i in elev:
        FGLOBAL.write('%d,%d,%1.3f\n' % (meeting_id,bin,i) )
        bin += 1
        sum2 += (i - mean_elevation)**2

    sum2norm = sum2 / len(elev) # variance
    sigma = math.sqrt(sum2norm) # std dev
    return [sum_up, sum_down, mean_elevation, sigma]

################################################################################
# Main Driver Script - nothing fancy as I only need to extract a few quantities
# from each file, then move on to deeper analyses within a different script. 
gpx_info = dir + 'gpx_discover_new.csv'
df = pd.read_csv(gpx_info)
cols = list(df.columns)
ID, UP, DOWN, MEAN, SIGMA = [], [], [], [], []
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
    features = get_gpx_info(gpx, meeting_id)
    if len(features)<2: # Filtering the garbage results
        continue
    ID.append(meeting_id)
    UP.append(features[0])
    DOWN.append(features[1])
    MEAN.append(features[2])
    SIGMA.append(features[3])
    print( '\t %d \t %1.3f \t %1.3f \t %1.3f \t %1.3f \n' %
           (meeting_id, features[0], features[1], features[2], features[3]) )

# Make an easier to read CSV table so I do not have to rely on hand-me-downs
f = open("gpx_elevation_map_new.csv", "w")
for idx, val in enumerate(ID):
    f.write('%d,%1.3f,%1.3f,%1.3f,%1.3f\n' %
            (ID[idx], UP[idx], DOWN[idx], MEAN[idx], SIGMA[idx]))
