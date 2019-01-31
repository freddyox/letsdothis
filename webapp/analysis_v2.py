import pandas as pd

class Analysis:
    def __init__(self):
        self.race_type = '10K'
        self.events = {}
        self.set_variables(self.race_type)
        
    def set_variables(self, type):
        self.race_type = type
        self.input_dir = '/home/freddy/insight/letsdothis/inputs/'
        self.input_age   = self.race_type + '/age_map_' + self.race_type + '.csv'
        self.input_times = self.race_type + '/avg_times_' + self.race_type + '.csv'
        self.input_beta  = self.race_type + '/beta_' + self.race_type + '.csv'
        self.input_gpx   = self.race_type + '/gpx_info_' + self.race_type + '.csv'
        self.input_dist  = self.race_type + '/d_dist_' + self.race_type + '.csv'
        self.input_evts  = self.race_type + '/event_title_list_v2_' + self.race_type + '.csv'
        self.set_events()

    def set_events(self):
        events_df = pd.read_csv(self.input_dir + self.input_evts)
        self.events = dict(zip(events_df.ID,events_df.event))

    def get_events(self):
        return self.events
    
    def print_evts(self):
        for key, val in self.events.items():
            print(key,val)

    def get_score(self,dval):
        df_d = pd.read_csv(self.input_dir + self.input_dist)
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

    def get_gpx_info(self, id):
        gpx_df = pd.read_csv(self.input_dir + self.input_gpx)
        sum_up = dict(zip(gpx_df.meeting_id, gpx_df.sum_up))[id]
        diff   = dict(zip(gpx_df.meeting_id, gpx_df['diff']))[id]
        sigma  = dict(zip(gpx_df.meeting_id, gpx_df.sigma))[id]
        return [sum_up,sigma,diff]

    def get_min_time_simple(self, id):
        df = pd.read_csv(self.input_dir + self.input_times)
        time_map = dict(zip(df.meeting_id, df.min_time))
        return time_map[id]

    def make_map(self,filename):
        df = pd.read_csv(filename, header=None)
        amap = {}
        for index, row in df.iterrows():
            amap[df.values[index][0]] = df.values[index][1]
        return amap

    def predict(age_type, gender_type, race_type, event_type):
        age_map = self.make_map(self.input_dir + self.input_age)
        sex_map = {'Female': 1, 'Male': 2}
        age_type    =  pd.Series(age_type)
        gender_type =  pd.Series(gender_type)
        race_type   =  pd.Series(race_type)
        ID          =  int(pd.Series(event_type)[0])

        #print(race_type)
    
        sex      = gender_type.map(sex_map).astype(int)
        age      = age_type.map(age_map).astype(int)
        gpx_info = self.get_gpx_info(ID)
        time     = self.get_min_time_simple(ID)
        beta_map = self.make_map(input_dir+input_beta)

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
