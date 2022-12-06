import requests
orig_coord = 1, 1
dest_coord = 1, 1

orig_coord = 50.8987019, -1.3112051
dest_coord = 50.8975905, -1.314

url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
result = requests.get(url)
print(url)
print(result.status_code)
print(result.json())
driving_time = result['rows'][0]['elements'][0]['duration']['value']
print(driving_time)