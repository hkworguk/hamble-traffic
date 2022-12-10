import pandas as pd
import json
import requests

class DataStore(object):

    def __init__(self, path, date):
        
        self._df = None

        # If the file exists then load it
        # file format data/2022-12-01.csv

        # else create a new one

    def add_rows(self, df):
        pass


class JourneyTime(object):

    BASE_URL = f'https://maps.googleapis.com/maps/api/distancematrix/json?'

    def __init__(self, origin, destination, key):
        self._origin = origin
        self._destination = destination
        self._key = key

    def run_queries(self):
        modes = ['driving', 'cycling']

        for mode in modes:
            self.query(mode)

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

            print(result.json())

            journey_time = result.json()['rows'][0]['elements'][0]['duration']['value']
            
            # Extract the distance to see if it's non-standard route
            print(journey_time)

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

    jt = JourneyTime(hamble, windhover, api_key)

    jt.run_queries()

if __name__ == '__main__':
    main()
