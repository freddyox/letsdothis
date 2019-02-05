from flask import render_template, url_for, request, Flask
from app import app
import pandas as pd
from flaskext.mysql import MySQL
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
plt.switch_backend('agg')
import numpy as np
import operator # sorting dictionary
import random
import string

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'freddy'
app.config['MYSQL_DATABASE_PASSWORD'] = 'N@c1remaLane88'
app.config['MYSQL_DATABASE_DB'] = 'app'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cur  = conn.cursor()

conversion={'Mar': 26.219,
            '10K': 6.214
}


@app.route('/')
@app.route('/index')
def index():
    events = sql_get_events("Mar")
    # Let's sort the events, which is nicer for the user
    events_sort = sorted(events.items(), key=operator.itemgetter(1))
    return render_template("index.html", events=events_sort)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/output')
def output():
    sex_map = {'Female': 1, 'Male': 2}
    age_map = {'U11':0,'U13':1,'U15':2,'U17':3,'U20':4,'U23':5,
               'SEN':6,'V35':7,'V40':8,'V45':9,'V50':10,'V55':11,
               'V60':12,'V65':13,'V70':14,'V75':15,'V80':16,'V85':17}

    age_type    = str(request.args.get('age'))
    gender_type = str(request.args.get('gender'))
    race_type   = str(request.args.get('race'))
    event_type  = str(request.args.get('event'))
    args = []
    args.append(age_type)
    args.append(gender_type)
    args.append(race_type)

    age_type    =  pd.Series(age_type)
    gender_type =  pd.Series(gender_type)
    ID          =  int(pd.Series(event_type)[0])
        
    # Build the appropriate material
    age      = age_type.map(age_map).astype(int)
    sex      = gender_type.map(sex_map).astype(int)
    event    = get_event(ID)
    args.append(event)
    
    print('User Input:')
    print('\t age   = {}'.format(age))
    print('\t sex   = {}'.format(sex))
    print('\t race  = {}'.format(race_type))
    print('\t ID    = {}'.format(ID))
    print('\t Event = {}'.format(event))
    
    time     = get_time(ID, event, True)
    gpx_info = get_gpx_info(ID, event, True)
    print('Course Input:')
    print('\t time   = {}'.format(time))
    print('\t sum_up = {}'.format(gpx_info[0]))
    print('\t sigma  = {}'.format(gpx_info[1]))
    print('\t diff   = {}'.format(gpx_info[2]))
      
    beta     = get_beta(race_type)
    X = [age, sex, time, gpx_info[0], gpx_info[1],gpx_info[2]]
    
    # Perform the dot product for our user:
    betax = 0.0
    for idx, val in enumerate(X):
        betax += X[idx]*beta[idx]
        print(idx, X[idx], beta[idx])

    score = get_score(float(betax), race_type)
    print('Output:')
    print('betaX: {}'.format(betax))
    print('score: {}'.format(score))

    gpx = gpx_info
    gpx.append(time)
    name = build_plot(beta, gpx, race_type, ID)
    return render_template("output.html", betax=betax, score=score,
                           event=event, beta=beta, args=args, name=name)

def build_plot(beta, gpx, race_type, meeting_id):
    labels = ['Age', 'Sex', 'Time', 'Elevation', 'Elevation \n Std. Dev.', 'Elevation \n Difference']
    xint = range(len(labels))

    palette = []

    for i in beta:
        if i <= 0:
            palette.append('#b7040e')
        else:
            palette.append('#07a64c')
    
    fig = plt.figure()
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    ax1.bar(xint, beta, width=1.0, color=palette)
    plt.ylabel('Importance', fontsize=12)
    plt.title('Regression Feature Importance')
    plt.xticks(xint, labels, rotation=0, wrap=True)
    plt.tight_layout()

    # Let's get the averages for the gpx list for comparision
    flags = ['sum_up', 'sigma', 'diff', 'min_time']
    averages = []
    for i in flags:
        avg = get_avg(str(i), str(race_type))
        averages.append(avg)

    palette2 = ['#ff7f0e','#1f77b4']
    ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=1)
    xint, vals = range(2), [gpx[3],averages[3]]
    min_val = min(gpx[3],averages[3])
    max_val = max(gpx[3],averages[3])
    ax2.bar(xint,vals, width=1.0, color=palette2)
    ax2.set_ylim(0.85*min_val, 1.15*max_val)
    plt.ylabel('Finish Time (min)', fontsize=10)
    plt.xticks(xint, ['Time', 'Average \n Time'], rotation=0, wrap=True)

    legend_elements = [Patch(facecolor=palette2[0], label='Course Median Time'),
                       Patch(facecolor=palette2[1], label='{} Median Time'.format(race_type))]
    ax2.legend(handles=legend_elements, loc='upper right', frameon=False)
    
    plt.tight_layout()

    elevation_dict = get_elevation_dict(meeting_id, race_type)
    bins, elevation = elevation_dict.keys(), elevation_dict.values()
    ax3 = plt.subplot2grid((2, 2), (1, 1), colspan=1)
    ax3.plot(bins, elevation)
    plt.ylabel('Elevation (m)', fontsize=10)
    plt.xlabel('Distance (mi)', fontsize=10)
    plt.tight_layout()
    
    rndstring = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
    name = 'app/static/images/plots/temp_{}.png'.format(str(rndstring))
    plt.savefig(name)
    return name[3:]

    
