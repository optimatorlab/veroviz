from veroviz._common import *

from veroviz._validation import valAddStaticAssignment
from veroviz._validation import valCreateAssignmentsFromNodeSeq2D
from veroviz._validation import valCreateAssignmentsFromLocSeq2D

from veroviz._createAssignments import privAddStaticAssignment
from veroviz._getShapepoints import privGetShapepoints2D

from veroviz.utilities import initDataframe
from veroviz._getTimeDistFromLocs2D import getTimeDistFromLocs2D


def addStaticAssignment(initAssignments=None, odID=1, objectID=None, modelFile=None, modelScale=VRV_DEFAULT_CESIUMMODELSCALE, modelMinPxSize=VRV_DEFAULT_CESIUMMODELMINPXSIZE, loc=None, startTimeSec=None, endTimeSec=None):

	"""
	This function adds an "object" to an assignments dataframe.  One use of this function is to add a package or other stationary 3D model to be displayed in Cesium.  This function is also useful for holding a vehicle stationary at a location (e.g., during service or loitering).  

	Parameters
	----------
	initAssignments: :ref:`Assignments` dataframe, Optional, default as None
		If provided, the function will append a row to this dataframe.
	odID: int, Optional, default as 1
		This field allows grouping of dataframe rows according to common origin/destination pairs.  Arc segments which are part of the same origin/destination share the same odID.
	objectID: int/string, Optional, default as None
		A descriptive name or index for this object.  In the case of adding a stationary vehicle performing a service activity, the `objectID` should typically be the same as the `objectID` used by the vehicle when it was in motion.  
	modelFile: string, Optional, default as None
		The relative path and filename of the 3D model associated with this object.  The 3D model, typically in the format of `.gltf` or `.glb`, will be visualized in Cesium.  The path should be relative to the directory where Cesium is installed (i.e., the `modelFile` should exist within the Cesium root directory).
	modelScale: int, Optional, default as 100
		The scale of the 3D model (specified by the `modelFile` argument) when displayed in Cesium, such that 100 represents 100%.
	modelMinPxSize: int, Optional, default as 75
		The minimum pixel size of the 3D model (specified by the `modelFile` argument) when displayed in Cesium.  When zooming out, the model will not be smaller than this size; zooming in can result in a larger model. 
	loc: list, Required, default as None
		The coordinate of the static object, expressed as either [lat, lon, alt] or [lat, lon]. If no altitude is provided, it will be assumed to be 0 meters above ground level.
	startTimeSec: int, Required, default as None,
		Specifies the time at which this object appears.  
	endTimeSec: int, Required, default as None
		Specifies when the object is no longer displayed.  To keep the object displayed forever, set `endTimeSec = -1`.  

	Return
	------
	:ref:`Assignments` pandas.dataframe
		An assignments dataframe with a new row associated with this stationary object.

	Example
	--------
	Import veroviz and check the latest version.
		>>> import veroviz as vrv
		>>> import os

		>>> vrv.checkVersion()
		
	Create two nodes.
		>>> myNodes = vrv.createNodesFromLocs(
		...     locs = [[42.1538, -78.4253],
		...             [42.6343, -78.1146]])
		>>> myNodes

	Move the truck from one node to the other.
		>>> myAssignments = vrv.getShapepoints2D(
		...     odID           = 0,
		...     objectID       = 'truck',
		...     modelFile      = 'veroviz/models/ub_truck.gltf',
		...     modelScale     = 80, 
		...     modelMinPxSize = 20, 
		...     startLoc       = list(myNodes.loc[0][['lat', 'lon']].values),
		...     endLoc         = list(myNodes.loc[1][['lat', 'lon']].values),
		...     routeType      = 'euclidean2D',
		...     dataProvider   = None,
		...     speedMPS       = vrv.convertSpeed(55, 'miles', 'hr', 'm', 's'))	
		
	Make the truck wait at the destination.
		>>> myAssignments = vrv.addStaticAssignment(
		...     initAssignments = myAssignments, 
		...     odID            = 0, 
		...     objectID        = 'truck', 
		...     modelFile       = 'veroviz/models/ub_truck.gltf', 
		...     modelScale      = 80, 
		...     modelMinPxSize  = 20, 
		...     loc             = list(myAssignments[myAssignments['objectID']=='truck'][['endLat', 'endLon']].values[0]), 
		...     startTimeSec    = myAssignments[myAssignments['objectID']=='truck']['endTimeSec'].values[0], 
		...     endTimeSec      = myAssignments[myAssignments['objectID']=='truck']['endTimeSec'].values[0] + 30)		

	Drop off a package.
		>>> myAssignments = vrv.addStaticAssignment(
		...     initAssignments = myAssignments, 
		...     odID            = 0, 
		...     objectID        = 'package', 
		...     modelFile       = 'veroviz/models/box_blue.gltf', 
		...     modelScale      = 50, 
		...     modelMinPxSize  = 10, 
		...     loc             = list(myAssignments[myAssignments['objectID']=='truck'][['endLat', 'endLon']].values[0]), 
		...     startTimeSec    = myAssignments[myAssignments['objectID']=='truck']['endTimeSec'].values[0] + 30, 
		...     endTimeSec      = -1)

	View in Leaflet.  Note that we can't see the truck waiting.  Also, the package doesn't show up in Leaflet.
		>>> vrv.createLeaflet(nodes=myNodes, arcs=myAssignments)
		

	Create Cesium output, so we can observe our truck and package.
		>>> vrv.createCesium(
		...     assignments = myAssignments, 
		...     nodes       = myNodes, 
		...     startTime   = '08:00:00', 
		...     cesiumDir   = os.environ['CESIUMDIR'],
		...     problemDir  = 'static_object_demo')
	"""

	# validatation
	[valFlag, errorMsg, warningMsg] = valAddStaticAssignment(initAssignments, odID, objectID, modelFile, modelScale, modelMinPxSize, loc, startTimeSec, endTimeSec)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	assignments = privAddStaticAssignment(
		initAssignments = initAssignments, 
		odID            = odID, 
		objectID        = objectID, 
		modelFile       = modelFile, 
		modelScale      = modelScale, 
		modelMinPxSize  = modelMinPxSize, 
		loc             = loc, 
		startTimeSec    = startTimeSec, 
		endTimeSec      = endTimeSec)

	return assignments
	
	

