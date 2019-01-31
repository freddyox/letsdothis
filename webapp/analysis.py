import pandas as pd

race_type = 'Mar'
input_dir = '/home/freddy/insight/letsdothis/inputs/'
input_age   = race_type + '/age_map_' + race_type + '.csv'
input_times = race_type + '/avg_times_' + race_type + '.csv'
input_beta  = race_type + '/beta_' + race_type + '.csv'
input_gpx   = race_type + '/gpx_info_' + race_type + '.csv'
input_dist  = race_type + '/d_dist_' + race_type + '.csv'
input_evts  = race_type + '/event_title_list_v2_' + race_type + '.csv'


def set_variables(race_type):
    race_type = race_type
    input_dir = '/home/freddy/insight/letsdothis/inputs/'
    input_age   = race_type + '/age_map_' + race_type + '.csv'
    input_times = race_type + '/avg_times_' + race_type + '.csv'
    input_beta  = race_type + '/beta_' + race_type + '.csv'
    input_gpx   = race_type + '/gpx_info_' + race_type + '.csv'
    input_dist  = race_type + '/d_dist_' + race_type + '.csv'
    input_evts  = race_type + '/event_title_list_v2_' + race_type + '.csv'    

def get_events(race_type):
    set_variables(race_type)
    
    events_df = pd.read_csv(input_dir+input_evts)
    events = dict(zip(events_df.ID,events_df.event))
    return events

# The distribution has already been integrated, just use arrays as
# a look-up table; this is O(N), which is acceptable
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

# Build the maps and return the relevant information
def get_gpx_info(id):
    gpx_df = pd.read_csv(input_dir+input_gpx)
    sum_up = dict(zip(gpx_df.meeting_id, gpx_df.sum_up))[id]
    diff   = dict(zip(gpx_df.meeting_id, gpx_df['diff']))[id]
    sigma  = dict(zip(gpx_df.meeting_id, gpx_df.sigma))[id]
    return [sum_up,sigma,diff]

def get_min_time_simple(ID):
    df = pd.read_csv(input_dir+input_times)
    time_map = dict(zip(df.meeting_id, df.min_time))
    return time_map[ID]

def make_map(filename):
    df = pd.read_csv(filename, header=None)
    amap = {}
    for index, row in df.iterrows():
        amap[df.values[index][0]] = df.values[index][1]
    return amap

def predict(age_type, gender_type, race_type, event_type):
    age_map = make_map(input_dir+input_age)
    sex_map = {'Female': 1, 'Male': 2}

    age_type    =  pd.Series(age_type)
    gender_type =  pd.Series(gender_type)
    race_type   =  pd.Series(race_type)
    ID          =  int(pd.Series(event_type)[0])

    #print(race_type)
    
    sex      = gender_type.map(sex_map).astype(int)
    age      = age_type.map(age_map).astype(int)
    gpx_info = get_gpx_info(ID)
    time     = get_min_time_simple(ID)
    beta_map = make_map(input_dir+input_beta)

    # calculate beta
    x = [age, sex, time, gpx_info[0], gpx_info[1],gpx_info[2]]
    b = [beta_map['age_group'], beta_map['sex'],beta_map['min_time'],
         beta_map['sum_up'],beta_map['sigma'],beta_map['diff']]
    
    betax = 0.0
    for idx, val in enumerate(x):
        betax += x[idx]*b[idx]
        
    print(float(betax))
    betax = float(betax)
    score = float(get_score(betax))
    return [betax,score]
