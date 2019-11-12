from veroviz._common import *
from veroviz._internal import distributeTimeDist
from veroviz._internal import locs2Dict
from veroviz._internal import loc2Dict

def mqGetSnapToRoadLatLon(loc, APIkey):
	"""
	A function to get snapped latlng for one coordinate using MapQuest

	Parameters
	----------
	loc: list
		The location to be snapped to road
	APIkey: string, Required
		Enables us to access to MapQuest server

	Returns
	-------
	list
		A snapped locations in the format of [lat, lon], notice that this function will lost the info of altitude of the location.
	"""

	dicLoc = loc2Dict(loc)

	snapToRoadUrl = ('http://www.mapquestapi.com/geocoding/v1/batch?key=%s&thumbMaps=false&outFormat=json&location=%s,%s') % (APIkey, dicLoc['lat'], dicLoc['lon'])
	data = []
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', snapToRoadUrl)
		data = json.loads(response.data.decode('utf-8'))

		snapLoc = [data['results'][0]['locations'][0]['latLng']['lat'], data['results'][0]['locations'][0]['latLng']['lng']]
	except:
		print("Message: Unable to connect MapQuest, the most common causes are 1) that your computer isn't connected to the network; 2) an invalid key is provided.")

	return snapLoc

def mqGetSnapToRoadLatLonBatch(locs, APIkey):
	"""
	A function to get snapped latlng for one coordinate using MapQuest

	Parameters
	----------
	locs: list of lists
		The locations to be snapped to road
	APIkey: string, Required
		Enables us to access to MapQuest server

	Returns
	-------
	list of lists
		A list of snapped locations in the format of [[lat, lon], [lat, lon], ...], notice that this function will lost the info of altitude of the locations.
	"""

	maxBatchSize = 100
	numBatches = int(math.ceil(len(locs) / float(maxBatchSize)))
	snapToRoadUrlBase = ('http://www.mapquestapi.com/geocoding/v1/batch?key=%s&thumbMaps=false&outFormat=json') % (APIkey)

	dicLocs = locs2Dict(locs)
	
	try:
		for batch in range(0, numBatches):
			snapToRoadUrl = snapToRoadUrlBase	
			for i in range(maxBatchSize * batch, min(len(locs), maxBatchSize * (batch + 1))):
				snapToRoadUrl += ('&location=%s,%s') % (dicLocs[i]['lat'], dicLocs[i]['lon'])
			data = []
		
			http = urllib3.PoolManager()
			response = http.request('GET', snapToRoadUrl)
			data = json.loads(response.data.decode('utf-8'))
			
			snapLocs = [[data['results'][j]['locations'][0]['latLng']['lat'], data['results'][j]['locations'][0]['latLng']['lng']] for j in range(0, len(data['results']))]
	except:
		print("Message: Unable to connect MapQuest, the most common causes are 1) that your computer isn't connected to the network; 2) an invalid key is provided.")

	return snapLocs

