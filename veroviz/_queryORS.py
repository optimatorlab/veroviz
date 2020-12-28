from veroviz._common import *
from veroviz._internal import distributeTimeDist
from veroviz._internal import loc2Dict
from veroviz._internal import locs2Dict, bitFieldDecomp


def orsGetSnapToRoadLatLon(loc, APIkey):
	"""
	A function to get snapped latlng for one coordinate using ORS
	Parameters
	----------
	loc: list
		The location to be snapped to road
	Returns
	-------
	list
		A snapped location in the format of [lat, lon].  Note that this function will lose the info of altitude of the location.
	"""

	# There is no function in ORS that snaps to a road.
	# Instead, issue a driving request from a location to itself.
	dicLoc = loc2Dict(loc)
    
	snapToRoadUrl = ('https://api.openrouteservice.org/v2/directions/driving-car/geojson')
	
	headers = {
				'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
				'Authorization': APIkey,
				'Content-Type': 'application/json'}
    
	try:
		# ORS uses [lon, lat] order:
		coordinates  = [[dicLoc['lon'], dicLoc['lat']], 
						[dicLoc['lon'], dicLoc['lat']]]
		radiuses     = [-1, -1]
		elevation = "false"
		extra_info = []
		
		encoded_body = json.dumps({
			"coordinates": coordinates,
			"elevation": elevation, 
			"extra_info": extra_info,
			"instructions": "false",
			"radiuses": radiuses})

		http = urllib3.PoolManager()
		response = http.request('POST', snapToRoadUrl, headers=headers, body=encoded_body)
    
		data = json.loads(response.data.decode('utf-8'))
		http_status = response.status

		if (http_status == 200):
			# OK
			# ORS uses [lon, lat] order:
			snapLoc = [data['features'][0]['geometry']['coordinates'][0][1], 
						data['features'][0]['geometry']['coordinates'][0][0]] 
            
			return snapLoc
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return
	except:
		print("Error: ", sys.exc_info()[1])
		raise 


