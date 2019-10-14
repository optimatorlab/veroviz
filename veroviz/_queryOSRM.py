from veroviz._common import *
from veroviz._internal import distributeTimeDist
from veroviz._internal import loc2Dict
from veroviz._internal import locs2Dict

def osrmGetSnapToRoadLatLon(loc):
	"""
	A function to get snapped latlng for one coordinate using OSRM

	Parameters
	----------
	loc: list
		The location to be snapped to road

	Returns
	-------
	list
		A snapped locations in the format of [lat, lon], notice that this function will lost the info of altitude of the location.
	"""

	dicLoc = loc2Dict(loc)
	snapToRoadUrl = ('http://router.project-osrm.org/nearest/v1/driving/%s,%s') % (dicLoc['lon'], dicLoc['lat']) # OSRM use lon/lat
	data = []

	try:
		http = urllib3.PoolManager()
		response = http.request('GET', snapToRoadUrl)
		data = json.loads(response.data.decode('utf-8'))

		snapLoc = [data['waypoints'][0]['location'][1], data['waypoints'][0]['location'][0]] # OSRM use lon/lat
	except:
		print ("Message: OSRM is currently not available, please try again later.")

	return snapLoc

def osrmGetShapepointsTimeDist(startLoc, endLoc):
	"""
	A function to get a list of shapepoints from start coordinate to end coordinate, the result of this function is not as detailed as mpqGetShapepointTimeDist, however, it is faster.

	Parameters
	----------
	startLoc: list
		Start location, the format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt]
	endLoc: list
		End location, the format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt]

	Returns
	-------
	path: list of lists
		A list of coordinates in sequence that shape the route from startLoc to endLoc
	timeInSeconds: double
		time between current shapepoint and previous shapepoint, the first element should be 0
	distInMeters: double
		distance between current shapepoint and previous shapepoint, the first element should be 0
	"""

	dicStartLoc = loc2Dict(startLoc)
	dicEndLoc = loc2Dict(endLoc)
	shapepointsUrl = ('http://router.project-osrm.org/route/v1/driving/%s,%s;%s,%s?steps=true') % (dicStartLoc['lon'], dicStartLoc['lat'], dicEndLoc['lon'], dicEndLoc['lat']) # OSRM use lon/lat
	data = []

	try:
		http = urllib3.PoolManager()
		response = http.request('GET', shapepointsUrl)
		data = json.loads(response.data.decode('utf-8'))

		path = []
		for i in range(len(data['routes'])):
			for j in range(len(data['routes'][i]['legs'])):
				for k in range(len(data['routes'][i]['legs'][j]['steps'])):
					for m in range(len(data['routes'][i]['legs'][j]['steps'][k]['intersections'])):
						path.append([data['routes'][i]['legs'][j]['steps'][k]['intersections'][m]['location'][1], data['routes'][i]['legs'][j]['steps'][k]['intersections'][m]['location'][0]])
		totalTimeInSecond = data['routes'][0]['duration']
		[timeInSeconds, distInMeters] = distributeTimeDist(path, totalTimeInSecond)
	except:
		print ("Message: OSRM is currently not available, please try again later.")

	return [path, timeInSeconds, distInMeters]

def osrmGetTimeDistOnePair(startLoc, endLoc):
	"""
	A function to get a total time and total distance between two given coordinates

	Parameters
	----------
	startLoc: list
		Start location, the format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt]
	endLoc: list
		End location, the format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt]

	Returns
	-------
	timeSeconds: double
		time between current shapepoint and previous shapepoint, the first element should be 0
	distMeters: double
		distance between current shapepoint and previous shapepoint, the first element should be 0
	"""

	dicStartLoc = loc2Dict(startLoc)
	dicEndLoc = loc2Dict(endLoc)
	timeDistUrl = ('http://router.project-osrm.org/route/v1/driving/%s,%s;%s,%s') % (dicStartLoc['lon'], dicStartLoc['lat'], dicEndLoc['lon'], dicEndLoc['lat']) # OSRM use lon/lat
	data = []

	try:
		http = urllib3.PoolManager()
		response = http.request('GET', timeDistUrl)
		data = json.loads(response.data.decode('utf-8'))

		timeSeconds = data['routes'][0]['duration']
		distMeters = data['routes'][0]['distance']
	except:
		print ("Message: OSRM is currently not available, please try again later.")

	return [timeSeconds, distMeters]

def osrmGetTimeDist(fromLocs, toLocs):
	"""
	A function to get distance and time matrices between a list of starting coordinates and a list of ending coordinates

	Parameters
	----------
	fromLocs: list of lists
		A list of starting coordinates, the format is [[lat1, lon1], [lat2, lon2], ...]
	toLocs: list of lists
		A list of ending coordinates, the format is [[lat1, lon1], [lat2, lon2], ...]

	Returns
	-------
	timeInSeconds: double
		time between current shapepoint and previous shapepoint, the first element should be 0
	distInMeters: double
		distance between current shapepoint and previous shapepoint, the first element should be 0
	"""
	timeSeconds = {}
	distMeters = {}
	for i in range(len(fromLocs)):
		for j in range(len(toLocs)):
			[time, dist] = osrmGetTimeDistOnePair(fromLocs[i], toLocs[j])
			timeSeconds[i, j] = time
			distMeters[i, j] = dist

	return [timeSeconds, distMeters]