def sql_get_events(flag, unique=True):
    sql_select_query = """SELECT meeting_id, event_title FROM race_info WHERE race_type = %s ORDER BY event_title"""

    cur.execute(sql_select_query, (str(flag), ))
    record = cur.fetchall()
    events = {}
    for row in record:
        events[row[0]] = row[1]

    if not unique:
        return events

    invert = {}
    for k, v in events.items():
        if v not in invert:
            invert[v] = k

    unique_events = {}
    for k, v in invert.items():
        unique_events[v] = k

    return unique_events

def get_event(ID):
    sql_select_query = """SELECT event_title FROM race_info WHERE meeting_id = %s"""
    cur.execute(sql_select_query, (str(ID), ))
    record = cur.fetchall()
    return record[0][0]

def get_time(ID, event, use_event=True):
    sql_select_query = """SELECT meeting_id, min_time FROM race_info WHERE event_title = %s"""
    flag = str(event)
    cur.execute(sql_select_query, (str(flag), ))
    record = cur.fetchall()

    if len(record) > 1:
        print('{} has {} records => averaging times'.format(event,len(record)))
    time_avg = 0.0
    for row in record:
        time_avg += row[1]
    N = len(record)
    time_avg /= N
    return time_avg

def get_gpx_info(ID, event, use_event=True):
    sql_select_query = """SELECT meeting_id, sum_up, sigma, diff FROM race_info WHERE meeting_id = %s"""
    flag = str(ID)
    if use_event:
        sql_select_query = """SELECT meeting_id, sum_up, sigma, diff FROM race_info WHERE event_title = %s"""
        flag = str(event)
        
    cur.execute(sql_select_query, (str(flag), ))
    record = cur.fetchall()
    print(record)
    results = [0.0, 0.0, 0.0]
    for row in record:
        results[0] += row[1]
        results[1] += row[2]
        results[2] += row[3]
        
    N = len(record)
    results[0] /= N
    results[1] /= N
    results[2] /= N
    print('Found {0} records for {1}'.format(N, event))
    return results
     
def get_beta(race):
    sql_select_query = """SELECT age,sex,time,sum_up,sigma,diff FROM beta WHERE race_type = %s"""
    cur.execute(sql_select_query, (str(race), ))
    record = cur.fetchall()
    row = record[0]
    beta = []
    for i in row:
        beta.append(i)
    return beta
    
def get_score(betax, race_type):
    sql_select_query = """SELECT * FROM d_dist WHERE race_type = %s"""
    cur.execute(sql_select_query, (str(race_type), ))
    record = cur.fetchall()
    bins, xs, ys, dxs = [], [], [], []
    for row in record:
        bins.append(row[0])
        xs.append(row[1])
        ys.append(row[2])
        dxs.append(row[3])
        
    score = -1.0
    for idx,val in enumerate(xs):
        dx  = dxs[idx]*0.5
        dlo = xs[idx] - dx
        dhi = xs[idx] + dx
        if (betax >= dlo) and (betax < dhi):
            score = ys[idx]
            break
    return score

def get_avg(column_name, race_type):
    sql_select_query = """SELECT  AVG(min_time), AVG(sum_up), AVG(sigma), AVG(diff), AVG(dt) FROM race_info WHERE race_type = %s"""
    input = [str(race_type)]
    cur.execute(sql_select_query, input)
    record = cur.fetchall()
    rec_dict = {'min_time': record[0][0],
                'sum_up'  : record[0][1],
                'sigma'   : record[0][2],
                'diff'    : record[0][3],
                'dt'      : record[0][4]}
    if column_name in rec_dict:
        return rec_dict[column_name]
    else:
        return 0.0

def get_elevation_dict(meeting_id, race_type):
    sql_select_query = """SELECT bin,elevation FROM gpx WHERE meeting_id = %s"""
    input = [str(meeting_id)]
    cur.execute(sql_select_query, input)
    record = cur.fetchall()
    data = {}
    N = len(record)
    for row in record:
        xval = (row[0] / N) * conversion[str(race_type)]
        data[xval] = row[1]
    return data
