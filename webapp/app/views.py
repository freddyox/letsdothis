from flask import render_template, url_for
from app import app
from flask import request
import pandas as pd

race_type = '10K'
input_dir = '/home/freddy/insight/letsdothis/inputs/'
input_age   = race_type + '/age_map_' + race_type + '.csv'
input_times = race_type + '/avg_times_' + race_type + '.csv'
input_beta  = race_type + '/beta_' + race_type + '.csv'
input_gpx   = race_type + '/gpx_info_' + race_type + '.csv'
input_dist  = race_type + '/d_dist_' + race_type + '.csv'
input_evts  = race_type + '/event_title_list_v2_' + race_type + '.csv'
events_df = pd.read_csv(input_dir+input_evts)
events = dict(zip(events_df.ID,events_df.event))

def get_score(dval):
    df_d = pd.read_csv(input_dir+input_dist)
    bins, xs, ys, dxs = [], [], [], []
    for index,row in df_d.iterrows():
        bins.append(row.bin)
        xs.append(row.xval)
        ys.append(row.yval)
        dxs.append(row.dx)
        score = -1.0
    for idx,val in enumerate(xs):
        dx = dxs[idx]*0.5
        dlo = xs[idx] - dx
        dhi = xs[idx] + dx
        if dval >= dlo and dval < dhi:
            score = ys[idx]
            break
    return score

def get_gpx_info(id):
    gpx_df = pd.read_csv(input_dir+input_gpx)
    sum_up = dict(zip(gpx_df.meeting_id, gpx_df.sum_up))[id]
    diff   = dict(zip(gpx_df.meeting_id, gpx_df['diff']))[id]
    sigma  = dict(zip(gpx_df.meeting_id, gpx_df.sigma))[id]
    return [sum_up,sigma,diff]

def get_min_time(ID,sex,age):
    df = pd.read_csv(input_dir+input_times)
    temp=df[(df.meeting_id==ID) & (df.sex==sex)]
    Age = list(temp['age_group'].values)
    success = False
    if age in Age:
        age = age # Do nothing
        success = True
    else:
        Age.sort()
        success = False
        for i in Age:
            if i>age:
                age = i
                success=True
                break
        # Need to go backwards now
        if not success:
            for i in range(len(Age)-1,-1,-1):
                if Age[i] < age:
                    age = Age[i]
                    break
    #print(age,success)
    row = temp.loc[(temp['age_group']==age) & 
                   (temp['sex']==sex) &
                   (temp['meeting_id'] == ID)]
    return (row.min_time).item()

def make_map(filename):
    df = pd.read_csv(filename, header=None)
    amap = {}
    for index, row in df.iterrows():
        amap[df.values[index][0]] = df.values[index][1]
    return amap

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", events=events)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/output')
def output():
    age_type = str(request.args.get('age'))
    gender_type = str(request.args.get('gender'))
    race_type = str(request.args.get('race'))
    event_type = str(request.args.get('event'))
    
    age_map = {'U11':0,'U13':1,'U15':2,'U17':3,'U20':4,'U23':5,
               'SEN':6,'V35':7,'V40':8,'V45':9,'V50':10,'V55':11,
               'V60':12,'V65':13,'V70':14,'V75':15,'V80':16,'V85':17}
    sex_map = {'Female': 1, 'Male': 2}

    age_type    =  pd.Series(age_type)
    gender_type =  pd.Series(gender_type)
    race_type   =  pd.Series(race_type)
    ID  =  int(pd.Series(event_type)[0])
    
    sex      = gender_type.map(sex_map).astype(int)
    age      = age_type.map(age_map).astype(int)
    gpx_info = get_gpx_info(ID)
    time = get_min_time(ID,int(sex),int(age))
    beta_map = make_map(input_dir+input_beta)

    # calculate beta
    x = [age, sex, time, gpx_info[0], gpx_info[1],gpx_info[2]]
    b = [beta_map['age_group'], beta_map['sex'],beta_map['min_time'],
             beta_map['sum_up'],beta_map['sigma'],beta_map['diff']]
    betax = 0.0
    for idx, val in enumerate(x):
        betax += x[idx]*b[idx]

    betax = float(betax)
    score = float(get_score(betax))    
    print(betax,score)    
    print(gender_type[0], age_type[0])
    return render_template("output.html", betax=betax, score=score)