def orsGetShapepointsTimeDist(startLoc, endLoc, travelMode='fastest', APIkey=None, requestExtras=True):
	"""
	A function to get a list of shapepoints from start coordinate to end coordinate. 
	Parameters
	----------
	startLoc: list
		Start location.  The format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt]
	endLoc: list
		End location.  The format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt]
	travelMode: string, {fastest}
		Optional, default as 'fastest'. Choose a travel mode as a parameter for ORS
	Returns
	-------
	path: list of lists
		A list of coordinates in sequence that shape the route from startLoc to endLoc
	extras: dictionary of dictionaries
		Describes extra information, such as waynames, waytypes, elevation, etc.	
	timeInSeconds: list
		time between current shapepoint and previous shapepoint, the first element should be 0 
	distInMeters: list
		distance between current shapepoint and previous shapepoint, the first element should be 0
	"""

	dicStartLoc = loc2Dict(startLoc)
	dicEndLoc = loc2Dict(endLoc)

	"""
	The following "profile" options are available in ORS:
		'driving-car'		('fastest')	
		'driving-hgv'		('truck' - fastest)
		'cycling-regular'	('cycling')
		'cycling-road'
		'cycling-mountain'
		'cycling-electric'
		'foot-walking'
		'foot-hiking'
		'wheelchair'
		
		There is no "shortest" option    
	"""

	preference = 'fastest'
		
	try:
		travelMode = travelMode.lower()
	except:
		pass

	if (travelMode == 'fastest'):
		profile = 'driving-car'
	elif (travelMode == 'shortest'):
		profile = 'driving-car'
		preference = 'shortest'	
	elif (travelMode == 'pedestrian'):
		profile = 'foot-walking'
	elif (travelMode == 'cycling'):
		profile = 'cycling-road'
	elif (travelMode == 'truck'):
		profile = 'driving-hgv'
	elif (travelMode == 'wheelchair'):
		profile = 'wheelchair'
	else:
		print("Error: Invalid travelMode.")
		return    
    
	shapepointsUrl = ('https://api.openrouteservice.org/v2/directions/%s/geojson' % (profile))
	
	headers = {
				'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
				'Authorization': APIkey,
				'Content-Type': 'application/json'}

	try:

		# ORS uses [lon, lat] order:
		coordinates  = [[dicStartLoc['lon'],dicStartLoc['lat']], 
						[dicEndLoc['lon'],dicEndLoc['lat']]]
		units        = 'm'
		radiuses     = [-1, -1]
		if (requestExtras):
			elevation = "true"
			extra_info = ["steepness","surface","waycategory","waytype","tollways"]
		else:
			elevation = "false"
			extra_info = []
		
		encoded_body = json.dumps({
			"coordinates": coordinates,
			"elevation": elevation, 
			"extra_info": extra_info,
			"instructions": "true",
			"preference": preference,
			"radiuses": radiuses,
			"units": units})

		http = urllib3.PoolManager()
		response = http.request('POST', shapepointsUrl, headers=headers, body=encoded_body)

		data = json.loads(response.data.decode('utf-8'))
		http_status = response.status

		if (http_status == 200):
			# OK
			# ORS uses [lon, lat] order:
			path = []
			extras = {}
			timeInSeconds = []
			distInMeters = []
			for i in range(len(data['features'][0]['geometry']['coordinates'])):
				path.append([data['features'][0]['geometry']['coordinates'][i][1], 
							 data['features'][0]['geometry']['coordinates'][i][0]])
				if (requestExtras):
					extras[i] = {}
					if (len(data['features'][0]['geometry']['coordinates'][i]) >= 2):
						extras[i]['elev'] = data['features'][0]['geometry']['coordinates'][i][2]
					else:
						extras[i]['elev'] = None

			segs = data['features'][0]['properties']['segments']
			for i in range(len(segs)):
				for j in range(len(segs[i]['steps'])):
					# Find arrival times for each shapepoint location.
					# ORS gives times for groups of waypoints...we need more granularity.

					subpathTimeSec = segs[i]['steps'][j]['duration']
					wpStart = segs[i]['steps'][j]['way_points'][0]
					wpEnd = segs[i]['steps'][j]['way_points'][1]

					[tmpTimeSec, tmpDistMeters] = distributeTimeDist(path[wpStart:wpEnd+1], subpathTimeSec)
					if (len(timeInSeconds) == 0):
						timeInSeconds += tmpTimeSec
						distInMeters += tmpDistMeters
					else:
						timeInSeconds += tmpTimeSec[1:]
						distInMeters += tmpDistMeters[1:]
					
					if (requestExtras):
						if (wpStart == 0):
							extras[0]['wayname'] = segs[i]['steps'][j]['name']
						for k in range(wpStart+1, wpEnd+1):
							extras[k]['wayname'] = segs[i]['steps'][j]['name']	
			
			if (requestExtras):
				ex = data['features'][0]['properties']['extras']
				if ('waycategory' in ex):
					for [wpStart, wpEnd, val] in ex['waycategory']['values']:
						if (wpStart == 0):
							extras[0]['waycategory'] = bitFieldDecomp(val, orsWaycategoryDict)
						for i in range(wpStart+1, wpEnd+1):
							extras[i]['waycategory'] = bitFieldDecomp(val, orsWaycategoryDict)
	
				if ('surface' in ex):
					for [wpStart, wpEnd, val] in ex['surface']['values']:
						if (wpStart == 0):
							extras[0]['surface'] = orsSurfaceDict[val] if val in orsSurfaceDict else None
						for i in range(wpStart+1, wpEnd+1):
							extras[i]['surface'] = orsSurfaceDict[val] if val in orsSurfaceDict else None

				if ('waytypes' in ex):
					for [wpStart, wpEnd, val] in ex['waytypes']['values']:
						if (wpStart == 0):
							extras[0]['waytype'] = orsWaytypeDict[val] if val in orsWaytypeDict else None
						for i in range(wpStart+1, wpEnd+1):
							extras[i]['waytype'] = orsWaytypeDict[val] if val in orsWaytypeDict else None
				
				if ('steepness' in ex):
					for [wpStart, wpEnd, val] in ex['steepness']['values']:
						if (wpStart == 0):
							extras[0]['steepness'] = val
						for i in range(wpStart+1, wpEnd+1):
							extras[i]['steepness'] = val
	
				if ('tollways' in ex):
					for [wpStart, wpEnd, val] in ex['tollways']['values']:
						if (wpStart == 0):
							extras[0]['tollway'] = bool(val) if type(val) is bool else None
						for i in range(wpStart+1, wpEnd+1):
							extras[i]['tollway'] = bool(val) if type(val) is bool else None
			
			# Just for fun, let's print some other info we got (but didn't save):
			# print("ascent: {}".format(data['features'][0]['properties']['ascent']))
			# print("descent: {}".format(data['features'][0]['properties']['descent']))
			
			return [path, extras, timeInSeconds, distInMeters]
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return

	except:
		print("Error: ", sys.exc_info()[1])
		raise

