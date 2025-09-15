from veroviz._common import *
from veroviz._validation import *
from veroviz._geometry import *
from veroviz._internal import *
from veroviz._geocode import privGeocode, privReverseGeocode
from veroviz._isochrones import privIsochrones
from veroviz._elevation import privGetElevationLocs
from veroviz._elevation import privGetElevationNodes, privGetElevationArcsAsgn
from veroviz._weather import privGetWeather
from veroviz._createEntitiesFromList import privCreateNodesFromLocs
from veroviz._getTimeDistFromLocs2D import getTimeDistFromLocs2D
from veroviz._nearestNodes import privNearestNodes
from veroviz._utilities import privInitDataframe, privConvertDistance, privConvertTime, privConvertSpeed, privGetMapBoundary, privExportDataframe, privAssignmentsToPaths, privArcsToPaths, privClosestPointLoc2Path


def convertSpeed(speed=None, fromUnitsDist=None, fromUnitsTime=None, toUnitsDist=None, toUnitsTime=None):
	"""
	Convert a speed to different units.

	Parameters
	----------
	speed: float, Required
		The numeric value describing a speed to be converted.
	fromUnitsDist: string, Required
		Distance units for the given speed, before conversion. See :ref:`Units` for options.
	fromUnitsTime: string, Required
		Time units for the given speed, before conversion. See :ref:`Units` for options.
	toUnitsDist: string, Required
		Distance units for the speed after conversion. See :ref:`Units` for options.
	toUnitTime: string, Required
		Time units for the speed after conversion. See :ref:`Units` for options.
	
	Returns
	-------
	float
		Speed after conversion

	Example
	-------
		>>> import veroviz as vrv
		>>> speedFPS = 10
		>>> speedMPH = vrv.convertSpeed(speedFPS, 'ft', 's', 'mi', 'h')
		>>> speedMPH
		6.818198764711	
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valConvertSpeed(speed, fromUnitsDist, fromUnitsTime, toUnitsDist, toUnitsTime)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
	
	return privConvertSpeed(speed, fromUnitsDist, fromUnitsTime, toUnitsDist, toUnitsTime)
	

def convertDistance(distance=None, fromUnits=None, toUnits=None):
	"""
	Convert a distance to different units.

	Parameters
	----------
	distance: float, Required
		The numeric value describing a distance to be converted.
	fromUnits: string, Required
		Distance units before conversion. See :ref:`Units` for options.
	toUnits: string, Required
		Distance units after conversion. See :ref:`Units` for options.

	Returns
	-------
	float
		Distance after conversion

	Example
	-------
		>>> import veroviz as vrv
		>>> distanceMiles = 1.0
		>>> distanceKilometers = vrv.convertDistance(distanceMiles, 'miles', 'km')
		>>> distanceKilometers
		1.60934

	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valConvertDistance(distance, fromUnits, toUnits)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	return privConvertDistance(distance, fromUnits, toUnits)
	

def convertTime(time=None, fromUnits=None, toUnits=None):
	"""
	Convert a time to different units.

	Parameters
	----------
	time: float, Required
		The numeric value describing a time to be converted.
	fromUnits: string, Required
		Time units before conversion. See :ref:`Units` for options.
	toUnits: string, Required
		Time units after conversion. See :ref:`Units` for options.

	Returns
	-------
	float
		Time after conversion

	Example
	-------
		>>> import veroviz as vrv
		>>> timeHours = 1.5
		>>> timeMinutes = vrv.convertTime(timeHours, 'h', 'min')
		>>> timeMinutes
		90.0

	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valConvertTime(time, fromUnits, toUnits)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	return privConvertTime(time, fromUnits, toUnits)


def convertArea(area=None, fromUnits=None, toUnits=None):
	"""
	Convert an area from `fromUnits` to `toUnits`.
	
	Parameters
	----------
	area: float, Required
		The numeric value describing an area to be converted.
	fromUnits: string, Required
		Area units, before conversion. See :ref:`Units` for options.
	toUnits: string, Required
		Desired units of area after conversion. See :ref:`Units` for options.

	Returns
	-------
	float
		New value of area, after conversion.
		
	Example
	-------
		>>> import veroviz as vrv
		>>> areaSQKM = 1.0
		>>> areaSqMiles = vrv.convertArea(50, 'sqkm', 'sqmi')	
		>>> areaSqMiles
		>>> 19.305
	"""

	[valFlag, errorMsg, warningMsg] = valConvertArea(area, fromUnits, toUnits)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
		
	try:
		fromUnits = fromUnits.lower()
	except:
		pass
				
	# Convert input to square meters:	
	fromUnits = areaUnitsDictionary[fromUnits]
	if (fromUnits == 'sqft'):
		tmpArea = area / VRV_CONST_SQFT_PER_SQMETER 
	elif (fromUnits == 'sqmi'):
		tmpArea = area / VRV_CONST_SQMILES_PER_SQMETER
	elif (fromUnits == 'sqkm'):
		tmpArea = area / VRV_CONST_SQKM_PER_SQMETER
	else:
		tmpArea = area
	
	try:
		toUnits = toUnits.lower()
	except:
		pass
		
	# Convert from square meters to desired output units:
	toUnits = areaUnitsDictionary[toUnits]
	if (toUnits == 'sqft'):
		convArea = tmpArea * VRV_CONST_SQFT_PER_SQMETER 
	elif (toUnits == 'sqmi'):
		convArea = tmpArea * VRV_CONST_SQMILES_PER_SQMETER
	elif (toUnits == 'sqkm'):
		convArea = tmpArea * VRV_CONST_SQFT_PER_SQMETER
	else:
		convArea = tmpArea
	
	return convArea

def lengthFromNodeSeq(nodeSeq=None, lengthDict=None):
	"""
	Calculate the total "length" (either in time or distance) along a path defined by a sequence of node IDs.

	Parameters
	----------
	nodeSeq: list, Required
		An ordered list of node IDs.  These IDs must be included in the `id` column of the :ref:`Nodes` dataframe specified in the `nodes` input argument to this function. The format for `nodeSeq` is [node_id_1, node_id_2, ...].
	lengthDict: dictionary, Required

	Return
	------
	float
		Total length of the path.

	Example
	-------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Define some sample locations and create a nodes dataframe:
		>>> locs = [[42.8871085, -78.8731949],
		...         [42.8888311, -78.8649649],
		...         [42.8802158, -78.8660787],
		...         [42.8845705, -78.8762794],
		...         [42.8908031, -78.8770140]]
		>>> myNodes = vrv.createNodesFromLocs(locs=locs)

	Calculate time and distance matrices:
		>>> [timeSecDict, distMetersDict] = vrv.getTimeDist2D(nodes = myNodes, routeType = 'euclidean2D', speedMPS = 15)

	Define a sequence of nodes to visit:
		>>> nodeSeq = [1, 3, 2]

	Find the total travel time to visit the nodes:
		>>> totalTimeSec = vrv.lengthFromNodeSeq(nodeSeq, timeSecDict)
		>>> totalTimeSec
		128.18625959871764
		
	Find the total length of the node sequence:
		>>> totalDistMeters = vrv.lengthFromNodeSeq(nodeSeq, distMetersDict)
		>>> totalDistMeters
		1922.793893980765		
	"""
	[valFlag, errorMsg, warningMsg] = valLengthFromNodeSeq(nodeSeq, lengthDict)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	length = 0
	for i in range(0, len(nodeSeq)-1):
		length += lengthDict[nodeSeq[i], nodeSeq[i+1]]
	return length

def calcPerimeter2D(path=None, closeLoop=False, distUnits='meters'):
	"""
	Calculate the total geodesic distance along a path defined by [lat, lon] coordinates.

	Parameters
	----------
	path: list of lists, Required, default as None
	A list of coordinates that form a path, in the format of [[lat, lon], [lat, lon], ...] or [[lat, lon, alt], [lat, lon, alt], ...].  If provided, altitude will be ignored.
	closeLoop: Boolean, Optional, default as False
	Indicates whether the path should be closed (i.e., connecting the last location to the first).
	distUnits: string, Optional, default as 'meters'
	Specifies the desired distance units for the output. See :ref:`Units` for options.
	
	Returns
	-------
	float
		Total length of the path.

	Example
	-------
	>>> import veroviz as vrv
	>>> locs = [[42.80, -78.90, 0], [42.82, -78.92, 0], [42.84, -78.94, 0]]
	>>> perimDist = vrv.calcPerimeter2D(path=locs, closeLoop=True, distUnits='mi')
	>>> perimDist
	6.857172388864359
	"""

	[valFlag, errorMsg, warningMsg] = valCalcPerimeter2D(path, closeLoop, distUnits)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	dist = 0
	for i in range(0, len(path) - 1):
		dist += distance2D(path[i][0:2], path[i + 1][0:2])

	if (closeLoop):
		dist += distance2D(path[-1][0:2], path[0][0:2])

	dist = convertDistance(dist, 'meters', distUnits)

	return dist

def calcArea(poly=None):
	"""
	Calculate the area, in square meters, of a polygon.
	
	Parameters
	----------
	poly: list of lists, Required
		A polygon defined as a list of individual locations, in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored. 
		
	Returns
	-------
	float
	Area, in meters, of the polygon.
	
	Example
	-------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()
	
	Define a sequence of locations:
		>>> locs = [[42.82, -78.80, 0], [42.86, -78.82, 0], [42.84, -78.84, 0]]

	Calculate the area of the polygon formed by these locations:
		>>> area = vrv.calcArea(poly=locs)
		>>> area	
		5449365.537915299
	
	Draw the polygon:
		>>> myNodes = vrv.createNodesFromLocs(locs)
		>>> myMap = vrv.addLeafletPolygon(points=locs, fillColor='red')
		>>> myMap = vrv.createLeaflet(mapObject=myMap, nodes=myNodes)
		>>> myMap		
	"""
	
	[valFlag, errorMsg, warningMsg] = valCalcArea(poly)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
			
	area = geoAreaOfPolygon(poly)
	
	return area		

def initDataframe(dataframeType=None):
	"""
	Return an empty dataframe of a given type.

	Parameters
	----------
	dataframeType: string, Required
		The options are 'Nodes', 'Arcs', and 'Assignments'.  These options are case insensitive.

	Returns
	-------
	pandas.dataframe
		A dataframe of the given type.  See :ref:`Nodes`, :ref:`Arcs`, and :ref:`Assignments` for details on each dataframe type.

	Example
	-------
		>>> import veroviz as vrv
		>>> newNodes = vrv.initDataframe('Nodes')
		>>> newNodes
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valInitDataframe(dataframeType)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	return privInitDataframe(dataframeType)
	
	
def getMapBoundary(nodes=None, arcs=None, locs=None):
	"""
	Find the smallest rectangle that encloses a collection of nodes, arcs, assignments, and/or locations.  This function returns a list of lists, of the form [minLat, maxLon], [maxLat, minLon]].  This is equivalent to finding the southeast and northwest corners of the rectangle.
	
	Parameters
	----------
	nodes: :ref:`Nodes`, Conditional, `nodes`, `arcs`, and `locs` cannot be None at the same time
		A :ref:`Nodes` dataframe.
	arcs: :ref:`Arcs` or :ref:`Assignments`, Conditional, `nodes`, `arcs`, and `locs` cannot be None at the same time
		An :ref:`Arcs` or :ref:`Assignments` dataframe.
	locs: list of lists, Conditional, `nodes`, `arcs`, and `locs` cannot be None at the same time
		A list of individual locations, in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  
	Returns
	-------
	list of lists
		In form of [[minLat, maxLon], [maxLat, minLon]].  These two points denote the southeast and northwest corners of the boundary rectangle.

	Example
	-------
		>>> import veroviz as vrv
		>>>
		>>> # Create 3 nodes, with blue pin markers (default):
		>>> myNodes = vrv.createNodesFromLocs(
		...     locs = [[42.1343, -78.1234], 
		...             [42.5323, -78.2534], 
		...             [42.9812, -78.1353]])
		>>> 
		>>> # Create 1 arc, with orange arrows (default):
		>>> myArc = vrv.createArcsFromLocSeq(locSeq = [[42.62, -78.20], 
		...                                            [42.92, -78.30]])
		>>> 
		>>> # Define 2 locations, with altitude.  (We'll color these purple later):
		>>> myLocs = [[42.03, -78.26, 100], [42.78, -78.25, 200]] 
		>>>
		>>> # Find the boundary of these objects:
		>>> myBoundary = vrv.getMapBoundary(nodes = myNodes,
		...                                 arcs  = myArc,
		...                                 locs  = myLocs)
		>>> myBoundary
		[[42.03, -78.1234], [42.9812, -78.3]]
		
		>>> # Initialize a map with nodes (blue) and an arc (orange):
		>>> myMap = vrv.createLeaflet(nodes = myNodes, 
		...                           arcs  = myArc)
		>>>
		>>> # Add red (default) circle markers for the locations:
		>>> for i in range(0, len(myLocs)):
		...    myMap = vrv.addLeafletMarker(mapObject = myMap, 
		...                                 center    = myLocs[i])    
		>>>
		>>> # Convert myBoundary to a 4-point polygon:
		>>> myBoundingRegion = [myBoundary[0], 
		...                     [myBoundary[0][0], myBoundary[1][1]], 
		...                     myBoundary[1], 
		...                     [myBoundary[1][0], myBoundary[0][1]]]
		>>>
		>>> # Add the bounding region to the map:
		>>> myMap = vrv.createLeaflet(mapObject      = myMap, 
		...                           boundingRegion = myBoundingRegion)
		>>> # Display the map:
		>>> myMap
	"""
	# validation
	[valFlag, errorMsg, warningMsg] = valGetMapBoundary(nodes, arcs, locs)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	return privGetMapBoundary(nodes, arcs, locs)


def convertMatricesDataframeToDictionary(dataframe=None):
	"""
	This function is intended for use with time/distance matrices, which are stored in veroviz as Python dictionaries. This function transforms a matrix dataframe into  a dictionary, such that the indices of columns and rows become a tuple key for the dictionary.

	Parameters
	----------
	dataframe: pandas.dataframe, Required
		The rows and columns are both integers. There should not be duplicated origin/destination pairs.

	Return
	------
	dictionary
		The keys are tuples of (originIndex, destinationIndex)

	Note
	----
	Pandas dataframes can be confusing when used with time and distance matrices.  In particular, suppose you have a distance dataframe named `distDF`.  The value of `distDF[1][2]` will actually return the distance from 2 to 1.  Conversely, if you have a distance dictionary named `distDict`, the value of `distDict[1,2]` will be the distance from 1 to 2.
	
	Example
	-------
	Prepare some data.
		>>> import veroviz as vrv
		>>> locs = [
		...     [42.1538, -78.4253], 
		...     [42.3465, -78.6234], 
		...     [42.6343, -78.1146]]
		>>> exampleNodes = vrv.createNodesFromLocs(locs=locs)
		>>> [timeDict, distDict] = vrv.getTimeDist2D(
		...     nodes        = exampleNodes, 
		...     routeType    = 'fastest', 
		...     dataProvider = 'OSRM-online')
		>>> [timeDict]
		[{(1, 1): 0.0,
		  (1, 2): 2869.9,
		  (1, 3): 4033.9,
		  (2, 1): 2853.3,
		  (2, 2): 0.0,
		  (2, 3): 4138.2,
		  (3, 1): 4037.8,
		  (3, 2): 4055.4,
		  (3, 3): 0.0}]

		>>> print("The travel time from node 1 to node 2 is %.2f seconds" % (timeDict[1, 2]))
		The travel time from node 1 to node 2 is 2869.90 seconds

		
	timeDict is a dictionary.  Convert to a dataframe:
		>>> timeDF = vrv.convertMatricesDictionaryToDataframe(timeDict)
		>>> timeDF

		>>> # NOTE:  The travel time from 1 to 2 is NOT found by timeDF[1][2].
		>>> # INSTEAD, you must use timeDF[2][1]
		>>> # Pandas uses the form timeDF[COLUMN_INDEX][ROW_INDEX]
		>>> timeDF[1][2], timeDF[2][1], timeDict[1, 2], timeDict[2, 1]
		(2853.3, 2869.9, 2869.9, 2853.3)


	We can transform a dataframe into a dictionary
		>>> timeDict2 = vrv.convertMatricesDataframeToDictionary(timeDF)
		>>> timeDict2
		>>> # This should be the same as `timeDict`
		{(1, 1): 0.0,
		 (1, 2): 2869.9,
		 (1, 3): 4033.9,
		 (2, 1): 2853.3,
		 (2, 2): 0.0,
		 (2, 3): 4138.2,
		 (3, 1): 4037.8,
		 (3, 2): 4055.4,
		 (3, 3): 0.0}

		>>> # Find the travel time *from* 1 *to* 3:
		>>> timeDict2[1,3]
		4033.9
		
	"""

	# Make sure an input argument was provided
	if (dataframe is None):
		print("Error: dataframe is missing as an input to function `convertMatricesDataframeToDictionary()`.")		
		return

	# Make sure the input is a dataframe
	if (type(dataframe) is not pd.core.frame.DataFrame):
		print("Error: The input to function `convertMatricesDataframeToDictionary()` must be a pandas dataframe.")		
		return
	
	dictionary = {}
	try:
		(rowNum, columnNum) = dataframe.shape
		for i in range(rowNum):
			for j in range(columnNum):
				dictionary[dataframe.index[i], dataframe.columns[j]] = dataframe.at[dataframe.index[i], dataframe.columns[j]]
	except:
		print("Error: Duplicated key values, please check the columns and rows of dataframe")

	return dictionary

