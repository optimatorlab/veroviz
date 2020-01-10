from veroviz._common import *
from veroviz._validation import *
from veroviz._geometry import *
from veroviz._internal import *
from veroviz._geocode import privGeocode, privReverseGeocode

def convertSpeed(speed, fromUnitsDist, fromUnitsTime, toUnitsDist, toUnitsTime):
	"""
	Convert a speed to different units.

	Parameters
	----------
	speed: float
		The numeric value describing a speed to be converted.
	fromUnitsDist: string
		Distance units for the given speed, before conversion. See :ref:`Units` for options.
	fromUnitsTime: string
		Time units for the given speed, before conversion. See :ref:`Units` for options.
	toUnitsDist: string
		Distance units for the speed after conversion. See :ref:`Units` for options.
	toUnitTime: string
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	try:
		fromUnitsDist = fromUnitsDist.lower()
	except:
		pass

	fromUnitsDist = distanceUnitsDictionary[fromUnitsDist]
	if (fromUnitsDist == 'm'):
		tmpSpeed = speed * 1.0
	elif (fromUnitsDist == 'km'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_KILOMETER
	elif (fromUnitsDist == 'mi'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_MILE
	elif (fromUnitsDist == 'ft'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_FEET
	elif (fromUnitsDist == 'yard'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_YARD
	elif (fromUnitsDist == 'nmi'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_NAUTICAL_MILE

	try:
		fromUnitsTime = fromUnitsTime.lower()
	except:
		pass

	fromUnitsTime = timeUnitsDictionary[fromUnitsTime]
	if (fromUnitsTime == 's'):
		tmpSpeed = tmpSpeed / 1.0
	elif (fromUnitsTime == 'min'):
		tmpSpeed = tmpSpeed / VRV_CONST_SECONDS_PER_MINUTE
	elif (fromUnitsTime == 'h'):
		tmpSpeed = tmpSpeed / VRV_CONST_SECONDS_PER_HOUR

	try:
		toUnitsDist = toUnitsDist.lower()
	except:
		pass

	toUnitsDist = distanceUnitsDictionary[toUnitsDist]
	if (toUnitsDist == 'm'):
		tmpSpeed = tmpSpeed / 1.0
	elif (toUnitsDist == 'km'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_KILOMETER
	elif (toUnitsDist == 'mi'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_MILE
	elif (toUnitsDist == 'ft'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_FEET
	elif (toUnitsDist == 'yard'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_YARD
	elif (toUnitsDist == 'nmi'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_NAUTICAL_MILE

	try:
		toUnitsTime = toUnitsTime.lower()
	except:
		pass

	toUnitsTime = timeUnitsDictionary[toUnitsTime]
	if (toUnitsTime == 's'):
		convSpeed = tmpSpeed * 1.0
	elif (toUnitsTime == 'min'):
		convSpeed = tmpSpeed * VRV_CONST_SECONDS_PER_MINUTE
	elif (toUnitsTime == 'h'):
		convSpeed = tmpSpeed * VRV_CONST_SECONDS_PER_HOUR

	return convSpeed

def convertDistance(distance, fromUnits, toUnits):
	"""
	Convert a distance to different units.

	Parameters
	----------
	distance: float
		The numeric value describing a distance to be converted.
	fromUnits: string
		Distance units before conversion. See :ref:`Units` for options.
	toUnits: string
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	try:
		fromUnits = fromUnits.lower()
	except:
		pass

	fromUnits = distanceUnitsDictionary[fromUnits]
	if (fromUnits == 'm'):
		tmpDist = distance * 1.0
	elif (fromUnits == 'km'):
		tmpDist = distance * VRV_CONST_METERS_PER_KILOMETER
	elif (fromUnits == 'mi'):
		tmpDist = distance * VRV_CONST_METERS_PER_MILE
	elif (fromUnits == 'ft'):
		tmpDist = distance * VRV_CONST_METERS_PER_FEET
	elif (fromUnits == 'yard'):
		tmpDist = distance * VRV_CONST_METERS_PER_YARD
	elif (fromUnits == 'nmi'):
		tmpDist = distance * VRV_CONST_METERS_PER_NAUTICAL_MILE

	try:
		toUnits = toUnits.lower()
	except:
		pass

	toUnits = distanceUnitsDictionary[toUnits]
	if (toUnits == 'm'):
		convDist = tmpDist / 1.0
	elif (toUnits == 'km'):
		convDist = tmpDist / VRV_CONST_METERS_PER_KILOMETER
	elif (toUnits == 'mi'):
		convDist = tmpDist / VRV_CONST_METERS_PER_MILE
	elif (toUnits == 'ft'):
		convDist = tmpDist / VRV_CONST_METERS_PER_FEET
	elif (toUnits == 'yard'):
		convDist = tmpDist / VRV_CONST_METERS_PER_YARD
	elif (toUnits == 'nmi'):
		convDist = tmpDist / VRV_CONST_METERS_PER_NAUTICAL_MILE

	return convDist

