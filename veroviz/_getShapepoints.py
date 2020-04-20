from veroviz._common import *

from veroviz._queryPgRouting import pgrGetShapepointsTimeDist
from veroviz._queryMapQuest import mqGetShapepointsTimeDist
from veroviz._queryOSRM import osrmGetShapepointsTimeDist
from veroviz._queryORS import orsGetShapepointsTimeDist

from veroviz._internal import distributeTimeDist
from veroviz._internal import locs2Dict
from veroviz._internal import loc2Dict
from veroviz._internal import replaceBackslashToSlash, addHeadSlash
from veroviz._internal import stripCesiumColor

from veroviz._buildFlightProfile import buildNoLoiteringFlight
from veroviz._buildFlightProfile import getTimeDistFromFlight
from veroviz._buildFlightProfile import addLoiterTimeToFlight

from veroviz._geometry import geoDistance2D

from veroviz.utilities import convertDistance
from veroviz.utilities import initDataframe

def privGetShapepoints2D(odID=1, objectID=None, modelFile=None, startLoc=None, endLoc=None, startTimeSec=0.0, expDurationSec=None, routeType='euclidean2D', speedMPS=None, leafletColor=VRV_DEFAULT_LEAFLETARCCOLOR, leafletWeight=VRV_DEFAULT_LEAFLETARCWEIGHT, leafletStyle=VRV_DEFAULT_LEAFLETARCSTYLE, leafletOpacity=VRV_DEFAULT_LEAFLETARCOPACITY, useArrows=True, modelScale=VRV_DEFAULT_CESIUMMODELSCALE, modelMinPxSize=VRV_DEFAULT_CESIUMMODELMINPXSIZE, cesiumColor=VRV_DEFAULT_CESIUMPATHCOLOR, cesiumWeight=VRV_DEFAULT_CESIUMPATHWEIGHT, cesiumStyle=VRV_DEFAULT_CESIUMPATHSTYLE, cesiumOpacity=VRV_DEFAULT_CESIUMPATHOPACITY, ganttColor=VRV_DEFAULT_GANTTCOLOR, popupText=None, dataProvider=None, dataProviderArgs=None):

	# Replace backslash
	modelFile = replaceBackslashToSlash(modelFile)

	# Ensure leading slash
	modelFile = addHeadSlash(modelFile)

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	try:
		routeType = routeType.lower()
	except:
		pass
			
	if (startLoc != endLoc):
		extras = {}
		if (routeType == 'euclidean2d'):
			[path, time, dist] = _eucGetShapepointsTimeDist(startLoc, endLoc, speedMPS, expDurationSec)
		elif (routeType == 'manhattan'):
			[path, time, dist] = _manGetShapepointsTimeDist(startLoc, endLoc, speedMPS, expDurationSec)
		elif (routeType == 'fastest' and dataProviderDictionary[dataProvider] == 'pgrouting'):
			databaseName = dataProviderArgs['databaseName']
			[path, time, dist] = pgrGetShapepointsTimeDist(startLoc, endLoc, databaseName)
		elif (routeType == 'fastest' and dataProviderDictionary[dataProvider] == 'osrm-online'):
			[path, time, dist] = osrmGetShapepointsTimeDist(startLoc, endLoc)
		elif (routeType in ['fastest', 'shortest', 'pedestrian'] and dataProviderDictionary[dataProvider] == 'mapquest'):
			APIkey = dataProviderArgs['APIkey']
			[path, time, dist] = mqGetShapepointsTimeDist(startLoc, endLoc, routeType, APIkey)
		elif (routeType in ['fastest', 'pedestrian', 'cycling', 'truck'] and dataProviderDictionary[dataProvider] == 'ors-online'):
			APIkey = dataProviderArgs['APIkey']
			if ('requestExtras' in dataProviderArgs.keys()):
				requestExtras = dataProviderArgs['requestExtras']
			else:
				requestExtras = True
			[path, extras, time, dist] = orsGetShapepointsTimeDist(startLoc, endLoc, routeType, APIkey, requestExtras)
		else:
			return

		# Check if the original point is too far away from the actual start point of the shapepoints from query
		distOri = geoDistance2D(startLoc, path[0])
		if (distOri >= VRV_DEFAULT_DISTANCE_ERROR_TOLERANCE): # Go back to 10m after testing
			print("Message: The origin point (lat: %s, lon: %s) is %.1f meters away from the road. You might find a gap between the origin point and the route." % (startLoc[0], startLoc[1], distOri))

		# Check if the actual end point is too far away from destination point
		distDes = geoDistance2D(path[-1], endLoc)
		if (distDes >= VRV_DEFAULT_DISTANCE_ERROR_TOLERANCE): # Go back to 10m after testing
			print("Message: The destination point (lat: %s, lon: %s) is %.1f meters away from the road. You might find a gap between destination point and the route." % (endLoc[0], endLoc[1], distDes))

		# convert distance to accumulated distance
		accDist = []
		accDist.append(0)
		for i in range(1, len(dist)):
			accDist.append(accDist[i - 1] + dist[i])

		# If `expDurationSec` is provided, override `speedMPS` and datasource, otherwise, if `speedMPS` is provided, override datasource
		if (expDurationSec != None):
			[newTime, newDist] = distributeTimeDist(path, expDurationSec)
			time = newTime
			dist = newDist
		elif (speedMPS != None and expDurationSec == None):
			newExpDurationSec = accDist[len(accDist) - 1] / speedMPS
			[newTime, newDist] = distributeTimeDist(path, newExpDurationSec)
			time = newTime
			dist = newDist

		# convert time to accumulated time
		accTime = []
		accTime.append(startTimeSec)
		for i in range(1, len(dist)):
			accTime.append(accTime[i - 1] + time[i])

		# For maintainability, convert locs into dictionary
		dicPath = locs2Dict(path)

		# shapepoint dataframe
		assignments = initDataframe('Assignments')

		# generate assignments
		for i in range(1, len(path)):
			startElev   = extras[i-1]['elev'] if (i-1) in extras else None
			endElev     = extras[i]['elev'] if i in extras else None
			wayname     = extras[i]['wayname'] if (i-1) in extras else None
			
			waycategory = extras[i]['waycategory'] if (i-1) in extras else None
			surface     = extras[i]['surface'] if (i-1) in extras else None
			waytype     = extras[i]['waytype'] if (i-1) in extras else None
			steepness   = extras[i]['steepness'] if (i-1) in extras else None
			tollway     = extras[i]['tollway'] if (i-1) in extras else None
			
			assignments = assignments.append({
				'odID' : odID,
				'objectID' : objectID, 
				'modelFile' : modelFile,
				'startTimeSec' : accTime[i - 1],
				'startLat' : dicPath[i - 1]['lat'],
				'startLon' : dicPath[i - 1]['lon'],
				'startAltMeters' : dicPath[i - 1]['alt'],
				'endTimeSec' : accTime[i],
				'endLat' : dicPath[i]['lat'],
				'endLon' : dicPath[i]['lon'],
				'endAltMeters' : dicPath[i]['alt'],
				'leafletColor' : leafletColor,
				'leafletWeight' : leafletWeight,
				'leafletStyle' : leafletStyle,
				'useArrows' : useArrows,
				'leafletOpacity' : leafletOpacity,
				'modelScale' : modelScale,
				'modelMinPxSize' : modelMinPxSize,
				'cesiumColor' : stripCesiumColor(cesiumColor),
				'cesiumWeight' : cesiumWeight,
				'cesiumStyle' : cesiumStyle,
				'cesiumOpacity' : cesiumOpacity,
				'ganttColor' : ganttColor, 
				'popupText' : popupText,
				'startElevMeters' : startElev,
				'endElevMeters' : endElev,
				'wayname' : wayname,
				'waycategory' : waycategory,
				'surface' : surface,
				'waytype' : waytype, 
				'steepness' : steepness,
				'tollway' : tollway
				}, ignore_index=True)
	else:
		# For maintainability, convert locs into dictionary
		dicStartLoc = loc2Dict(startLoc)

		if (dataProviderDictionary[dataProvider] == 'ors-online'):
			[[lat, lon, elev]] = orsGetElevation([startLoc], dataProviderArgs['APIkey'])
		else:
			elev = None
			
		assignments = initDataframe('Assignments')
		assignments = assignments.append({
			'odID' : odID,
			'objectID' : objectID, 
			'modelFile' : modelFile,
			'startTimeSec' : startTimeSec,
			'startLat' : dicStartLoc['lat'],
			'startLon' : dicStartLoc['lon'],
			'startAltMeters' : dicStartLoc['alt'],
			'endTimeSec' : expDurationSec + startTimeSec if (expDurationSec is not None) else startTimeSec,
			'endLat' : dicStartLoc['lat'],
			'endLon' : dicStartLoc['lon'],
			'endAltMeters' : dicStartLoc['alt'],
			'leafletColor' : leafletColor,
			'leafletWeight' : leafletWeight,
			'leafletStyle' : leafletStyle,
			'useArrows' : useArrows,
			'leafletOpacity' : leafletOpacity,
			'modelScale' : modelScale,
			'modelMinPxSize' : modelMinPxSize,
			'cesiumColor' : stripCesiumColor(cesiumColor),
			'cesiumWeight' : cesiumWeight,
			'cesiumStyle' : cesiumStyle,
			'cesiumOpacity' : cesiumOpacity,
			'ganttColor' : ganttColor, 
			'popupText' : popupText,
			'startElevMeters' : elev,
			'endElevMeters' : elev,
			'wayname' : None,
			'waycategory' : None,
			'surface' : None,
			'waytype' : None, 
			'steepness' : None,
			'tollway' : None
			}, ignore_index=True)

	return assignments