def convertMatricesDictionaryToDataframe(dictionary=None):
	"""
	This function is intended for use with time/distance matrices, which are stored in veroviz as Python dictionaries. This function transforms a matrix dictionary into a pandas dataframe.  The dictionary is assumed to have 2-tuple indices (the first index represents the ID of the "from" location, the second index is the ID of the "to" location).  In the resulting pandas dataframe, the row indices will represent the "from" location, the column indices the "to" location.

	Parameters
	----------
	dictionary: 
		The keys are tuples of (originIndex, destinationIndex) format.

	Return
	------
	pandas.dataframe
		The keys in the dictionary should be 2-tuples, the first value will be a row index, the second value will be a column index.

	Note
	----
	Pandas dataframes can be confusing when used with time and distance matrices.  In particular, suppose you have a distance dataframe named `distDF`.  The value of `distDF[1][2]` will actually return the distance from 2 to 1.  Conversely, if you have a distance dictionary named `distDict`, the value of `distDict[1,2]` will be the distance from 1 to 2.
	
	Example
	-------
	Prepare some data.
		>>> import veroviz as vrv
		>>> locs = [
		...     [42.1538, -78.4253], 
		...     [42.3465, -78.6234], 
		...     [42.6343, -78.1146]]
		>>> exampleNodes = vrv.createNodesFromLocs(locs=locs)
		>>> [timeDict, distDict] = vrv.getTimeDist2D(
		...     nodes        = exampleNodes, 
		...     routeType    = 'fastest', 
		...     dataProvider = 'OSRM-online')
		>>> [timeDict]
		[{(1, 1): 0.0,
		  (1, 2): 2869.9,
		  (1, 3): 4033.9,
		  (2, 1): 2853.3,
		  (2, 2): 0.0,
		  (2, 3): 4138.2,
		  (3, 1): 4037.8,
		  (3, 2): 4055.4,
		  (3, 3): 0.0}]

		>>> print("The travel time from node 1 to node 2 is %.2f seconds" % (timeDict[1, 2]))
		The travel time from node 1 to node 2 is 2869.90 seconds

		
	timeDict is a dictionary.  Convert to a dataframe:
		>>> timeDF = vrv.convertMatricesDictionaryToDataframe(timeDict)
		>>> timeDF

		>>> # NOTE:  The travel time from 1 to 2 is NOT found by timeDF[1][2].
		>>> # INSTEAD, you must use timeDF[2][1]
		>>> # Pandas uses the form timeDF[COLUMN_INDEX][ROW_INDEX]
		>>> timeDF[1][2], timeDF[2][1], timeDict[1, 2], timeDict[2, 1]
		(2853.3, 2869.9, 2869.9, 2853.3)


	We can transform a dataframe into a dictionary
		>>> timeDict2 = vrv.convertMatricesDataframeToDictionary(timeDF)
		>>> timeDict2
		>>> # This should be the same as `timeDict`
		{(1, 1): 0.0,
		 (1, 2): 2869.9,
		 (1, 3): 4033.9,
		 (2, 1): 2853.3,
		 (2, 2): 0.0,
		 (2, 3): 4138.2,
		 (3, 1): 4037.8,
		 (3, 2): 4055.4,
		 (3, 3): 0.0}

		>>> # Find the travel time *from* 1 *to* 3:
		>>> timeDict2[1,3]
		4033.9
	"""

	# Make sure an input argument was provided
	if (dictionary is None):
		print("Error: dictionary is missing as an input to function `convertMatricesDictionaryToDataframe()`.")		
		return

	# Make sure the input is a dictionary
	if (type(dictionary) is not dict):
		print("Error: The input to function `convertMatricesDictionaryToDataframe()` must be a python dictionary.")		
		return


	rows = []
	columns = []
	keys = dictionary.keys()

	for keys in dictionary:
		if (len(keys) != 2):
			print("Error: This dictionary is not a legitimate matrix, the key values should be pairs.")
			return

	try:
		for keys in dictionary:
			if (keys[0] not in rows):
				rows.append(keys[0])
			if (keys[1] not in columns):
				columns.append(keys[1])
		rows = rows.sort()
		columns = columns.sort()

		dataframe = pd.DataFrame(columns=columns, index=rows)
		for keys in dictionary:
			dataframe.at[keys[0], keys[1]] = dictionary[keys]
		
	except:
		print("Error: Failed to convert dictionary to dataframe.")

	return dataframe

def exportDataToCSV(data=None, filename=None):
	"""
	Export a dataframe or python time/distance matrix dictionary to a `.csv` file.

	Parameters
	----------
	data: pandas.dataframe or dictionary
		The data to be exported.  This can be a :ref:`Nodes`, :ref:`Arcs`, or :ref:`Assignments` dataframe, or it can be a time/distance python dictionary.
	filename: string
		The path and name of file to be exported.

	Examples
	--------
	The following examples will be the same as examples in :meth:`~veroviz.utilities.importDataFromCSV`.

	Import veroviz and check if it is the latest version:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Create a nodes dataframe:
		>>> nodesDF = vrv.createNodesFromLocs(
		...              locs = [[42.1538, -78.4253], 
		...                      [42.3465, -78.6234], 
		...                      [42.6343, -78.1146]])
		>>> nodesDF	

	Save the nodesDF dataframe as a .csv file in a subdirectory named "test":
		>>> vrv.exportDataToCSV(data = nodesDF, filename = 'test/nodes.csv')
	
	Import the dataframe we just saved:
		>>> importedNodes = vrv.importDataFromCSV(
		...     dataType = 'nodes',
		...     filename = 'test/nodes.csv')
		>>> importedNodes

	If the data type is inconsistent with the data, an error message will be thrown and nothing will be imported.
		>>> importedArcs = vrv.importDataFromCSV(
		...     dataType = 'arcs', 
		...     filename = 'test/nodes.csv')
		Error: test/nodes.csv was not successfully imported.  Check the data type.

	Similarly we can import and export the 'arcs' and 'assignments' dataframe

	For time/distance matrices, they are saved as dictionaries in VeRoViz, here is an example of how to import/export them.

	Get travel time/distance matrices using the nodes we just created:
		>>> [timeDict, distDict] = vrv.getTimeDist2D(
		...           nodes        = nodesDF, 
		...           routeType    = 'fastest', 
		...           dataProvider = 'OSRM-online')
		>>> timeDict
		{(1, 1): 0.0,
		 (1, 2): 2869.9,
		 (1, 3): 4033.9,
		 (2, 1): 2853.3,
		 (2, 2): 0.0,
		 (2, 3): 4138.2,
		 (3, 1): 4037.8,
		 (3, 2): 4055.4,
		 (3, 3): 0.0}

	Export the time dictionary to a .csv file in a subdirectory named "test":
		>>> vrv.exportDataToCSV(data = timeDict, filename = 'test/timeMatrix.csv')

	Import the saved dictionary
		>>> importedTime = vrv.importDataFromCSV(
		...     dataType = 'matrix',
		...     filename = 'test/timeMatrix.csv')
		>>> importedTime
		{(1, 1): 0.0,
		 (1, 2): 2869.9,
		 (1, 3): 4033.9,
		 (2, 1): 2853.3,
		 (2, 2): 0.0,
		 (2, 3): 4138.2,
		 (3, 1): 4037.8,
		 (3, 2): 4055.4,
		 (3, 3): 0.0}

	"""

	# Make sure both input args are provided:
	if ((data is None) or (filename is None)):
		print("Error: 1 or more of the 2 required input parameters to function `exportDataToCSV()` are missing.")
		return
	
	# Replace backslash
	filename = replaceBackslashToSlash(filename)

	if (type(filename) is not str):
		print("Error: filename should be a string, please check the inputs.")
		return

	# Get directory
	if ("/" in filename):
		path = ""
		pathList = filename.split('/')
		if (len(pathList) > 1):
			for i in range(len(pathList) - 1):
				path = path + pathList[i] + '/'
			if not os.path.exists(path):
				os.makedirs(path, exist_ok=True)

	# Exporting
	if (type(data) is pd.core.frame.DataFrame):
		dataframe = data
		dataframe.to_csv(path_or_buf=filename, encoding='utf-8')
	elif (type(data) is dict):
		dataframe = convertMatricesDictionaryToDataframe(data)
		dataframe.to_csv(path_or_buf=filename, encoding='utf-8')

	if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
		print("Message: Data written to %s." % (filename))

	return

def importDataFromCSV(dataType=None, filename=None):
	"""
	Import from a `.csv` file into a dataframe or python time/distance matrix dictionary.

	Parameters
	----------
	dataType: string, Required
		The type of data to be imported.  Valid options are 'nodes', 'arcs', 'assignments', or 'matrix'.
	filename: string, Required
		The path and the name of the file to be imported.

	Return
	------
	pandas.dataframe or dictionary
		The resulting object depends on the data that are imported.  If the data are 'nodes', 'arcs' or 'assignments', return pandas.dataframe; otherwise, if the data are 'matrix', return dictionary.

	Examples
	--------
	The following examples will be the same as examples in :meth:`~veroviz.utilities.exportDataToCSV`

	Import veroviz and check if it is the latest version:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Create a nodes dataframe:
		>>> nodesDF = vrv.createNodesFromLocs(
		...              locs = [[42.1538, -78.4253], 
		...                      [42.3465, -78.6234], 
		...                      [42.6343, -78.1146]])
		>>> nodesDF	

	Save the nodesDF dataframe as a .csv file in a subdirectory named "test":
		>>> vrv.exportDataToCSV(data = nodesDF, filename = 'test/nodes.csv')
	
	Import the dataframe we just saved:
		>>> importedNodes = vrv.importDataFromCSV(
		...     dataType = 'nodes',
		...     filename = 'test/nodes.csv')
		>>> importedNodes

	If the data type is inconsistent with the data, an error message will be thrown and nothing will be imported.
		>>> importedArcs = vrv.importDataFromCSV(
		...     dataType = 'arcs', 
		...     filename = 'test/nodes.csv')
		Error: test/nodes.csv was not successfully imported.  Check the data type.

	Similarly we can import and export the 'arcs' and 'assignments' dataframe

	For time/distance matrices, they are saved as dictionaries in VeRoViz, here is an example of how to import/export them.

	Get travel time/distance matrices using the nodes we just created:
		>>> [timeDict, distDict] = vrv.getTimeDist2D(
		...           nodes        = nodesDF, 
		...           routeType    = 'fastest', 
		...           dataProvider = 'OSRM-online')
		>>> timeDict
		{(1, 1): 0.0,
		 (1, 2): 2869.9,
		 (1, 3): 4033.9,
		 (2, 1): 2853.3,
		 (2, 2): 0.0,
		 (2, 3): 4138.2,
		 (3, 1): 4037.8,
		 (3, 2): 4055.4,
		 (3, 3): 0.0}

	Export the time dictionary to a .csv file in a subdirectory named "test":
		>>> vrv.exportDataToCSV(data = timeDict, filename = 'test/timeMatrix.csv')

	Import the saved dictionary
		>>> importedTime = vrv.importDataFromCSV(
		...     dataType = 'matrix',
		...     filename = 'test/timeMatrix.csv')
		>>> importedTime
		{(1, 1): 0.0,
		 (1, 2): 2869.9,
		 (1, 3): 4033.9,
		 (2, 1): 2853.3,
		 (2, 2): 0.0,
		 (2, 3): 4138.2,
		 (3, 1): 4037.8,
		 (3, 2): 4055.4,
		 (3, 3): 0.0}

	"""

	# Make sure both input args are provided:
	if ((dataType is None) or (filename is None)):
		print("Error: 1 or more of the 2 required input parameters to function `importDataFromCSV()` are missing.")
		return

	# Replace backslash
	filename = replaceBackslashToSlash(filename)

	if (type(filename) is not str):
		print("Error: filename should be a string, please check the inputs.")
		return

	# validation - The validation of this script is different from others
	try:
		if (dataType.lower() in {'nodes', 'arcs', 'assignments'}):
			data = pd.read_csv(filename, index_col=0)
			if (dataType.lower() == 'nodes'):
				[valFlag, errorMsg, warningMsg] = valNodes(data)
				if (valFlag and warningMsg == ""):
					# print("Message: %s was successfully imported as Nodes dataframe" % filename)
					pass
				else:
					print("%s  %s was not successfully imported." % (errorMsg, filename))
					return
			elif (dataType.lower() == 'arcs'):
				[valFlag, errorMsg, warningMsg] = valArcs(data)
				if (valFlag and warningMsg == ""):
					# print("Message: %s was successfully imported as Arcs dataframe" % filename)
					pass
				else:
					print("%s  %s was not successfully imported." % (errorMsg, filename))
					return
			elif (dataType.lower() == 'assignments'):
				[valFlag, errorMsg, warningMsg] = valAssignments(data)
				if (valFlag and warningMsg == ""):
					# print("Message: %s was successfully imported as Assignments dataframe" % filename)
					pass
				else:
					print("%s  %s was not successfully imported." % (errorMsg, filename))
					return
			else:
				return

		elif (dataType.lower() == 'matrix'):
			dataframe = pd.read_csv(filename, index_col=0)
			dataframe.columns = dataframe.columns.astype(int)
			data = convertMatricesDataframeToDictionary(dataframe)
		else:
			print("Error: data type not supported.  Expected 'nodes', 'arcs', 'assignments' or 'matrix' (for time matrix or distance matrix)")

	except (TypeError, ValueError):
		print("Error: Cannot import file: %s, check if `dataType` is correct for inputs." % (filename))

	except IOError:
		print("Error: Cannot import file: %s" % (filename))

	return data

def exportDataframe(dataframe=None, filename=None):
	"""
	Exports a nodes, arcs, or assignments dataframe to a `.csv` file.

	Parameters
	----------
	dataframe: pandas.dataframe, Required
		The dataframe to be exported.  This can be a :ref:`Nodes`, :ref:`Arcs`, or :ref:`Assignments` dataframe.
	filename: string, Required
		The path and the name of file to be exported.

	Example
	-------	
	Import veroviz and check if it is the latest version:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()
	
	Create a nodes dataframe:
		>>> nodesDF = vrv.createNodesFromLocs(locs=[
		...     [42.1538, -78.4253], 
		...     [42.3465, -78.6234], 
		...     [42.6343, -78.1146]])
		>>> nodesDF
	
	Save the nodesDF dataframe as a .csv file in a subdirectory named "test":
		>>> vrv.exportDataframe(dataframe = nodesDF, filename = 'test/nodes.csv')
	
	Import the saved dataframe:
		>>> importedNodesDF = vrv.importDataframe('test/nodes.csv')
		>>> importedNodesDF
	"""

	# Make sure both input args are provided:
	if ((dataframe is None) or (filename is None)):
		print("Error: 1 or more of the 2 required input parameters to function `exportDataframe()` are missing.")
		return

	return privExportDataframe(dataframe, filename)
	

