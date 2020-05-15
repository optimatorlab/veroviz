from veroviz._common import *

from veroviz._utilities import privConvertDistance
from veroviz._utilities import privConvertTime

from veroviz._geometry import geoDistance2D
from veroviz._internal import locs2Dict
from veroviz._internal import loc2Dict

from veroviz._queryPgRouting import pgrGetTimeDist
from veroviz._queryORS import orsGetTimeDistAll2All
from veroviz._queryORS import orsGetTimeDistMany2One
from veroviz._queryORS import orsGetTimeDistOne2Many
from veroviz._queryORSlocal import orsLocalGetTimeDistAll2All
from veroviz._queryORSlocal import orsLocalGetTimeDistMany2One
from veroviz._queryORSlocal import orsLocalGetTimeDistOne2Many
from veroviz._queryOSRM import osrmGetTimeDist
from veroviz._queryMapQuest import mqGetTimeDistAll2All
from veroviz._queryMapQuest import mqGetTimeDistMany2One
from veroviz._queryMapQuest import mqGetTimeDistOne2Many

def getTimeDistFromLocs2D(fromLocs=None, fromRows=None, toLocs=None, toCols=None, outputDistUnits='meters', outputTimeUnits='seconds', routeType='euclidean2d', speedMPS=None, dataProvider=None, dataProviderArgs=None):

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	try:
		routeType = routeType.lower()
	except:
		pass

	# Do queries to find DICTIONARIES of distance and time matrices
	distMeters = {}
	timeSecs = {}
	if (routeType == 'euclidean2d'):
		[timeSecs, distMeters] = _getTimeDistEuclidean2D(fromLocs, toLocs, speedMPS)
	elif (routeType == 'manhattan'):
		[timeSecs, distMeters] = _getTimeDistManhattan(fromLocs, toLocs, speedMPS)
	elif (routeType == 'fastest' and dataProviderDictionary[dataProvider] == 'pgrouting'):
		databaseName = dataProviderArgs['databaseName']
		[timeSecs, distMeters] = _getTimeDistPgRouting(fromLocs, toLocs, databaseName, speedMPS)
	elif (routeType == 'fastest' and dataProviderDictionary[dataProvider] == 'osrm-online'):
		[timeSecs, distMeters] = _getTimeDistOSRM(fromLocs, toLocs, speedMPS)
	elif (routeType in ['fastest', 'shortest', 'pedestrian'] and dataProviderDictionary[dataProvider] == 'mapquest'):
		APIkey = dataProviderArgs['APIkey']
		[timeSecs, distMeters] = _getTimeDistMapQuest(fromLocs, toLocs, routeType, APIkey, speedMPS)
	elif (routeType in ['fastest', 'pedestrian', 'cycling', 'truck', 'wheelchair'] and dataProviderDictionary[dataProvider] == 'ors-online'):
		APIkey = dataProviderArgs['APIkey']
		[timeSecs, distMeters] = _getTimeDistORS(fromLocs, toLocs, routeType, APIkey, speedMPS)
	elif (routeType in ['fastest', 'pedestrian', 'cycling', 'truck'] and dataProviderDictionary[dataProvider] == 'ors-local'):
		port = dataProviderArgs['port']
		[timeSecs, distMeters] = _getTimeDistORSlocal(fromLocs, toLocs, routeType, port, speedMPS)
	else:
		return

	# Rename the keyvalues by fromRows and toCols and reset output units
	dist = {}
	time = {}
	for i in range(len(fromRows)):
		for j in range(len(toCols)):
			dist[fromRows[i], toCols[j]] = distMeters[i, j] * privConvertDistance(1.0, 'm', outputDistUnits)
			time[fromRows[i], toCols[j]] = timeSecs[i, j] * privConvertTime(1.0, 's', outputTimeUnits)

	return [time, dist]

def _getTimeDistEuclidean2D(fromLocs, toLocs, speedMPS):
	"""
	Generate two dictionaries, one for time, another for distance, using euclidean (in 2D)

	Parameters
	----------
	fromLocs: list, Required
		The start node coordinates in format of [[lat, lon], [lat, lon], ... ]
	toLocs: list, Required
		The End node coordinates in format of [[lat, lon], [lat, lon], ... ]
	speedMPS: float, Required
		A constant speed for calculation

	returns
	-------
	timeSecs: dictionary
		A dictionary for time from nodes to nodes, unit is in [seconds]
	distMeters: dictionary
		A dictionary for distance from nodes to nodes, unit is in [meters]
	
	"""

	distMeters = {}
	timeSecs = {}
	for i in range(len(fromLocs)):
		for j in range(len(toLocs)):
			eucDist = geoDistance2D(fromLocs[i], toLocs[j])
			distMeters[i, j] = eucDist
			timeSecs[i, j] = eucDist / speedMPS
	return [timeSecs, distMeters]

