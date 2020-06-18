from veroviz._common import *
from veroviz._validation import valSnapNodesToRoad
from veroviz._validation import valGetSnapLoc
from veroviz._validation import valGetSnapLocBatch

from veroviz._getSnapLoc import privGetSnapLocBatch
from veroviz._getSnapLoc import privGetSnapLoc

def snapNodesToRoad(nodes=None, dataProvider=None, dataProviderArgs=None):
	"""
	Updates the locations of nodes within a dataframe, such that each node becomes located on a road network.

	Parameters
	----------
	nodes: :ref:`Nodes`, Required, default as None
		A :ref:`Nodes` dataframe containing an existing set of nodes.  
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for generating nodes on a road network. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.

	Returns
	-------
	:ref:`Nodes` dataframe
		A copy of the input `nodes` dataframe, with updated lat/lon values.	

	Example
	-------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Also, import os so we can use environment variables for data provider API keys:
		>>> import os
		
	Create a :ref:`Nodes` dataframe by :meth:`~veroviz.generateNodes.createNodesFromLocs` with two nodes that are off the road network:
		>>> exampleNodes = vrv.createNodesFromLocs(
		...     locs = [[42.80, -78.00],
		...             [42.81, -78.004]],
		...     leafletColor = 'red')


	These nodes are not aligned with the road network.  The following examples demonstrate how to move the nodes to lat/lon locations that correspond to roads.
		>>> # Use OSRM as data provider
		>>> snappedNodes = vrv.snapNodesToRoad(
		...     nodes        = exampleNodes, 
		...     dataProvider = 'OSRM-online')

	Display the original (red) and OSRM-snapped (green) nodes to see the effects of snapping.
		>>> myMap = vrv.createLeaflet(nodes=exampleNodes, mapBackground='Stamen Toner')
		>>> myMap = vrv.createLeaflet(nodes=snappedNodesOSRM, mapObject=myMap)
		>>> myMap	

	We can also use ORS, MapQuest, or pgRouting as the data source.  In these cases, an API key or database name should be provided.
		>>> # Use MapQuest as data provider, and change node colors to purple:
		>>> snappedNodesMQ = vrv.snapNodesToRoad(
		...     nodes            = exampleNodes,
		...     dataProvider     = 'MapQuest',
		...     dataProviderArgs = { 'APIkey' : os.environ['MAPQUESTKEY']})
		>>> snappedNodesMQ['leafletColor'] = 'purple'	
	
		>>> # Add the MapQuest-snapped (purple) nodes to our map:
		>>> myMap = vrv.createLeaflet(nodes=snappedNodesMQ, mapObject=myMap)
		>>> myMap
	
		>>> # Use ORS as data provider, and change node colors to blue:
		>>> snappedNodesORS = vrv.snapNodesToRoad(
		...     nodes            = exampleNodes,
		...     dataProvider     = 'ORS-online',
		...     dataProviderArgs = {'APIkey': os.environ['ORSKEY']})
		>>> snappedNodesORS['leafletColor'] = 'blue'	

		>>> # Add the ORS-snapped (blue) nodes to our map:
		>>> myMap = vrv.createLeaflet(nodes=snappedNodesORS, mapObject=myMap)
		>>> myMap

		>>> # Use pgRouting as data provider, and change node colors to black:
		>>> snappedNodesPGR = vrv.snapNodesToRoad(
		...     nodes        = exampleNodes,
		...     dataProvider = 'pgRouting',
		...     dataProviderArgs = {'databaseName': 'YOUR_DATABASENAME'})
		>>> snappedNodesPGR['leafletColor'] = 'black'	

		>>> # Add the pgRouting-snapped (black) nodes to our map:
		>>> myMap = vrv.createLeaflet(nodes=snappedNodesPGR, mapObject=myMap)
		>>> myMap

	"""
	
	# validation
	[valFlag, errorMsg, warningMsg] = valSnapNodesToRoad(nodes, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	# List of lat/lon before snapping
	locs = list(zip(nodes['lat'].tolist(), nodes['lon'].tolist()))
	snapNodes = nodes.copy()

	# Find list of snapped coordins
	snapLocs = privGetSnapLocBatch(locs, dataProvider, dataProviderArgs)

	# Make a copy of nodes and replace lat/lon columns withn snapped lat/lon	
	snapNodes['lat'] = list(zip(*snapLocs))[0]
	snapNodes['lon'] = list(zip(*snapLocs))[1]

	return snapNodes

def getSnapLocBatch(locs=None, dataProvider=None, dataProviderArgs=None):

	"""
	Snap multiple locations, each given by [lat, lon] coordinates, to their nearest locations on a road network.
	

	Parameters
	----------
	locs: list of lists, Required
		A list of GPS coordinates of node locations, in the form of [[lat, lon], [lat, lon], ...]
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for finding routes or generate nodes on a road network. See :ref:`Data Providers` for options and requirements of options.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data provider, veroviz need some extra parameters such as API keys or database name. See :ref:`Data Providers` for the keys required for different data provider.
	
	Returns
	-------
	list of lists
		A list of snapped locations in the format of [[lat, lon], [lat, lon], ...].  Note: Any altitude values provided as inputs in the `loc` parameter will be lost in the return.

	Example
	-------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Also, import os so we can use environment variables for data provider API keys:
		>>> import os

	Snap a given list of location to their nearest streets:
		>>> locs = [
		...     [42.00, -78.00],
		...     [42.10, -78.00],
		...     [42.20, -78.00]]
		>>> snapLocs = vrv.getSnapLocBatch(
		...     locs             = locs,
		...     dataProvider     = 'MapQuest',
		...     dataProviderArgs = {'APIkey': os.environ['MAPQUESTKEY']})
		>>> snapLocs
		[[41.999401, -78.003876], [42.100021, -77.995549], [42.1993, -78.001011]]
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valGetSnapLocBatch(locs, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	snapLocs = privGetSnapLocBatch(locs, dataProvider, dataProviderArgs)
	
	return snapLocs

def getSnapLoc(loc=None, dataProvider=None, dataProviderArgs=None):

	"""
	Snap a given single location, given by [lat, lon] coordinates, to the nearest location on a road network.

	Parameters
	----------
	loc: list, Required
		Coordinates of a location, expressed as either [lat, lon, alt] or [lat, lon].  Note: This function returns only latitude and longitude; any altitude values provided as inputs will be lost in the return.
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for finding routes or generate nodes on a road network. See :ref:`Data Providers` for options and requirements of options.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data provider, veroviz need some extra parameters such as API keys or database name. See :ref:`Data Providers` for the keys required for different data provider.
	
	Return
	------
	list
		A snapped location in the format of [lat, lon].  Any altitude values provided as inputs in the `loc` parameter will be lost in the return.

	Note
	----
	This function returns only latitude and longitude.  Any altitude values provided as inputs in the `loc` parameter will be lost in the return.
	
	Example
	-------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Snap a given location to the nearest street:
		>>> loc = [42.00, -78.00]
		>>> snapLoc = vrv.getSnapLoc(
		...     loc          = loc,
		...     dataProvider = 'OSRM-online')
		>>> snapLoc
		[41.999401, -78.003876]

	View the original (red) and snapped (green) locations on a map
		>>> myMap = vrv.addLeafletMarker(center=loc, fillColor='red')
		>>> myMap = vrv.addLeafletMarker(center=snapLoc, fillColor='green', mapObject=myMap)
		>>> myMap
		
	NOTE: This function returns only latitude and longitude. Any altitude values provided as inputs in the loc parameter will be lost in the return.		
		>>> loc3D = [42.00, -78.00, 100]
		>>> snapLoc = vrv.getSnapLoc(
		...     loc          = loc3D,
		...     dataProvider = 'OSRM-online')
		>>> snapLoc
		[41.999401, -78.003876]
		
	"""
	
	# validation
	[valFlag, errorMsg, warningMsg] = valGetSnapLoc(loc, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	snapLoc = privGetSnapLoc(loc, dataProvider, dataProviderArgs)
	
	return snapLoc