def createAssignmentsFromNodeSeq2D(initAssignments=None, nodeSeq=None, nodes=None, serviceTimeSec=0.0, odID=1, objectID=None, modelFile=None, modelScale=VRV_DEFAULT_CESIUMMODELSCALE, modelMinPxSize=VRV_DEFAULT_CESIUMMODELMINPXSIZE, startTimeSec=0.0, expDurationArgs=None, routeType='euclidean2D', speedMPS=None,   leafletColor=VRV_DEFAULT_LEAFLETARCCOLOR, leafletWeight=VRV_DEFAULT_LEAFLETARCWEIGHT, leafletStyle=VRV_DEFAULT_LEAFLETARCSTYLE, leafletOpacity=VRV_DEFAULT_LEAFLETARCOPACITY, useArrows=True, cesiumColor=VRV_DEFAULT_CESIUMPATHCOLOR, cesiumWeight=VRV_DEFAULT_CESIUMPATHWEIGHT, cesiumStyle=VRV_DEFAULT_CESIUMPATHSTYLE, cesiumOpacity=VRV_DEFAULT_CESIUMPATHOPACITY, dataProvider=None, dataProviderArgs=None):
	"""
	This function generates an "assignments" dataframe containing all of the "shapepoints" between successive node locations, including timestamps indicating the departure and arrival times for each shapepoint. Shapepoints are pairs of GPS coordinates that are connected by straight lines.  For a particular origin and destination, numerous individual shapepoints can be combined to define a travel route along a road network.  

	Notes
	----
	This function is for vehicles traveling on a ground plane (2-dimensional).  For vehicles requiring an altitude component (e.g., drones), a 3D version of this function is provided by `createAssignmentsFromNodeSeq3D()`.
	
	This function creates an assignments dataframe from a sequence of nodes.  Similar functions are available to create an assignments dataframe from an arcs dataframe (createShapepointsFromArcs()) or from a sequence of locations (createShapepointsFromLocSeq()).
	
	Parameters
	----------
	initAssignments: :ref:`Assignments` dataframe, Optional, default as None
		If provided, the function will append rows to this dataframe.
	nodeSeq: list, Required
		An ordered list of node IDs.  These IDs must be included in the `id` column of the :ref:`Nodes` dataframe specified in the `nodes` input argument to this function. The format for `nodeSeq` is [node_id_1, node_id_2, ...].
	nodes: :ref:`Nodes`, Required
		A :ref:`Nodes` dataframe, which must contain the individual node IDs specified in the `nodeSeq` input argument.
	serviceTimeSec: float, Optional, default as 0.0
		Specifies a duration, in seconds, that the vehicle will be stationary at each destination node.  This service (stationary) time will not be applied to the first node in `nodeSeq`.
	odID: int, Optional, default as 1
		This field allows grouping of dataframe rows according to common origin/destination pairs.  Arc segments which are part of the same origin/destination share the same odID.
	objectID: int/string, Optional, default as None
		A descriptive name or index for a particular vehicle or object (e.g., 'truck 1', or 'red car'). 
	modelFile: string, Optional, default as None
		The relative path and filename of the 3D model associated with this object.  The 3D model, typically in the format of `.gltf` or `.glb`, will be visualized in Cesium.  The path should be relative to the directory where Cesium is installed (i.e., the `modelFile` should exist within the Cesium root directory).				
	startTimeSec: float, Optional, default as 0.0 
		The time, in seconds, at which the vehicle may leave the starting location.
	expDurationArgs: dictionary, Optional, default as None
		Sometimes there are inconsistencies between the travel times specified in the turn-by-turn navigation (i.e., shapepoints) and the travel matrices (i.e., from the getTimeDist functions).  The `expDurationArgs` field may take three different values.
		First, if `expDurationArgs` is `None` (default), the travel times will be based solely on the turn-by-turn times.  Second, if `expDurationArgs` is a dictionary with a key of `'timeSecDict'` and a corresponding value of a time dictionary (as output by `getTimeDist2D()`), then all shapepoint travel time will be adjusted/redistributed to match the values in the time dictionary.  Finally, if `expDurationArgs` is a dictionary with a key of `'getTravelTimes'` and a corresponding value of `True`, then this function will call the `getTimeDist2D()` function for each origin/destination pair.  In this case, all shapepoint travel times will be adjusted/redistributed to match the resulting values.
	routeType: string, Optional, default as 'euclidean2D'
		This describes a characteristic of the travel mode.  Possible values are: 'euclidean2D', 'manhattan', 'fastest', 'shortest', 'pedestrian', 'cycling', and 'truck'.  The 'euclidean2D' and 'manhattan' options are calculated directly from GPS coordinates, without a road network.  Neither of these two options require a data provider.  However, the other options rely on road network information and require a data provider.  Furthermore, some of those other options are not supported by all data providers.  See :ref:`Data Providers` for details.
	speedMPS: float, Conditional, default as None
		Speed of the vehicle, in units of meters per second. For route types that are not road-network based (i.e., 'euclidean2D' and 'manhattan'), this field is required to calculate travel times. Otherwise, if a route type already incorporates travel speeds from road network data, (i.e., 'fastest', 'shortest', and 'pedestrain'), this input argument may be ignored.  If provided, `speedMPS` will override travel speed data used by the route type option.
	leafletColor: string, Optional, default as "orange"
		The color of the route when displayed in Leaflet.  See :ref:`Leaflet style` for a list of available colors.
	leafletWeight: int, Optional, default as 3
		The pixel width of the route when displayed in Leaflet. 
	leafletStyle: string, Optional, default as 'solid'
		The line style of the route when displayed in Leaflet.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Leaflet style` for more information.
	leafletOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the route when displayed in Leaflet. Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	useArrows: bool, Optional, default as True
		Indicates whether arrows should be shown on the route when displayed in Leaflet.
	modelScale: int, Optional, default as 100
		The scale of the 3D model (specified by the `modelFile` argument) when displayed in Cesium, such that 100 represents 100%.
	modelMinPxSize: int, Optional, default as 75
		The minimum pixel size of the 3D model (specified by the `modelFile` argument) when displayed in Cesium.  When zooming out, the model will not be smaller than this size; zooming in can result in a larger model. 
	cesiumColor: string, Optional, default as "Cesium.Color.ORANGE"
		The color of the route when displayed in Cesium.  See :ref:`Cesium Style` for a list of available colors.
	cesiumWeight: int, Optional, default as 3
		The pixel width of the route when displayed in Cesium. 
	cesiumStyle: string, Optional, default as 'solid'
		The line style of the route when displayed in Cesium.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Cesium Style` for more information.
	cesiumOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the route when displayed in Cesium. Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for obtaining the shapepoints. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.

	Returns
	-------
	:ref:`Assignments` dataframe
		An :ref:`Assignments` dataframe containing an ordered sequence of paired GPS coordinates describing the collection of straight-line segments required to travel through the provided sequence of nodes.

	Examples
	--------
	Import veroviz and check if it's the latest version:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	The following examples assume the use of ORS as the data provider. If you have saved your API key as an environment variable, you may use `os.environ` to access it:
		>>> import os
		>>> ORS_API_KEY = os.environ['ORSKEY']
		>>> # Otherwise, you may specify your key here:
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'
	
	Generate a :ref:`Nodes` dataframe from a list of coordinates.  See :meth:`~veroviz.generateNodes.generateNodes` for other methods to generate "nodes" dataframes.
	    >>> locs = [
	    ...     [42.1538, -78.4253], 
	    ...     [42.3465, -78.6234], 
	    ...     [42.6343, -78.1146]]
	    >>> exampleNodes = vrv.createNodesFromLocs(locs=locs)

	Example 1 - A simple example using Euclidean travel, and no service times.  The assignments dataframe will have 3 rows.
		>>> assignmentsDF = vrv.createAssignmentsFromNodeSeq2D(
	    ...     nodeSeq        = [1, 3, 2, 1], 
	    ...     nodes          = exampleNodes, 
	    ...     serviceTimeSec = 0.0, 
		...     objectID       = 'Blue Car', 
		...     modelFile      = 'veroviz/models/car_blue.gltf', 
	    ...     routeType      = 'euclidean2D',
	    ...     speedMPS       = 10)
		>>> assignmentsDF
		
	Example 2 - The vehicle will follow the road network, resulting in an assignments dataframe with significantly more than 3 rows.  The vehicle will remain stationary at nodes 3, 2, and 1 (the destination nodes).  The travel time for each origin/destination pair will be calculated separately.
		>>> assignmentsDF = vrv.createAssignmentsFromNodeSeq2D(
	    ...     initAssignments  = None, 
	    ...     nodeSeq          = [1, 3, 2, 1], 
	    ...     nodes            = exampleNodes, 
	    ...     serviceTimeSec   = 20.0, 
		...     odID             = 1, 
		...     objectID         = 'Blue Car', 
		...     modelFile        = 'veroviz/models/car_blue.gltf', 
	    ...     expDurationArgs  = {'getTravelTimes': True}, 
	    ...     routeType        = 'fastest',
	    ...     dataProvider     = 'ORS-online',
	    ...     dataProviderArgs = {'APIkey' : ORS_API_KEY})
		>>> assignmentsDF
			
	Example 3 - 
		>>> # Generate a matrix of travel times:
		>>> [timeSec, distMeters] = vrv.getTimeDist2D(
	    ...     nodes            = exampleNodes,
	    ...     matrixType       = 'all2all',
	    ...     outputDistUnits  = 'meters',
	    ...     outputTimeUnits  = 'seconds',
	    ...     routeType        = 'fastest',
	    ...     speedMPS         = None,   
	    ...     dataProvider     = 'ORS-online',
	    ...     dataProviderArgs = {'APIkey' : ORS_API_KEY})

		>>> # Make our car wait for 65 seconds before starting:
		>>> assignmentsDF = vrv.addStaticAssignment(
		...     odID         = 0, 
		...     objectID     = 'Blue Car', 
		...     modelFile    = 'veroviz/models/car_blue.gltf', 
		...     loc          = [exampleNodes.loc[exampleNodes['id'] == 1]['lat'].values[0],
		...                     exampleNodes.loc[exampleNodes['id'] == 1]['lon'].values[0]], 
		...     startTimeSec = 0.0, 
		...     endTimeSec   = 65.0)		
		
		>>> # This example includes all of the available input arguments:
		>>> newAssignmentsDF = vrv.createAssignmentsFromNodeSeq2D(
	    ...     initAssignments  = assignmentsDF, 
	    ...     nodeSeq          = [1, 3, 2, 1], 
	    ...     nodes            = exampleNodes, 
	    ...     serviceTimeSec   = 20.0, 
		...     odID             = 1, 
		...     objectID         = 'Blue Car', 
		...     modelFile        = 'veroviz/models/car_blue.gltf', 
		...     modelScale       = 100,
		...     modelMinPxSize   = 75,
	    ...     startTimeSec     = 65.0, 
	    ...     expDurationArgs  = {'timeSecDict': timeSec}, 
	    ...     routeType        = 'fastest',
	    ...     speedMPS         = None,   
		...     leafletColor     = 'blue', 
		...     leafletWeight    = 3, 
		...     leafletStyle     = 'dashed', 
		...     leafletOpacity   = 0.8, 
		...     useArrows        = True, 
		...     cesiumColor      = 'Cesium.Color.BLUE', 
		...     cesiumWeight     = 3, 
		...     cesiumStyle      = 'solid', 
		...     cesiumOpacity    = 0.8, 
	    ...     dataProvider     = 'ORS-online',
	    ...     dataProviderArgs = {'APIkey' : ORS_API_KEY})
		>>> newAssignmentsDF	

	View the assignments in Leaflet:  
		>>> myMap = vrv.createLeaflet(arcs=newAssignmentsDF, nodes=exampleNodes)
	
	View the assignments in Cesium:
		>>> vrv.createCesium(
		...     assignments = newAssignmentsDF, 
		...     nodes       = exampleNodes, 
		...     startTime   = '08:00:00', 
		...     cesiumDir   = os.environ['CESIUMDIR'],
		...     problemDir  = 'createAssignments_example')
	"""	
	
	# validatation
	[valFlag, errorMsg, warningMsg] = valCreateAssignmentsFromNodeSeq2D(initAssignments, nodeSeq, nodes, serviceTimeSec, modelScale, modelMinPxSize, expDurationArgs, odID, objectID, modelFile, startTimeSec, routeType, speedMPS, leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, dataProvider, dataProviderArgs)
	
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)
		
	# Initialize an assignments dataframe:
	assignmentsDF = initDataframe('assignments')

	# if the user provided an initNode dataframe, add the new points after it
	if (type(initAssignments) is pd.core.frame.DataFrame):
		assignmentsDF = pd.concat([assignmentsDF, initAssignments], ignore_index=True, sort=False)

	startTime = startTimeSec

	for i in range(0, len(nodeSeq)-1):
		startLoc = [nodes.loc[nodes['id'] == nodeSeq[i]]['lat'].values[0],
					nodes.loc[nodes['id'] == nodeSeq[i]]['lon'].values[0]]
		endLoc   = [nodes.loc[nodes['id'] == nodeSeq[i+1]]['lat'].values[0],
					nodes.loc[nodes['id'] == nodeSeq[i+1]]['lon'].values[0]]

		if (expDurationArgs == None):
			expDurationSec = None
		elif ('timeSecDict' in expDurationArgs):
			# The user has provided a time dictionary
			expDurationSec = expDurationArgs['timeSecDict'][nodeSeq[i], nodeSeq[i+1]]	
		elif ('getTravelTimes' in expDurationArgs):
			if (expDurationArgs['getTravelTimes']):
				# Call the data provider to get travel time
				[dicTime, dicDist] = getTimeDistFromLocs2D(fromLocs=[startLoc], fromRows=[0], toLocs=[endLoc], toCols=[0], outputDistUnits='meters', outputTimeUnits='seconds', routeType=routeType, speedMPS=speedMPS, dataProvider=dataProvider, dataProviderArgs=dataProviderArgs)

				[expDurationSec, distMeters] = [dicTime[0, 0], dicDist[0, 0]]

		tmpShapepoints = privGetShapepoints2D(
			odID=odID, 
			objectID=objectID, 
			modelFile=modelFile, 
			startLoc=startLoc, 
			endLoc=endLoc, 
			startTimeSec=startTime, 
			expDurationSec=expDurationSec,
			routeType=routeType, 
			speedMPS=speedMPS,   
			leafletColor=leafletColor, 
			leafletWeight=leafletWeight, 
			leafletStyle=leafletStyle, 
			leafletOpacity=leafletOpacity, 
			useArrows=useArrows, 
			modelScale=modelScale, 
			modelMinPxSize=modelMinPxSize, 
			cesiumColor=cesiumColor, 
			cesiumWeight=cesiumWeight, 
			cesiumStyle=cesiumStyle, 
			cesiumOpacity=cesiumOpacity, 
			dataProvider=dataProvider, 
			dataProviderArgs=dataProviderArgs)


		# Update the assignments dataframe:
		assignmentsDF = pd.concat([assignmentsDF, tmpShapepoints], ignore_index=True, sort=False)

		odID += 1

		# Update the time
		startTime = max(tmpShapepoints['endTimeSec'])	
	
		if (serviceTimeSec > 0):
			# Add loitering for service
			assignmentsDF = privAddStaticAssignment(
				initAssignments = assignmentsDF, 
				odID            = odID, 
				objectID        = objectID, 
				modelFile       = modelFile, 
				modelScale      = modelScale, 
				modelMinPxSize  = modelMinPxSize, 
				loc             = endLoc,
				startTimeSec    = startTime,
				endTimeSec      = startTime + serviceTimeSec)

			odID += 1

			# Update the time again
			startTime = startTime + serviceTimeSec

    			
	return assignmentsDF		
	
	

