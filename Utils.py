import pandas as pd
import json
import requests

class JourneyTime(object):

    def __init__(self, origin, destination):
        self._origin = origin
        self._destination = destination

    def run_queries(self):
        modes = ['driving', 'cycling']

        for mode in modes:
            self.query(mode)

    def query(self, mode):

        orig_pos = self._origin['lat'], self._origin['long']
        dest_pos = self._destination['lat'], self._destination['long']

        base_url = f'https://maps.googleapis.com/maps/api/distanceMatrix/json?'
        query_url = f'{base_url}origins={orig_pos}&destinations={dest_pos}&mode={mode}&language=en-EN&sensor=false'
        # https://maps.googleapis.com/maps/api/distancematrix/json?origins=(1, 1)                  &destinations=(1, 1)                  &mode=driving&language=en-EN&sensor=false
        # https://maps.googleapis.com/maps/api/distanceMatrix/json?origins=(50.8987019, -1.3112051)&destinations=(50.8975905, -1.3148369)&mode=driving&language=en-EN&sensor=false
        print(query_url)
        result = requests.get(query_url)

        print(result)
        journey_time = result['rows'][0]['elements'][0]['duration']['value']

        print(journey_time)


def main():

    hamble = {
        'name': 'Hamble',
        'lat': 50.8987019,
        'long': -1.3112051
    }

    windhover = {
        'name': 'Windhover',
        'lat': 50.8975905,
        'long': -1.3148369
    }

    jt = JourneyTime(hamble, windhover)

    jt.run_queries()

if __name__ == '__main__':
    main()