def orsGetTimeDistAll2All(locs, travelMode='fastest', APIkey=None):
	"""
	A function to generate distance and time matrices between given coordinates.
	Parameters
	----------
	locs: list of lists, Required
		The format is [[lat1, lon1], [lat2, lon2], ...]. A list of coordinates.
	travelMode: string, {fastest, pedestrian, cycling, truck}
		ORS provides multiple types of routing.  VeRoViz implements the following: 'fastest' (for car), 'pedestrian', 'cycling', and 'truck'.
	APIkey: string, Required
		Enables access to ORS server.
	
	Returns
	-------
	time: dictionary
		A square matrix, which provides the traveling time between each pair of coordinates.  Units are in seconds.
	dist: dictionary
		A square matrix, which provides the distance between each pair of coordinates.  Units are in meters.
	"""

	"""
	The following "profile" options are available in ORS:
		'driving-car'		('fastest')	
		'driving-hgv'
		'cycling-regular'
		'cycling-road'
		'cycling-mountain'
		'cycling-electric'
		'foot-walking'
		'foot-hiking'
		'wheelchair'
		
		There is no "shortest" option    
	"""
	
	try:
		travelMode = travelMode.lower()
	except:
		pass

	if (travelMode == 'fastest'):
		profile = 'driving-car'
	elif (travelMode == 'shortest'):
		profile = 'driving-car'		# FIXME -- same as 'fastest'
	elif (travelMode == 'pedestrian'):
		profile = 'foot-walking'
	elif (travelMode == 'cycling'):
		profile = 'cycling-road'
	elif (travelMode == 'truck'):
		profile = 'driving-hgv'
	elif (travelMode == 'wheelchair'):
		profile = 'wheelchair'
	else:
		print("Error: Invalid travelMode.")
		return    
    
	maxBatchSize = 50   # 50 x 50
	numBatches = int(math.ceil(len(locs) / float(maxBatchSize)))

	all2AllUrl = ('https://api.openrouteservice.org/v2/matrix/%s' % (profile))

	headers = {
				'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
				'Authorization': APIkey,
				'Content-Type': 'application/json'}

	distMeters = {}
	timeSecs = {}

	try:
		for rowBatch in range(0, numBatches):
			sourceLocs = []
			sources = []

			# ORS uses [lon, lat] order:
			for i in range(maxBatchSize * rowBatch, min(len(locs), maxBatchSize * (rowBatch + 1))):
				sources.append(len(sourceLocs))
				sourceLocs.append([locs[i][1],locs[i][0]])

			for colBatch in range(0, numBatches):
				destinations = []
				locations = list(sourceLocs)
				if (colBatch == rowBatch):
					# We're on the diagonal. Sources and Destinations are the same (all-to-all).
					encoded_body = json.dumps({
						"locations": sourceLocs,
						"metrics": ["distance","duration"],
						"units": "m"})
				else:
					# We're off-diagonal.  Sources and Destinations differ.
					for i in range(maxBatchSize * colBatch, min(len(locs), maxBatchSize * (colBatch + 1))):
						destinations.append(len(locations))
						locations.append([locs[i][1],locs[i][0]])

					encoded_body = json.dumps({
						"locations": locations,
						"sources": sources,
						"destinations": destinations,
						"metrics": ["distance","duration"],
						"units": "m"})

				if (len(locations) <= 1):
					# We have a 1x1 matrix.  Nothing to do. 
					row = maxBatchSize * rowBatch
					col = maxBatchSize * colBatch
					distMeters[row, col] = 0.0
					timeSecs[row, col] = 0.0
				else:
					http = urllib3.PoolManager()
					response = http.request('POST', all2AllUrl, headers=headers, body=encoded_body)

					data = json.loads(response.data.decode('utf-8'))
					http_status = response.status

					if (http_status == 200):
						# OK
						row = maxBatchSize * rowBatch
						for i in range(0, len(data['durations'])):
							col = maxBatchSize * colBatch
							for j in range(0, len(data['durations'][i])):
								distMeters[row, col] = data['distances'][i][j]
								timeSecs[row, col] = data['durations'][i][j]
								col += 1
							row += 1    
					else:
						# Error of some kind
						http_status_description = responses[http_status]
						print("Error Code %s: %s" % (http_status, http_status_description))
						return

		return [timeSecs, distMeters]

	except:
		print("Error: ", sys.exc_info()[1])
		raise