def mqGetShapepointsTimeDist(startLoc, endLoc, routeType='fastest', APIkey=None):
	"""
	A function to get a list of shapepoints from start coordinate to end coordinate

	Parameters
	----------

	startLoc: list, Required
		Start location, the format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt]
	endLoc: list, Required
		End location, the format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt]
	routeType: string, Optional, default as 'fastest'
		Route type of MapQuest query
	APIkey: string, Required
		Enables us to access to MapQuest server

	Returns
	-------
	path: list of lists
		A list of coordinates in sequence that shape the route from startLoc to endLoc
	time: float
		time between current shapepoint and previous shapepoint, the first element should be 0
	dist: float
		distance between current shapepoint and previous shapepoint, the first element should be 0
	"""
	
	try:
		routeType = routeType.lower()
	except:
		pass

	dicStartLoc = loc2Dict(startLoc)
	dicEndLoc = loc2Dict(endLoc)

	shapepointsUrl = ('http://www.mapquestapi.com/directions/v2/route?key=%s&from=%s,%s&to=%s,%s&fullShape=true&routeType=%s') % (
		APIkey, 
		dicStartLoc['lat'], 
		dicStartLoc['lon'], 
		dicEndLoc['lat'], 
		dicEndLoc['lon'], 
		routeType)
	data = []
	
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', shapepointsUrl)
		data = json.loads(response.data.decode('utf-8'))

		path = []

		totalTimeInSeconds = data['route']['time']

		maneuverIndexes = data['route']['shape']['maneuverIndexes']
		rawShapepoints = data['route']['shape']['shapePoints']

		for i in range(int(len(rawShapepoints) / 2)):
			if (len(path) > 0):
				if (rawShapepoints[i * 2] != path[-1][0] and rawShapepoints[i * 2 + 1] != path[-1][1]):
					path.append([rawShapepoints[i * 2], rawShapepoints[i * 2 + 1]])
			else:
				path.append([rawShapepoints[0], rawShapepoints[1]])

		[timeSecs, distMeters] = distributeTimeDist(path, totalTimeInSeconds)
	except:
		print("Message: Unable to connect MapQuest, the most common causes are 1) that your computer isn't connected to the network; 2) an invalid key is provided.")

	return [path, timeSecs, distMeters]

def mqGetTimeDistAll2All(locs, routeType='fastest', APIkey=None):
	"""
	A function to generate a distance and time matrice between given coordinates

	Parameters
	----------

	locs: list of lists, Required
		The format is [[lat1, lon1], [lat2, lon2], ...], a list of coordinates
	travelMode: string, {fastest, shortest, pedestrian}
		MapQuest provides three different types of routing, including 'fastest', 'shortest' (for car) and 'pedestrian'
	APIkey: string, Required
		Enables us to access to MapQuest server
	
	Returns
	-------
	time: dictionary
		A squared matrix, which provides the traveling time between each pair of coordinates, unit is in second
	dist: dictionary
		A squared matrix, which provides the distance between each pair of coordinates, units is in meters

	"""

	distMeters = {}
	timeSecs = {}

	try:
		routeType = routeType.lower()
	except:
		pass

	try:
		# If the number of coordinate is less than 25, query in one batch, if not, partition into n * one2many queries
		if (len(locs) <= 0): # Should be 25, however, mapQuest stopped supporting all2all flag, don't know why and don't know when can be restored
			all2AllUrl = ('http://www.mapquestapi.com/directions/v2/routematrix?key=%s&json={locations:[') % (APIkey)
			for i in range(len(locs)):
				all2AllUrl += ('{latLng:{lat:%s,lng:%s}},') % (locs[i][0], locs[i][1])
			all2AllUrl = all2AllUrl[:-1]
			all2AllUrl += ("],options:{all2All:true,routeType:%s,doReverseGeocode:false}}") % (routeType) 
			data = []

			http = urllib3.PoolManager()
			response = http.request('GET', all2AllUrl)
			data = json.loads(response.data.decode('utf-8'))

			distBatch = data['distance']
			timeBatch = data['time']
			for i in range(len(locs)):
				for j in range(len(locs)):
					distMeters[i, j] = distBatch[i][j]
					timeSecs[i, j] = timeBatch[i][j]
		else:
			for i in range(len(locs)):
				[timeRow, distRow] = mqGetTimeDistOne2Many(locs[i], locs, routeType, APIkey)
				for j in range(len(locs)):
					distMeters[i, j] = distRow[0, j]
					timeSecs[i, j] = timeRow[0, j]
	except:
		print("Message: Unable to connect MapQuest, the most common causes are 1) that your computer isn't connected to the network; 2) an invalid key is provided.")

	return [timeSecs, distMeters]