def privGetShapepoints3D(odID=1, objectID=None, modelFile=None, startTimeSec=0.0, startLoc=None, endLoc=None, takeoffSpeedMPS=None, cruiseSpeedMPS=None, landSpeedMPS=None, cruiseAltMetersAGL=None, routeType='square', climbRateMPS=None, descentRateMPS=None, earliestLandTime=-1, loiterPosition='arrivalAtAlt', leafletColor=VRV_DEFAULT_LEAFLETARCCOLOR, leafletWeight=VRV_DEFAULT_LEAFLETARCWEIGHT, leafletStyle=VRV_DEFAULT_LEAFLETARCSTYLE, leafletOpacity=VRV_DEFAULT_LEAFLETARCOPACITY, useArrows=True, modelScale=VRV_DEFAULT_CESIUMMODELSCALE, modelMinPxSize=VRV_DEFAULT_CESIUMMODELMINPXSIZE, cesiumColor=VRV_DEFAULT_CESIUMPATHCOLOR, cesiumWeight=VRV_DEFAULT_CESIUMPATHWEIGHT, cesiumStyle=VRV_DEFAULT_CESIUMPATHSTYLE, cesiumOpacity=VRV_DEFAULT_CESIUMPATHOPACITY, ganttColor=VRV_DEFAULT_GANTTCOLOR, popupText=None):

	# Replace backslash
	modelFile = replaceBackslashToSlash(modelFile)
	
	# Ensure leading slash
	modelFile = addHeadSlash(modelFile)

	# Generate flight profile without loitering
	flight = buildNoLoiteringFlight(routeType, startLoc, cruiseAltMetersAGL, endLoc, takeoffSpeedMPS, climbRateMPS, cruiseSpeedMPS, landSpeedMPS, descentRateMPS)

	# Calculate loiter time
	[totalTime, groundDistance, flightDistance] = getTimeDistFromFlight(flight)
	remainLoiterTime = 0
	if (earliestLandTime - startTimeSec > totalTime):
		remainLoiterTime = earliestLandTime - startTimeSec - totalTime
	else:
		remainLoiterTime = 0

	# Add loiter given loiter position
	flight = addLoiterTimeToFlight(
		flight=flight,
		loiterPosition=loiterPosition, 
		loiterTime=remainLoiterTime)

	# Build assignments dataframe
	assignments = initDataframe('assignments')
	for i in range(1, len(flight)):
		# For all segments in flight profile, loitering happens AFTER arrival at that position
		assignments = assignments.append({
			'odID': odID,
			'objectID': objectID,
			'modelFile': modelFile,
			'startTimeSec': startTimeSec + flight.iloc[i - 1]['pathEndTimeSec'],
			'startLat': flight.iloc[i - 1]['lat'],
			'startLon': flight.iloc[i - 1]['lon'],
			'startAltMeters': flight.iloc[i - 1]['altAGL'],
			'endTimeSec': startTimeSec + flight.iloc[i]['pathStartTimeSec'],
			'endLat': flight.iloc[i]['lat'],
			'endLon': flight.iloc[i]['lon'],
			'endAltMeters': flight.iloc[i]['altAGL'],
			'leafletColor': leafletColor,
			'leafletWeight': leafletWeight,
			'leafletStyle': leafletStyle,
			'leafletOpacity': leafletOpacity,
			'useArrows': useArrows,
			'modelScale' : modelScale,
			'modelMinPxSize' : modelMinPxSize,
			'cesiumColor': stripCesiumColor(cesiumColor),
			'cesiumWeight': cesiumWeight,
			'cesiumStyle': cesiumStyle,
			'cesiumOpacity': cesiumOpacity,
			'ganttColor': ganttColorFly, 
			'popupText': popupText,
			'startElevMeters' : None,
			'endElevMeters' : None,
			'wayname' : None,
			'waycategory' : None,
			'surface' : None,
			'waytype' : None, 
			'steepness' : None,
			'tollway' : None
			}, ignore_index=True)

		# If they need loitering, add the line of loitering
		if (flight.iloc[i]['loiterTime'] != 0):
			assignments = assignments.append({
				'odID': odID,
				'objectID': objectID,
				'modelFile': modelFile,
				'startTimeSec': startTimeSec + flight.iloc[i]['pathStartTimeSec'],
				'startLat': flight.iloc[i]['lat'],
				'startLon': flight.iloc[i]['lon'],
				'startAltMeters': flight.iloc[i]['altAGL'],
				'endTimeSec': startTimeSec + flight.iloc[i]['pathEndTimeSec'],
				'endLat': flight.iloc[i]['lat'],
				'endLon': flight.iloc[i]['lon'],
				'endAltMeters': flight.iloc[i]['altAGL'],
				'leafletColor': leafletColor,
				'leafletWeight': leafletWeight,
				'leafletStyle': leafletStyle,
				'leafletOpacity': leafletOpacity,
				'useArrows': useArrows,
				'modelScale' : modelScale,
				'modelMinPxSize' : modelMinPxSize,
				'cesiumColor': stripCesiumColor(cesiumColor),
				'cesiumWeight': cesiumWeight,
				'cesiumStyle': cesiumStyle,
				'cesiumOpacity': cesiumOpacity,
				'ganttColor': ganttColorLoiter, 
				'popupText': popupText,
				'startElevMeters' : None,
				'endElevMeters' : None,
				'wayname' : None,
				'waycategory' : None,
				'surface' : None,
				'waytype' : None, 
				'steepness' : None,
				'tollway' : None
				}, ignore_index=True)

	return assignments