def importDataframe(filename=None, intCols=False, useIndex=True):
	"""
	Imports a VeRoViz nodes, arcs, or assignments dataframe from a .csv file.  This function returns a pandas dataframe.

	Parameters
	----------
	filename: string, Required
		The path and the name of the file to be imported.
	intCols: boolean, Optional, default as False
		If the dataframe column names are integers (rather than text), set `intCols` to be True.  See notes below for more information.
	useIndex: boolean, Optional, default as True
		Setting this value to True means that the first column in the .csv will be used as the row indices.

	Note
	----
	If the dataframe is one of the following, the column names are not integers; leave `intCols=False` (default).  Also, leave `useIndex=True` (default):
	
	- nodes
	- arcs
	- assignments

	If you are importing the following matrices, it is recommended to use `importDataFromCSV()` function, the return value of that function will be a dictionary for matrix.

	- time matrix
	- distance matrix

	Return
	------
	pandas.dataframe
		A dataframe constructed from the contents of the imported .csv file.

	Example
	-------	
	Import veroviz and check if it is the latest version:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()
	
	Create a nodes dataframe:
		>>> nodesDF = vrv.createNodesFromLocs(locs=[
		...     [42.1538, -78.4253], 
		...     [42.3465, -78.6234], 
		...     [42.6343, -78.1146]])
		>>> nodesDF
	
	Save the nodesDF dataframe as a .csv file in a subdirectory named "test":
		>>> vrv.exportDataframe(dataframe = nodesDF, filename = 'test/nodes.csv')
	
	Import the saved dataframe:
		>>> importedNodesDF = vrv.importDataframe('test/nodes.csv')
		>>> importedNodesDF
	"""

	# Make sure filename is provided
	if (filename is None):
		print("Error: filename is missing as an input to function `importDataframe()`.")
		return

	# Replace backslash
	filename = replaceBackslashToSlash(filename)

	if (type(filename) is not str):
		print("Error: filename should be a string, please check the inputs.")
		return

	df = None
	
	try:
		if (useIndex):
			df = pd.read_csv(filename, index_col=0)	
		else:
			df = pd.read_csv(filename, index_col=False)	
		if (intCols):
			df.columns = df.columns.astype(int)
	except:
		print("Error: Cannot import %s, please check the inputs." % (filename))

	return df

def getConvexHull(locs=None):
	"""
	Find the convex hull of a set of points.
	
	Parameters
	----------
	locs: list of lists
		A list of individual locations, in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.

	Returns
	-------
	list of lists
		A list of lat/lon coordinates of the convex hull.  This is in the same form as the input points.
		
	Example
	-------
		>>> # Find the convex hull of 5 locs that straddle the Prime Meridian:
		>>> import veroviz as vrv
		>>> locs = [[51.4865,  0.0008], 
		...         [51.4777, -0.0002], 
		...         [51.4801,  0.0029], 
		...         [51.4726, -0.0161], 
		...         [51.4752,  0.0158]]
		>>> convexHull = vrv.getConvexHull(locs)
		>>> convexHull
		[[51.4726, -0.0161], [51.4865, 0.0008], [51.4752, 0.0158]]


		>>> # Display the 5 locations and the convex hull on a map:
		>>> myMap = None
		>>> for loc in locs:
		...     myMap = vrv.addLeafletMarker(mapObject=myMap, center=loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject=myMap, points=convexHull)
		>>> myMap
	"""
	
	# FIXME -- How does this work when crossing meridians?
	# I did some simple tests and it seems to be OK.

	[valFlag, errorMsg, warningMsg] = valGetConvexHull(locs)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	locs2D = []
	for i in range(len(locs)):
		locs2D.append([locs[i][0], locs[i][1]])
	
	ch2D = [locs[i] for i in scipy.spatial.ConvexHull(locs2D).vertices]

	ch = []
	for i in range(len(ch2D)):
		for j in range(len(locs2D)):
			if (abs(ch2D[i][0] - locs2D[j][0]) < 0.0001 and abs(ch2D[i][1] - locs2D[j][1]) < 0.0001):
				ch.append(locs[j])

	return ch

def isPointInPoly(loc=None, poly=None):
	"""
	Determine if a point is inside a polygon.  Points that are along the perimeter of the polygon (including vertices) are considered to be "inside".

	Parameters
	----------
	loc: list, Required
		The coordinate of the point, in either [lat, lon] or [lat, lon, alt] format.  If provided, the altitude will be ignored.
	poly: list of lists, Required
		A polygon defined as a list of individual locations, in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored. 

	Returns
	-------
	boolean
		The point is inside the polygon or not

	Examples
	--------
	Import veroviz:
		>>> import veroviz as vrv

	Example 1 - Location is inside polygon:
		>>> loc = [42.03, -78.05]
		>>> poly = [[42.00, -78.00], [42.10, -78.10], [42.00, -78.10]]
		>>> vrv.isPointInPoly(loc, poly)
		True
		
		>>> myMap = vrv.addLeafletMarker(center = loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap
	
	Example 2 - Location is outside polygon:
		>>> loc = [42.07, -78.05]
		>>> poly = [[42.00, -78.00], [42.10, -78.10], [42.00, -78.10]]
		>>> vrv.isPointInPoly(loc, poly)
		False

		>>> myMap = vrv.addLeafletMarker(center = loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 3 - Location is on the polygon boundary:
		>>> loc = [42.05, -78.10]
		>>> poly = [[42.00, -78.00], [42.10, -78.10], [42.00, -78.10]]
		>>> vrv.isPointInPoly(loc, poly)
		True

		>>> myMap = vrv.addLeafletMarker(center = loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap
						
	Example 4 - Location is on a polygon vertex:
		>>> loc = [42.10, -78.10]
		>>> poly = [[42.00, -78.00], [42.10, -78.10], [42.00, -78.10]]
		>>> vrv.isPointInPoly(loc, poly)
		True
		
		>>> myMap = vrv.addLeafletMarker(center = loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap
		
	Example 5 - Non-convex poly region:
		>>> loc = [42.50, -78.90]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [42.2, -78.5], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPointInPoly(loc, poly)

		>>> myMap = vrv.addLeafletMarker(center = loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap
		
	Example 6 - Altitudes are included (but ignored):
		>>> loc = [42.05, -78.10, 100]
		>>> poly = [[42.00, -78.00, 200], [42.10, -78.10, 300], [42.00, -78.10, 200]]
		>>> vrv.isPointInPoly(loc, poly)		
		True
		
		>>> myMap = vrv.addLeafletMarker(center = loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap
				
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valIsPointInPoly(loc, poly)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	loc2D = [loc[0], loc[1]]
	poly2D = []
	for i in range(len(poly)):
		poly2D.append([poly[i][0], poly[i][1]])

	inside = geoIsPointInPoly(loc2D, poly2D)
		
	return inside

def isPathInPoly(path=None, poly=None):
	"""
	Determine if a given path is completely within the boundary of a polygon. 

	Parameters
	----------
	path: list of lists, Required
		A list of coordinates in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  This is considered as an open polyline.
	poly: list of lists, Required
		A closed polygon defined as a list of individual locations, in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.
	
	
	Returns
	-------
	boolean
		True if the path lies entirely inside the polygon; False if at least one point of the path is not inside polygon.

	Examples
	--------
	Import veroviz:
		>>> import veroviz as vrv

	Example 1 - Entire path is inside polygon:
		>>> path = [[42.50, -78.10], [42.50, -78.50], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathInPoly(path, poly)
		True
		
		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 2 - One of the vertices is on the edge of the polygon:
		>>> path = [[42.50, -78.10], [43.00, -78.50], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathInPoly(path, poly)
		False

		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 3 - Part of the path is outside of the polygon:
		>>> path = [[42.50, -78.10], [43.10, -78.50], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathInPoly(path, poly)
		False
		
		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 4 - Endpoints are in the polygon, but the poly isn't convex:
		>>> path = [[42.50, -78.10], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [42.2, -78.5], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathInPoly(path, poly)
		True
		
		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 5 - Path and poly coordinates include altitude (which is ignored):
		>>> path = [[42.50, -78.10, 100], [42.50, -78.90, 200]]
		>>> poly = [[42.00, -78.00, 100], 
		...         [43.00, -78.00, 100], 
		...         [42.2, -78.5, 100], 
		...         [43.00, -79.00, 200], 
		...         [42.00, -79.00, 200]]
		>>> vrv.isPathInPoly(path, poly)
		True
		
		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valIsPathInPoly(path, poly)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	path2D = []
	for i in range(len(path)):
		path2D.append([path[i][0], path[i][1]])
	poly2D = []
	for i in range(len(poly)):
		poly2D.append([poly[i][0], poly[i][1]])

	inside = geoIsPathInPoly(path2D, poly2D)

	return inside

def isPathCrossPoly(path=None, poly=None):
	"""
	Determine if a given path crosses the boundary of a polygon.

	Parameters
	----------
	path: list of lists, Required
		A list of coordinates in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  This is considered as an open polyline.
	poly: list of lists, Required
		A closed polygon defined as a list of individual locations, in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.

	Returns
	-------
	boolean
		True if the path have intersection with the polygon, false if no intersection

	Examples
	--------
	First import veroviz
		>>> import veroviz

	Example 1 - Entire path is inside poly
		>>> path = [[42.50, -78.10], [42.50, -78.50], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathCrossPoly(path, poly)
		False

		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 2 - One of the vertices is on the edge of poly
		>>> path = [[42.50, -78.10], [43.00, -78.50], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathCrossPoly(path, poly)
		True

		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 3 - Part of the path is outside of poly:
		>>> path = [[42.50, -78.10], [43.10, -78.50], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathCrossPoly(path, poly)
		True
		
		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap
		
	Example 4 - Endpoints are in poly, but poly isn't convex:
		>>> path = [[42.50, -78.10], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [42.2, -78.5], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathCrossPoly(path, poly)
		False

		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap	
		
	Example 5 - Path and poly include altitudes (which are ignored):
		>>> path = [[42.50, -78.10, 100], [42.50, -78.90, 300]]
		>>> poly = [[42.00, -78.00, 100], 
		...         [43.00, -78.00, 200], 
		...         [42.2, -78.5, 100], 
		...         [43.00, -79.00, 300], 
		...         [42.00, -79.00, 100]]
		>>> vrv.isPathCrossPoly(path, poly)	
		
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valIsPathCrossPoly(path, poly)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	path2D = []
	for i in range(len(path)):
		path2D.append([path[i][0], path[i][1]])
	poly2D = []
	for i in range(len(poly)):
		poly2D.append([poly[i][0], poly[i][1]])

	crossFlag = geoIsPathCrossPoly(path2D, poly2D)

	return crossFlag

def isPassPath(loc=None, path=None, tolerance=None):
	'''
	Determine if any point along a path is within tolerance meters of a stationary point (i.e., did our path pass by the target?).

	Parameters
	----------
	loc: list, Required
		The stationary point to be tested if it has been passed, in either [lat, lon] or [lat, lon, alt] format.  If provided, the altitude will be ignored.
	path: list of lists, Required
		A list of coordinates in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  This is considered as an open polyline.
	tolerance: float, Required
		How close must the path be to the stationary location to be considered as "passed".  The units are in meters.
	
		
	Returns
	-------
	boolean
		Whether or not the path passes the point.

	Examples
	--------
	Prepare some data
		>>> import veroviz
		>>> path = [[42.50, -78.10], [42.50, -78.90]]

	Example 1 - The distance from the location to the path exceeds the tolerance.
		>>> awayLoc = [42.51, -78.50]
		>>> vrv.isPassPath(awayLoc, path, 1000)
		False
		
		>>> # Find the minimum distance, in meters, from the location to the path:
		>>> vrv.minDistLoc2Path(awayLoc, path)
		1105.9845259826711

		>>> myMap = vrv.addLeafletMarker(center = awayLoc)
		>>> myMap = vrv.addLeafletPolyline(mapObject = myMap, points = path)
		>>> myMap

	Example 2 - The distance from the location to the path is within the tolerance.
		>>> closeLoc = [42.505, -78.50]
		>>> vrv.isPassPath(closeLoc, path, 1000)
		True
		
		>>> # Find the minimum distance, in meters, from the location to the path:
		>>> vrv.minDistLoc2Path(closeLoc, path)	
		550.5689415111023
		
		>>> myMap = vrv.addLeafletMarker(center = closeLoc)
		>>> myMap = vrv.addLeafletPolyline(mapObject = myMap, points = path)
		>>> myMap
		
	Example 3 - Location and path include altitudes (which are ignored):
		>>> loc  = [42.505, -78.50, 100]
		>>> path = [[42.50, -78.40, 100], 
		...         [42.50, -78.60, 200], 
		...         [42.40, -78.70, 100]]
		>>> vrv.isPassPath(loc, path, 1000)
	'''

	# validation
	[valFlag, errorMsg, warningMsg] = valIsPassPath(loc, path, tolerance)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	loc2D = [loc[0], loc[1]]
	path2D = []
	for i in range(len(path)):
		path2D.append([path[i][0], path[i][1]])

	passFlag = geoIsPassPath(loc2D, path2D, tolerance)

	return passFlag

def pointInDistance2D(loc=None, direction=None, distMeters=None):
	"""
	Find the [lat, lon, alt] coordinate of a point that is a given distance away from a current location at a given heading. This can be useful for determining where a vehicle may be in the future (assuming constant velocity and straight-line travel).

	Parameters
	----------
	loc: list, Required
		The starting location, expressed as either [lat, lon, alt] or [lat, lon]. If no altitude is provided, it will be assumed to be 0 meters above ground level.		
	direction: float, Required
		The direction of travel from the current location, in units of degrees.  The range is [0, 360], where north is 0 degrees, east is 90 degrees, south is 180 degrees, and west is 270 degrees.
	distMeters: float, Required
		The straight-line distance to be traveled, in meters, from the current location in the given direction.

	Returns
	-------
	list
		A location a given distance away from the given location, in [lat, lon, alt] form.

	Example
	-------
		>>> import veroviz as vrv
		>>> startPt  = [42.80, -78.30, 200]
		>>> heading  = 45 # degrees. travel northeast.
		>>> distance = 300 # meters.
		>>> 
		>>> endPt = vrv.pointInDistance2D(startPt, heading, distance)
		>>> endPt
		
		>>> myArc = vrv.createArcsFromLocSeq(locSeq = [startPt, endPt])
		>>> myMap = vrv.createLeaflet(arcs=myArc)
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=startPt, fillColor='red')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=endPt, fillColor='green')
		>>> myMap
	"""
	
	# validation
	[valFlag, errorMsg, warningMsg] = valPointInDistance2D(loc, direction, distMeters)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	loc2D = [loc[0], loc[1]]

	newLoc = geoPointInDistance2D(loc2D, direction, distMeters)

	if (len(loc) == 3):
		newLoc = [newLoc[0], newLoc[1], loc[2]]

	return newLoc

def minDistLoc2Path(loc=None, path=None):
	"""
	Calculate the minimum distance, in [meters], from a single stationary location (target) to any point along a path.

	Parameters
	----------
	loc: list, Required
		The coordinate of the stationary location, in either [lat, lon] or [lat, lon, alt] format.  If provided, the altitude will be ignored.
	path: list of lists, Required
		A list of coordinates in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  

	Returns
	-------
	float
		The minimum distance, in meters, between the stationary location and the given polyline (path).

	Examples
	--------
	Prepare some data
		>>> import veroviz
		>>> path = [[42.50, -78.10], [42.50, -78.90]]
		>>> loc1 = [42.50, -78.50]
		>>> loc2 = [42.51, -78.50]
		>>> loc3 = [42.51, -78.00]

	Example 1 - The location is on the path:
		>>> vrv.minDistLoc2Path(loc1, path)
		0.0

	Example 2 - The minimum distance is between points on the path:
		>>> vrv.minDistLoc2Path(loc2, path)
		1105.9845259826711
		
	Example 3 - The minimum distance is to an endpoint of the path:
		>>> vrv.minDistLoc2Path(loc3, path)
		8293.970453010765

	Show the objects on a map:
		>>> myMap = vrv.addLeafletMarker(center=loc1, fillColor='blue')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=loc2, fillColor='green')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=loc3, fillColor='purple')
		>>> myMap = vrv.addLeafletPolyline(mapObject=myMap, points=path)
		>>> myMap
		
	Example 4 - The location and path include altitudes (which are ignored):
		>>> path2 = [[42.50, -78.40, 100], 
		...          [42.50, -78.60, 200], 
		...          [42.40, -78.70, 100]]
		>>> loc4  = [42.51, -78.3, 300]
		>>> vrv.minDistLoc2Path(loc4, path2)

	"""

	[valFlag, errorMsg, warningMsg] = valMinDistLoc2Path(loc, path)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	distMeters = geoMinDistLoc2Path(loc, path)

	return distMeters

def closestPointLoc2Path(loc=None, path=None):
	"""
	Finds the point along a given line that is closest to a given location.  Returns the [lat, lon] coordinates of the point, and the corresponding distance (in [meters]) from that point to the line.

	Parameters
	----------
	loc: list, Required
		The coordinate of the current coordinate, in [lat, lon, alt] format.
	path: list of lists, Required
		Specifies the ordered collection of lat/lon coordinates comprising a path.   This must be a list of lists, of the form `[[lat1, lon1], [lat2, lon2], ..., [latn, lonn]]` or `[[lat1, lon1, alt1], [lat2, lon2, alt2], ..., [latn, lonn, altn]]`.  If an altitude is provided with each coordinate, this component will be ignored. 	

	Returns
	-------
	minLoc: list specifying a location, in [lat, lon] format.
	distMeters: The distance from the given location to minLoc.

	Examples
	--------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Prepare some data
		>>> import veroviz
		>>> path = [[42.50, -78.65], [42.50, -78.40]]
		>>> loc1 = [42.50, -78.50]
		>>> loc2 = [42.51, -78.50]

	Draw the line and the 2 points on the map:
		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletMarker(mapObject = myMap,
		...                              center = loc1, 
		...                              radius = 14,
		...                              text='1', fontColor='black')
		>>> myMap = vrv.addLeafletMarker(mapObject = myMap,
		...                              center = loc2, 
		...                              radius = 14,
		...                              text='2', fontColor='black')
		>>> myMap

	Example 1 - The location is on the path:
		>>> vrv.closestPointLoc2Path(loc1, path)
		([42.5, -78.5], 0.0)

	Example 2 - The minimum distance is between points on the path:
		>>> vrv.closestPointLoc2Path(loc2, path)
		([42.5, -78.50000397522506], 1103.5612443321572)

	Example 3 - The location and path include altitudes (which are ignored):
		>>> path2 = [[42.50, -78.40, 100],
		...          [42.50, -78.60, 200],
		...          [42.40, -78.70, 100]]
		>>> loc3  = [42.51, -78.3, 300]
		>>> vrv.closestPointLoc2Path(loc3, path2)
		([42.5, -78.6, 0], 8293.970453010768)
		
	Draw the line, the reference point, and the nearest point on the map:
		>>> myMap = vrv.addLeafletPolyline(points = path2)
		>>> myMap = vrv.addLeafletMarker(mapObject = myMap,
		...                              center = loc3, 
		...                              radius = 14,
		...                              text='3', fontColor='black')
		>>> myMap = vrv.addLeafletMarker(mapObject = myMap, center = nearestPt, radius = 12)
		>>> myMap		
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valClosestPointLoc2Path(loc, path)
	if (not valFlag):
		print (errorMsg)
		return (None, None)
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	(minPoint, distMeters) = privClosestPointLoc2Path(loc, path)

	return (minPoint, distMeters)
	
	
