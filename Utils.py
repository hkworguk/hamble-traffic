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

        self._file_name = f'{self._date}.csv'
        
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
            self._df = pd.concat([self._df, df])

    def finalise(self):
        print(self._df.head())
        self._df.to_csv(self._file_handle, encoding='utf-8')


class JourneyTime(object):

    BASE_URL = f'https://maps.googleapis.com/maps/api/distancematrix/json?'

    def __init__(self, origin, destination, key):
        self._origin = origin
        self._destination = destination
        self._key = key

    def run_queries(self):
        modes = ['driving', 'bicycling']
        ret_val = pd.DataFrame()
        for mode in modes:
            ret_val = pd.concat([ret_val, self.query(mode)])
        return ret_val

    def query(self, mode):

        orig_pos = f'{self._origin["lat"]}, {self._origin["long"]}'
        dest_pos = f'{self._destination["lat"]}, {self._destination["long"]}'
        
        query_url = f'{JourneyTime.BASE_URL}key={self._key}&origins={orig_pos}&destinations={dest_pos}&mode={mode}&language=en-EN&sensor=false'

        result = requests.get(query_url)

        if result.status_code == 200:
            # {
            #   'destination_addresses': ['Address 1'], 
            #   'origin_addresses': ['Address 2'], 
            #   'rows': [
            #       {'elements': [{
            #           'distance': {'text': '1.3 km', 'value': 1349}, 
            #           'duration': {'text': '2 mins', 'value': 141}, 'status': 'OK'}
            #       ]}], 
            #   'status': 'OK'}

            journey = result.json()

            # Store the SI units
            #   distance = m
            #   duration = s
            data = {
                'timestamp':           pd.to_datetime('now', utc=True).replace(microsecond=0),
                'origin_address':      journey['origin_addresses'][0],
                'destination_address': journey['destination_addresses'][0],
                'origin_lat':          self._origin["lat"],
                'orign_long':          self._origin["long"],
                'destination_lat':     self._destination["lat"],
                'destination_long':    self._destination["lat"],
                'distance':            journey['rows'][0]['elements'][0]['distance']['value'],
                'duration':            journey['rows'][0]['elements'][0]['duration']['value'],
                'mode':                mode
            }

            df = pd.DataFrame(data, index=[0]) 
            # print(df)
            return df


def main():

    hamble = {
        'name': 'Hamble',
        'lat': 50.8599421,
        'long': -1.3413876
    }

    windhover = {
        'name': 'Windhover',
        'lat': 50.8975905,
        'long': -1.3148369
    }

    file_handle = open('../api.key','r')
    api_key = file_handle.read()

    dr = DailyReports('data/') # lazy

    jt1 = JourneyTime(hamble, windhover, api_key)
    jt2 = JourneyTime(windhover, hamble, api_key)

    dr.add_readings(jt1.run_queries(), jt2.run_queries())

    dr.finalise()

if __name__ == '__main__':
    main()