def createAssignmentsFromLocSeq2D(initAssignments=None, locSeq=None, serviceTimeSec=0.0, odID=1, objectID=None, modelFile=None, modelScale=VRV_DEFAULT_CESIUMMODELSCALE, modelMinPxSize=VRV_DEFAULT_CESIUMMODELMINPXSIZE, startTimeSec=0.0, expDurationArgs=None, routeType='euclidean2D', speedMPS=None, leafletColor=VRV_DEFAULT_LEAFLETARCCOLOR, leafletWeight=VRV_DEFAULT_LEAFLETARCWEIGHT, leafletStyle=VRV_DEFAULT_LEAFLETARCSTYLE, leafletOpacity=VRV_DEFAULT_LEAFLETARCOPACITY, useArrows=True, cesiumColor=VRV_DEFAULT_CESIUMPATHCOLOR, cesiumWeight=VRV_DEFAULT_CESIUMPATHWEIGHT, cesiumStyle=VRV_DEFAULT_CESIUMPATHSTYLE, cesiumOpacity=VRV_DEFAULT_CESIUMPATHOPACITY, dataProvider=None, dataProviderArgs=None):
	"""
	This function generates an "assignments" dataframe containing all of the "shapepoints" between successive locations, including timestamps indicating the departure and arrival times for each shapepoint. Shapepoints are pairs of GPS coordinates that are connected by straight lines.  For a particular origin and destination, numerous individual shapepoints can be combined to define a travel route along a road network.  

	Notes
	----
	This function is for vehicles traveling on a ground plane (2-dimensional).  For vehicles requiring an altitude component (e.g., drones), a 3D version of this function is provided by `createAssignmentsFromLocSeq3D()`.
	
	This function creates an assignments dataframe from a sequence of [lat, lon] locations.  Similar functions are available to create an assignments dataframe from an arcs dataframe (createShapepointsFromArcs()) or from a sequence of nodes (createShapepointsFromNodeSeq()).
	
	Parameters
	----------
	initAssignments: :ref:`Assignments` dataframe, Optional, default as None
		If provided, the function will append rows to this dataframe.
	locSeq: list of lists, Required, default as None
		An ordered list of locations that will be converted into an :ref:`Arcs` dataframe. The list should be formated as [[lat1, lon1], [lat2, lon2], ..., [latn, lonn]] or [[lat1, lon1, alt1], [lat2, lon2, alt2], ..., [latn, lonn, altn]].  If provided, altitude values will be ignored.
	serviceTimeSec: float, Optional, default as 0.0
		Specifies a duration, in seconds, that the vehicle will be stationary at each destination node.  This service (stationary) time will not be applied to the first node in `nodeSeq`.
	odID: int, Optional, default as 1
		This field allows grouping of dataframe rows according to common origin/destination pairs.  Arc segments which are part of the same origin/destination share the same odID.
	objectID: int/string, Optional, default as None
		A descriptive name or index for a particular vehicle or object (e.g., 'truck 1', or 'red car'). 
	modelFile: string, Optional, default as None
		The relative path and filename of the 3D model associated with this object.  The 3D model, typically in the format of `.gltf` or `.glb`, will be visualized in Cesium.  The path should be relative to the directory where Cesium is installed (i.e., the `modelFile` should exist within the Cesium root directory).				
	startTimeSec: float, Optional, default as 0.0 
		The time, in seconds, at which the vehicle may leave the starting location.
	expDurationArgs: dictionary, Optional, default as None
		Sometimes there are inconsistencies between the travel times specified in the turn-by-turn navigation (i.e., shapepoints) and the travel matrices (i.e., from the getTimeDist functions).  The `expDurationArgs` field may take two different values.
		First, if `expDurationArgs` is `None` (default), the travel times will be based solely on the turn-by-turn times.  Second, if `expDurationArgs` is a dictionary with a key of `'getTravelTimes'` and a corresponding value of `True`, then this function will call the `getTimeDist2D()` function for each origin/destination pair.  In this case, all shapepoint travel times will be adjusted/redistributed to match the resulting values.
	routeType: string, Optional, default as 'euclidean2D'
		This describes a characteristic of the travel mode.  Possible values are: 'euclidean2D', 'manhattan', 'fastest', 'shortest', 'pedestrian', 'cycling', and 'truck'.  The 'euclidean2D' and 'manhattan' options are calculated directly from GPS coordinates, without a road network.  Neither of these two options require a data provider.  However, the other options rely on road network information and require a data provider.  Furthermore, some of those other options are not supported by all data providers.  See :ref:`Data Providers` for details.
	speedMPS: float, Conditional, default as None
		Speed of the vehicle, in units of meters per second. For route types that are not road-network based (i.e., 'euclidean2D' and 'manhattan'), this field is required to calculate travel times. Otherwise, if a route type already incorporates travel speeds from road network data, (i.e., 'fastest', 'shortest', and 'pedestrain'), this input argument may be ignored.  If provided, `speedMPS` will override travel speed data used by the route type option.
	leafletColor: string, Optional, default as "orange"
		The color of the route when displayed in Leaflet.  See :ref:`Leaflet style` for a list of available colors.
	leafletWeight: int, Optional, default as 3
		The pixel width of the route when displayed in Leaflet. 
	leafletStyle: string, Optional, default as 'solid'
		The line style of the route when displayed in Leaflet.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Leaflet style` for more information.
	leafletOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the route when displayed in Leaflet. Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	useArrows: bool, Optional, default as True
		Indicates whether arrows should be shown on the route when displayed in Leaflet.
	modelScale: int, Optional, default as 100
		The scale of the 3D model (specified by the `modelFile` argument) when displayed in Cesium, such that 100 represents 100%.
	modelMinPxSize: int, Optional, default as 75
		The minimum pixel size of the 3D model (specified by the `modelFile` argument) when displayed in Cesium.  When zooming out, the model will not be smaller than this size; zooming in can result in a larger model. 
	cesiumColor: string, Optional, default as "Cesium.Color.ORANGE"
		The color of the route when displayed in Cesium.  See :ref:`Cesium Style` for a list of available colors.
	cesiumWeight: int, Optional, default as 3
		The pixel width of the route when displayed in Cesium. 
	cesiumStyle: string, Optional, default as 'solid'
		The line style of the route when displayed in Cesium.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Cesium Style` for more information.
	cesiumOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the route when displayed in Cesium. Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for obtaining the shapepoints. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.

	Returns
	-------
	:ref:`Assignments` dataframe
		An :ref:`Assignments` dataframe containing an ordered sequence of paired GPS coordinates describing the collection of straight-line segments required to travel through the provided sequence of locations.

	Examples
	--------
	Import veroviz and check if it's the latest version:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	The following examples assume the use of ORS as the data provider. If you have saved your API key as an environment variable, you may use `os.environ` to access it:
		>>> import os
		>>> ORS_API_KEY = os.environ['ORSKEY']
		>>> # Otherwise, you may specify your key here:
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'
	
	Specify a sequence of [lat, lon] or [lat, lon, alt] locations. 
	    >>> locs = [
	    ...     [42.1538, -78.4253, 30], 
	    ...     [42.3465, -78.6234, 30], 
	    ...     [42.6343, -78.1146, 40],
	    ...     [42.1538, -78.4253, 30]] 

	Example 1 - A simple example using Euclidean travel, and no service times.  The assignments dataframe will have 3 rows.
		>>> assignmentsDF = vrv.createAssignmentsFromLocSeq2D(
	    ...     locSeq         = locs, 
	    ...     serviceTimeSec = 0.0, 
		...     objectID       = 'Blue Car', 
		...     modelFile      = 'veroviz/models/car_blue.gltf', 
	    ...     routeType      = 'euclidean2D',
	    ...     speedMPS       = 10)
		>>> assignmentsDF
		
	Example 2 - The vehicle will follow the road network, resulting in an assignments dataframe with significantly more than 3 rows.  The vehicle will remain stationary at the destination locations.  The travel time for each origin/destination pair will be calculated separately.
		>>> # Make our car wait for 65 seconds before starting:
		>>> assignmentsDF = vrv.addStaticAssignment(
		...     odID         = 0, 
		...     objectID     = 'Blue Car', 
		...     modelFile    = 'veroviz/models/car_blue.gltf', 
		...     loc          = locs[0], 
		...     startTimeSec = 0.0, 
		...     endTimeSec   = 65.0)		

		>>> # This example includes all of the available input arguments:
		>>> newAssignmentsDF = vrv.createAssignmentsFromLocSeq2D(
	    ...     initAssignments  = assignmentsDF, 
	    ...     locSeq           = locs, 
	    ...     serviceTimeSec   = 20.0, 
		...     odID             = 1, 
		...     objectID         = 'Blue Car', 
		...     modelFile        = 'veroviz/models/car_blue.gltf', 
		...     modelScale       = 100,
		...     modelMinPxSize   = 75,
	    ...     startTimeSec     = 65.0, 
	    ...     expDurationArgs  = {'getTravelTimes': True}, 
	    ...     routeType        = 'fastest',
	    ...     speedMPS         = None,   
		...     leafletColor     = 'blue', 
		...     leafletWeight    = 3, 
		...     leafletStyle     = 'dashed', 
		...     leafletOpacity   = 0.8, 
		...     useArrows        = True, 
		...     cesiumColor      = 'Cesium.Color.BLUE', 
		...     cesiumWeight     = 3, 
		...     cesiumStyle      = 'solid', 
		...     cesiumOpacity    = 0.8, 
	    ...     dataProvider     = 'ORS-online',
	    ...     dataProviderArgs = {'APIkey' : ORS_API_KEY})
		>>> newAssignmentsDF			

	Generate a :ref:`Nodes` dataframe from our first three locations (the fourth location is a duplicate of the first).  See :meth:`~veroviz.generateNodes.generateNodes` for other methods to generate "nodes" dataframes.
	    >>> exampleNodes = vrv.createNodesFromLocs(locs=locs[0:3])

	View the assignments in Leaflet:  
		>>> myMap = vrv.createLeaflet(arcs=newAssignmentsDF, nodes=exampleNodes)
	
	View the assignments in Cesium:
		>>> vrv.createCesium(
		...     assignments = newAssignmentsDF, 
		...     nodes       = exampleNodes, 
		...     startTime   = '08:00:00', 
		...     cesiumDir   = os.environ['CESIUMDIR'],
		...     problemDir  = 'createAssignments_example')
	"""	
	
	# validatation
	[valFlag, errorMsg, warningMsg] = valCreateAssignmentsFromLocSeq2D(initAssignments, locSeq, serviceTimeSec, modelScale, modelMinPxSize, expDurationArgs, odID, objectID, modelFile, startTimeSec, routeType, speedMPS, leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, dataProvider, dataProviderArgs)
	
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)
		
	# Initialize an assignments dataframe:
	assignmentsDF = initDataframe('assignments')

	# if the user provided an initNode dataframe, add the new points after it
	if (type(initAssignments) is pd.core.frame.DataFrame):
		assignmentsDF = pd.concat([assignmentsDF, initAssignments], ignore_index=True, sort=False)

	startTime = startTimeSec

	for i in range(0, len(locSeq)-1):
		startLoc = locSeq[i]
		endLoc   = locSeq[i+1]

		if (expDurationArgs == None):
			expDurationSec = None
		elif ('getTravelTimes' in expDurationArgs):
			if (expDurationArgs['getTravelTimes']):
				# Call the data provider to get travel time
				[dicTime, dicDist] = getTimeDistFromLocs2D(fromLocs=[startLoc], fromRows=[0], toLocs=[endLoc], toCols=[0], outputDistUnits='meters', outputTimeUnits='seconds', routeType=routeType, speedMPS=speedMPS, dataProvider=dataProvider, dataProviderArgs=dataProviderArgs)

				[expDurationSec, distMeters] = [dicTime[0, 0], dicDist[0, 0]]

		tmpShapepoints = privGetShapepoints2D(
			odID=odID, 
			objectID=objectID, 
			modelFile=modelFile, 
			startLoc=startLoc, 
			endLoc=endLoc, 
			startTimeSec=startTime, 
			expDurationSec=expDurationSec,
			routeType=routeType, 
			speedMPS=speedMPS,   
			leafletColor=leafletColor, 
			leafletWeight=leafletWeight, 
			leafletStyle=leafletStyle, 
			leafletOpacity=leafletOpacity, 
			useArrows=useArrows, 
			modelScale=modelScale, 
			modelMinPxSize=modelMinPxSize, 
			cesiumColor=cesiumColor, 
			cesiumWeight=cesiumWeight, 
			cesiumStyle=cesiumStyle, 
			cesiumOpacity=cesiumOpacity, 
			dataProvider=dataProvider, 
			dataProviderArgs=dataProviderArgs)


		# Update the assignments dataframe:
		assignmentsDF = pd.concat([assignmentsDF, tmpShapepoints], ignore_index=True, sort=False)

		odID += 1

		# Update the time
		startTime = max(tmpShapepoints['endTimeSec'])	
	
		if (serviceTimeSec > 0):
			# Add loitering for service
			assignmentsDF = privAddStaticAssignment(
				initAssignments = assignmentsDF, 
				odID            = odID, 
				objectID        = objectID, 
				modelFile       = modelFile, 
				modelScale      = modelScale, 
				modelMinPxSize  = modelMinPxSize, 
				loc             = endLoc,
				startTimeSec    = startTime,
				endTimeSec      = startTime + serviceTimeSec)

			odID += 1

			# Update the time again
			startTime = startTime + serviceTimeSec

    			
	return assignmentsDF		