def closestPointLoc2Assignments(loc=None, assignments=None, objectID=None, ignoreStaticPoints=True):

	"""
	Finds the point along each path defined by the given assignments dataframe that is closest to a given location.  Returns the [lat, lon] coordinates of these points, and the corresponding distance (in [meters]) from each point to the each path.

	Returns a dictionary of lists of dictionaries.  The first dictionary's keys are objectIDs found in the 'assignments' dataframe.  For each 'objectID', a list is provided.  This list will contain the nearest point and the distance from the given location to that point.  If the objectID does not have any consecutive rows in the 'assignments' dataframe where the ending location differs from the starting location in the next row, then there will be only one result for each objectID.  

	Parameters
	----------
	loc: list, Required
		The coordinate of the current coordinate, in [lat, lon, alt] format.
	assignments: An :ref:`Assignments` dataframe, Required, default as None
		Each row of an :ref:`Assignments` dataframe describes the starting and ending location of an object, with corresponding start and end times (in seconds).
	objectID: string, Optional, default as None
		This is an identifier for each object in the `assignments` dataframe.  If `objectID` is None, then paths will be returned for each unique `objectID` found in the `assignments` dataframe.  Otherwise, only paths associated with the given `objectID` will be returned.
	ignoreStaticPoints: Boolean, Optional, default as True
		Static (stationary) points are rows in the 'assignments' dataframe where the starting and ending locations are identical.  If these are included in the path, you get a path segment of zero distance.  By default, we'll ignore these points, so each segment of the line is of non-zero distance.
	
	Returns
	-------
	A nested dictionary.  The keys of this dictionary are objectIDs.  For each objectID, a list is provided, where each list corresponds to a path associated with the objectID.  For each list, a dictionary containing keys of `nearestPt` (a list of the form [lat, lon]) and `distMeters` (a scalar) is provided.
	
	Example
	--------
	Import veroviz and check if the version is up-to-date
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	We'll begin by generating some data, which will be used by the `closestPointLoc2Assignments()` function.

		>>> # Specify 4 locations that could be visited:
		... locs = [[42.1648, -78.4293], 
		...         [42.1565, -78.4234], 
		...         [42.1443, -78.4246],
		...         [42.1113, -78.4212]]
        
        
		>>> # Now, create an :ref:`Assignments` dataframe for two vehicles (a truck and a car).  
		... 
		... # The truck will visit nodes 1 and 2.  
		... exampleAssignments = vrv.createAssignmentsFromLocSeq2D(
		...     locSeq         = locs[0:2],
		...     serviceTimeSec = 30.0,
		...     objectID       = 'Truck',
		...     routeType      = 'fastest',
		...     dataProvider   = 'OSRM-online',
		...     leafletColor   = 'red')
		... 
		... # The truck will then pause 45 seconds before taking a route from node 4 to node 3. 
		... # There is an obvious break in these routes.  
		... exampleAssignments = vrv.createAssignmentsFromLocSeq2D(
		...     initAssignments = exampleAssignments,
		...     locSeq          = locs[-1:1:-1],
		...     serviceTimeSec  = 30.0,
		...     startTimeSec    = max(exampleAssignments['endTimeSec']) + 45,
		...     objectID        = 'Truck',
		...     routeType       = 'fastest',
		...     dataProvider    = 'OSRM-online',
		...     leafletColor    = 'green')
		... 
		... # The car will visit nodes 1 and 4.
		... exampleAssignments = vrv.createAssignmentsFromLocSeq2D(
		...     initAssignments = exampleAssignments,
		...     locSeq          = [locs[0], locs[3]],
		...     serviceTimeSec  = 30.0,
		...     objectID        = 'Car',
		...     routeType       = 'fastest',
		...     dataProvider    = 'OSRM-online',
		...     leafletColor    = 'blue') 
        
        
	Visualize the locations and assignments. Generate a :ref:`Nodes` dataframe from a list of coordinates.  See :meth:`~veroviz.generateNodes.generateNodes` for other methods to generate "nodes" dataframes. 
		>>> exampleNodes = vrv.createNodesFromLocs(locs = locs)
		>>> myMap = vrv.createLeaflet(nodes = exampleNodes, arcs = exampleAssignments)
		>>> myMap

	Specify a location:
		>>> loc = [42.1382899, -78.3887493]
	
	Add a marker for the given location:
		>>> myMap = vrv.addLeafletMarker(mapObject = myMap,
		...                              center = loc, 
		...                              radius = 30,
		...                              text='Loc', fontColor='black')
		>>> myMap

	Find the nearest point to the given location for each vehicle in the assignments dataframe.  Note: The truck has two separate paths, so it will have two nearest points (one for each path).
		>>> closestPoints = vrv.closestPointLoc2Assignments(
		...	    loc                = loc, 
		...	    assignments        = exampleAssignments, 
		...	    objectID           = None, 
		...	    ignoreStaticPoints = True)	
		>>> closestPoints
		{'Truck': [{'nearestPoint': [42.157619, -78.422146], 'distMeters': 15506.568584267798},
		           {'nearestPoint': [42.129462, -78.409906], 'distMeters': 14152.410369937512}],
		  'Car':  [{'nearestPoint': [42.150689, -78.398545], 'distMeters': 13441.061529262752}]}		
		
	Plot these points on the map:
		>>> for objectID in closestPoints:
		...	    for i in range(0, len(closestPoints[objectID])):
		...	        myMap = vrv.addLeafletMarker(mapObject = myMap, 
		...	                                     center    = closestPoints[objectID][i]['nearestPoint'],
		...	                                     radius    = 14)
		>>>	myMap 	
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valClosestPointLoc2Assignments(loc, assignments, objectID, ignoreStaticPoints)
	if (not valFlag):
		print (errorMsg)
		return (None, None)
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
	
	paths = privAssignmentsToPaths(assignments, objectID, ignoreStaticPoints)
	
	closestPoints = {}
	for tmpObjectID in paths:
		closestPoints[tmpObjectID] = []
		for i in range(0, len(paths[tmpObjectID])):
			(minPoint, distMeters) = privClosestPointLoc2Path(loc, paths[tmpObjectID][i])
			closestPoints[tmpObjectID].append({'nearestPoint': minPoint, 'distMeters': distMeters})

	return closestPoints	
	
	
def closestPointLoc2Arcs(loc=None, arcs=None, objectID=None, ignoreStaticPoints=True):

	"""
	Finds the point along each path defined by the given arcs dataframe that is closest to a given location.  Returns the [lat, lon] coordinates of these points, and the corresponding distance (in [meters]) from each point to the each path.

	Returns a dictionary of lists of dictionaries.  The first dictionary's keys are objectIDs found in the 'arcs' dataframe.  For each 'objectID', a list is provided.  This list will contain the nearest point and the distance from the given location to that point.  If the objectID does not have any consecutive rows in the 'arcs' dataframe where the ending location differs from the starting location in the next row, then there will be only one result for each objectID.  

	Parameters
	----------
	loc: list, Required
		The coordinate of the current coordinate, in [lat, lon, alt] format.
	arcs: An :ref:`Arcs` dataframe, Required, default as None
		Each row of an :ref:`Arcs` dataframe describes the starting and ending location of an object.
	objectID: string, Optional, default as None
		This is an identifier for each object in the `arcs` dataframe.  If `objectID` is None, then paths will be returned for each unique `objectID` found in the `arcs` dataframe.  Otherwise, only paths associated with the given `objectID` will be returned.
	ignoreStaticPoints: Boolean, Optional, default as True
		Static (stationary) points are rows in the 'arcs' dataframe where the starting and ending locations are identical.  If these are included in the path, you get a path segment of zero distance.  By default, we'll ignore these points, so each segment of the line is of non-zero distance.
	
	Returns
	-------
	A nested dictionary.  The keys of this dictionary are objectIDs.  For each objectID, a list is provided, where each list corresponds to a path associated with the objectID.  For each list, a dictionary containing keys of `nearestPt` (a list of the form [lat, lon]) and `distMeters` (a scalar) is provided.
	
	Example
	--------
	Import veroviz and check if the version is up-to-date
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Specify 4 locations that could be visited:
		>>> locs = [[42.1648, -78.4293], 
		...         [42.1565, -78.4234], 
		...         [42.1443, -78.4246],
		...         [42.1113, -78.4212]]
		
		>>> # Now, create an :ref:`Arcs` dataframe for two vehicles.  
		... 
		... # The truck will visit nodes 1 and 2. 		
		... exampleArcs = vrv.createArcsFromLocSeq(
		... 	locSeq       = locs[0:2],
		... 	objectID     = 'Truck',
		... 	leafletColor = 'red')
		... 
		... # The truck will then take a route from node 4 to node 3.  There is an obvious break in these routes.  
		... exampleArcs = vrv.createArcsFromLocSeq(
		... 	initArcs     = exampleArcs,
		... 	locSeq       = locs[-1:1:-1],
		... 	objectID     = 'Truck',
		... 	leafletColor = 'green')
		... 
		... # The car will visit nodes 1 and 4.
		... exampleArcs = vrv.createArcsFromLocSeq(
		... 	initArcs     = exampleArcs,
		... 	locSeq       = [locs[0], locs[3]],
		... 	objectID     = 'Car',
		... 	leafletColor = 'blue')		

	Visualize the locations and arcs. Generate a :ref:`Nodes` dataframe from a list of coordinates.  See :meth:`~veroviz.generateNodes.generateNodes` for other methods to generate "nodes" dataframes. 
		>>> exampleNodes = vrv.createNodesFromLocs(locs = locs)
		>>> myMap = vrv.createLeaflet(nodes = exampleNodes, arcs = exampleArcs)
		>>> myMap

	Specify a location:
		>>> loc = [42.1382899, -78.3887493]
	
	Add a marker for the given location:
		>>> myMap = vrv.addLeafletMarker(mapObject = myMap,
		...                              center = loc, 
		...                              radius = 30,
		...                              text='Loc', fontColor='black')

	Find the nearest point to the given location for each vehicle in the arcs dataframe.  Note: The truck has two separate paths, so it will have two nearest points (one for each path).
		>>> closestPoints = vrv.closestPointLoc2Arcs(
		...	    loc                = loc, 
		...	    arcs               = exampleArcs, 
		...	    objectID           = None, 
		...	    ignoreStaticPoints = True)	
		>>> closestPoints
		{'Truck': [{'nearestPoint': [42.157619, -78.422146], 'distMeters': 15506.568584267798},
		           {'nearestPoint': [42.129462, -78.409906], 'distMeters': 14152.410369937512}],
		  'Car':  [{'nearestPoint': [42.150689, -78.398545], 'distMeters': 13441.061529262752}]}		
		
	Plot these points on the map:
		>>> for objectID in closestPoints:
		...	    for i in range(0, len(closestPoints[objectID])):
		...	        myMap = vrv.addLeafletMarker(mapObject = myMap, 
		...	                                     center    = closestPoints[objectID][i]['nearestPoint'],
		...	                                     radius    = 14)
		>>>	myMap 	
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valClosestPointLoc2Arcs(loc, arcs, objectID, ignoreStaticPoints)
	if (not valFlag):
		print (errorMsg)
		return (None, None)
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
	
	paths = privArcsToPaths(arcs, objectID, ignoreStaticPoints)
	
	closestPoints = {}
	for tmpObjectID in paths:
		closestPoints[tmpObjectID] = []
		for i in range(0, len(paths[tmpObjectID])):
			(minPoint, distMeters) = privClosestPointLoc2Path(loc, paths[tmpObjectID][i])
			closestPoints[tmpObjectID].append({'nearestPoint': minPoint, 'distMeters': distMeters})

	return closestPoints
		
	