def orsGetTimeDistOne2Many(fromLoc, toLocs, travelMode='fastest', APIkey=None):
	"""
	A function to generate distance and time matrices between given coordinates.
	Parameters
	----------
	fromLoc: list, Required
		One coordinate, in the format of [lat, lon].
	toLocs: list of lists, Required
		The format is [[lat1, lon1], [lat2, lon2], ...], a list of coordinates.
	travelMode: string, {fastest, pedestrian, cycling, truck}
		ORS provides multiple types of routing.  VeRoViz implements the following: 'fastest' (for car), 'pedestrian', 'cycling', and 'truck'.
	APIkey: string, Required
		Enables access to ORS server.
	
	Returns
	-------
	time: dictionary
		A 1-row matrix, which provides the travel time from a given location to numerous other locations. Units are in seconds.
	dist: dictionary
		A 1-row matrix, which provides the distance from a given location to numerous other locations. Units are in meters.
	"""

    
	"""
	The following "profile" options are available in ORS:
		'driving-car'		('fastest')	
		'driving-hgv'
		'cycling-regular'
		'cycling-road'
		'cycling-mountain'
		'cycling-electric'
		'foot-walking'
		'foot-hiking'
		'wheelchair'
		
		There is no "shortest" option    
	"""
	
	try:
		travelMode = travelMode.lower()
	except:
		pass

	if (travelMode == 'fastest'):
		profile = 'driving-car'
	elif (travelMode == 'shortest'):
		profile = 'driving-car'		# FIXME -- same as 'fastest'
	elif (travelMode == 'pedestrian'):
		profile = 'foot-walking'
	elif (travelMode == 'cycling'):
		profile = 'cycling-road'
	elif (travelMode == 'truck'):
		profile = 'driving-hgv'
	elif (travelMode == 'wheelchair'):
		profile = 'wheelchair'
	else:
		print("Error: Invalid travelMode.")
		return    
    
	one2ManyBatchSize = 2500 # < 2500 (50 x 50)
	numBatches = int(math.ceil(len(toLocs) / float(one2ManyBatchSize)))
	one2ManyUrlBase = ('https://api.openrouteservice.org/v2/matrix/%s' % (profile))

	headers = {
				'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
				'Authorization': APIkey,
				'Content-Type': 'application/json'}

	distMeters = {}
	timeSecs = {}

	try:
		for batch in range(0, numBatches):
			locations = []
			sources = []
			destinations = []
    
			# ORS uses [lon, lat] order:
			sources.append(0)
			locations.append([fromLoc[1], fromLoc[0]])
			for i in range(one2ManyBatchSize * batch, min(len(toLocs), one2ManyBatchSize * (batch + 1))):
				destinations.append(len(locations))
				locations.append([toLocs[i][1],toLocs[i][0]])
        
			encoded_body = json.dumps({
				"locations": locations,
				"sources": sources,
				"destinations": destinations,
				"metrics": ["distance","duration"],
				"units": "m"})

			http = urllib3.PoolManager()
			response = http.request('POST', one2ManyUrlBase, headers=headers, body=encoded_body)

			data = json.loads(response.data.decode('utf-8'))
			http_status = response.status

			if (http_status == 200):
				# OK
				col = one2ManyBatchSize * batch
				for i in range(0, len(data['durations'])):
					for j in range(0, len(data['durations'][i])):
						# print(data['distances'][i][j])
						# print(data['durations'][i][j])
						distMeters[0, col] = data['distances'][i][j]
						timeSecs[0, col] = data['durations'][i][j]
						col += 1
			else:
				# Error of some kind
				http_status_description = responses[http_status]
				print("Error Code %s: %s" % (http_status, http_status_description))
				return

		return [timeSecs, distMeters]
                    
	except:
		print("Error: ", sys.exc_info()[1])
		raise