def mqGetTimeDistOne2Many(fromLoc, toLocs, routeType='fastest', APIkey=None):
	"""
	A function to generate a distance and time matrice between a given coordinate and a list of coordinates

	Parameters
	----------
	fromLoc: list, Required
		One coordinate in the format of [lat, lon]
	toLocs: list of lists, Required
		The format is [[lat1, lon1], [lat2, lon2], ...], a list of coordinates
	travelMode: string, {fastest, shortest, pedestrian}
		MapQuest provides three different types of routing, including 'fastest', 'shortest' (for car) and 'pedestrian'
	APIkey: string
		Required, enables us to access to MapQuest server
	
	Returns
	-------
	time: dictionary
		A squared matrix, which provides the traveling time between each pair of coordinates, unit is in second
	dist: dictionary
		A squared matrix, which provides the distance between each pair of coordinates, units is in meters

	"""

	one2ManyBatchSize = 90 # < 100
	numBatches = int(math.ceil(len(toLocs) / float(one2ManyBatchSize)))
	one2ManyUrlBase = ('http://www.mapquestapi.com/directions/v2/routematrix?key=%s&json={locations:[') % (APIkey)

	distMeters = {}
	timeSecs = {}

	try:
		routeType = routeType.lower()
	except:
		pass

	try:
		for batch in range(0, numBatches):
			one2ManyUrl = one2ManyUrlBase
			# fromLoc should contain one and only one coordinate
			one2ManyUrl += ('{latLng:{lat:%s,lng:%s}},') % (fromLoc[0], fromLoc[1])
			for i in range(one2ManyBatchSize * batch, min(len(toLocs), one2ManyBatchSize * (batch + 1))):
				# toLocs is a list of coordinates, in [[lat, lon], [lat, lon], ..., [lat, lon]] format
				one2ManyUrl += ('{latLng:{lat:%s,lng:%s}},') % (toLocs[i][0], toLocs[i][1])
			one2ManyUrl = one2ManyUrl[:-1]
			one2ManyUrl += ("],options:{oneToMany:true,routeType:%s,doReverseGeocode:false}}") % (routeType)
			data = []
			
			http = urllib3.PoolManager()
			response = http.request('GET', one2ManyUrl)
			data = json.loads(response.data.decode('utf-8'))

			distBatch = data['distance']
			timeBatch = data['time']
			for i in range(one2ManyBatchSize * batch, min(len(toLocs), one2ManyBatchSize * (batch + 1))):
				distMeters[0, i] = distBatch[i - one2ManyBatchSize * batch + 1] * VRV_CONST_METERS_PER_MILE
				timeSecs[0, i] = timeBatch[i - one2ManyBatchSize * batch + 1]
	except:
		print("Message: Unable to connect MapQuest, the most common causes are 1) that your computer isn't connected to the network; 2) an invalid key is provided.")

	return [timeSecs, distMeters]