def convertTime(time, fromUnits, toUnits):
	"""
	Convert a time to different units.

	Parameters
	----------
	time: float
		The numeric value describing a time to be converted.
	fromUnits: string
		Time units before conversion. See :ref:`Units` for options.
	toUnits: string
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	try:
		fromUnits = fromUnits.lower()
	except:
		pass

	fromUnits = timeUnitsDictionary[fromUnits]
	if (fromUnits == 's'):
		tmpTime = time * 1.0
	elif (fromUnits == 'min'):
		tmpTime = time * VRV_CONST_SECONDS_PER_MINUTE
	elif (fromUnits == 'h'):
		tmpTime = time * VRV_CONST_SECONDS_PER_HOUR

	try:
		toUnits = toUnits.lower()
	except:
		pass

	toUnits = timeUnitsDictionary[toUnits]
	if (toUnits == 's'):
		convTime = tmpTime / 1.0
	elif (toUnits == 'min'):
		convTime = tmpTime / VRV_CONST_SECONDS_PER_MINUTE
	elif (toUnits == 'h'):
		convTime = tmpTime / VRV_CONST_SECONDS_PER_HOUR

	return convTime

def convertArea(area, fromUnits, toUnits):
	"""
	Convert an area from `fromUnits` to `toUnits`.

	Parameters
	----------
	area: float
		The numeric value describing an area to be converted.
	fromUnits: string
		Area units, before conversion. See :ref:`Units` for options.
	toUnits: string
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
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

def initDataframe(dataframeType):
	"""
	Return an empty dataframe of a given type.

	Parameters
	----------
	dataframeType: string
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	try:
		dataframeType = dataframeType.lower()
	except:
		pass

	if (dataframeType == 'nodes'):
		dataframe = pd.DataFrame(
			columns=nodesColumnList)
	elif (dataframeType == 'assignments'):
		dataframe = pd.DataFrame(
			columns=assignmentsColumnList)
	elif (dataframeType == 'arcs'):
		dataframe = pd.DataFrame(
			columns=arcsColumnList)
	else:
		return

	return dataframe

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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	# Adjust the scope of the map to proper
	allLats = []
	allLons = []
	if (nodes is not None):
		allLats.extend(nodes['lat'].tolist())
		allLons.extend(nodes['lon'].tolist())

	if (arcs is not None):
		allLats.extend(arcs['startLat'].tolist())
		allLats.extend(arcs['endLat'].tolist())
		allLons.extend(arcs['startLon'].tolist())
		allLons.extend(arcs['endLon'].tolist())

	if (locs is not None):
		for i in range(len(locs)):
			allLats.append(locs[i][0])
			allLons.append(locs[i][1])

	maxLat = max(allLats)
	minLat = min(allLats)
	maxLon = max(allLons)
	minLon = min(allLons)

	if (abs(maxLat - minLat) < 0.0001):
		maxLat = maxLat + 0.05
		minLat = minLat - 0.05
	if (abs(maxLon - minLon) < 0.0001):
		maxLon = maxLon + 0.05
		minLon = minLon - 0.05

	maxLat = maxLat + 0.01
	minLat = minLat - 0.01
	maxLon = maxLon + 0.01
	minLon = minLon - 0.01

	return [[minLat, maxLon], [maxLat, minLon]]

def convertMatricesDataframeToDictionary(dataframe):
	"""
	This function is intended for use with time/distance matrices, which are stored in veroviz as Python dictionaries. This function transforms a matrix dataframe into  a dictionary, such that the indices of columns and rows become a tuple key for the dictionary.

	Parameters
	----------
	dataframe: pandas.dataframe
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

	dictionary = {}
	try:
		(rowNum, columnNum) = dataframe.shape
		for i in range(rowNum):
			for j in range(columnNum):
				dictionary[dataframe.index[i], dataframe.columns[j]] = dataframe.at[dataframe.index[i], dataframe.columns[j]]
	except:
		print("Error: Duplicated key values, please check the columns and rows of dataframe")

	return dictionary