def orsGetTimeDistMany2One(fromLocs, toLoc, travelMode='fastest', APIkey=None):
	"""
	A function to generate distance and time matrices from one set of locations to a single location.
	Parameters
	----------
	fromLocs: list of lists, Required
		The format is [[lat1, lon1], [lat2, lon2], ...], a list of coordinates.
	toLoc: list, Required
		One coordinate, in the format of [lat, lon].
	travelMode: string, {fastest, pedestrian, cycling, truck}
		ORS provides multiple types of routing.  VeRoViz implements the following: 'fastest' (for car), 'pedestrian', 'cycling', and 'truck'.
	APIkey: string, Required
		Enables access to ORS server.
	
	Returns
	-------
	time: dictionary
		A 1-column matrix, which provides the travel time from a given set of locations a single location. Units are in seconds.
	dist: dictionary
		A 1-column matrix, which provides the distance from a given set of locations to a single location. Units are in meters.
	"""

    
	"""
	The following "profile" options are available in ORS:
		'driving-car'		('fastest')	
		'driving-hgv'
		'cycling-regular'
		'cycling-road'
		'cycling-mountain'
		'cycling-electric'
		'foot-walking'
		'foot-hiking'
		'wheelchair'
		
		There is no "shortest" option    
	"""
	
	try:
		travelMode = travelMode.lower()
	except:
		pass

	if (travelMode == 'fastest'):
		profile = 'driving-car'
	elif (travelMode == 'shortest'):
		profile = 'driving-car'		# FIXME -- same as 'fastest'
	elif (travelMode == 'pedestrian'):
		profile = 'foot-walking'
	elif (travelMode == 'cycling'):
		profile = 'cycling-road'
	elif (travelMode == 'truck'):
		profile = 'driving-hgv'
	elif (travelMode == 'wheelchair'):
		profile = 'wheelchair'
	else:
		print("Error: Invalid travelMode.")
		return
    
    
	many2OneBatchSize = 2500 # < 2500 (50 x 50)
	numBatches = int(math.ceil(len(fromLocs) / float(many2OneBatchSize)))
	many2OneUrlBase = ('https://api.openrouteservice.org/v2/matrix/%s' % (profile))

	headers = {
				'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
				'Authorization': APIkey,
				'Content-Type': 'application/json'}

	distMeters = {}
	timeSecs = {}

	try:
		for batch in range(0, numBatches):
			locations = []
			sources = []
			destinations = []
    
			# ORS uses [lon, lat] order:
			for i in range(many2OneBatchSize * batch, min(len(fromLocs), many2OneBatchSize * (batch + 1))):
				sources.append(len(locations))
				locations.append([fromLocs[i][1],fromLocs[i][0]])
			destinations.append(len(locations))
			locations.append([toLoc[1],toLoc[0]])

			encoded_body = json.dumps({
				"locations": locations,
				"sources": sources,
				"destinations": destinations,
				"metrics": ["distance","duration"],
				"units": "m"})

			http = urllib3.PoolManager()
			response = http.request('POST', many2OneUrlBase, headers=headers, body=encoded_body)

			data = json.loads(response.data.decode('utf-8'))
			http_status = response.status

			if (http_status == 200):
				# OK
				row = many2OneBatchSize * batch
				for i in range(0, len(data['durations'])):
					for j in range(0, len(data['durations'][i])):
						# print(data['distances'][i][j])
						# print(data['durations'][i][j])
						distMeters[row, 0] = data['distances'][i][j]
						timeSecs[row, 0] = data['durations'][i][j]
						row += 1
			else:
				# Error of some kind
				http_status_description = responses[http_status]
				print("Error Code %s: %s" % (http_status, http_status_description))
				return

		return [timeSecs, distMeters]
                    
	except:
		print("Error: ", sys.exc_info()[1])
		raise


def orsGeocode(text, APIkey):
	"""
	Geocode from a text string using ORS
	
	Parameters
	----------
	text: string
		A text string describing an address, city, or landmark.
	APIkey: string
		Enables access to ORS server.
			    
	Returns
	-------
	loc: list
		A geocoded location in the format of [lat, lon].
	"""
    
	# ORS uses [lon, lat] order:
	geocodeUrl = ('https://api.openrouteservice.org/geocode/search?api_key=%s&text=%s&size=1' % (APIkey, text))
    
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', geocodeUrl)
		data = json.loads(response.data.decode('utf-8'))

		http_status = response.status

		if (http_status == 200):
			# OK
			# ORS uses [lon, lat] order:
			loc = [data['features'][0]['geometry']['coordinates'][1], 
				   data['features'][0]['geometry']['coordinates'][0]] 
			return loc
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return
	except:
		print("Error: ", sys.exc_info()[1])
		raise 
		