def closestNode2Loc(loc=None, nodes=None):
	"""
	Returns the closest node in the dataframe to the given location.  Also returns the Euclidean distance (in [meters]) from the location to the nearest node.

	Parameters
	----------
	loc: list, Required
		The coordinate of given location, in [lat, lon, alt] format.
	nodes: A :ref:`Nodes` dataframe, Required
		Dataframe containing an existing set of nodes.

	Returns
	-------
	minNodeID: int
		A node id of the closest node
	distMeters: float
		The minimum distance is returned

	Examples
	--------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Prepare some sample data.
		>>> # A single location:
		>>> loc1 = [42.885, -78.861]
		>>> 
		>>> # A collection of locations, which we'll
		>>> # convert to a "nodes" dataframe:
		>>> locs = [[42.8871085, -78.8731949],
		...         [42.8888311, -78.8649649],
		...         [42.8802158, -78.8660787],
		...         [42.8845705, -78.8762794],
		...         [42.8908031, -78.8770140]]
		>>> 
		>>> myNodes = vrv.createNodesFromLocs(locs = locs, 
		...                                   leafletIconPrefix = "custom", 
		...                                   leafletIconType   = "12-white-12")

	Example 1 - Closest node:
		>>> [nearestNode, distMeters] = vrv.closestNode2Loc(loc1, myNodes)
		>>> nearestNode, distMeters
		(2, 534.828771310757)

	Show the five nodes from the dataframe and the reference location:
		>>> myMap = vrv.createLeaflet(nodes = myNodes)
		>>> myMap = vrv.addLeafletIcon(mapObject = myMap, location = loc1, iconColor='red')
		>>> myMap
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valClosestNode2Loc(loc, nodes)
	if (not valFlag):
		print (errorMsg)
		return [None, None]
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	distMeters = sys.maxsize  # float('Inf')
	minNodeID = None

	for i in range(len(nodes)):
		nodeLat=nodes.iloc[i]['lat']
		nodeLon=nodes.iloc[i]['lon']
		tmpDistMeters = distance2D(loc, [nodeLat, nodeLon])

		if (tmpDistMeters < distMeters):
			distMeters = tmpDistMeters
			minNodeID = nodes.iloc[i]['id']

	if (minNodeID == None):
		return [None, None]

	return [minNodeID, distMeters]	
	
def nearestNodes(origin=None, nodes=None, k=1, costDict=None, metric='distance', routeType='euclidean2D', speedMPS=None, dataProvider=None, dataProviderArgs=None):
	"""
	Returns a pandas dataframe with 2 columns, 'id' and 'cost'.  The 'id' column represents a nodeID, the 'cost' represents either a time or a distance (consistent with the data provided by costDict).  The dataframe is sorted according to ascending values of 'cost'.  The top k rows are returned (i.e., the nearest k nodes).

	Parameters
	----------
	origin: list or integer, Required, default as None
		This function finds the k nearest nodes to this starting location.  `origin` can be a location, specified as a list of the form [lat, lon] or [lat, lon, alt].  If provided, the altitude will be ignored.  Alternatively, `origin` can be a nodeID.  In this case, `origin` must be a value in the 'id' column of the `nodes` input.
	nodes: :ref:`Nodes`, Required, default as None
		A :ref:`Nodes` dataframe containing the nodes representing destinations from the origin.
	k: integer, Required, default as 1
		This function finds the k nodes nearest to the origin.  If k <= 0, the function will simply return all nodes in ascending order of "cost" (excluding the `origin`, if `origin` is a nodeID).
	costDict: dictionary, Optional, default as None
		If provided, this should be one of the two output dictionaries from the VeRoViz getTimeDist2D() function.  If not provided, this information will be generated according to the fields below.
	metric: string, Conditional, default as 'distance'
		Indicates if "nearness" is according to 'time' or 'distance' (the two valid options for this parameter).  This parameter is only required if `origin` is a location ([lat, lon]) or if `costDict` is None, as this implies that the function will need to build a valid cost dictionary.  In other words, this parameter is ignored if `origin` is a valid nodeID and if `costDict` is not None.        
	routeType: string, Optional, default as 'euclidean2D'
		This describes a characteristic of the travel mode.  Possible values are: 'euclidean2D', 'manhattan', 'fastest', 'shortest', 'pedestrian', 'cycling', and 'truck'.  The 'euclidean2D' and 'manhattan' options are calculated directly from GPS coordinates, without a road network.  Neither of these two options require a data provider.  However, the other options rely on road network information and require a data provider.  Furthermore, some of those other options are not supported by all data providers.  See :ref:`Data Providers` for details.
	speedMPS: float, Conditional, default as None
		Speed of the vehicle, in units of meters per second. For route types that are not road-network based (i.e., 'euclidean2D' and 'manhattan'), this field is required to calculate travel times. Otherwise, if a route type already incorporates travel speeds from road network data, (i.e., 'fastest', 'shortest', and 'pedestrain'), this input argument may be ignored.  If provided, `speedMPS` will override travel speed data used by the route type option.
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for obtaining the travel data. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.

	Returns
	-------
	pandas dataframe

	Examples
	--------
	Import veroviz and check if the version is up-to-date
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Generate a :ref:`Nodes` dataframe from a list of coordinates.  See :meth:`~veroviz.generateNodes.generateNodes` for other methods to generate "nodes" dataframes.
		>>> locs = [
		...     [42.1538, -78.4253], 
		...     [42.3465, -78.6234], 
		...     [42.6343, -78.1146]]
		>>> exampleNodes = vrv.createNodesFromLocs(locs=locs)

	Example 1 - Find the k=1 node closest to node 3, according to Euclidean distance
		>>> vrv.nearestNodes(nodes = exampleNodes, origin = 3, k = 1)    

	Example 2 - Find the k=2 nodes closest to [42, -78], according to the travel time obtained from ORS-online.  This example includes all input parameters.
		>>> import os
		>>> ORS_API_KEY     = os.environ['ORSKEY']
		>>> # ORS_API_KEY   = 'YOUR_ORS_KEY_GOES_HERE'

		>>> vrv.nearestNodes(origin           = [42, -78], 
		...                  nodes            = exampleNodes, 
		...                  k                = 2, 
		...                  costDict         = None, 
		...                  metric           = 'time', 
		...                  routeType        = 'fastest',
		...                  speedMPS         = None, 
		...                  dataProvider     = 'ors-online', 
		...                  dataProviderArgs = {'APIkey': ORS_API_KEY})

	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valNearestNodes(origin, nodes, k, costDict, metric, routeType, speedMPS, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	
	# If origin is a [lat, lon], we need to create a node
	if (type(origin) is list):
		originType = 'loc'
		originNodeID = max(nodes['id']) + 1
		nodes = privCreateNodesFromLocs(locs=[origin], initNodes=nodes, 
										startNode=originNodeID, 
										dataProvider=dataProvider, 
										dataProviderArgs=dataProviderArgs)
	else:
		originType = 'node'
		originNodeID = origin


	if ((originType == 'loc') or (costDict is None)):
		# Need to get time or dist matrix
	
		# Specify the list of rows and columns of output dataframes
		# This is 'one2many'.
		fromRows = [originNodeID]
		toCols = nodes[nodes['id'] != originNodeID]['id'].tolist()

		# Specify lists of coordinates, in [lat, lon] format
		fromLocs = []
		toLocs = []
		for i in range(0, len(fromRows)):
			fromLocs.append([nodes.loc[nodes['id'] == fromRows[i], 'lat'].values[0], nodes.loc[nodes['id'] == fromRows[i], 'lon'].values[0]])
		for i in range(0, len(toCols)):
			toLocs.append([nodes.loc[nodes['id'] == toCols[i], 'lat'].values[0], nodes.loc[nodes['id'] == toCols[i], 'lon'].values[0]])

		if (routeType in ['euclidean2D', 'manhatan']):
			if (metric == 'distance'):
				speedMPS = 1   # dummy value

		# Get time/dist
		[timeSec, distMeters] = getTimeDistFromLocs2D(fromLocs=fromLocs, 
											 fromRows=fromRows, 
											 toLocs=toLocs, 
											 toCols=toCols, 
											 outputDistUnits='meters', 
											 outputTimeUnits='seconds', 
											 routeType=routeType, 
											 speedMPS=speedMPS, 
											 dataProvider=dataProvider, 
											 dataProviderArgs=dataProviderArgs)

		if (metric == 'distance'):
			costDict = distMeters
		else:
			costDict = timeSec
	
	return privNearestNodes(nodes, originNodeID, k, costDict)
	
	
def assignmentsToPaths(assignments=None, objectID=None, ignoreStaticPoints=True):
	"""
	Returns a dictionary of lists of paths.  The dictionary's keys are objectIDs found in the 'assignments' dataframe.  For each 'objectID', a list is provided.  This list will contain one or more paths associated with that objectID.  If the objectID does not have any consecutive rows in the 'assignments' dataframe where the ending location differs from the starting location in the next row, then there will be only one path.  

	Parameters
	----------
	assignments: An :ref:`Assignments` dataframe, Required, default as None
		Each row of an :ref:`Assignments` dataframe describes the starting and ending location of an object, with corresponding start and end times (in seconds).
	objectID: string, Optional, default as None
		This is an identifier for each object in the `assignments` dataframe.  If `objectID` is None, then paths will be returned for each unique `objectID` found in the `assignments` dataframe.  Otherwise, only paths associated with the given `objectID` will be returned.
	ignoreStaticPoints: Boolean, Optional, default as True
		Static (stationary) points are rows in the 'assignments' dataframe where the starting and ending locations are identical.  If these are included in the path, you get a path segment of zero distance.  By default, we'll ignore these points, so each segment of the line is of non-zero distance.
	
	Returns
	-------
	A dictionary of lists of paths

	Example
	--------
	Import veroviz and check if the version is up-to-date
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	We'll begin by generating some data, which will be used by the `assignmentsToPaths()` function.

		>>> # Specify 4 locations that could be visited:
		... locs = [[42.1648, -78.4293], 
		...         [42.1565, -78.4234], 
		...         [42.1443, -78.4246],
		...         [42.1113, -78.4212]]
        
        
		>>> # Now, create an :ref:`Assignments` dataframe for two vehicles (a truck and a car).  
		... 
		... # The truck will visit nodes 1 and 2.  
		... exampleAssignments = vrv.createAssignmentsFromLocSeq2D(
		...     locSeq         = locs[0:2],
		...     serviceTimeSec = 30.0,
		...     objectID       = 'Truck',
		...     routeType      = 'fastest',
		...     dataProvider   = 'OSRM-online',
		...     leafletColor   = 'red')
		... 
		... # The truck will then pause 45 seconds before taking a route from node 4 to node 3. 
		... # There is an obvious break in these routes.  
		... exampleAssignments = vrv.createAssignmentsFromLocSeq2D(
		...     initAssignments = exampleAssignments,
		...     locSeq          = locs[-1:1:-1],
		...     serviceTimeSec  = 30.0,
		...     startTimeSec    = max(exampleAssignments['endTimeSec']) + 45,
		...     objectID        = 'Truck',
		...     routeType       = 'fastest',
		...     dataProvider    = 'OSRM-online',
		...     leafletColor    = 'green')
		... 
		... # The car will visit nodes 1 and 4.
		... exampleAssignments = vrv.createAssignmentsFromLocSeq2D(
		...     initAssignments = exampleAssignments,
		...     locSeq          = [locs[0], locs[3]],
		...     serviceTimeSec  = 30.0,
		...     objectID        = 'Car',
		...     routeType       = 'fastest',
		...     dataProvider    = 'OSRM-online',
		...     leafletColor    = 'blue') 
        
        
	Visualize the locations and assignments. Generate a :ref:`Nodes` dataframe from a list of coordinates.  See :meth:`~veroviz.generateNodes.generateNodes` for other methods to generate "nodes" dataframes. 
		>>> exampleNodes = vrv.createNodesFromLocs(locs = locs)
		>>> vrv.createLeaflet(nodes = exampleNodes, arcs = exampleAssignments)


	Generate the paths for each vehicle:
		>>> myPaths = vrv.assignmentsToPaths(assignments=exampleAssignments, objectID=None, ignoreStaticPoints=True)
		
	Investigate some details of the output:	
		>>> len(myPaths['Truck'])
		2
		
		>>> myPaths['Truck']
		[[[42.16451, -78.429309], [42.164482, -78.427724], [42.157619, -78.422146]],
		 [[42.11118, -78.418862],
		  [42.120028, -78.41856],
		  [42.119975, -78.415146],
		  [42.121504, -78.414822],
		  [42.122706, -78.41427],
		  [42.126237, -78.412131],
		  [42.129462, -78.409906],
		  [42.130688, -78.413378],
		  [42.130762, -78.418572],
		  [42.130914, -78.420397],
		  [42.130984, -78.420506],
		  [42.137118, -78.428013],
		  [42.139694, -78.426846],
		  [42.142291, -78.424425],
		  [42.14424, -78.424135]]]
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valAssignmentsToPaths(assignments, objectID, ignoreStaticPoints)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)


	paths = privAssignmentsToPaths(assignments, objectID, ignoreStaticPoints)
	
	return paths
	    	
def arcsToPaths(arcs=None, objectID=None, ignoreStaticPoints=True):
	"""
	Returns a dictionary of lists of paths.  The dictionary's keys are objectIDs found in the 'arcs' dataframe.  For each 'objectID', a list is provided.  This list will contain one or more paths associated with that objectID.  If the objectID does not have any consecutive rows in the 'arcs' dataframe where the ending location differs from the starting location in the next row, then there will be only one path.  

	Parameters
	----------
	arcs: An :ref:`Arcs` dataframe, Required, default as None
		Each row of an :ref:`Arcs` dataframe describes the starting and ending location of an object.
	objectID: string, Optional, default as None
		This is an identifier for each object in the `arcs` dataframe.  If `objectID` is None, then paths will be returned for each unique `objectID` found in the `arcs` dataframe.  Otherwise, only paths associated with the given `objectID` will be returned.
	ignoreStaticPoints: Boolean, Optional, default as True
		Static (stationary) points are rows in the 'arcs' dataframe where the starting and ending locations are identical.  If these are included in the path, you get a path segment of zero distance.  By default, we'll ignore these points, so each segment of the line is of non-zero distance.
	
	Returns
	-------
	A dictionary of lists of paths

	Example
	--------
	Import veroviz and check if the version is up-to-date
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Specify 4 locations that could be visited:
		>>> locs = [[42.1648, -78.4293], 
		...         [42.1565, -78.4234], 
		...         [42.1443, -78.4246],
		...         [42.1113, -78.4212]]
		
		>>> # Now, create an :ref:`Arcs` dataframe for two vehicles.  
		... 
		... # The truck will visit nodes 1 and 2. 		
		... exampleArcs = vrv.createArcsFromLocSeq(
		... 	locSeq       = locs[0:2],
		... 	objectID     = 'Truck',
		... 	leafletColor = 'red')
		... 
		... # The truck will then take a route from node 4 to node 3.  There is an obvious break in these routes.  
		... exampleArcs = vrv.createArcsFromLocSeq(
		... 	initArcs     = exampleArcs,
		... 	locSeq       = locs[-1:1:-1],
		... 	objectID     = 'Truck',
		... 	leafletColor = 'green')
		... 
		... # The car will visit nodes 1 and 4.
		... exampleArcs = vrv.createArcsFromLocSeq(
		... 	initArcs     = exampleArcs,
		... 	locSeq       = [locs[0], locs[3]],
		... 	objectID     = 'Car',
		... 	leafletColor = 'blue')		

	Visualize the locations and arcs. Generate a :ref:`Nodes` dataframe from a list of coordinates.  See :meth:`~veroviz.generateNodes.generateNodes` for other methods to generate "nodes" dataframes. 
		>>> exampleNodes = vrv.createNodesFromLocs(locs = locs)
		>>> vrv.createLeaflet(nodes = exampleNodes, arcs = exampleArcs)

	Generate the paths for each vehicle:
		>>> myPaths = vrv.arcsToPaths(arcs=exampleArcs, objectID=None, ignoreStaticPoints=True)
		>>> myPaths
		{'Truck': [[[42.1648, -78.4293], [42.1565, -78.4234]],
		  [[42.1113, -78.4212], [42.1443, -78.4246]]],
		 'Car': [[[42.1648, -78.4293], [42.1113, -78.4212]]]}
		
	Investigate some details of the output:	
		>>> len(myPaths['Truck'])
		2
		
		>>> myPaths['Truck']
		[[[42.1648, -78.4293], [42.1565, -78.4234]],
		 [[42.1113, -78.4212], [42.1443, -78.4246]]]
 	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valArcsToPaths(arcs, objectID, ignoreStaticPoints)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	paths = privArcsToPaths(arcs, objectID, ignoreStaticPoints)
	
	return paths
	

def nodesToLocs(nodes=None, includeAlt=False):
	"""
	Returns a list of lists (i.e., locations) from a nodes dataframe.  If `includeAlt` is False (default), the return will be of the form [[lat,lon], ..., [lat,lon]]; otherwise, the return is of the form [[lat,lon,altMeters], ..., [lat,lon,altMeters]].  

	Parameters
	----------
	nodes: A :ref:`Nodes` dataframe, Required, default as None
		Dataframe containing a collection of nodes.
	includeAlt: Boolean, Optional, default as False
		If False, only latitude and longitude values are returned.  If True, the value in the `altMeters` column of the nodes dataframe is also returned with each lat/lon pair. 
	
	Returns
	-------
	A list of lists, with each sub-list representing the location of one node.

	Example
	--------
	Import veroviz and check if the version is up-to-date
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Generate 4 nodes:
		>>> exampleNodes = vrv.generateNodes(
		...     nodeDistrib      = 'normal', 
		...     nodeDistribArgs  = {
		...         'center'         : [42.90, -78.80], 
		...         'stdDev'         : 10000
		...     },
		...     numNodes         = 4)
		
	Convert to locations (including altitudes in meters):
		>>> vrv.nodesToLocs(exampleNodes, includeAlt=True)
		[[42.895314077862146, -78.80362790487085, 0.0],
		 [42.92242495208993, -78.82243490871062, 0.0],
		 [42.98842769922963, -78.74302258092918, 0.0],
		 [42.880876136692564, -78.81444943020881, 0.0]]		
	"""
	
	[valFlag, errorMsg, warningMsg] = valNodesToLocs(nodes, includeAlt)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	df = pd.DataFrame(nodes[['lat', 'lon', 'altMeters']])
	
	if (includeAlt):
		locs = list(map(list, zip(df.lat, df.lon, df.altMeters)))        
	else:
		locs = list(map(list, zip(df.lat, df.lon)))
	
	return locs 

	
def distance2D(loc1=None, loc2=None):
	"""
	Calculates the geodesic distance, in meters, between two locations, using the geopy library.  Altitude is ignored.

	Parameters
	----------
	loc1: list, Required
		First location, in [lat, lon] format.
	loc2: list, Required
		Second location, in [lat, lon] format.
	
	Return
	------
	float
		Geodesic distance, in meters, between the two locations.

	Example
	-------
		>>> import veroviz as vrv
		>>> loc1 = [42.80, -78.90]
		>>> loc2 = [42.82, -78.92]
		>>> dist2D = vrv.distance2D(loc1, loc2)
		>>> dist2D
		2759.0335974131926
	"""

	[valFlag, errorMsg, warningMsg] = valDistance2D(loc1, loc2)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
	
	distMeters = geoDistance2D(loc1, loc2)

	return distMeters

def distance3D(loc1=None, loc2=None):
	"""
	Estimates the distance, in meters, between two point, including changes in altitude.  The calculation combines geopy's geodesic distance (along the surface of an ellipsoidal model of the earth) with a simple estimate of additional travel distance due to altitude changes.

	Parameters
	----------
	loc1: list, Required
		First location, in [lat, lon, alt] format.
	loc2: list, Required
		Second location, in [lat, lon, alt] format.
	
	Return
	------
	float
		Distance, in meters, between the two locations.

	Example
	-------
		>>> import veroviz as vrv
		>>> loc1 = [42.80, -78.90, 0]
		>>> loc2 = [42.82, -78.92, 300]
		>>> dist3D = vrv.distance3D(loc1, loc2)
		>>> dist3D
		2775.2957304861734
	"""
	
	[valFlag, errorMsg, warningMsg] = valDistance3D(loc1, loc2)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	distMeters = geoDistance3D(loc1, loc2)

	return distMeters

def distancePath2D(path=None):
	"""
	Calculate the total geodesic distance, in meters, along a path defined by [lat, lon] coordinates.  

	Parameters
	----------
	path: list of lists, Required
		A list of coordinates that form a path, in the format of [[lat, lon], [lat, lon], ...].

	Return
	------
	float
		Total length of the path, in meters.

	Example
	-------
		>>> import veroviz as vrv
		>>> locs = [[42.80, -78.90], [42.82, -78.92], [42.84, -78.94]]
		>>> path = vrv.distancePath2D(locs)
		>>> path
		5517.760959357638
	"""

	[valFlag, errorMsg, warningMsg] = valDistancePath2D(path)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	dist = 0
	for i in range(0, len(path) - 1):
		dist += geoDistance2D(path[i], path[i + 1])

	return dist

def getHeading(currentLoc=None, goalLoc=None):
	"""
	Finds the heading required to travel from a current location to a goal location.  North is 0-degrees, east is 90-degrees, south is 180-degrees, west is 270-degrees.

	Parameters
	----------
	currentLoc: list, Required
		The [lat, lon] of current location
	goalLoc: list, Required
		The [lat, lon] of goal location

	Return
	------
	float
		Heading at current location towards goal location in degrees.

	Example
	-------
		>>> import veroviz as vrv
		>>> locCurrent = [42.80, -78.90]
		>>> locGoal    = [42.85, -78.85]
		>>> heading = vrv.getHeading(locCurrent, locGoal)
		>>> heading
		36.24057197338239
		
		>>> # View the arc from the current location to the goal:
		>>> arc = vrv.createArcsFromLocSeq(locSeq = [locCurrent, locGoal])
		>>> vrv.createLeaflet(arcs=arc)		
	"""

	[valFlag, errorMsg, warningMsg] = valGetHeading(currentLoc, goalLoc)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	bearingInDegree = geoGetHeading(currentLoc, goalLoc)

	return bearingInDegree

def findLocsAtTime(assignments=None, timeSec=0.0):
	"""
	Finds the estimated location of each unique `objectID` in an input `assignments` dataframe at the given time.  The output is a dictionary, where the keys are unique objectIDs.  The corresponding value for each `objectID` key will be `None` if the object is not defined at the given value of `timeSec`, the value will be a list of the form [lat, lon, alt] if a single match is found, or the value will be a list of lists of the form [[lat1, lon1, alt1], ..., [latn, lonn, altn]] if n matches are found.  In the latter case, this is typically indicative of duplicate entries in the assignments dataframe (as each object should not appear in multiple locations simultaneously).

	Parameters
	----------
	assignments: :ref:`Assignments` dataframe, Required, default as None
		Each row of an :ref:`Assignments` dataframe describes the starting and ending location of an object, with corresponding start and end times (in seconds).
	timeSec: float, Optional, default as 0.0
		The time, in seconds, at which it is desired to find an estimate of each object's location.
	
	Return
	------
	dictionary
		A dictionary describing the estimated location of each unique `objectID` in the input assignments dataframe.  See above for a description of the key/value pairs.

	Example
	-------
	Import veroviz and check if it's the latest version:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Define 5 node locations, as [lat, lon] pairs:
		>>> locs = [[42.8871085, -78.8731949],
		...         [42.8888311, -78.8649649],
		...         [42.8802158, -78.8660787],
		...         [42.8845705, -78.8762794],
		...         [42.8908031, -78.8770140]]

	Generate a nodes dataframe from these locations:
		>>> myNodes = vrv.createNodesFromLocs(locs=locs)

	Construct an assignments dataframe for two vehicles, a drone and a truck.  The truck will visit nodes 1 -> 2 -> 3 -> 1.  The drone will visit nodes 1 -> 4 -> 5 -> 1.
		>>> mySolution = {
		...     'truck': [[1,2], [2,3], [3,1]],
		...     'drone': [[1,4], [4,5], [5,1]]
		... }

	Define some information about our 2 vehicles, for use below:
		>>> vehicleProperties = {
		...     'drone': {'model': 'veroviz/models/drone.glb',
		...               'leafletColor': 'red',
		...               'cesiumColor': 'red'},
		...     'truck': {'model': 'veroviz/models/ub_truck.glb',
		...               'leafletColor': 'blue',
		...               'cesiumColor': 'blue'}
		... }

	This example assumes the use of ORS as the data provider. 
		>>> # If you have saved your API key as an environment variable, you may use `os.environ` to access it:
		>>> import os
		>>> ORS_API_KEY = os.environ['ORSKEY']
		>>> # Otherwise, you may specify your key here:
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'

	Initialize an empty assignments dataframe:
		>>> myAssignments = vrv.initDataframe('assignments')


	Build assignments for the truck route:
		>>> endTimeSec = 0.0
		>>> for arc in mySolution['truck']:
		...     [myAssignments, endTimeSec] = vrv.addAssignment2D(
		...             initAssignments  = myAssignments,
		...             objectID         = 'truck',
		...             modelFile        = vehicleProperties['truck']['model'],
		...             startLoc         = list(myNodes[myNodes['id'] == arc[0]][['lat', 'lon']].values[0]),
		...             endLoc           = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...             startTimeSec     = endTimeSec,
		...             leafletColor     = vehicleProperties['truck']['leafletColor'],
		...             cesiumColor      = vehicleProperties['truck']['cesiumColor'], 
		...             routeType        = 'fastest',
		...             dataProvider     = 'ORS-online', 
		...             dataProviderArgs = {'APIkey': ORS_API_KEY})
		>>> myAssignments
		
	Build assignments for the drone deliveries:
		>>> endTimeSec = 0.0
		>>> for arc in mySolution['drone']:
		...     [myAssignments, endTimeSec] = vrv.addAssignment3D(
		...         initAssignments    = myAssignments,
		...         objectID           = 'drone',
		...         modelFile          = vehicleProperties['drone']['model'],
		...         startLoc           = list(myNodes[myNodes['id'] == arc[0]][['lat', 'lon']].values[0]),
		...         endLoc             = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...         startTimeSec       = endTimeSec,
		...         takeoffSpeedMPS    = vrv.convertSpeed(30, 'miles', 'hr', 'meters', 'sec'),
		...         cruiseSpeedMPS     = vrv.convertSpeed(80, 'miles', 'hr', 'meters', 'sec'),
		...         landSpeedMPS       = vrv.convertSpeed( 5, 'miles', 'hr', 'meters', 'sec'),
		...         cruiseAltMetersAGL = vrv.convertDistance(350, 'feet', 'meters'),
		...         routeType          = 'square',
		...         leafletColor       = vehicleProperties['drone']['leafletColor'],
		...         cesiumColor        = vehicleProperties['drone']['cesiumColor'])
		>>> myAssignments
		
	Show the nodes and assignments on a map:
		>>> vrv.createLeaflet(nodes=myNodes, arcs=myAssignments)

	Find the location of each vehicle at time 30.0:
		>>> currentLocs = vrv.findLocsAtTime(assignments=myAssignments, timeSec=30.0)
		>>> 
		>>> # Or, we can just find the location of the drone at time 30.0:
		>>> # currentLocs = vrv.findLocsAtTime(
		>>> #    assignments=myAssignments[myAssignments['objectID'] == 'drone'], 
		>>> #    timeSec=30.0)
		>>> currentLocs
		
	Display the estimated locations on a map:		
		>>> myMap = vrv.createLeaflet(nodes=myNodes, arcs=myAssignments)
		>>> for objectID in currentLocs:
		...     if (type(currentLocs[objectID]) is list):
		...         # This objectID has at least 1 location at this time:
		...         if (type(currentLocs[objectID][0]) is list):
		...             # There were multiple matches for this objectID:
		...             for i in currentLocs[objectID]:
		...                 myMap = vrv.addLeafletMarker(mapObject=myMap, center=i)
		...         else:
		...             # We only have one location for this objectID:
		...             myMap = vrv.addLeafletMarker(mapObject=myMap, 
		...                                          center=currentLocs[objectID], 
		...                                          radius=9, 
		...                                          fillOpacity=0.7, 
		...                                          fillColor='black')
		>>> myMap		
	"""

	[valFlag, errorMsg, warningMsg] = valFindLocsAtTime(assignments, timeSec)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)


	output = {}

	asgnCopy = assignments.copy()

	# Get list of unique objectIDs:
	uniqueIDs = list(asgnCopy['objectID'].unique())

	# Replace "-1" end time with +infinity
	asgnCopy.loc[asgnCopy['endTimeSec'] < 0, 'endTimeSec'] = sys.maxsize  # float('Inf')

	for objectID in uniqueIDs:
		tmpAsgn = asgnCopy[(asgnCopy['objectID'] == objectID) & 
			(asgnCopy['startTimeSec'] <= timeSec) & 
			(asgnCopy['endTimeSec'] >= timeSec)] 
	
		if (len(tmpAsgn) == 0):
			output[objectID] = None
			print("Warning: objectID `%s` is not tracked at time %.2f seconds" % (objectID, timeSec))
		else:
			outList = []
			for id in tmpAsgn.index:
				startLat     = tmpAsgn['startLat'].at[id]
				startLon     = tmpAsgn['startLon'].at[id]
				startAlt     = tmpAsgn['startAltMeters'].at[id]
				startTimeSec = tmpAsgn['startTimeSec'].at[id]
			
				endLat     = tmpAsgn['endLat'].at[id]
				endLon     = tmpAsgn['endLon'].at[id]
				endAlt     = tmpAsgn['endAltMeters'].at[id]
				endTimeSec = tmpAsgn['endTimeSec'].at[id]

				# Find percentage of time:
				if (endTimeSec < sys.maxsize):
					pct = (timeSec - startTimeSec) / (endTimeSec - startTimeSec)
				else:
					pct = 0.0
			
				# Find distance from start to end:
				distMeters = geoDistance2D([startLat, startLon], [endLat, endLon])
			
				if (distMeters == 0.0):
					newLoc = [startLat, startLon]
				else: 
					# Get initial heading from start to end:
					hdgDeg = geoGetHeading([startLat, startLon], [endLat, endLon])

					# Get expected lat/lon coords:
					newLoc = geoPointInDistance2D([startLat, startLon], hdgDeg, distMeters*pct)

				# Interpolate altitude:
				newAlt = startAlt + (endAlt - startAlt)*pct
			
				# Add to our list of expected locations for this id:
				outList.append([newLoc[0], newLoc[1], newAlt])

			if (len(outList) == 1):
				output[objectID] = outList[0]
					
			else:
				# 
				print("Warning: objectID `%s` appears in %d matching rows.  Perhaps the assignments dataframe has duplicate entries?" % (objectID, len(tmpAsgn)))
				output[objectID] = outList
	
	return output			
				
