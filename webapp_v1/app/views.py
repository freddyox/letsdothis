from flask import render_template, url_for, request, Flask
from app import app
import pandas as pd
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'freddy'
app.config['MYSQL_DATABASE_PASSWORD'] = 'N@c1remaLane88'
app.config['MYSQL_DATABASE_DB'] = 'app'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cur =conn.cursor()
    
@app.route('/')
@app.route('/index')
def index():
    events = sql_get_events("Mar")
    return render_template("index.html", events=events)

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

    age_type    =  pd.Series(age_type)
    gender_type =  pd.Series(gender_type)
    ID          =  int(pd.Series(event_type)[0])
        
    # Build the appropriate material
    age      = age_type.map(age_map).astype(int)
    sex      = gender_type.map(sex_map).astype(int)

    print('User Input:')
    print('\t age   = {}'.format(age))
    print('\t sex   = {}'.format(sex))
    print('\t race  = {}'.format(race_type))
    print('\t ID    = {}'.format(ID))
    print('\t Event = {}'.format(get_event(ID)))
    
    time     = get_time(ID)
    gpx_info = get_gpx_info(ID, get_event(ID), True)
    print('Course Input:')
    print('\t time   = {}'.format(time))
    print('\t sum_up = {}'.format(gpx_info[0]))
    print('\t sigma  = {}'.format(gpx_info[1]))
    print('\t diff   = {}'.format(gpx_info[2]))
      
    beta     = get_beta(race_type)
    X = [age, sex, time, gpx_info[0], gpx_info[1],gpx_info[2]]
    betax = 0.0
    for idx, val in enumerate(X):
        betax += X[idx]*beta[idx]
        print(idx, X[idx], beta[idx])

    score = get_score(float(betax), race_type)
    return render_template("output.html", betax=betax, score=score)
  
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

def get_time(ID):
    sql_select_query = """SELECT meeting_id, min_time FROM race_info WHERE meeting_id = %s"""
    cur.execute(sql_select_query, (str(ID), ))
    record = cur.fetchall()
    return record[0][1]

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