def convertMatricesDictionaryToDataframe(dictionary):
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

def exportDataToCSV(data, filename):
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

	if (VRV_SETTING_SHOWOUTPUTMESSAGE):
		print("Message: Data written to %s." % (filename))

	return

def importDataFromCSV(dataType, filename):
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

def exportDataframe(dataframe, filename):
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

	try:
		dataframe.to_csv(path_or_buf=filename, encoding='utf-8')
		if (VRV_SETTING_SHOWOUTPUTMESSAGE):
			print("Message: Data written to %s." % (filename))
	except:
		print("Error: Cannot export dataframe, please check the inputs.")

	return

def importDataframe(filename, intCols=False, useIndex=True):
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

	# Replace backslash
	filename = replaceBackslashToSlash(filename)

	if (type(filename) is not str):
		print("Error: filename should be a string, please check the inputs.")
		return

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

def getConvexHull(locs):
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
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

def isPointInPoly(loc, poly):
	"""
	Determine if a point is inside a polygon.  Points that are along the perimeter of the polygon (including vertices) are considered to be "inside".

	Parameters
	----------
	loc: list
		The coordinate of the point, in either [lat, lon] or [lat, lon, alt] format.  If provided, the altitude will be ignored.
	poly: list of lists
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	loc2D = [loc[0], loc[1]]
	poly2D = []
	for i in range(len(poly)):
		poly2D.append([poly[i][0], poly[i][1]])

	inside = geoIsPointInPoly(loc2D, poly2D)

	return inside

def isPathInPoly(path, poly):
	"""
	Determine if a given path is completely within the boundary of a polygon.

	Parameters
	----------
	path: list of lists
		A list of coordinates in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  This is considered as an open polyline.
	poly: list of lists
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	path2D = []
	for i in range(len(path)):
		path2D.append([path[i][0], path[i][1]])
	poly2D = []
	for i in range(len(poly)):
		poly2D.append([poly[i][0], poly[i][1]])

	inside = geoIsPathInPoly(path2D, poly2D)

	return inside

def isPathCrossPoly(path, poly):
	"""
	Determine if a given path crosses the boundary of a polygon.

	Parameters
	----------
	path: list of lists
		A list of coordinates in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  This is considered as an open polyline.
	poly: list of lists
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	path2D = []
	for i in range(len(path)):
		path2D.append([path[i][0], path[i][1]])
	poly2D = []
	for i in range(len(poly)):
		poly2D.append([poly[i][0], poly[i][1]])

	crossFlag = geoIsPathCrossPoly(path2D, poly2D)

	return crossFlag

def isPassPath(loc, path, tolerance):
	'''
	Determine if any point along a path is within tolerance meters of a stationary point.
	(did our path pass by the target?)

	Parameters
	----------
	loc: list
		The stationary point to be tested if it has been passed, in either [lat, lon] or [lat, lon, alt] format.  If provided, the altitude will be ignored.
	path: list of lists
		A list of coordinates in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  This is considered as an open polyline.
	tolerance: float
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	loc2D = [loc[0], loc[1]]
	path2D = []
	for i in range(len(path)):
		path2D.append([path[i][0], path[i][1]])

	passFlag = geoIsPassPath(loc2D, path2D, tolerance)

	return passFlag

def pointInDistance2D(loc, direction, distMeters):
	"""
	Find the [lat, lon, alt] coordinate of a point that is a given distance away from a current location at a given heading. This can be useful for determining where a vehicle may be in the future (assuming constant velocity and straight-line travel).

	Parameters
	----------
	loc: list
		The starting location, expressed as either [lat, lon, alt] or [lat, lon]. If no altitude is provided, it will be assumed to be 0 meters above ground level.
	direction: float
		The direction of travel from the current location, in units of degrees.  The range is [0, 360], where north is 0 degrees, east is 90 degrees, south is 180 degrees, and west is 270 degrees.
	distMeters: float
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	loc2D = [loc[0], loc[1]]

	newLoc = geoPointInDistance2D(loc2D, direction, distMeters)

	if (len(loc) == 3):
		newLoc = [newLoc[0], newLoc[1], loc[2]]

	return newLoc