def mqGetTimeDistMany2One(fromLocs, toLoc, routeType='fastest', APIkey=None):
	"""
	A function to generate a distance and time matrice between given list of coordinates and one coordinate

	Parameters
	----------
	fromLocs: list of lists
		The format is [[lat1, lon1], [lat2, lon2], ...], a list of coordinates
	toLoc: list
		In the format of [lat, lon]
	travelMode: string, {fastest, shortest, pedestrian}
		MapQuest provides three different types of routing, including 'fastest', 'shortest' (for car) and 'pedestrian'
	APIkey: string
		Enables us to access to MapQuest server
	
	Returns
	-------
	time: dictionary
		A squared matrix, which provides the traveling time between each pair of coordinates, unit is in second
	dist: dictionary
		A squared matrix, which provides the distance between each pair of coordinates, units is in meters

	"""

	many2OneBatchSize = 40 # < 50
	numBatches = int(math.ceil(len(fromLocs) / float(many2OneBatchSize)))
	many2OneUrlBase = ('http://www.mapquestapi.com/directions/v2/routematrix?key=%s&json={locations:[') % (APIkey)

	distMeters = {}
	timeSecs = {}

	try:
		routeType = routeType.lower()
	except:
		pass

	try:
		for batch in range(0, numBatches):
			many2OneUrl = many2OneUrlBase
			# fromLocs should contain one and only one coordinate
			many2OneUrl += ('{latLng:{lat:%s,lng:%s}},') % (toLoc[0], toLoc[1])
			for i in range(many2OneBatchSize * batch, min(len(fromLocs), many2OneBatchSize * (batch + 1))):
				# toCoordList is a list of coordinates, in [[lat, lon], [lat, lon], ..., [lat, lon]] format
				many2OneUrl += ('{latLng:{lat:%s,lng:%s}},') % (fromLocs[i][0], fromLocs[i][1])
			many2OneUrl = many2OneUrl[:-1]
			many2OneUrl += ("],options:{manyToOne:true,routeType:%s,doReverseGeocode:false}}") % (routeType)
			data = []

			http = urllib3.PoolManager()
			response = http.request('GET', many2OneUrl)
			data = json.loads(response.data.decode('utf-8'))

			distBatch = data['distance']
			timeBatch = data['time']
			for i in range(many2OneBatchSize * batch, min(len(fromLocs), many2OneBatchSize * (batch + 1))):
				distMeters[i, 0] = distBatch[i - many2OneBatchSize * batch + 1] * VRV_CONST_METERS_PER_MILE
				timeSecs[i, 0] = timeBatch[i - many2OneBatchSize * batch + 1]
	except:
		print("Message: Unable to connect MapQuest, the most common causes are 1) that your computer isn't connected to the network; 2) an invalid key is provided.")

	return [timeSecs, distMeters]
	
def mqGeocode(text, APIkey):
	"""
	Geocode from a text string using MapQuest
	
	Parameters
	----------
	text: string
		A text string describing an address, city, or landmark.
	    
	Returns
	-------
	loc: list
		A geocoded location in the format of [lat, lon].
	"""
	
	geocodeUrl = ('http://www.mapquestapi.com/geocoding/v1/address?key=%s&maxResults=1&thumbMaps=false&outFormat=json&location=%s') % (APIkey, text)
	
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', geocodeUrl)
		data = json.loads(response.data.decode('utf-8'))
		http_status = response.status
		if (data['info']['statuscode'] == 0):
			loc = [data['results'][0]['locations'][0]['latLng']['lat'], data['results'][0]['locations'][0]['latLng']['lng']]
			return loc
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return
	except:
		print("Message: Unable to connect to MapQuest, the most common causes are 1) that your computer isn't connected to the network; 2) an invalid key is provided.")
		print("Error: ", sys.exc_info()[1])
		raise 
		
def mqReverseGeocode(loc, APIkey):
	"""
	Reverse Geocode from a [lat, lon] or [lat, lon, alt] location using MapQuest
	
	Parameters
	----------
	loc: list
		Of the form [lat, lon] or [lat, lon, alt].  If provided, altitude will be ignored.
	    
	Returns
	-------
	snapLoc: list
		Of the form [lat, lon].  This is the nearest point to the given (input) location.
	address: dictionary
		A dataProvider-specific dictionary containing address details.
	"""
	
	geocodeUrl = ('http://www.mapquestapi.com/geocoding/v1/reverse?key=%s&thumbMaps=false&outFormat=json&includeNearestIntersection=true&includeRoadMetadata=true&location=%s,%s') % (APIkey, loc[0], loc[1])
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', geocodeUrl)
		data = json.loads(response.data.decode('utf-8'))
		http_status = response.status
		if (data['info']['statuscode'] == 0):
			snapLoc = [data['results'][0]['locations'][0]['latLng']['lat'], 
                       data['results'][0]['locations'][0]['latLng']['lng']]
			address = data['results'][0]['locations'][0]
			return (snapLoc, address)
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return
	except:
		print("Message: Unable to connect to MapQuest, the most common causes are that 1) your computer isn't connected to the network; 2) an invalid key was provided.")
		print("Error: ", sys.exc_info()[1])
		raise
		