def _eucGetShapepointsTimeDist(startLoc, endLoc, speedMPS, expDurationSec):
	path = [startLoc, endLoc]
	dist = [0, geoDistance2D(startLoc, endLoc)]
	if (expDurationSec != None):
		time = [0, expDurationSec]
	else:
		time = [0, dist[1] / speedMPS]	
	return [path, time, dist]


def _manGetShapepointsTimeDist(startLoc, endLoc, speedMPS, expDurationSec, verticalFirst=True):
	# if verticalFirst is true, it means go north/south firt then go east/west
	if verticalFirst:
		path = [startLoc, [endLoc[0], startLoc[1]], endLoc]
		dist = [0, geoDistance2D(startLoc, [endLoc[0], startLoc[1]]), geoDistance2D([endLoc[0], startLoc[1]], endLoc)]
	else:
		path = [startLoc, [startLoc[0], endLoc[1]], endLoc]
		dist = [0, geoDistance2D(startLoc, [startLoc[0], endLoc[1]]), geoDistance2D([startLoc[0], endLoc[1]], endLoc)]

	if (expDurationSec != None):
		time = [0, expDurationSec * dist[1] / (dist[1] + dist[2]), expDurationSec * dist[2] / (dist[1] + dist[2])]
	else:
		time = [0, dist[1] / speedMPS, dist[2] / speedMPS]

	return [path, time, dist]