def _getTimeDistManhattan(fromLocs, toLocs, speedMPS):
	"""
	Generate two dictionaries, one for time, another for distance, using Manhattan

	Parameters
	----------
	fromLocs: list, Required
		The start node coordinates in format of [[lat, lon], [lat, lon], ... ]
	toLocs: list, Required
		The End node coordinates in format of [[lat, lon], [lat, lon], ... ]
	speedMPS: float, Required
		A constant speed for calculation

	returns
	-------
	timeSecs: dictionary
		A dictionary for time from nodes to nodes, unit is in [seconds]
	distMeters: dictionary
		A dictionary for distance from nodes to nodes, unit is in [meters]
	
	"""

	distMeters = {}
	timeSecs = {}
	for i in range(len(fromLocs)):
		for j in range(len(toLocs)):
			fromLocsDict = locs2Dict(fromLocs)
			toLocsDict = locs2Dict(toLocs)
			manDist = geoDistance2D(fromLocs[i], (fromLocsDict[i]['lat'], toLocsDict[j]['lon'])) + geoDistance2D((fromLocsDict[i]['lat'], toLocsDict[j]['lon']), toLocs[j])
			distMeters[i, j] = manDist
			timeSecs[i, j] = manDist / speedMPS
	return [timeSecs, distMeters]

def _getTimeDistOSRM(fromLocs, toLocs, speedMPS):
	"""
	Generate two dictionaries, one for time, another for distance, using OSRM

	Parameters
	----------
	fromLocs: list, Required
		The start node coordinates in format of [[lat, lon], [lat, lon], ... ]
	toLocs: list, Required
		The End node coordinates in format of [[lat, lon], [lat, lon], ... ]
	speedMPS: float, Required
		A constant speed for calculation

	returns
	-------
	timeSecs: dictionary
		A dictionary for time from nodes to nodes, unit is in [seconds]
	distMeters: dictionary
		A dictionary for distance from nodes to nodes, unit is in [meters]
	
	"""

	[timeSecs, distMeters] = osrmGetTimeDist(fromLocs, toLocs)

	if (speedMPS != None):
		for i in range(len(fromLocs)):
			for j in range(len(toLocs)):
				timeSecs[i, j] = distMeters[i, j] / speedMPS

	return [timeSecs, distMeters]

def _getTimeDistPgRouting(fromLocs, toLocs, databaseName, speedMPS):
	"""
	Generate two dictionaries, one for time, another for distance, using pgRouting

	Parameters
	----------
	fromLocs: list, Required
		The start node coordinates in format of [[lat, lon], [lat, lon], ... ]
	toLocs: list, Required
		The End node coordinates in format of [[lat, lon], [lat, lon], ... ]
	databaseName: string, Conditional
		If you are hosting a data provider on your local machine (e.g., pgRouting), you'll need to specify the name of the local database. See :ref:`Data Providers`
	speedMPS: float, Required
		A constant speed for calculation

	returns
	-------
	timeSecs: dictionary
		A dictionary for time from nodes to nodes, unit is in [seconds]
	distMeters: dictionary
		A dictionary for distance from nodes to nodes, unit is in [meters]
	
	"""
	
	[timeSecs, distMeters] = pgrGetTimeDist(fromLocs, toLocs, databaseName)

	if (speedMPS != None):
		for i in range(len(fromLocs)):
			for j in range(len(toLocs)):
				timeSecs[i, j] = distMeters[i, j] / speedMPS

	return [timeSecs, distMeters]

def _getTimeDistMapQuest(fromLocs, toLocs, travelMode, APIkey, speedMPS):
	"""
	Generate two dictionaries, one for time, another for distance, using MapQuest

	Parameters
	----------
	fromLocs: list, Required
		The start node coordinates in format of [[lat, lon], [lat, lon], ... ]
	toLocs: list, Required
		The End node coordinates in format of [[lat, lon], [lat, lon], ... ]
	travelMode: string, Required
		The travel mode for MapQuest, options are 'fastest', 'shortest', 'pedestrian'
	APIkey: string, Required
		Some data providers require an API key (which you'll need to register for). See :ref:`Data Providers`
	speedMPS: float, Required
		A constant speed for calculation

	returns
	-------
	timeSecs: dictionary
		A dictionary for time from nodes to nodes, unit is in [seconds]
	distMeters: dictionary
		A dictionary for distance from nodes to nodes, unit is in [meters]
	
	"""

	if (fromLocs == toLocs):
		locs = fromLocs.copy()
		[timeSecs, distMeters] = mqGetTimeDistAll2All(locs, travelMode, APIkey)
	elif (len(fromLocs) == 1):
		fromLoc = fromLocs[0]
		[timeSecs, distMeters] = mqGetTimeDistOne2Many(fromLoc, toLocs, travelMode, APIkey)
	elif (len(toLocs) == 1):
		toLoc = toLocs[0]
		[timeSecs, distMeters] = mqGetTimeDistMany2One(fromLocs, toLoc, travelMode, APIkey)
	else:
		for i in range(len(fromLocs)):
			[timeRow, distRow] = mqGetTimeDistOne2Many(fromLocs[i], toLocs, routeType, APIkey)
			for j in range(len(toLocs)):
				distMeters[i, j] = distRow[0, j]
				timeSecs[i, j] = timeRow[0, j]

	if (speedMPS != None):
		for i in range(len(fromLocs)):
			for j in range(len(toLocs)):
				timeSecs[i, j] = distMeters[i, j] / speedMPS

	return [timeSecs, distMeters]

