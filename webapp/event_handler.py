import pandas as pd

class event_handler:
    def __init__(self):
        self.race_type = '10K'
        self.input_dir = '/home/freddy/insight/letsdothis/inputs/'
        self.input_evts  = self.race_type + '/event_title_list_v2_' + self.race_type + '.csv'
        self.events = self.get_events(self.race_type)

    def set_vars(self, race):
        self.race_type = race
        self.input_evts  = self.race_type + '/event_title_list_v2_' + self.race_type + '.csv'
        
    def get_events(self,race):
        self.set_vars(race)
        events_df = pd.read_csv(self.input_dir + self.input_evts)
        self.events = dict(zip(events_df.ID,events_df.event))
        return self.events
