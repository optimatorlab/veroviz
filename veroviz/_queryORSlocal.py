from veroviz._common import *
from veroviz._internal import distributeTimeDist
from veroviz._internal import loc2Dict
from veroviz._internal import locs2Dict, bitFieldDecomp


def orsLocalGetSnapToRoadLatLon(loc, port):
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
    
	# ORS uses [lon, lat] order:
	snapToRoadUrl = ('http://localhost:%s/ors/directions?profile=driving-car&geometry_format=geojson&coordinates=%s,%s|%s,%s&elevation=false' % (port, dicLoc['lon'], dicLoc['lat'], dicLoc['lon'], dicLoc['lat']))
 
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', snapToRoadUrl)
		data = json.loads(response.data.decode('utf-8'))

		http_status = response.status

		if (http_status == 200):
			# OK
			# ORS uses [lon, lat] order:
			snapLoc = [data['routes'][0]['geometry']['coordinates'][0][1], 
					   data['routes'][0]['geometry']['coordinates'][0][0]] 
            
			return snapLoc
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return
	except:
		print("Error: ", sys.exc_info()[1])
		raise 


def orsLocalGetShapepointsTimeDist(startLoc, endLoc, travelMode='fastest', port=8081, requestExtras=True):
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
	"""

	units      = 'm'
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
	# elif (travelMode == 'wheelchair'):
	#	profile = 'wheelchair'
	else:
		print("Error: Invalid travelMode.")
		return    
    
	spUrl  = ('http://localhost:%s/ors/directions?profile=%s' % (port, profile))
	spUrl += '&coordinates=%s,%s|%s,%s' % (dicStartLoc['lon'],dicStartLoc['lat'], dicEndLoc['lon'],dicEndLoc['lat'])
	spUrl += '&geometry_format=geojson'
	if (requestExtras):
		spUrl += '&extra_info=steepness|surface|waycategory|waytype|tollways'
		elevation = "true"
	else:
		elevation = "false"
	spUrl += '&elevation=%s' % (elevation)
	spUrl += '&radiuses=-1|-1'
	spUrl += '&units=m'
	spUrl += '&instructions=true'
	spUrl += '&preference=%s' % (preference)
		
	try:

		http = urllib3.PoolManager()
		response = http.request('GET', spUrl)

		data = json.loads(response.data.decode('utf-8'))
		http_status = response.status

		if (http_status == 200):
			# OK
			# ORS uses [lon, lat] order:
			path = []
			extras = {}
			timeInSeconds = []
			distInMeters = []
			for i in range(len(data['routes'][0]['geometry']['coordinates'])):
				path.append([data['routes'][0]['geometry']['coordinates'][i][1], 
							 data['routes'][0]['geometry']['coordinates'][i][0]])
				if (requestExtras):
					extras[i] = {}
					if (len(data['routes'][0]['geometry']['coordinates'][i]) >= 2):
						extras[i]['elev'] = data['routes'][0]['geometry']['coordinates'][i][2]
					else:
						extras[i]['elev'] = None

			segs = data['routes'][0]['segments']
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
				ex = data['routes'][0]['extras']
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

def orsLocalGetTimeDistAll2All(locs, travelMode='fastest', port=8081):
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
	# elif (travelMode == 'wheelchair'):
	# 	profile = 'wheelchair'
	else:
		print("Error: Invalid travelMode.")
		return    
    
	maxBatchSize = 50   # 50 x 50
	numBatches = int(math.ceil(len(locs) / float(maxBatchSize)))

	all2AllUrlBase  = ('http://localhost:%s/ors/matrix?profile=%s' % (port, profile))
	all2AllUrlBase += '&metrics=distance|duration'
	all2AllUrlBase += '&units=m'

	distMeters = {}
	timeSecs = {}

	try:
		for rowBatch in range(0, numBatches):
			sourceLocs = []
			sources = []
			sourceLocsFlat = []

			# ORS uses [lon, lat] order:
			sourceLocsFlat = []
			for i in range(maxBatchSize * rowBatch, min(len(locs), maxBatchSize * (rowBatch + 1))):
				sources.append(len(sourceLocs))
				sourceLocs.append([locs[i][1],locs[i][0]])
				sourceLocsFlat.append('%s,%s' % (locs[i][1], locs[i][0]))

			for colBatch in range(0, numBatches):
				destinations = []
				locations = list(sourceLocs)
				if (colBatch == rowBatch):
					# We're on the diagonal. Sources and Destinations are the same (all-to-all).
					all2AllUrl  = all2AllUrlBase
					all2AllUrl += '&locations=%s' % ('|'.join(sourceLocsFlat)) 
					
				else:
					# We're off-diagonal.  Sources and Destinations differ.
					for i in range(maxBatchSize * colBatch, min(len(locs), maxBatchSize * (colBatch + 1))):
						destinations.append(len(locations))
						locations.append([locs[i][1],locs[i][0]])

					locationsFlat = []
					for i in locations:
						locationsFlat.append('%s,%s' % (i[0],i[1]))
					sourcesFlat = []
					for i in sources:
						sourcesFlat.append('%s' % i)
					destinationsFlat = []
					for i in destinations:
						destinationsFlat.append('%s' % i)

					all2AllUrl  = all2AllUrlBase
					all2AllUrl += '&locations=%s' % ('|'.join(locationsFlat)) 
					all2AllUrl += '&sources=%s' % ('|'.join(sourcesFlat)) 
					all2AllUrl += '&destinations=%s' % ('|'.join(destinationsFlat)) 

				if (len(locations) <= 1):
					# We have a 1x1 matrix.  Nothing to do. 
					row = maxBatchSize * rowBatch
					col = maxBatchSize * colBatch
					distMeters[row, col] = 0.0
					timeSecs[row, col] = 0.0
				else:
					http = urllib3.PoolManager()
					response = http.request('GET', all2AllUrl)

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


def orsLocalGetTimeDistOne2Many(fromLoc, toLocs, travelMode='fastest', port=8081):
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
	# elif (travelMode == 'wheelchair'):
	# 	profile = 'wheelchair'
	else:
		print("Error: Invalid travelMode.")
		return    
    
	one2ManyBatchSize = 2500 # < 2500 (50 x 50)
	numBatches = int(math.ceil(len(toLocs) / float(one2ManyBatchSize)))
	one2ManyUrlBase  = ('http://localhost:%s/ors/matrix/?profile=%s' % (port, profile))
	one2ManyUrlBase += '&metrics=distance|duration'
	one2ManyUrlBase += '&units=m'

	distMeters = {}
	timeSecs = {}

	try:
		for batch in range(0, numBatches):
			locations = []
			sources = []
			destinations = []
    
			# ORS uses [lon, lat] order:
			sources.append('0')
			locations.append('%s,%s' % (fromLoc[1], fromLoc[0]))
			for i in range(one2ManyBatchSize * batch, min(len(toLocs), one2ManyBatchSize * (batch + 1))):
				destinations.append(str(len(locations)))
				locations.append('%s,%s' % (toLocs[i][1],toLocs[i][0]))
        
			one2ManyUrl  = one2ManyUrlBase
			one2ManyUrl += '&locations=%s' % ('|'.join(locations))
			one2ManyUrl += '&sources=%s' % ('|'.join(sources))
			one2ManyUrl += '&destinations=%s' % ('|'.join(destinations))
									
			http = urllib3.PoolManager()
			response = http.request('GET', one2ManyUrl)

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


def orsLocalGetTimeDistMany2One(fromLocs, toLoc, travelMode='fastest', port=8081):
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
	# elif (travelMode == 'wheelchair'):
	#	profile = 'wheelchair'
	else:
		print("Error: Invalid travelMode.")
		return
    
    
	many2OneBatchSize = 2500 # < 2500 (50 x 50)
	numBatches = int(math.ceil(len(fromLocs) / float(many2OneBatchSize)))
	many2OneUrlBase  = ('https://localhost:%s/ors/matrix/?profile=%s' % (port, profile))
	many2OneUrlBase += '&metrics=distance|duration'
	many2OneUrlBase += '&units=m'

	distMeters = {}
	timeSecs = {}

	try:
		for batch in range(0, numBatches):
			locations = []
			sources = []
			destinations = []
    
			# ORS uses [lon, lat] order:
			for i in range(many2OneBatchSize * batch, min(len(fromLocs), many2OneBatchSize * (batch + 1))):
				sources.append(str(len(locations)))
				locations.append('%s,%s' % (fromLocs[i][1],fromLocs[i][0]))
			destinations.append(str(len(locations)))
			locations.append('%s,%s' % (toLoc[1],toLoc[0]))

			many2OneUrl  = many2OneBase
			many2OneUrl += '&locations=%s' % ('|'.join(locations))
			many2OneUrl += '&sources=%s' % ('|'.join(sources))
			many2OneUrl += '&destinations=%s' % ('|'.join(destinations))

			http = urllib3.PoolManager()
			response = http.request('GET', many2OneUrl)

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





def orsLocalIsochrones(loc, locType, travelMode, rangeType, rangeSize, interval, smoothing, port):
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
	    

	units      = 'm'	# only applicable if rangeType == 'distance'
	areaUnits  = 'm'
	if (rangeType == 'time'):
		valueUnits = 'seconds'
	else:
		valueUnits = 'meters'

	isoUrl  = 'http://localhost:%s/ors/isochrones/?profile=%s' % (port, travelMode)
	isoUrl += '&locations=%s,%s' % (loc[1], loc[0])	# lon/lat order
	isoUrl += '&location_type=%s' % (locType)
	isoUrl += '&attributes=%s|%s' % ('area', 'reachfactor')	# total_pop broken?
	isoUrl += '&range=%s' % (rangeSize)
	isoUrl += '&interval=%s' % (interval)
	isoUrl += '&range_type=%s' % (rangeType)
	isoUrl += '&smoothing=%s' % (smoothing)
	isoUrl += '&area_units=%s' % (areaUnits)
	isoUrl += '&units=%s' % (units)
	
	try:
	
		http = urllib3.PoolManager()
		response = http.request('GET', isoUrl)
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


# def orsLocalGeocode(text, APIkey):
		
# def orsLocalReverseGeocode(loc, APIkey):

# def orsLocalGetElevation(locs, APIkey):
		