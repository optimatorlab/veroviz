from veroviz._common import *

from veroviz._queryPgRouting import pgrGetSnapToRoadLatLon
from veroviz._queryPgRouting import pgrGetNearestStreet
from veroviz._queryORS import orsGetSnapToRoadLatLon
from veroviz._queryOSRM import osrmGetSnapToRoadLatLon
from veroviz._queryMapQuest import mqGetSnapToRoadLatLon
from veroviz._queryMapQuest import mqGetSnapToRoadLatLonBatch
from veroviz._queryORSlocal import orsLocalGetSnapToRoadLatLon

def privGetSnapLocBatch(locs=None, dataProvider=None, dataProviderArgs=None):

	"""
	A function to snap nodes to road network using different data sources

	Parameters
	----------
	locs: list of lists, Required
		A list of GPS coordinates of node locations, in the form of [[lat, lon], [lat, lon], ...]
	dataProvider: string, Required, See :ref:`Data Providers`
		Datasource of the road network
	dataProviderArgs: dictionary, Optional, default as None
		For some data provider, veroviz need some extra parameters such as API keys or database name. See :ref:`DataProviders` for the keys required for different data provider.
	
	Returns
	-------
	list of lists
		A list of snapped coordinates given a node dataframe
	"""

	try:
		dataProvider = dataProvider.lower()
	except:
		pass
		
	# snap nodes based on different data providers
	snapLocs = []
	if (dataProviderDictionary[dataProvider] == 'mapquest'):
		APIkey = dataProviderArgs['APIkey']
		if (len(locs) > 1):
			snapLocs = mqGetSnapToRoadLatLonBatch(locs, APIkey)
		else:
			snapLoc = mqGetSnapToRoadLatLon(locs[0], APIkey)
			snapLocs.append(snapLoc)

	elif (dataProviderDictionary[dataProvider] == 'pgrouting'):
		databaseName = dataProviderArgs['databaseName']
		for i in range(len(locs)):
			street = pgrGetNearestStreet(locs[i], databaseName)
			snapLoc = pgrGetSnapToRoadLatLon(street['gid'], locs[i], databaseName)
			snapLocs.append(snapLoc)

	elif (dataProviderDictionary[dataProvider] == 'osrm-online'):
		for i in range(len(locs)):
			snapLoc = osrmGetSnapToRoadLatLon(locs[i])
			snapLocs.append(snapLoc)

	elif (dataProviderDictionary[dataProvider] == 'ors-online'):
		APIkey = dataProviderArgs['APIkey']
		for i in range(len(locs)):
			snapLoc = orsGetSnapToRoadLatLon(locs[i], APIkey)
			snapLocs.append(snapLoc)

	elif (dataProviderDictionary[dataProvider] == 'ors-local'):
		port = dataProviderArgs['port']
		for i in range(len(locs)):
			snapLoc = orsLocalGetSnapToRoadLatLon(locs[i], port)
			snapLocs.append(snapLoc)

	for i in range(len(locs)):
		if (len(locs[i]) == 3):
			snapLocs[i] = [snapLocs[i][0], snapLocs[i][1], locs[i][2]]
	
	return snapLocs

def privGetSnapLoc(loc=None, dataProvider=None, dataProviderArgs=None):

	"""
	A function to snap one node to road network using different data sources

	Parameters
	----------
	loc: list, Required
		Coordinates of a location, expressed as either [lat, lon, alt] or [lat, lon].  Note: This function returns only latitude and longitude; any altitude values provided as inputs will be lost in the return.
	dataProvider: string, Required, See :ref:`Data Providers`
		Datasource of the road network
	dataProviderArgs: dictionary, Optional, default as None
		For some data provider, veroviz need some extra parameters such as API keys or database name. See :ref:`DataProviders` for the keys required for different data provider.
	
	Returns
	-------
	list
		A snapped coordinate given a node dataframe
	"""
	
	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	snapLoc = None
	if (dataProviderDictionary[dataProvider] == 'mapquest'):
		APIkey = dataProviderArgs['APIkey']
		snapLoc = mqGetSnapToRoadLatLon(loc, APIkey)

	elif (dataProviderDictionary[dataProvider] == 'pgrouting'):
		databaseName = dataProviderArgs['databaseName']
		street = pgrGetNearestStreet(loc, databaseName)
		snapLoc = pgrGetSnapToRoadLatLon(street['gid'], loc, databaseName)

	elif (dataProviderDictionary[dataProvider] == 'osrm-online'):
		snapLoc = osrmGetSnapToRoadLatLon(loc)			

	elif (dataProviderDictionary[dataProvider] == 'ors-online'):
		APIkey = dataProviderArgs['APIkey']
		snapLoc = orsGetSnapToRoadLatLon(loc, APIkey)			

	elif (dataProviderDictionary[dataProvider] == 'ors-local'):
		port = dataProviderArgs['port']
		snapLoc = orsLocalGetSnapToRoadLatLon(loc, port)			
	
	
	if (len(loc) == 3):
		snapLoc = [snapLoc[0], snapLoc[1], loc[2]]

	return snapLoc