def minDistLoc2Path(loc, path):
	"""
	Calculate the minimum distance, in [meters], from a single stationary location (target) to any point along a path.

	Parameters
	----------
	loc: list
		The coordinate of the stationary location, in either [lat, lon] or [lat, lon, alt] format.  If provided, the altitude will be ignored.
	path: list of lists
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	distMeters = geoMinDistLoc2Path(loc, path)

	return distMeters

def distance2D(loc1, loc2):
	"""
	Calculates the geodesic distance between two locations, using the geopy library.  Altitude is ignored.

	Parameters
	----------
	loc1: list
		First location, in [lat, lon] format.
	loc2: list
		Second location, in [lat, lon] format.

	Return
	------
	float
		Geodesic distance between the two locations.

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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	distMeters = geoDistance2D(loc1, loc2)

	return distMeters

def distance3D(loc1, loc2):
	"""
	Estimates the distance between two point, including changes in altitude.  The calculation combines geopy's geodesic distance (along the surface of an ellipsoidal model of the earth) with a simple estimate of additional travel distance due to altitude changes.

	Parameters
	----------
	loc1: list
		First location, in [lat, lon, alt] format.
	loc2: list
		Second location, in [lat, lon, alt] format.

	Return
	------
	float
		Distance between the two locations.

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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	distMeters = geoDistance3D(loc1, loc2)

	return distMeters

def distancePath2D(path):
	"""
	Calculate the total geodesic distance along a path defined by [lat, lon] coordinates.

	Parameters
	----------
	path: list of lists
		A list of coordinates that form a path, in the format of [[lat, lon], [lat, lon], ...].

	Return
	------
	float
		Total length of the path.

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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	dist = 0
	for i in range(0, len(path) - 1):
		dist += distance2D(path[i], path[i + 1])

	return dist