def orsReverseGeocode(loc, APIkey):
	"""
	Reverse Geocode from a [lat, lon] or [lat, lon, alt] location using ORS
	
	Parameters
	----------
	loc: list
		Of the form [lat, lon] or [lat, lon, alt].  If provided, altitude will be ignored.
	APIkey: string
		Enables access to ORS server.
	    
	Returns
	-------
	snapLoc: list
		Of the form [lat, lon].  This is the nearest point to the given (input) location.
	address: dictionary
		A dataProvider-specific dictionary containing address details.
	"""    
    
	# ORS uses [lon, lat] order:
	geocodeUrl = ('https://api.openrouteservice.org/geocode/reverse?api_key=%s&point.lon=%s&point.lat=%s&size=1' % (APIkey, loc[1], loc[0]))
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', geocodeUrl)
		data = json.loads(response.data.decode('utf-8'))

		http_status = response.status

		if (http_status == 200):
			# OK
			# ORS uses [lon, lat] order:
			snapLoc = [data['features'][0]['geometry']['coordinates'][1], 
				       data['features'][0]['geometry']['coordinates'][0]] 
			address = data['features'][0]['properties']
			return (snapLoc, address)
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return
	except:
		print("Error: ", sys.exc_info()[1])
		raise 



def orsIsochrones(loc, locType, travelMode, rangeType, rangeSize, interval, smoothing, APIkey):
	"""
	Finds isochrones to or from a given location. 

	Parameters
	----------
	loc: list
		A GPS coordinate of the form [lat, lon] or [lat, lon, alt].  If provided, altitude will be ignored (i.e., assumed to be 0).
	locType: string
		Specifies whether `location` is the start or the destination.  Valid options are 'start' or 'destination'
	travelMode: string
		Specifies the mode of travel.  Valid options are: 'driving-car', 'driving-hgv', 'cycling-regular', 'cycling-road', 'cycling-mountain', 'cycling-electric', 'foot-walking', 'foot-hiking', or 'wheelchair'.
	rangeType: string
		Indicates whether the isochrones are based on distance or time.  Valid options are 'distance' or 'time'.
	rangeSize: positive float
		The isochrones will indicate the area accessible from the given location within the rangeSize.  rangeSize is in units of [meters] if rangeType equals 'distance'; rangeSize is in units of [seconds] if rangeType equals 'time'.
	interval: float
		If provided, this parameter can be used to generate multiple concentric isochrones.  For example, if rangeSize = 90, and interval = 30, isochrones will be identified for ranges of 30, 60, and 90 units.  If interval is not provided (as is the default), only one isochrone will be determined.
	smoothing: float in range [0, 100]
		Indicates the granularity of the isochrones.  Smoothing values close to 0 will produce jagged isochrones; values close to 100 will generally result in smooth isochrones.		
	APIkey: string
		Enables access to ORS server.
	
	Returns
	-------
	dictionary with nested dictionaries and lists

	"""
		
	try:
		travelMode = travelMode.lower()
	except:
		pass

	try:
		locType = locType.lower()
	except:
		pass
	    
	isoUrl = ('https://api.openrouteservice.org/v2/isochrones/%s' % (travelMode))

	headers = {
				'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
				'Authorization': APIkey,
				'Content-Type': 'application/json'}

	try:

		# ORS uses [lon, lat] order:
		locations  = [[loc[1], loc[0]]]
		attributes = ['area', 'reachfactor', 'total_pop']
		units      = 'm'	# only applicable if rangeType == 'distance'
		areaUnits  = 'm'
		if (rangeType == 'time'):
			valueUnits = 'seconds'
		else:
			valueUnits = 'meters'
		
		encoded_body = json.dumps({
			"locations": locations,
			"location_type": locType,
			"attributes": attributes,
			"range": [rangeSize],
			"interval": interval,
			"range_type": rangeType,
			"smoothing": smoothing,
			"area_units": areaUnits,
			"units": units})

		http = urllib3.PoolManager()
		response = http.request('POST', isoUrl, headers=headers, body=encoded_body)

		data = json.loads(response.data.decode('utf-8'))
		http_status = response.status

		if (http_status == 200):
			# OK	
			iso = {}

			iso['location'] = loc

			# Build boundingRegion, from [wLon, sLat, eLon, nLat]
			# Ex:  [8.685772, 49.417915, 8.689263, 49.421278]
			[wLon, sLat, eLon, nLat] = data['bbox']
			iso['boundingRegion'] = [[sLat, wLon], [nLat, wLon], [nLat, eLon], [sLat, eLon], [sLat, wLon]]

			iso['isochrones'] = []

			for i in range(0, len(data['features'])):
				if ('value' in data['features'][i]['properties']):
					value = data['features'][i]['properties']['value']
				else:
					value = None
				if ('area' in data['features'][i]['properties']):
					area = data['features'][i]['properties']['area']
				else:
					area = None
				if ('total_pop' in data['features'][i]['properties']):
					pop = data['features'][i]['properties']['total_pop']
				else:
					pop = None
				if ('reachfactor' in data['features'][i]['properties']):
					reachfactor = data['features'][i]['properties']['reachfactor']
				else:
					reachfactor = None
					
				iso['isochrones'].append({
					'value'      : value,
					'valueUnits' : valueUnits,
					'area'       : area,
					'pop'        : pop,
					'reachfactor': reachfactor,
					'poly'       : []
					})
	
				for j in range(0, len(data['features'][i]['geometry']['coordinates'])):
					tmp = []
					for k in range(0, len(data['features'][i]['geometry']['coordinates'][j])):
						tmp.append([
							data['features'][i]['geometry']['coordinates'][j][k][1], 
							data['features'][i]['geometry']['coordinates'][j][k][0] ])
			
					iso['isochrones'][i]['poly'].append(tmp)            
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return

		return iso

	except:
		print("Error: ", sys.exc_info()[1])
		raise