def geocode(location=None, dataProvider=None, dataProviderArgs=None):
	"""
	Convert a street address, city, state, or zip code to GPS coordinates ([lat, lon] format).

	Parameters
	----------
	location: string, Required
		A text string indicating a street address, state, or zip code.
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for generating nodes on a road network. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.
	
	Return
	------
	list
		A GPS coordinate, of the form [lat, lon].

	Note
	----
	Neither pgRouting nor OSRM are supported.  
	pgRouting would require a database of the entire planet.  
	OSRM doesn't have a geocode function.

	Examples
	--------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()
	
	The following examples assume the use of ORS or MapQuest as the data provider.  If you have saved your API keys as environment variables, you may use `os.environ` to access them:
		>>> import os
		>>> 
		>>> ORS_API_KEY = os.environ['ORSKEY']
		>>> MQ_API_KEY = os.environ['MAPQUESTKEY']
		>>> 
		>>> # Otherwise, you may specify your keys here:
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'
		>>> # MQ_API_KEY = 'YOUR_MAPQUEST_KEY_GOES_HERE'

	Example 1 - Find [lat, lon] of Buckingham Palace, without specifying a data provider:
		>>> myLoc = vrv.geocode(location='Westminster, London SW1A 1AA, United Kingdom')
		>>> myLoc
		[51.5008719, -0.1252387]
	
	Example 2 - Find [lat, lon] of Buckingham Palace, using ORS-online as the data provider:
		>>> myLoc = vrv.geocode(location         ='Westminster, London SW1A 1AA, United Kingdom', 
		...                     dataProvider     ='ors-online', 
		...                     dataProviderArgs = {'APIkey': ORS_API_KEY})
		>>> myLoc
		[51.497991, -0.12875]
        
	Example 3 - Find [lat, lon] of Seattle, Washington, USA:
		>>> myLoc = vrv.geocode(location         ='seattle, wa', 
		...                     dataProvider     ='mapquest', 
		...                     dataProviderArgs = {'APIkey': MQ_API_KEY})
		>>> myLoc
		[47.603229, -122.33028]

	Example 4 - Find [lat, lon] of the state of Florida, USA:
		>>> myLoc = vrv.geocode(location         ='florida', 
		...                     dataProvider     ='ors-ONLINE', 
		...                     dataProviderArgs = {'APIkey': ORS_API_KEY})
		>>> myLoc
		[27.97762, -81.769611]

	Example 5 - Find [lat, lon] of the Space Needle (in Seattle, WA):
		>>> myLoc = vrv.geocode(location         ='space needle', 
		...                     dataProvider     ='ors-ONLINE', 
		...                     dataProviderArgs = {'APIkey': ORS_API_KEY})
		>>> myLoc
		[47.620336, -122.349314]  

	Draw the geocoded location as a red dot on a Leaflet map:
		>>> vrv.addLeafletMarker(center=myLoc)
		 
	"""
	
	# validation
	[valFlag, errorMsg, warningMsg] = valGeocode(location, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	loc = privGeocode(location, dataProvider, dataProviderArgs)
	
	return loc
	
def reverseGeocode(location=None, dataProvider=None, dataProviderArgs=None):    
	"""
	Convert a GPS coordinate (of the form [lat, lon] or [lat, lon, alt]) to an address.  If altitude is provided it will be ignored.

	Parameters
	----------
	location: list, Required
		A GPS coordinate of the form [lat, lon] or [lat, lon, alt].
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for generating nodes on a road network. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.
	
	Return
	------
	list
		A GPS coordinate, of the form [lat, lon], indicating the location of the returned address.  Note that this location might not match the input coordinates.
	dictionary
		A dataProvider-specific dictionary containing address details.  The keys in this dictionary may differ according to data provider.

	Note
	----
	Neither pgRouting nor OSRM are supported.  
	pgRouting would require a database of the entire planet.  
	OSRM doesn't have a geocode function.

	Examples
	--------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()
	
	The following examples assume the use of ORS or MapQuest as the data provider.  If you have saved your API keys as environment variables, you may use `os.environ` to access them:
		>>> import os
		>>> 
		>>> ORS_API_KEY = os.environ['ORSKEY']
		>>> MQ_API_KEY = os.environ['MAPQUESTKEY']
		>>> 
		>>> # Otherwise, you may specify your keys here:
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'
		>>> # MQ_API_KEY = 'YOUR_MAPQUEST_KEY_GOES_HERE'
	
	Example 1 -- Without specifying a dataProvider:
		>>> [loc, addr] = vrv.reverseGeocode(location=[47.603229, -122.33028])
		>>> loc
		[47.6030474, -122.3302567]
        
		>>> addr
		{'place_id': 18472401,
		 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
		 'osm_type': 'node',
		 'osm_id': 1769027877,
		 'lat': '47.6030474',
		 'lon': '-122.3302567',
		 'display_name': 'SDOT, 4th Avenue, West Edge, International District/Chinatown, Seattle, King County, Washington, 98104, USA',
		 'address': {'bicycle_parking': 'SDOT',
		 'road': '4th Avenue',
		 'neighbourhood': 'West Edge',
		 'suburb': 'International District/Chinatown',
		 'city': 'Seattle',
		 'county': 'King County',
		 'state': 'Washington',
		 'postcode': '98104',
		 'country': 'USA',
		 'country_code': 'us'},
		 'boundingbox': ['47.6029474', '47.6031474', '-122.3303567', '-122.3301567']}
	
	Example 2 -- Using MapQuest:
		>>> [loc, addr] = vrv.reverseGeocode(location         = [47.603229, -122.33028], 
		...                                  dataProvider     = 'MapQuest', 
		...                                  dataProviderArgs = {'APIkey': MQ_API_KEY})
		>>> loc
		[47.603229, -122.33028]
		
		>>> addr
		{'street': '431 James St',
		 'adminArea6': '',
		 'adminArea6Type': 'Neighborhood',
		 'adminArea5': 'Seattle',
		 'adminArea5Type': 'City',
		 'adminArea4': 'King',
		 'adminArea4Type': 'County',
		 'adminArea3': 'WA',
		 'adminArea3Type': 'State',
		 'adminArea1': 'US',
		 'adminArea1Type': 'Country',
		 'postalCode': '98104',
		 'geocodeQualityCode': 'L1AAA',
		 'geocodeQuality': 'ADDRESS',
		 'dragPoint': False,
		 'sideOfStreet': 'R',
		 'linkId': '0',
		 'unknownInput': '',
		 'type': 's',
		 'latLng': {'lat': 47.603229, 'lng': -122.33028},
		 'displayLatLng': {'lat': 47.603229, 'lng': -122.33028},
		 'nearestIntersection': {'streetDisplayName': '4th Ave',
		 'distanceMeters': '0.0',
		 'latLng': {'longitude': -122.33028, 'latitude': 47.603229},
		 'label': 'James St & 4th Ave'},
		 'roadMetadata': {'speedLimitUnits': 'mph',
		 'tollRoad': None,
		 'speedLimit': 25}}
		 
	Example 3 -- Using OpenRouteService:
		>>> [loc, addr] = vrv.reverseGeocode(location         = [47.603229, -122.33028], 
		...                                  dataProvider     = 'ORS-online', 
		...                                  dataProviderArgs = {'APIkey': ORS_API_KEY})
		>>> loc
		[47.603077, -122.330139]
		
		>>> addr
		{'id': 'node/4491511984',
		 'gid': 'openstreetmap:venue:node/4491511984',
		 'layer': 'venue',
		 'source': 'openstreetmap',
		 'source_id': 'node/4491511984',
		 'name': '4th Ave & James St',
		 'confidence': 0.8,
		 'distance': 0.02,
		 'accuracy': 'point',
		 'country': 'United States',
		 'country_gid': 'whosonfirst:country:85633793',
		 'country_a': 'USA',
		 'region': 'Washington',
		 'region_gid': 'whosonfirst:region:85688623',
		 'region_a': 'WA',
		 'county': 'King County',
		 'county_gid': 'whosonfirst:county:102086191',
		 'county_a': 'KN',
		 'locality': 'Seattle',
		 'locality_gid': 'whosonfirst:locality:101730401',
		 'neighbourhood': 'Pioneer Square',
		 'neighbourhood_gid': 'whosonfirst:neighbourhood:85866047',
		 'continent': 'North America',
		 'continent_gid': 'whosonfirst:continent:102191575',
		 'label': '4th Ave & James St, Seattle, WA, USA'}
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valReverseGeocode(location, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return (None, None)
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	[loc, address] = privReverseGeocode(location, dataProvider, dataProviderArgs)

	return (loc, address)	

def isochrones(location=None, locationType='start', travelMode='driving-car', rangeType='distance', rangeSize=None, interval=None, smoothing=25, dataProvider=None, dataProviderArgs=None):    
	"""
	Finds isochrones (lines corresponding to points of equal distance or time from a given location) to or from a given location.  

	Parameters
	----------
	location: list, Required
		A GPS coordinate of the form [lat, lon] or [lat, lon, alt].  If provided, altitude will be ignored (i.e., assumed to be 0).
	locationType: string, Required, default as 'start'
		Specifies whether `location` is the start or the destination.  Valid options are 'start' or 'destination'
	travelMode: string, Required, default as 'driving-car'
		Specifies the mode of travel.  Valid options are: 'driving-car', 'driving-hgv', 'cycling-regular', 'cycling-road', 'cycling-mountain', 'cycling-electric', 'foot-walking', 'foot-hiking', or 'wheelchair'.
	rangeType: string, Required, default as 'distance'
		Indicates whether the isochrones are based on distance or time.  Valid options are 'distance' or 'time'.
	rangeSize: positive float, Required, default as None
		The isochrones will indicate the area accessible from the given location within the rangeSize.  rangeSize is in units of [meters] if rangeType equals 'distance'; rangeSize is in units of [seconds] if rangeType equals 'time'.
	interval: float, Optional, default as None
		If provided, this parameter can be used to generate multiple concentric isochrones.  For example, if rangeSize = 90, and interval = 30, isochrones will be identified for ranges of 30, 60, and 90 units.  If interval is not provided (as is the default), only one isochrone will be determined.
	smoothing: float in range [0, 100], Optional, default as 25
		Indicates the granularity of the isochrones.  Smoothing values close to 0 will produce jagged isochrones; values close to 100 will generally result in smooth isochrones.	
	dataProvider: string, Required, default as None
		Specifies the data source to be used for obtaining isochrone data. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Required, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.
	
	Return
	------
	dictionary with nested dictionaries and lists
		Check the note for the structure of dictionary.

	Note
	----
	This dictionary has the following structure:
		>>> {
		>>>     'location': [lat, lon],		# Matches the user's 'location' input value
		>>>     'boundingRegion': [[lat, lon], [lat, lon], [lat, lon], [lat, lon]],  # The smallest rectangle that encloses all isochrones.
		>>>     'isochrones':
		>>>     [
		>>>         {
		>>>             'value':  # Either the time or distance assoc. with this isochrone.
		>>>             'valueUnits': # either 'seconds' or 'meters'.
		>>>             'area':  # The area enclosed by the isochrone, in square meters.
		>>>             'pop':   # The estimated population within the isochrone.
		>>>             'reachfactor':  # FIXME -- not sure what this represents.
		>>>             'poly': [[]]	# A list of lists describing polylines.
		>>>                 # A list of GPS coordinates, of the form [[[lat, lon], [lat, lon], ..., [lat, lon]], []] defining a polygon.  This polygon describes the isochrones.
		>>>         },
		>>>         {
		>>>             ...
		>>>         }
		>>>     ]
		>>> }    						
		
	Note
	----
	Currently, only 'ors-online' and 'ors-local' are supported.  Neither mapQuest, pgRouting, nor OSRM are supported, as they don't appear to have native support for isochrones.  

	Examples
	--------
                     	
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()
	
	The following examples assume the use of ORS as the data provider.  If you have saved your API keys as environment variables, you may use `os.environ` to access them:
		>>> import os
		>>> 
		>>> ORS_API_KEY = os.environ['ORSKEY']
		>>> 
		>>> # Otherwise, you may specify your keys here:
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'

	Example 1 - Get distance-based isochrones from a given location:
		>>> iso = vrv.isochrones(location         = [43.00154, -78.7871],
		...                      rangeType        = 'distance', 
		...                      rangeSize        = 4000, 
		...                      dataProvider     = 'ors-online', 
		...                      dataProviderArgs = {'APIkey': os.environ['ORSKEY']})
		>>> iso
	
	Draw the result on a Leaflet map:
		>>> vrv.addLeafletIsochrones(iso=iso)
		>>> 
		>>> # Click on the shaded area of the map for additional info

	Example 2 - This example includes all function arguments:
		>>> iso2 = vrv.isochrones(location         = [43.00154, -78.7871], 
		...                       locationType     = 'start', 
		...                       travelMode       = 'driving-car', 
		...                       rangeType        = 'time', 
		...                       rangeSize        = vrv.convertTime(5, 'minutes', 'seconds'), 
		...                       interval         = vrv.convertTime(1, 'minutes', 'seconds'), 
		...                       smoothing        = 5, 
		...                       dataProvider     ='ors-online', 
		...                       dataProviderArgs = {'APIkey': os.environ['ORSKEY']})
		>>>
		>>> vrv.addLeafletIsochrones(iso=iso2)
		
	Customize the map by using the `addLeafletPolygon()` function:	
		>>>	myColors = ['red', 'blue', 'green']
		>>>	
		>>>	myMap = vrv.addLeafletIcon(location=iso2['location'])
		>>>	
		>>>	for i in range(len(iso2['isochrones'])-1, -1, -1):
		...     lineColor = myColors[i % len(myColors)]
		...     fillColor = lineColor
		...     for j in range(0, len(iso2['isochrones'][i]['poly'])):
		...         myMap = vrv.addLeafletPolygon(mapObject = myMap,
		...                                       points    = iso2['isochrones'][i]['poly'][j],
		...                                       lineColor = lineColor,
		...                                       fillColor = fillColor)
		>>>	
		>>>	myMap   	
	"""
	
	
	# validation
	[valFlag, errorMsg, warningMsg] = valIsochrones(location, locationType, travelMode, rangeType, rangeSize, interval, smoothing, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return None
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	
	if (interval == None):
		interval = rangeSize
	else:
		interval = min(interval, rangeSize)
		
	iso = privIsochrones(location, locationType, travelMode, rangeType, rangeSize, interval, smoothing, dataProvider, dataProviderArgs)
	
	return iso

def createGantt(assignments=None, objectIDorder=None, separateByModelFile=False, mergeByodID=True, splitOnColorChange=True, title=None, xAxisLabel='time', xGrid=False, yGrid=False, xMin=0, xMax=None, xGridFreq=60, timeFormat='s', overlayColumn=None, missingColor='lightgray', filename=None):
	"""
	EXPERIMENTAL.  Draws a Gantt chart from an :ref:`Assignments` dataframe.  This has the appearance of a horizontal bar chart.  The x-axis indicates the elapsed time.  Each `objectID` forms a horizontal bar.

	Parameters
	----------
	assignments: :ref:`Assignments` dataframe, Required, default as None
		The activities and event times are drawn from the `Assignments` dataframe.  Bar colors are specified by the `leafletColor` column of the dataframe.
	objectIDorder: list, Optional, default as None
		A list containing values from the `objectID` column of the `assignments` dataframe.  If provided, this list will be used to determine the order in which `objectID`s are displayed on the y-axis of the Gantt chart, where the first item in the list will be on the bottom and the last item will be on top.
	separateByModelFile: boolean, Optional, default as False
		If `True`, Gantt chart bars will be formed by the unique combination of the `objectID` and `modelFile` columns of the `assignments` dataframe.  By default, only the `objectID` column will be used to specify the bars.  Note: This field affects the y-axis groupings.
	mergeByodID: boolean, Optional, default as True
		If `True`, consecutive assignments that have the same `odID` value (for a particular row of the Gantt chart) and do not have a gap in timing (i.e., the end time of the preceding assignment row equals the start time of the next assignment) will be combined into a single cell.  If `False`, each row of the assignments dataframe will result in a separate Gantt chart cell.  This can lead to a very cluttered figure.
	splitOnColorChange: boolean, Optional, default as True
		If `True`, a cell will be split if the `ganttColor` value in the preceding assignment is different (even if the odID is the same and there are no timing gaps).  This case typically would occur if a static assignment (such as a service activity) was appended to a route, and the static assignment has the same odID, and the static assignment did have a `ganttColor` value in the `assignments` dataframe, and `missingColor` is not None.  This defaults to True to help flag these cases; in which case you probably want to fix your assignments dataframe.
	title: string, Optional, default as None
		A title to appear above the Gantt chart.
	xAxisLabel: string, Optional, default as 'time'
		A label to appear below the x-axis.		  
	xGrid: boolean, Optional, default as False
		If `True`, vertical lines will be displayed on the Gantt chart.
	yGrid: boolean, Optional, default as False
		If `True`, horizontal lines will be displayed on the Gantt chart.
	xMin: non-negative float, Optional, default as 0 
		Specifies the minimum value to display on the x-axis, in units of [seconds].
	xMax: positive float, Optional, default as None
		Specifies the maximum value to display on the x-axis, in units of [seconds].  If None (default), xMax will be automatically determined from the `endTimeSeconds` column of the `assignments` dataframe.
	xGridFreq: positive float, Optional, default as 60
		Specifies the spacing between tick labels on the x-axis, in units of [seconds].
	timeFormat: string, Optional, default as 's'
		Specifies the formatting of the x-axis tick marks.  Valid options are: 'DHMS' (days:hours:minutes:seconds), 'HMS' (hours:minutes:seconds), 'MS' (minutes:seconds), 'D' (fractional number of days), 'H' (fractional number of hours), 'M' (fractional number of minutes), or 'S' (integer number of seconds).
	overlayColumn: string, Optional, default as None
		There are three options: None, 'odID', or 'index'.  If None (default), no labels will be shown within each bar cell of the Gantt chart.  If 'odID', each bar cell will display the corresponding odID value.  This only makes sense if `mergeByodID` is True.  If 'index', each bar cell will display the index column value of the `assignments` dataframe.  This can be cluttered, but may be useful for debugging (allowing a mapping from the Gantt chart elements to the particular rows of the assignments dataframe).
	missingColor: string, Optional, default as 'lightgray'
		Specifies the default color to use if the assignments dataframe is missing a color for a particular row.  Use `None` if you do not want to use a default color.
	filename: string, Optional, default as None
		If provided, the Gant chart will be saved to this file.  The image format will be automatically determined by the file extension (e.g., `.jpg`, `.png`, or `.pdf`).

	Return
	------
	object
		A matplotlib figure object.

	Examples
	--------					
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Start by defining some locations for our vehicles to visit:
		>>> locs = [[42.8871085, -78.8731949],
		...         [42.8888311, -78.8649649],
		...         [42.8802158, -78.8660787],
		...         [42.8845705, -78.8762794],
		...         [42.8908031, -78.8770140]]

	Convert these locations into a `Nodes` dataframe:
		>>> myNodes = vrv.createNodesFromLocs(locs=locs)
		>>> myNodes

	A car will start at node 1, visit nodes 2 and 3, and then return to node 1.  A truck will follow a route from 1->5->4->1.
		>>> mySolution = {
		...     'car': [[1,2], [2,3], [3,1]],
		...     'truck': [[1,5], [5,4], [4,1]]
		>>> }
		mySolution

	Define some properties to use when building the `Assignments` dataframe:
		>>> vehicleProperties = {
		...     'car':   {'model': 'veroviz/models/car_red.gltf',
		...               'color': 'red'},
		...     'truck': {'model': 'veroviz/models/ub_truck.glb',
		...               'color': 'blue'}
		>>> }

	Build the assignments dataframe for the 2 vehicle routes.  No service times, Euclidean travel:
		>>> myAssignments = vrv.initDataframe('assignments')
		>>> for v in mySolution:
		...     endTimeSec = 0.0
		...     for arc in mySolution[v]:
		...         [myAssignments, endTimeSec] = vrv.addAssignment2D(
		...             initAssignments = myAssignments,
		...             objectID        = v,
		...             modelFile       = vehicleProperties[v]['model'],
		...             startLoc        = list(myNodes[myNodes['id'] == arc[0]][['lat', 'lon']].values[0]),
		...             endLoc          = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...             startTimeSec    = endTimeSec,
		...             routeType       = 'euclidean2D',
		...             speedMPS        = vrv.convertSpeed(25, 'miles', 'hour', 'meters', 'second'),
		...             leafletColor    = vehicleProperties[v]['color'],
		...             cesiumColor     = vehicleProperties[v]['color'],
		...             ganttColor      = vehicleProperties[v]['color'])
		>>> myAssignments

	Create a Gantt chart using the default settings:
		>>> vrv.createGantt(assignments = myAssignments, 
		...                 xAxisLabel  = 'time [seconds]')

	Create (and save) a Gantt chart using all of the available settings:
		>>> vrv.createGantt(assignments         = myAssignments, 
		...                 objectIDorder       = ['truck', 'car'], 
		...                 separateByModelFile = False,
		...                 mergeByodID         = True,
		...                 splitOnColorChange  = True,
		...                 title               = 'My Title',
		...                 xAxisLabel          = 'time [mm:ss]',
		...                 xGrid               = True,
		...                 yGrid               = False,
		...                 xMin                = 0,
		...                 xMax                = None,
		...                 xGridFreq           = 30,
		...                 timeFormat          = 'MS',
		...                 overlayColumn       = 'odID',
		...                 missingColor        = 'lightgray',
		...                 filename            = 'myGantt.png')
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valCreateGantt(assignments, objectIDorder, separateByModelFile, mergeByodID, splitOnColorChange, title, xAxisLabel, xGrid, yGrid, xMin, xMax, xGridFreq, timeFormat, overlayColumn, missingColor, filename)
	if (not valFlag):
		print (errorMsg)
		return None
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)


	BAR_HEIGHT    = 8
	BAR_STEP_SIZE = 10

	fig, ax = plt.subplots(dpi=200)

	if (objectIDorder is None):
		objectIDorder = list(assignments['objectID'].unique())
	
	
	if (separateByModelFile):
		# Group y-axis labels by objectID and modelFile:
		# yLabels = list((assignments['objectID'].map(str) + ' - ' + assignments['modelFile'].map(str)).unique())
		yLabels = []
		yTicks  = []
		y       = 2
		for objectID in objectIDorder:
			modelFiles = list(assignments[assignments['objectID'] == objectID]['modelFile'].unique())
			for i in range(0, len(modelFiles)):
				yLabels.append(str(objectID) + ' - ' + str(modelFiles[i]))
				yTicks.append(y + BAR_HEIGHT/2) 
				y += BAR_HEIGHT
			y += 2
	else:
		# Only group y-axis labels by objectID
		# yGroups = list(assignments['objectID'].unique())
		yLabels = objectIDorder
		yTicks  = []
		y = 2 
		for i in range(0, len(yLabels)):
			yTicks.append(y + BAR_HEIGHT/2)
			y += BAR_STEP_SIZE

	yTicks.append(y)

	maxEnd = max(assignments['endTimeSec'])

	if (xMax is None):
		xMax = xMin + math.ceil((maxEnd - xMin)/xGridFreq) * xGridFreq
	
	ax.set_xlim(xMin, xMax)

	for i in range(0, len(yLabels)):
		myLabel = yLabels[i]
		y = yTicks[i]
		if (separateByModelFile):
			dummy = pd.DataFrame(assignments[assignments['objectID'].map(str) + ' - ' + assignments['modelFile'].map(str) == myLabel])
			dummy['asgnIndex'] = assignments[assignments['objectID'].map(str) + ' - ' + assignments['modelFile'].map(str) == myLabel].index
		else:    
			dummy = pd.DataFrame(assignments[assignments['objectID'].isin([myLabel])])
			dummy['asgnIndex'] = assignments[assignments['objectID'].isin([myLabel])].index

		# Replace -1 endTime:
		dummy.loc[dummy['endTimeSec'] < 0, 'endTimeSec'] = maxEnd
		
		# If user doesn't want color change to trigger a break,
		# and if a missing color name is specified,
		# go ahead and replace missing colors now.
		if (not splitOnColorChange):
			if (missingColor is not None):
				dummy.loc[dummy['ganttColor'].isin([None]), 'ganttColor'] = missingColor

		# Sort by odID and startTime:
		dummy = dummy.sort_values(by=['odID', 'startTimeSec'], ascending=True)
		dummy = dummy.reset_index(drop=True)
		
		# Add new columns, with values from the *next* row:
		dummy[['next_odID', 'next_startTimeSec', 'next_ganttColor']] = pd.DataFrame(dummy[1:][['odID', 'startTimeSec', 'ganttColor']].values)

		start_x = None
		for j in list(dummy.index):
			# Set the starting x coordinate for a new cell:
			if (start_x is None):
				myColor = dummy.loc[j]['ganttColor']
				if (myColor is None):
					if (missingColor is None):
						break
					else:
						myColor = missingColor
				start_x = dummy.loc[j]['startTimeSec']
				odID    = dummy.loc[j]['odID']	
			
			# Check for ending condition of the cell
			# Break in times,
			# mergeByodID and change in odIDs
			# splitOnColorChange and change in colors
			if (start_x is not None):
				if ( (not mergeByodID) or \
					 (dummy.loc[j]['endTimeSec'] != dummy.loc[j]['next_startTimeSec']) or \
					 (dummy.loc[j]['odID'] != dummy.loc[j]['next_odID']) or \
					 (splitOnColorChange and (dummy.loc[j]['ganttColor'] != dummy.loc[j]['next_ganttColor'])) ):

					endTime = dummy.loc[j]['endTimeSec']
					duration = endTime - start_x
				
					ax.broken_barh([(start_x, duration)], (y-BAR_HEIGHT/2, BAR_HEIGHT), fc=myColor, ec='black')

					if (overlayColumn == 'index'):
						if (xMin <= (start_x + duration/2.0) <= xMax):
							overlayText = dummy.loc[j]['asgnIndex']
							plt.text((start_x + duration/2.0), y, overlayText, color='black', fontsize=12, ha='center', va='center')
					elif (overlayColumn == 'odID'):
						if (xMin <= (start_x + duration/2.0) <= xMax):
							overlayText = odID
							plt.text((start_x + duration/2.0), y, overlayText, color='black', fontsize=12, ha='center', va='center')
					
					start_x = None		


	if (title is not None):
		plt.title(title)

	ax.set_ylim(0, max(yTicks))

	if (xAxisLabel is not None):
		ax.set_xlabel(xAxisLabel)

	if (len(yTicks) > len(yLabels)):
		yTicks = yTicks[0:len(yLabels)]
		
	ax.set_xticks(range(int(xMin), int(xMax+1), int(xGridFreq)))
	ax.set_yticks(yTicks)
	ax.set_yticklabels(yLabels, minor=False)
	ax.set_yticks(yTicks, minor=False)

	ax.grid(xGrid, axis='x')     
	ax.grid(yGrid, axis='y')     

	if (timeFormat.lower() == 'dhms'):
		ax.xaxis.set_major_formatter(plt.FuncFormatter(fmtDHMS))
	elif (timeFormat.lower() == 'hms'):
		ax.xaxis.set_major_formatter(plt.FuncFormatter(fmtHMS))
	elif (timeFormat.lower() == 'ms'):
		ax.xaxis.set_major_formatter(plt.FuncFormatter(fmtMS))
	elif (timeFormat.lower() == 'd'):
		ax.xaxis.set_major_formatter(plt.FuncFormatter(fmtD))
	elif (timeFormat.lower() == 'h'):
		ax.xaxis.set_major_formatter(plt.FuncFormatter(fmtH))
	elif (timeFormat.lower() == 'm'):
		ax.xaxis.set_major_formatter(plt.FuncFormatter(fmtM))
	else:
		ax.xaxis.set_major_formatter(plt.FuncFormatter(fmtS))

	
	if (filename is not None):
		fig.savefig(filename, bbox_inches='tight')

	plt.close();

	return fig
	