def getHeading(currentLoc, goalLoc):
	"""
	Finds the heading required to travel from a current location to a goal location.  North is 0-degrees, east is 90-degrees, south is 180-degrees, west is 270-degrees.

	Parameters
	----------
	currentLoc: list
		The [lat, lon] of current location
	goalLoc: list
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
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
		...     'drone': {'model': 'veroviz/models/drone.gltf',
		...               'leafletColor': 'red',
		...               'cesiumColor': 'Cesium.Color.RED'},
		...     'truck': {'model': 'veroviz/models/ub_truck.gltf',
		...               'leafletColor': 'blue',
		...               'cesiumColor': 'Cesium.Color.BLUE'}
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)


	output = {}

	asgnCopy = assignments.copy()

	# Get list of unique objectIDs:
	uniqueIDs = list(asgnCopy['objectID'].unique())

	# Replace "-1" end time with +infinity
	asgnCopy.loc[asgnCopy['endTimeSec'] < 0, 'endTimeSec'] = float('Inf')

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
				if (endTimeSec < float('Inf')):
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
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
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
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	[loc, address] = privReverseGeocode(location, dataProvider, dataProviderArgs)

	return (loc, address)

def closestNodeLoc2Path(loc, path):
    """
    Gives the closest node on a path given a given GPS location

    Parameters
    ----------
    loc: list
        The coordinate of the current coordinate, in [lat, lon, alt] format
    path:
        list of lists
        A list of coordinates in the form of [[lat, lon], [lat, lon], ..., [lat, lon]], it will be considered as open polyline
    Returns
    -------
    minLoc: list of lat and lon of a location
        A location in distance with given direction, in [lat, lon] form.
    """

    distMeters = geoDistance3D(loc, path[0])
    minLoc = path[0]

    for i in range(len(path)):
        tmpDistMeters = geoDistance3D(loc, path[i])
        tempLoc = path[i]
        if (distMeters > tmpDistMeters):
            distMeters = tmpDistMeters
            minLoc = tempLoc

    return minLoc

    distMeters = geoDistance3D(loc, path[0])
    minLoc = path[0]

    for i in range(len(path)):
        tmpDistMeters = geoDistance3D(loc, path[i])
        tempLoc = path[i]
        if (distMeters > tmpDistMeters):
            distMeters = tmpDistMeters
            minLoc = tempLoc

    return minLoc

def closestPointLoc2Path(loc, line):
     """
    Given a line of a path find the closest point on a path given a given GPS location

    Parameters
    ----------
    loc: list
        The coordinate of the current coordinate, in [lat, lon, alt] format
    line:
        list of locations
        A list of two coordinates in the form of [lat, lon]
    Returns
    -------
    minLoc: list of lat and lon of a location
        A location in distance with given direction, in [lat, lon] form.
    """
    # The line is denoted as AB, the stationary location is denoted by S
    locA = line[0]
    locB = line[1]
    locS = loc
    minLoc =[locA[0],locA[1]]

    # Check if the loc is on line, if so return the location
    if (geoIsOnSegment(loc, line)):
            return locS


    # Vectors start from A
    vecAS = [float(locS[0] - locA[0]), float(locS[1] - locA[1])]
    vecAB = [float(locB[0] - locA[0]), float(locB[1] - locA[1])]

    # Vectors start from B
    vecBS = [float(locS[0] - locB[0]), float(locS[1] - locB[1])]
    vecBA = [float(locA[0] - locB[0]), float(locA[1] - locB[1])]

    # cos value for A angle and B angle
    cosSAB = geoFindCos(vecAS, vecAB)
    cosSBA = geoFindCos(vecBS, vecBA)

    # if both angles are sharp, the closest point will be in the line and sloved for, otherwise the closest point is at the edge and that location is returned
    if (cosSAB >= 0 and cosSBA >= 0):
        print(2)
        xA = locA[0]
        yA =locA[1]

        xB = locB[0]
        yB =locB[1]

        xS = locS[0]
        yS =locS[1]

        dx = xB-xA
        dy = yB-yA

        det = dx*dx + dy*dy
        a = (((dy*(yS-yA)) + (dx*(xS-xA)))/ det)

        xP = xA+(a*dx)
        yP = yA+(a*dy)

        minLoc = [xP,yP]

    else:
        distAS = geoDistance2D(locS, locA)
        distBS = geoDistance2D(locS, locB)

        if(distAS < distBS):
            print(3)
            minLoc = locA
        else:
            print(3)
            minLoc = locB

    return minLoc

def minDistLoc2Path(loc, path):
  """
    Given a path, it find the closest point on a path given a given GPS location

    Parameters
    ----------
    loc: list
        The coordinate of the current coordinate, in [lat, lon, alt] format
    Path:
        list of locations
        A list of coordinates in the form of [lat, lon]
    Returns
    -------
    minLoc: list of lat and lon of a location
        A location in distance with given direction, in [lat, lon] form.
    """
    lstLine = []
    for i in range(1, len(path)):
        lstLine.append([path[i - 1], path[i]])

    distMeters = closestPointLoc2Path(loc, lstLine[0])
    minPoint = loc

    for i in range(len(lstLine)):
        tmpDistMeters = geoMinDistLoc2Line(loc, lstLine[i])
        minPoint = geoMinLoc2Line(loc, lstLine[i])

        if (distMeters > tmpDistMeters):
            distMeters = tmpDistMeters
            minPoint = geoMinLoc2Line(loc, lstLine[i])

    return minPoint