def orsGetElevation(locs, APIkey):
	"""
	EXPERIMENTAL.  Finds the elevation, in units of meters above mean sea level (MSL), for a given location or list of locations.  

	Parameters
	----------
	locs: list of lists, Required, default as None
		A list of one or more GPS coordinate of the form [[lat, lon], ...] or [[lat, lon, alt], ...].  If altitude is included in locs, the function will add the elevation to the input altitude.  Otherwise, the input altitude will be assumed to be 0.
	APIkey: string
		Enables access to ORS server.
	
	Return
	------
	list of lists, of the form [[lat, lon, altMSL], [lat, lon, altMSL], ..., [lat, lon, altMSL]].
	"""
		
	if (len(locs) == 1):
		dataType = 'point'
		elevUrl = ('https://api.openrouteservice.org/elevation/point')
		geometry = [locs[0][1], locs[0][0]]   # ORS uses [lon, lat] order:

		encoded_body = json.dumps({
			"format_in": "point",
			"format_out": "point",
			"geometry": geometry})		
	else:
		dataType = 'line'
		elevUrl = ('https://api.openrouteservice.org/elevation/line')
		geometry = []
		for i in range(0, len(locs)):
			geometry.append([locs[i][1], locs[i][0]])

		encoded_body = json.dumps({
			"format_in": "polyline",
			"format_out": "polyline",
			"geometry": geometry})
	
	headers = {
				'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
				'Authorization': APIkey,
				'Content-Type': 'application/json; charset=utf-8'}

	try:
		
		http = urllib3.PoolManager()
		response = http.request('POST', elevUrl, headers=headers, body=encoded_body)

		data = json.loads(response.data.decode('utf-8'))
		http_status = response.status

		locsWithAlt = []
		
		if (http_status == 200):
			# OK
			if (dataType == 'point'):
				# data['geometry'][]
				if (len(locs[0]) == 2):
					alt = data['geometry'][2]
				else:
					alt = locs[0][2] + data['geometry'][2]
				locsWithAlt.append([ data['geometry'][1], data['geometry'][0], alt ])
			else:
				# data['geometry'][[],[],...]
				for i in range(0, len(data['geometry'])):
					if (len(locs[i]) == 2):
						alt = data['geometry'][i][2]
					else:
						alt = locs[i][2] + data['geometry'][i][2]
					locsWithAlt.append([ data['geometry'][i][1], data['geometry'][i][0], alt ])
			
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return

		return locsWithAlt

	except:
		print("Error: ", sys.exc_info()[1])
		raise
		