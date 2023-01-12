import pandas as pd
from pathlib import Path
import requests
from datetime import datetime

class DailyReports(object):

    def __init__(self, root_dir_path):
        
        self._df = None

        time_stamp = datetime.today()

        self._date = time_stamp.strftime('%Y-%m-%d')
        self._year = time_stamp.strftime('%Y')
        self._month = time_stamp.strftime("%b")

        self._file_name = f'{self._date}.csv.gz'
        
        self._file_handle = Path(root_dir_path, self._year, self._month, self._file_name)
        self._file_handle.parent.mkdir(exist_ok=True, parents=True)

        # Load it into a pandas dataframe
        if Path.exists(self._file_handle):
            print("Loading existing")
            self._df = pd.read_csv(self._file_handle)
        else:
            print("Creating new")
            self._df = pd.DataFrame()

    def add_readings(self, *args):
        # Append the df to the main data frame
        for df in args:
            #print(df.head())
            self._df = pd.concat([self._df, df], axis=0)

    def finalise(self):
        #print(self._df.head())
        self._df.to_csv(self._file_handle, encoding='utf-8', index=False, compression="gzip")

    # Adds in short origin and destination if it does not exist
    @staticmethod
    def refactor_origin_destination(root_dir):
        
        for path in Path(root_dir).rglob('*.csv.gz'):
            print(path)
            df = pd.read_csv(path)
            
            df.loc[df['origin_address'].str.contains("Bert"),'origin'] = 'Windhover'
            df.loc[df['origin_address'].str.contains("Hamble"),'origin'] = 'Hamble'
            df.loc[df['destination_address'].str.contains("Bert"),'destination'] = 'Windhover'
            df.loc[df['destination_address'].str.contains("Hamble"),'destination'] = 'Hamble'

            df.to_csv(path, encoding='utf-8', index=False)#, compression="gzip")


class JourneyTime(object):

    BASE_URL = f'https://maps.googleapis.com/maps/api/distancematrix/json?'

    def __init__(self, origin, destination, key):
        self._origin = origin
        self._destination = destination
        self._key = key

    def run_queries(self):
        modes = ['driving']
        ret_val = pd.DataFrame()
        for mode in modes:
            ret_val = pd.concat([ret_val, self.query(mode)], axis=0)
        return ret_val

    def query(self, mode):

        orig_pos = f'{self._origin["lat"]}, {self._origin["long"]}'
        dest_pos = f'{self._destination["lat"]}, {self._destination["long"]}'
        
        query_url = f'{JourneyTime.BASE_URL}origins={orig_pos}&destinations={dest_pos}&departure_time=now&key={self._key}&mode={mode}&language=en-EN'

        result = requests.get(query_url)

        if result.status_code == 200:
            # {
            #   'destination_addresses': ['Address 1'], 
            #   'origin_addresses': ['Address 2'], 
            #   'rows': [
            #       {'elements': [{
            #           'distance': {'text': '1.3 km', 'value': 1349}, 
            #           'duration': {'text': '2 mins', 'value': 141},
            #           'duration_in_traffic': {'text': '10 mins', 'value': 586},
            #           'status': 'OK'}
            #       ]}], 
            #   'status': 'OK'}

            journey = result.json()
            # print(journey)
            # Store the SI units
            #   distance = m
            #   duration = s
            data = {
                'timestamp':           pd.to_datetime('now', utc=True).replace(microsecond=0),
                'origin':              self._origin['name'],
                'destination':         self._destination['name'],
                'origin_address':      journey['origin_addresses'][0],
                'destination_address': journey['destination_addresses'][0],
                'origin_lat':          self._origin["lat"],
                'orign_long':          self._origin["long"],
                'destination_lat':     self._destination["lat"],
                'destination_long':    self._destination["lat"],
                'distance':            journey['rows'][0]['elements'][0]['distance']['value'],
                'duration':            journey['rows'][0]['elements'][0]['duration_in_traffic']['value'],
                'mode':                mode
            }

            df = pd.DataFrame(data, index=[0]) 
            # print(df)
            return df


def refactor():
    DailyReports.refactor_origin_destination('data/')

def run_query():

    journeys = [
        (
            {'name': 'Hamble', 'lat': 50.8599421, 'long': -1.3413876},
            {'name': 'Windhover','lat': 50.8975905, 'long': -1.3148369}
        ),
        (
            {'name': 'Hound','lat': 50.8762178,'long': -1.328644},
            {'name': 'Mallards', 'lat': 50.8826763, 'long': -1.325972,}
        )
    ]

    file_handle = open('../api.key','r')
    api_key = file_handle.read()

    dr = DailyReports('data/') # lazy

    print(f'Runing Queries')

    for _ , (x, y) in enumerate(journeys):
        jt1 = JourneyTime(x, y, api_key)
        jt2 = JourneyTime(y, x, api_key)

        print(f'Runing query - {x["name"]} to/from {y["name"]} {datetime.now()}')
        dr.add_readings(jt1.run_queries(), jt2.run_queries())
        dr.finalise()

    print('Queries complete')

def main():
    # TODO: Add argparse
    run_query()
    #refactor()

if __name__ == '__main__':
    main()