def _getTimeDistORS(fromLocs, toLocs, travelMode, APIkey, speedMPS):
	"""
	Generate two dictionaries, one for time, another for distance, using ORS-online

	Parameters
	----------
	fromLocs: list, Required
		The start node coordinates in format of [[lat, lon], [lat, lon], ... ]
	toLocs: list, Required
		The End node coordinates in format of [[lat, lon], [lat, lon], ... ]
	travelMode: string, Required
		The travel mode for ORS, options are 'fastest', 'pedestrian', 'cycling', 'truck'
	APIkey: string, Required
		Some data providers require an API key (which you'll need to register for). See :ref:`Data Providers`
	speedMPS: float, Required
		A constant speed for calculation

	returns
	-------
	timeSecs: dictionary
		A dictionary for time from nodes to nodes, unit is in [seconds]
	distMeters: dictionary
		A dictionary for distance from nodes to nodes, unit is in [meters]
	
	"""

	if (fromLocs == toLocs):
		locs = fromLocs.copy()
		[timeSecs, distMeters] = orsGetTimeDistAll2All(locs, travelMode, APIkey)
	elif (len(fromLocs) == 1):
		fromLoc = fromLocs[0]
		[timeSecs, distMeters] = orsGetTimeDistOne2Many(fromLoc, toLocs, travelMode, APIkey)
	elif (len(toLocs) == 1):
		toLoc = toLocs[0]
		[timeSecs, distMeters] = orsGetTimeDistMany2One(fromLocs, toLoc, travelMode, APIkey)
	else:
		for i in range(len(fromLocs)):
			[timeRow, distRow] = orsGetTimeDistOne2Many(fromLocs[i], toLocs, routeType, APIkey)
			for j in range(len(toLocs)):
				distMeters[i, j] = distRow[0, j]
				timeSecs[i, j] = timeRow[0, j]

	if (speedMPS != None):
		for i in range(len(fromLocs)):
			for j in range(len(toLocs)):
				timeSecs[i, j] = distMeters[i, j] / speedMPS

	return [timeSecs, distMeters]	
	
def _getTimeDistORSlocal(fromLocs, toLocs, travelMode, port, speedMPS):
	"""
	Generate two dictionaries, one for time, another for distance, using ORS-local

	Parameters
	----------
	fromLocs: list, Required
		The start node coordinates in format of [[lat, lon], [lat, lon], ... ]
	toLocs: list, Required
		The End node coordinates in format of [[lat, lon], [lat, lon], ... ]
	travelMode: string, Required
		The travel mode for ORS, options are 'fastest', 'pedestrian', 'cycling', 'truck'
	port: string, Required
		localhost connection port
	speedMPS: float, Required
		A constant speed for calculation

	returns
	-------
	timeSecs: dictionary
		A dictionary for time from nodes to nodes, unit is in [seconds]
	distMeters: dictionary
		A dictionary for distance from nodes to nodes, unit is in [meters]
	
	"""

	if (fromLocs == toLocs):
		locs = fromLocs.copy()
		[timeSecs, distMeters] = orsLocalGetTimeDistAll2All(locs, travelMode, port)
	elif (len(fromLocs) == 1):
		fromLoc = fromLocs[0]
		[timeSecs, distMeters] = orsLocalGetTimeDistOne2Many(fromLoc, toLocs, travelMode, port)
	elif (len(toLocs) == 1):
		toLoc = toLocs[0]
		[timeSecs, distMeters] = orsLocalGetTimeDistMany2One(fromLocs, toLoc, travelMode, port)
	else:
		for i in range(len(fromLocs)):
			[timeRow, distRow] = orsLocalGetTimeDistOne2Many(fromLocs[i], toLocs, routeType, port)
			for j in range(len(toLocs)):
				distMeters[i, j] = distRow[0, j]
				timeSecs[i, j] = timeRow[0, j]

	if (speedMPS != None):
		for i in range(len(fromLocs)):
			for j in range(len(toLocs)):
				timeSecs[i, j] = distMeters[i, j] / speedMPS

	return [timeSecs, distMeters]		