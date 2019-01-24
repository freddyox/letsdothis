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
ext = 'gpx_data/'
conversion={'marathon'         : 26.219,
            'half_marathon'    : 13.109,
            'quarter_marathon' :  6.555,
            '6hours'           : -1.000,
            'ultra_marathon'   : -1.000
}

def convert(dist):
    if dist[-1] is 'm':
            return float(dist[:-1])
    elif dist[-1] is 'k':
            return float(dist[:-1])*km2mi
    else:
        return -1.0

def check_race(race, evt):
    if race is None:
        print('Race field is empty...returning 0')
        return -1.0

    race_list = race.split()
    if len(race_list)==0:
        return -1.0
    
    # look at the easy case first:
    if len(race_list) == 1:
        dist = race_list[0].strip()
        if dist in conversion:
            return conversion[dist]
        else:
            return convert(dist)
    else:
        max = 0.0
        for i in race_list:
            dist = convert(i.strip())
            if dist > max:
                max = dist
            print('Multiple types found, returning max of %1.3f' % max)
            return max    
        
def get_gpx_info(filename, dist):
    name = ext+filename
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
        print('File not found, moving on...')

    sum_up, sum_down = 0.0, 0.0    
    for i in range(len(elev)-1):
        dy = elev[i+1] - elev[i]
        if dy > 0.0:
            sum_up += dy
        else:
            sum_down += dy
       # print('+dy, -dy \t %1.3f, %1.3f, %1.3f, %1.3f, %1.3f' %
        #      (sum_up, sum_down, dy, elev[i+1], elev[i]))
################################################################################
gpx_info = 'gpx_discover.csv'
df = pd.read_csv(gpx_info)
cols = list(df.columns)

for index, row in df.iterrows():
    name = str(row[cols[3]])
    if 'no result' in name.lower():
        print('skipping row %d' % index)
        continue
    
    url   = row[cols[0]]
    event = row[cols[1]]
    race  = str(row[cols[2]])
    gpx   = row[cols[3]]
    dist = check_race(race.lower(),event)
    
    get_gpx_info(gpx, dist)
    #if index==0:
    #    break
    
#def get_site_text(url):
#    #print(url)
#    r = requests.get(url)
#    return r.text
#soup = BeautifulSoup( get_site_text(str(url)), "html.parser")
#tables = soup.find_all("table", id="cphBody_gvP")
#for tr in soup.find_all('tr')[2:]:
#    tds = tr.find_all('td')
#    print(tds)