def getElevationLocs(locs=None, dataProvider=None, dataProviderArgs=None):    
	"""
	EXPERIMENTAL.  Finds the elevation, in units of meters above mean sea level (MSL), for a given location or list of locations.  

	Parameters
	----------
	locs: list of lists, Required, default as None
		A list of one or more GPS coordinate of the form [[lat, lon], ...] or [[lat, lon, alt], ...].  If altitude is included in locs, the function will add the elevation to the input altitude.  Otherwise, the input altitude will be assumed to be 0.
	dataProvider: string, Required, default as None
		Specifies the data source to be used for obtaining elevation data. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Required, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.
	
	Return
	------
	list of lists, of the form [[lat, lon, altMSL], [lat, lon, altMSL], ..., [lat, lon, altMSL]].
		
	Note
	----
	Currently, only 'ors-online', 'usgs', and 'elevapi' are supported.
	Neither mapQuest, pgRouting, nor OSRM are supported, as they don't appear to have native support for elevation.  

	Examples
	--------

	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()
	
	The `getElevationLocs()` function requires a data provider.  If you have saved your API keys as environment variables, you may use `os.environ` to access them:
		>>> import os
		>>> 
		>>> ORS_API_KEY = os.environ['ORSKEY']
		>>> 
		>>> # Otherwise, you may specify your keys here:
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'

	Define a set of locations:
		>>> locs = [[42.8871085, -78.8731949],
		...         [42.8888311, -78.8649649],
		...         [42.8802158, -78.8660787],
		...         [42.8845705, -78.8762794],
		...         [42.8908031, -78.8770140]]

	Use ORS to find the elevations of all locations:
		>>> vrv.getElevationLocs(locs             = locs, 
		...                      dataProvider     = 'ors-online', 
		...                      dataProviderArgs = {'APIkey': ORS_API_KEY})

		[[42.887108, -78.873195, 196.0],
		 [42.888831, -78.864965, 185.0],
		 [42.880216, -78.866079, 183.0],
		 [42.884571, -78.876279, 200.0],
		 [42.890803, -78.877014, 187.0]]		
		
	Use ORS to find the elevation of a single location, with a starting elevation/altitude:
		>>> vrv.getElevationLocs(locs             = [[42.888, -78.864, 100]], 
		...                      dataProvider     = 'ors-online', 
		...                      dataProviderArgs = {'APIkey': ORS_API_KEY})
		
		[[42.888, -78.864, 284.0]]
		
	Use the US Geological Survey data:
		>>> vrv.getElevationLocs(locs             = locs, 
		...                      dataProvider     = 'usgs')		
		
		[[42.8871085, -78.8731949, 187.66],
		 [42.8888311, -78.8649649, 185.15],
		 [42.8802158, -78.8660787, 181.1],
		 [42.8845705, -78.8762794, 185.64],
		 [42.8908031, -78.877014, 186.25]]
		 

	Use Elevation-API:
		>>> vrv.getElevationLocs(locs             = [[42.888, -78.864, 100]], 
		...                      dataProvider     = 'elevapi',

		[[42.888, -78.864, 292.0]]		 
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valGetElevationLocs(locs, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return None
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
		
	locsWithAlt = privGetElevationLocs(locs, dataProvider, dataProviderArgs)
	
	return locsWithAlt

def getElevationDF(dataframe=None, replaceOnlyNone=True, dataProvider=None, dataProviderArgs=None): 
	"""
	EXPERIMENTAL.  Replaces missing (`None`) values for elevation columns of the provided dataframe.  New values are in units of meters above mean sea level (MSL).  CAUTION: This function will overwrite the elevation data in the input dataframe.

	Parameters
	----------
	dataframe: pandas.dataframe, Required
		The dataframe to be exported.  This can be a :ref:`Nodes`, :ref:`Arcs`, or :ref:`Assignments` dataframe.
	replaceOnlyNone: Boolean, Optional, default as True
		If True, only find elevation data associated for rows in which this data is missing from the input dataframe.  If False, find (and overwrite) all elevation data with new values.
	dataProvider: string, Required, default as None
		Specifies the data source to be used for obtaining elevation data. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Required, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.
	
	Return
	------
	A pandas dataframe.
		
	Note
	----
	Currently, only 'ors-online', 'usgs', and 'elevapi' are supported.
	Neither mapQuest, pgRouting, nor OSRM are supported, as they don't appear to have native support for elevation.  

	Examples
	--------
                     	
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()
	
	The `getElevationDF()` function requires a data provider.  If you have saved your API keys as environment variables, you may use `os.environ` to access them:
		>>> import os
		>>> 
		>>> ORS_API_KEY = os.environ['ORSKEY']
		>>> 
		>>> # Otherwise, you may specify your keys here:
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'

	Create a Nodes dataframe.  Note that, by default, there is no elevation data:
		>>> myNodes = vrv.generateNodes(
		...     numNodes        = 4,
		...     nodeType        = 'depot', 
		...     nodeDistrib     = 'normal', 
		...     nodeDistribArgs = {
		...         'center' : [42.30, -78.00], 
		...         'stdDev' : 1000
		...     })
		>>> myNodes['elevMeters']

		0    None
		1    None
		2    None
		3    None
		Name: elevMeters, dtype: object

	Find missing elevation data using ORS-online:
		>>> vrv.getElevationDF(dataframe        = myNodes, 
		...                    dataProvider     = 'ors-online',
		...                    dataProviderArgs = {'APIkey': ORS_API_KEY})
		>>> myNodes['elevMeters']

		0    460
		1    448
		2    461
		3    446
		Name: elevMeters, dtype: int64

	Overwrite elevation data using USGS:
		>>> vrv.getElevationDF(dataframe       = myNodes, 
		...                    replaceOnlyNone = False,
		...                    dataProvider    = 'usgs')
		>>> myNodes['elevMeters']

		0    442.58
		1    447.53
		2    455.06
		3    444.21
		Name: elevMeters, dtype: object

	Replace elevation data using Elevation-API:
		>>> vrv.getElevationDF(dataframe        = myNodes, 
		...                    replaceOnlyNone = False,
		...                    dataProvider     = 'elevAPI',
		>>> myNodes['elevMeters']

		0    192
		1    192
		2    192
		3    178
		4    178
		Name: elevMeters, dtype: int64
	
	Create an Arcs dataframe from a sequence of nodes:
		>>> myArcs = vrv.createArcsFromNodeSeq(
		...     nodeSeq = [1, 2, 3, 4],
		...     nodes   = myNodes)

	Find missing start/end elevations in the arcs dataframe, using USGS data:
		>>> vrv.getElevationDF(dataframe        = myArcs, 
		...                    dataProvider     = 'usgs')
		>>> myArcs[['startElevMeters', 'endElevMeters']]
			startElevMeters	endElevMeters
		0	187.66	185.15
		1	185.15	181.1
		2	181.1	185.64
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valGetElevationDF(dataframe, replaceOnlyNone, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return None
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
		
	# Make copy of dataframe
	dataframe = pd.DataFrame(dataframe)
		
	# Find out the type of dataframe we have:
	dfCols = list(dataframe.columns)
	if (('lat' in dfCols) and ('lon' in dfCols) and ('elevMeters' in dfCols)):
		dfWithAlt = privGetElevationNodes(dataframe, replaceOnlyNone, dataProvider, dataProviderArgs)
	elif (('startElevMeters' in dfCols) and ('endElevMeters' in dfCols)):
		dfWithAlt = privGetElevationArcsAsgn(dataframe, replaceOnlyNone, dataProvider, dataProviderArgs)	
	else:
		# This shouldn't happen...validation should catch issues
		print('Error: Invalid/unknown dataframe configuration.')
		return
		
	return dfWithAlt

def getWeather(location=None, id=None, initDF=None, metricUnits=False, dataProvider=None, dataProviderArgs=None):  
	"""
	EXPERIMENTAL.  Get weather information (current and forecasted) for a specified [lat, lon] location.

	Parameters
	----------
	location: list, Required
		A GPS coordinate of the form [lat, lon] or [lat, lon, alt].  If provided, altitude will be ignored.
	id: integer, Optional, default as None
		This value may be used to link the resulting dataframe with a different dataframe.  For example, the id could match a nodeID from a nodes dataframe.  If `id=None` and `initDF` is a weather dataframe, a new unique id will be automatically chosen.
	initDF: pandas dataframe, Optional, default as None
		If provided, the resulting weather dataframe will be appended to this dataframe.  `initDF` should be the result of calling this function.
	metricUnits: boolean, Optional, default as False
		If True, metric units (e.g., Celsius) will be used.  Otherwise, imperial units (e.g., Fahrenheit) will be used.
	dataProvider: string, Required, default as None
		Specifies the data source to be used for obtaining elevation data. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Required, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.
	
	Return
	------
	A pandas weather dataframe.
		
	Examples
	--------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()
	
	Example 1: A simple example using the minium input arguments.
		>>> myDF = vrv.getWeather(location         = [42, -78], 
		...                       dataProvider     = 'openweather', 
		...                       dataProviderArgs = {'APIkey': 'ENTER KEY HERE'})
	
	Example 2: Append to the dataframe created above.  This example uses all of the functional arguments.
		>>> myDF = vrv.getWeather(location         = [40, -80], 
		...                       id               = 2, 
		...                       initDF           = myDF, 
		...                       metricUnits      = False, 
		...                       dataProvider     = 'openweather', 
		...                       dataProviderArgs = {'APIkey': 'ENTER KEY HERE'})
	
	"""
	
	# validation
	[valFlag, errorMsg, warningMsg] = valGetWeather(location, id, initDF, metricUnits, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return None
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
	
	# Get an ID:
	if (id == None):
		id = 1
		if (type(initDF) is pd.core.frame.DataFrame):
			if (len(initDF) > 0):
				id = max(initDF['id'])+1
			
	weatherDF = privGetWeather(location, id, metricUnits, dataProvider, dataProviderArgs)

	# Combine with init dataframe:
	if (type(initDF) is pd.core.frame.DataFrame):
		if (len(initDF) > 0):
			weatherDF = pd.concat([initDF, weatherDF], ignore_index=True, sort=False)

	return weatherDF
