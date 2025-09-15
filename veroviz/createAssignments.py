from veroviz._common import *

from veroviz._validation import valAddAssignment2D
from veroviz._validation import valAddAssignment3D
from veroviz._validation import valAddStaticAssignment
from veroviz._validation import valCreateAssignmentsFromArcs2D
from veroviz._validation import valCreateAssignmentsFromNodeSeq2D
from veroviz._validation import valCreateAssignmentsFromLocSeq2D

from veroviz._createAssignments import privAddStaticAssignment
from veroviz._getShapepoints import privGetShapepoints2D
from veroviz._getShapepoints import privGetShapepoints3D

from veroviz._utilities import privInitDataframe
from veroviz._getTimeDistFromLocs2D import getTimeDistFromLocs2D

from veroviz._internal import stripCesiumColor

def addAssignment2D(initAssignments=None, odID=1, objectID=None, modelFile=None, startLoc=None, endLoc=None, startTimeSec=0.0, expDurationSec=None, routeType='euclidean2D', speedMPS=None, leafletColor=config['VRV_DEFAULT_LEAFLETARCCOLOR'], leafletWeight=config['VRV_DEFAULT_LEAFLETARCWEIGHT'], leafletStyle=config['VRV_DEFAULT_LEAFLETARCSTYLE'], leafletOpacity=config['VRV_DEFAULT_LEAFLETARCOPACITY'], leafletCurveType=config['VRV_DEFAULT_ARCCURVETYPE'], leafletCurvature=config['VRV_DEFAULT_ARCCURVATURE'], useArrows=True, modelScale=config['VRV_DEFAULT_CESIUMMODELSCALE'], modelMinPxSize=config['VRV_DEFAULT_CESIUMMODELMINPXSIZE'], cesiumColor=config['VRV_DEFAULT_CESIUMPATHCOLOR'], cesiumWeight=config['VRV_DEFAULT_CESIUMPATHWEIGHT'], cesiumStyle=config['VRV_DEFAULT_CESIUMPATHSTYLE'], cesiumOpacity=config['VRV_DEFAULT_CESIUMPATHOPACITY'], ganttColor=config['VRV_DEFAULT_GANTTCOLOR'], popupText=None, dataProvider=None, dataProviderArgs=None):

	"""
	This function appends to an existing :ref:`Assignments` dataframe, or creates a new :ref:`Assignments` dataframe if `initAssignments` is None.  The new rows in this dataframe describe all of the "shapepoints" between given starting and ending locations, including timestamps indicating the departure and arrival times for each shapepoint. Shapepoints are pairs of GPS coordinates that are connected by straight lines.  For a given origin and destination, numerous individual shapepoints can be combined to define a travel route along a road network.   

	Note
	----
	This function is for vehicles traveling on a ground plane (2-dimensional).  For vehicles requiring an altitude component (e.g., drones), a 3D version of this function is provided by `addAssignment3D()`.
	
	Parameters
	----------
	initAssignments: :ref:`Assignments` dataframe, Optional, default as None
		If provided, the function will append this dataframe.
	odID: int, Optional, default as 1
		This field allows grouping of dataframe rows according to common origin/destination pairs.  Arc segments which are part of the same origin/destination share the same odID.
	objectID: int/string, Optional, default as None
		A descriptive name or index for a particular vehicle or object (e.g., 'truck 1', or 'red car'). 
	modelFile: string, Optional, default as None
		The relative path and filename of the 3D model associated with this object.  The 3D model, typically in the format of `.gltf` or `.glb`, will be visualized in Cesium.  The path should be relative to the directory where Cesium is installed (i.e., the `modelFile` should exist within the Cesium root directory).
	startLoc: list, Required, default as None
		The starting location, expressed as either [lat, lon, alt] or [lat, lon]. If no altitude is provided, it will be assumed to be 0 meters above ground level.
	endLoc: list, Required, default as None
		The ending location, expressed as either [lat, lon, alt] or [lat, lon]. If no altitude is provided, it will be assumed to be 0 meters above ground level.
	startTimeSec: float, Optional, default as 0.0 
		The time, in seconds, at which the vehicle may leave the starting location.
	expDurationSec: float, Optional, default as None
		This is the number of seconds we expect to travel from the start to the end location. This value typically comes from the traval time matrix (see the getTimeDist functions).  Including an expected duration will help keep these two values in alignment.  If necessary, travel times for the individual shapepoints will be redistributed.
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
	leafletCurveType: string, Optional, default as 'straight'
		The type of curve to be shown on leaflet map for :ref:Arc dataframes (curves will not be applied to :ref:Assignments dataframes). The options are 'Bezier', 'greatcircle', and 'straight'. If Bezier is provided, the leafletCurvature is also required. If greatcircle is provided, the arc follow the curvature of the Earth.
	leafletCurvature: float in (-90, 90), Conditional, default as 45
		If leafletCurveType is 'Bezier', then leafletCurvature is required; otherwise this argument will not be used. The curvature specifies the angle between a straight line connecting the two nodes and the curved arc emanating from those two nodes. Therefore, this value should be in the open interval (-90, 90), although values in the (-45, 45) range tend to work best.
	useArrows: bool, Optional, default as True
		Indicates whether arrows should be shown on the route when displayed in Leaflet.
	modelScale: int, Optional, default as 100
		The scale of the 3D model (specified by the `modelFile` argument) when displayed in Cesium, such that 100 represents 100%.
	modelMinPxSize: int, Optional, default as 75
		The minimum pixel size of the 3D model (specified by the `modelFile` argument) when displayed in Cesium.  When zooming out, the model will not be smaller than this size; zooming in can result in a larger model. 
	cesiumColor: string, Optional, default as "orange"
		The color of the route when displayed in Cesium.  See :ref:`Cesium Style` for a list of available colors.
	cesiumWeight: int, Optional, default as 3
		The pixel width of the route when displayed in Cesium. 
	cesiumStyle: string, Optional, default as 'solid'
		The line style of the route when displayed in Cesium.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Cesium Style` for more information.
	cesiumOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the route when displayed in Cesium. Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	ganttColor: string, Optional, default as "darkgray"
		The color of the route elements when displayed in a Gantt chart. 
	popupText: string, Optional, default as None
		Text (or HTML) that will be displayed when a user clicks on the arc in either Leaflet or Cesium. 	
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for obtaining the shapepoints. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.

	Returns
	-------
	:ref:`Assignments` dataframe
		An :ref:`Assignments` dataframe containing an ordered sequence of paired GPS coordinates describing the collection of straight-line segments required to travel from a start location to an end location.
		
	endTimeSec: float
		The time, in seconds, at which the end location is reached.  
		
		
	Examples
	--------
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
		>>> myNodes

	View these nodes on a map:
		>>> vrv.createLeaflet(nodes=myNodes)

	We're going to hard-code a solution.
		>>> # A car will start at node 1, visit nodes 2 and 3, and then return to node 1.
		>>> # A truck will follow a route from 1->5->4->1.
		>>> mySolution = {
		...     'car': [[1,2], [2,3], [3,1]],
		...     'truck': [[1,5], [5,4], [4,1]]
		>>> }

	Define some information about our 2 vehicles, for later use:
		>>> vehicleProperties = {
		...     'car':   {'model': 'veroviz/models/car_red.gltf',
		...               'leafletColor': 'red',
		...               'cesiumColor': 'red'},
		...     'truck': {'model': 'veroviz/models/ub_truck.glb',
		...               'leafletColor': 'blue',
		...               'cesiumColor': 'blue'}
		>>> }

	The following examples assume the use of ORS as the data provider. If you have saved your API key as an environment variable, you may use `os.environ` to access it:
		>>> import os
		>>> ORS_API_KEY = os.environ['ORSKEY']
		>>> # Otherwise, you may specify your key here:
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'
	
	
	Example 1 -- The vehicles will visit the nodes in their routes, without any service times. Assume Euclidean travel (ignoring the road network).	
		>>> # Build the assignments dataframe for the 2 vehicle routes.
		>>> # No service times, Euclidean travel:
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
		...             leafletColor    = vehicleProperties[v]['leafletColor'],
		...             cesiumColor     = vehicleProperties[v]['cesiumColor'])
		>>> myAssignments	
	
		>>> # Show the routes (and nodes) on a map:
		>>> vrv.createLeaflet(nodes=myNodes, arcs=myAssignments)	
	
	
	Example 2 -- The vehicles will now travel on the road network, but we'll still ignore service times.
		>>> # No service times, Travel on road network:
		>>> myAssignments = vrv.initDataframe('assignments')
		>>> for v in mySolution:
		...     endTimeSec = 0.0
		...     for arc in mySolution[v]:
		...         [myAssignments, endTimeSec] = vrv.addAssignment2D(
		...             initAssignments  = myAssignments,
		...             objectID         = v,
		...             modelFile        = vehicleProperties[v]['model'],
		...             startLoc         = list(myNodes[myNodes['id'] == arc[0]][['lat', 'lon']].values[0]),
		...             endLoc           = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...             startTimeSec     = endTimeSec,
		...             leafletColor     = vehicleProperties[v]['leafletColor'],
		...             cesiumColor      = vehicleProperties[v]['cesiumColor'], 
		...             routeType        = 'fastest',
		...             dataProvider     = 'ORS-online', 
		...             dataProviderArgs = {'APIkey': ORS_API_KEY})
		>>> myAssignments 

		>>> # Show the routes (and nodes) on a map:
		>>> vrv.createLeaflet(nodes=myNodes, arcs=myAssignments)	
	
	Example 3 -- The vehicles are still following the road network, but now we'll force them to match the travel times specified in a travel matrix.	
		>>> # We'll first create the travel time and distance matrices:
		>>> [timeSec, distMeters] = vrv.getTimeDist2D(nodes            = myNodes,
		...                                           routeType        = 'fastest',
		...                                           dataProvider     = 'ORS-online',
		...                                           dataProviderArgs = {'APIkey': ORS_API_KEY})	

		>>> # No service times, Travel on road network, use travel times from the distance matrix:
		>>> # added "expDurationSec"
		>>> myAssignments = vrv.initDataframe('assignments')
		>>> for v in mySolution:
		...     endTimeSec = 0.0
		...     for arc in mySolution[v]:
		...         [myAssignments, endTimeSec] = vrv.addAssignment2D(
		...             initAssignments  = myAssignments,
		...             objectID         = v,
		...             modelFile        = vehicleProperties[v]['model'],
		...             startLoc         = list(myNodes[myNodes['id'] == arc[0]][['lat', 'lon']].values[0]),
		...             endLoc           = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...             startTimeSec     = endTimeSec,
		...             expDurationSec   = timeSec[arc[0], arc[1]],
		...             leafletColor     = vehicleProperties[v]['leafletColor'],
		...             cesiumColor      = vehicleProperties[v]['cesiumColor'], 
		...             routeType        = 'fastest',
		...             dataProvider     = 'ORS-online', 
		...             dataProviderArgs = {'APIkey': ORS_API_KEY})
		>>> myAssignments   


	Example 4 -- Add service times at each destination node
		>>> # 60-second service times at destinations, Travel on road network, use travel times from the distance matrix.
		>>> # Added use of `addStaticAssignment()` function for the service component.
		>>> myAssignments = vrv.initDataframe('assignments')
		>>> for v in mySolution:
		...     endTimeSec = 0.0
		...     for arc in mySolution[v]:
		...         [myAssignments, endTimeSec] = vrv.addAssignment2D(
		...             initAssignments  = myAssignments,
		...             objectID         = v,
		...             modelFile        = vehicleProperties[v]['model'],
		...             startLoc         = list(myNodes[myNodes['id'] == arc[0]][['lat', 'lon']].values[0]),
		...             endLoc           = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...             startTimeSec     = endTimeSec,
		...             expDurationSec   = timeSec[arc[0], arc[1]],
		...             leafletColor     = vehicleProperties[v]['leafletColor'],
		...             cesiumColor      = vehicleProperties[v]['cesiumColor'], 
		...             routeType        = 'fastest',
		...             dataProvider     = 'ORS-online', 
		...             dataProviderArgs = {'APIkey': ORS_API_KEY})
		...         
		...         myAssignments = vrv.addStaticAssignment(
		...             initAssignments  = myAssignments,
		...             objectID         = v,
		...             modelFile        = vehicleProperties[v]['model'],
		...             loc              = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...             startTimeSec     = endTimeSec,
		...             endTimeSec       = endTimeSec + 60.0)
        
		...         endTimeSec += 60
		>>> myAssignments  	
	
	
	Example 5 -- Extend the previous example to show packages being left at destination nodes	
		>>> # 30-second service times at destinations, Travel on road network:
		>>> # added another use of `addStaticAssignment()` function to drop packages.
		>>> myAssignments = vrv.initDataframe('assignments')
		>>> for v in mySolution:
		...     endTimeSec = 0.0
		...     for arc in mySolution[v]:
		...         [myAssignments, endTimeSec] = vrv.addAssignment2D(
		...             initAssignments  = myAssignments,
		...             objectID         = v,
		...             modelFile        = vehicleProperties[v]['model'],
		...             startLoc         = list(myNodes[myNodes['id'] == arc[0]][['lat', 'lon']].values[0]),
		...             endLoc           = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...             startTimeSec     = endTimeSec,
		...             leafletColor     = vehicleProperties[v]['leafletColor'],
		...             cesiumColor      = vehicleProperties[v]['cesiumColor'], 
		...             routeType        = 'fastest',
		...             dataProvider     = 'ORS-online', 
		...             dataProviderArgs = {'APIkey': ORS_API_KEY})
		...         
		...         myAssignments = vrv.addStaticAssignment(
		...             initAssignments  = myAssignments,
		...             objectID         = v,
		...             modelFile        = vehicleProperties[v]['model'],
		...             loc              = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...             startTimeSec     = endTimeSec,
		...             endTimeSec       = endTimeSec + 30.0)
		...         
		...         endTimeSec += 30
		... 
		...         myAssignments = vrv.addStaticAssignment(
		...             initAssignments  = myAssignments,
		...             objectID         = 'package %s %d' % (v, arc[1]),
		...             modelFile        = '/veroviz/models/box_yellow.gltf',
		...             loc              = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...             startTimeSec     = endTimeSec,
		...             endTimeSec       = -1)        
		>>> myAssignments 
	

	If you have saved your Cesium path as an environment variable, you may use `os.environ` to access it:
		>>> import os
		>>> CESIUM_DIR = os.environ['CESIUMDIR']
		>>> # Otherwise, you may specify the patch to Cesium here:
		>>> # CESIUM_DIR = '/provide/path/to/Cesium/' 

	Generate a 3D movie of the routes:
		>>> vrv.createCesium(assignments = myAssignments, 
		...                  nodes       = myNodes, 
		...                  cesiumDir   = CESIUM_DIR, 
		...                  problemDir  = 'addAssignment2D_example')

	"""
	
	# validatation
	[valFlag, errorMsg, warningMsg] = valAddAssignment2D(initAssignments, odID, objectID, modelFile, startLoc, endLoc, startTimeSec, expDurationSec, routeType, speedMPS, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor, dataProvider, dataProviderArgs)
	
	if (not valFlag):
		print (errorMsg)
		return (None, None)
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
		
	# Initialize an assignments dataframe:
	assignmentsDF = None

	# if the user provided an initAssignments dataframe, add the new points after it
	if (type(initAssignments) is pd.core.frame.DataFrame):
		if (len(initAssignments) > 0):
			assignmentsDF = pd.DataFrame(initAssignments.copy(), columns = privInitDataframe('assignments').columns)
			odID = max(max(assignmentsDF['odID'])+1, odID)
	
	tmpShapepoints = privGetShapepoints2D(
		odID             = odID, 
		objectID         = objectID, 
		modelFile        = modelFile, 
		startLoc         = startLoc, 
		endLoc           = endLoc, 
		startTimeSec     = startTimeSec, 
		expDurationSec   = expDurationSec,
		routeType        = routeType, 
		speedMPS         = speedMPS,   
		leafletColor     = leafletColor, 
		leafletWeight    = leafletWeight, 
		leafletStyle     = leafletStyle, 
		leafletOpacity   = leafletOpacity, 
		leafletCurveType = leafletCurveType, 
		leafletCurvature = leafletCurvature,		
		useArrows        = useArrows, 
		modelScale       = modelScale, 
		modelMinPxSize   = modelMinPxSize, 
		cesiumColor      = stripCesiumColor(cesiumColor), 
		cesiumWeight     = cesiumWeight, 
		cesiumStyle      = cesiumStyle, 
		cesiumOpacity    = cesiumOpacity,
		ganttColor       = ganttColor, 
		popupText        = popupText,
		dataProvider     = dataProvider, 
		dataProviderArgs = dataProviderArgs)

	# Capture the end time
	endTimeSec = max(tmpShapepoints['endTimeSec'])

	# Update the assignments dataframe:
	if (assignmentsDF is not None):
		assignmentsDF = pd.concat([assignmentsDF, tmpShapepoints], ignore_index=True, sort=False)
	else:
		assignmentsDF = pd.DataFrame(tmpShapepoints, columns = privInitDataframe('assignments').columns)
		
	return (assignmentsDF, endTimeSec)
	

def addAssignment3D(initAssignments=None, odID=1, objectID=None, modelFile=None, startTimeSec=0.0, startLoc=None, endLoc=None, takeoffSpeedMPS=None, cruiseSpeedMPS=None, landSpeedMPS=None, cruiseAltMetersAGL=None, routeType='square', climbRateMPS=None, descentRateMPS=None, earliestLandTime=-1, loiterPosition='arrivalAtAlt', leafletColor=config['VRV_DEFAULT_LEAFLETARCCOLOR'], leafletWeight=config['VRV_DEFAULT_LEAFLETARCWEIGHT'], leafletStyle=config['VRV_DEFAULT_LEAFLETARCSTYLE'], leafletOpacity=config['VRV_DEFAULT_LEAFLETARCOPACITY'], leafletCurveType=config['VRV_DEFAULT_ARCCURVETYPE'], leafletCurvature=config['VRV_DEFAULT_ARCCURVATURE'],  useArrows=True, modelScale=config['VRV_DEFAULT_CESIUMMODELSCALE'], modelMinPxSize=config['VRV_DEFAULT_CESIUMMODELMINPXSIZE'], cesiumColor=config['VRV_DEFAULT_CESIUMPATHCOLOR'], cesiumWeight=config['VRV_DEFAULT_CESIUMPATHWEIGHT'], cesiumStyle=config['VRV_DEFAULT_CESIUMPATHSTYLE'], cesiumOpacity=config['VRV_DEFAULT_CESIUMPATHOPACITY'], ganttColor=config['VRV_DEFAULT_GANTTCOLOR'], popupText=None):

	"""
	This function appends to an existing :ref:`Assignments` dataframe, or creates a new :ref:`Assignments` dataframe if `initAssignments` is None.  The new rows in this dataframe describe all of the vehicle movements between given starting and ending locations, including timestamps indicating the departure and arrival times for each intermediate point. 

	Note
	----
	This function is for vehicles whose travel path includes changes in altitude (e.g., drones).  For ground vehicles traveling on a ground plane, a 2-dimensional version of this function is provided by `addAssignment2D()`.

	Parameters
	----------
	odID: int, Optional, default as 1
		This field allows grouping of dataframe rows according to common origin/destination pairs.  Arc segments which are part of the same origin/destination share the same odID.
	objectID: int/string, Optional, default as None
		A descriptive name or index for a particular vehicle or object (e.g., 'plane 1', or 'blue drone'). 
	modelFile: string, Optional, default as None
		The relative path and filename of the 3D model associated with this object.  The 3D model, typically in the format of `.gltf` or `.glb`, will be visualized in Cesium.  The path should be relative to the directory where Cesium is installed (i.e., the `modelFile` should exist within the Cesium root directory).
	startTimeSec: float, Optional, default as 0.0 
		The time, in seconds, at which the vehicle may leave the starting location.
	startLoc: list, Required, default as 'None'
		The starting location, expressed as either [lat, lon, alt] or [lat, lon]. If no altitude is provided, it will be assumed to be 0 meters above ground level.
	endLoc: list, Required, default as 'None'
		The ending location, expressed as either [lat, lon, alt] or [lat, lon]. If no altitude is provided, it will be assumed to be 0 meters above ground level.
	takeoffSpeedMPS: float, Conditional, default as None
		The speed of the aircraft, in meters per second, during the "takeoff" phase.  This will apply only to 'square' and 'trapezoidal' route types.  The takeoff phase is the first component of these route types, and is associated with an increase in altitude.  The takeoff speed is assumed to be constant, and ignores acceleration.  See :ref:`Flight Profile and Flight Path` for additional information.
	cruiseSpeedMPS: float, Conditional, default as None
		The speed of the aircraft, in meters per second, during the "cruising" phase.  This will apply to all of the route options.  Typically, the cruising phase occurs at a constant altitude, as specified by `cruiseAltMetersAGL`.  However, for the 'triangular' route type, cruiseSpeedMPS specifies the constant travel speed during both the ascent to, and immediate descent from, the cruise altitude.  In the 'triangle' route type, the aircraft has no horizontal travel at the cruise altitude.  In all cases, the cruise speed is assumed to be constant, and ignores acceleration.  See :ref:`Flight Profile and Flight Path` for additional information.
	landSpeedMPS: float, Conditional, default as None
		The speed of the aircraft, in meters per second, during the "landing" phase. This will apply to only the 'square' and 'trapezoidal' route types.  The landing phase is the last component of these route types, and is associated with a decrease in altitude.  The landing speed is assumed to be constant, and ignore deceleration.  See :ref:`Flight Profile and Flight Path` for additional information.
	cruiseAltMetersAGL: float, Conditional, default as None
		The altitude, in meters above ground level, at which the aircraft is in the "cruise" phase.  This phase is typically associated with horizontal movement at a fixed altitude.  The exception is for the 'triangular' route type, in which case the aircraft instantaneously transitions from ascent to descent at the cruise altitude (i.e., there is no horizontal travel at this altitude).  All but the 'straight' route type require/use the cruise altitude.  See :ref:`Flight Profile and Flight Path` for additional details.
	routeType: string, Optional, default as 'square'
		Specifies the basic shape of the flight profile.  Valid options include 'square', 'triangular', 'trapezoidal', and 'straight'.  The square profile involves a vertical takeoff to a cruising altitude, horizontal travel at the cruising altitude, and a vertical landing.  The trapezoidal profile describes a takeoff phase in which the aircraft increases altitude and travels horizontally towards the destination until reaching the cruising altitude, horizontal travel at the cruising altitude, and a landing phase in which the aircraft decreases altitude and travels horizontally until reaching the destination.  For the trapezoidal profile, the horizontal movement during the takeoff and landing phases is a function of the `climbRateMPS` and `descentRateMPS`, respectively.  The triangular profile describes an ascent to the cruising altitude followed immediately by a descent to the destination.  Finally, the straight profile describes straight-line flight directly from the starting location to the ending location; the altitudes of these two locations may differ.  See :ref:`Flight Profile and Flight Path` for a description of these flight profiles.
	climbRateMPS: float, Conditional, default as None
		This parameter is used only for the 'trapezoidal' route type, and is in units of meters per second.  It describes the rate at which the aircraft increases its altitude, relative to the value of `takeoffSpeedMPS`.  If `climbRateMPS == takeoffSpeedMPS`, then the takeoff phase will be purely vertical.  If `climbRateMPS` is close to zero, then the takeoff phase will be characterized by a slow increase in altitude (and longer horizontal flight).  The aircraft's actual travel speed during the climb will be `takeoffSpeedMPS`.  See :ref:`Flight Profile and Flight Path` for additional details.
	descentRateMPS: float, Conditional, default as None
		This parameter is used only for the 'trapezoidal' route type, and is in units of meters per second.  It describes the rate at which the aircraft decreases its altitude, relative to the value of `landSpeedMPS`.  If `descentRateMPS == landSpeedMPS`, then the landing phase will be purely vertical.  If `descentRateMPS` is close to zero, then the landing phase will be characterized by a slow decrease in altitude (and longer horizontal flight).  The aircraft's actual travel speed during the descent will be `landSpeedMPS`.  See :ref:`Flight Profile and Flight Path` for additional details.
	earliestLandTime: float, Optional, default as -1
		Specifies the earliest time, in seconds, that the vehicle is allowed to complete travel to the ending location.  This parameter is useful in cases where time windows exist, or if a flying vehicle must wait for another vehicle (e.g., a drone that cannot land until a truck has arrived to recover it).  The default value of `-1` indicates that there is no restriction on the earliest landing time.
	loiterPosition: string, Optional, default as 'arrivalAtAlt'
		The position where the vehicle loiters if its un-delayed travel time from start to end would result in an arrival before `earliestLandTime`.  Valid options are 'beforeTakeoff', 'takeoffAtAlt', 'arrivalAtAlt', 'afterLand'. See :ref:`Flight Profile and Flight Path` for details.
	leafletColor: string, Optional, default as "orange"
		The color of the route when displayed in Leaflet.  See :ref:`Leaflet style` for a list of available colors.
	leafletWeight: int, Optional, default as 3
		The pixel width of the route when displayed in Leaflet. 
	leafletStyle: string, Optional, default as 'solid'
		The line style of the route when displayed in Leaflet.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Leaflet style` for more information.
	leafletOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the route when displayed in Leaflet. Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	leafletCurveType: string, Optional, default as 'straight'
		The type of curve to be shown on leaflet map for :ref:Arc dataframes (curves will not be applied to :ref:Assignments dataframes). The options are 'Bezier', 'greatcircle', and 'straight'. If Bezier is provided, the leafletCurvature is also required. If greatcircle is provided, the arc follow the curvature of the Earth.
	leafletCurvature: float in (-90, 90), Conditional, default as 45
		If leafletCurveType is 'Bezier', then leafletCurvature is required; otherwise this argument will not be used. The curvature specifies the angle between a straight line connecting the two nodes and the curved arc emanating from those two nodes. Therefore, this value should be in the open interval (-90, 90), although values in the (-45, 45) range tend to work best.
	useArrows: bool, Optional, default as True
		Indicates whether arrows should be shown on the route when displayed in Leaflet.
	modelScale: int, Optional, default as 100
		The scale of the 3D model (specified by the `modelFile` argument) when displayed in Cesium, such that 100 represents 100%.
	modelMinPxSize: int, Optional, default as 75
		The minimum pixel size of the 3D model (specified by the `modelFile` argument) when displayed in Cesium.  When zooming out, the model will not be smaller than this size; zooming in can result in a larger model. 
	cesiumColor: string, Optional, default as "orange"
		The color of the route when displayed in Cesium.  See :ref:`Cesium Style` for a list of available colors.
	cesiumWeight: int, Optional, default as 3
		The pixel width of the route when displayed in Cesium. 
	cesiumStyle: string, Optional, default as 'solid'
		The line style of the route when displayed in Cesium.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Cesium Style` for more information.
	cesiumOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the route when displayed in Cesium. Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	ganttColor: string, Optional, default as "darkgray"
		The color of the route elements when displayed in a Gantt chart.  	
	popupText: string, Optional, default as None
		Text (or HTML) that will be displayed when a user clicks on the arc in either Leaflet or Cesium.
		
	Return
	-------
	:ref:`Assignments` dataframe
		An :ref:`Assignments` dataframe containing an ordered sequence of paired GPS coordinates and altitudes describing the collection of straight-line segments required to travel from a start location to an end location.

	Examples
	--------
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
		>>> myNodes

	View these nodes on a map:
		>>> vrv.createLeaflet(nodes=myNodes)


	Example 1 -- Assume a single drone delivers packages from node 1 to all other nodes.
		>>> # Hard-code a solution:
		>>> mySolution = {
		...     'drone': [[1,2,1], [1,3,1], [1,4,1], [1,5,1]]
		>>> }


	Define some information about our drone, for later use:
		>>> vehicleProperties = {
		...     'drone': {'modelPackage': 'veroviz/models/drone_package.glb',
		...               'modelEmpty': 'veroviz/models/drone.glb',
		...               'leafletColor': 'red',
		...               'cesiumColor': 'red'},
		>>> }



	Build the assignments for the drone deliveries:
		>>> myAssignments = vrv.initDataframe('assignments')
		>>> 
		>>> endTimeSec = 0.0
		>>> for arc in mySolution['drone']:
		...     # Fly from i to j with a package:
		...     [myAssignments, endTimeSec] = vrv.addAssignment3D(
		...         initAssignments    = myAssignments,
		...         objectID           = 'drone',
		...         modelFile          = vehicleProperties['drone']['modelPackage'],
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
		... 
		...     # Drop off a package
		...     myAssignments = vrv.addStaticAssignment(
		...             initAssignments  = myAssignments,
		...             objectID         = 'package %d' % (arc[1]),
		...             modelFile        = '/veroviz/models/box_yellow.gltf',
		...             loc              = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...             startTimeSec     = endTimeSec,
		...             endTimeSec       = -1)  
		...         
		...     # Fly from j to k empty:
		...     [myAssignments, endTimeSec] = vrv.addAssignment3D(
		...         initAssignments    = myAssignments,
		...         objectID           = 'drone',
		...         modelFile          = vehicleProperties['drone']['modelEmpty'],
		...         startLoc           = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...         endLoc             = list(myNodes[myNodes['id'] == arc[2]][['lat', 'lon']].values[0]),
		...         startTimeSec       = endTimeSec,
		...         takeoffSpeedMPS    = vrv.convertSpeed(30, 'miles', 'hr', 'meters', 'sec'),
		...         cruiseSpeedMPS     = vrv.convertSpeed(80, 'miles', 'hr', 'meters', 'sec'),
		...         landSpeedMPS       = vrv.convertSpeed( 5, 'miles', 'hr', 'meters', 'sec'),
		...         cruiseAltMetersAGL = vrv.convertDistance(350, 'feet', 'meters'),
		...         routeType          = 'square',
		...         leafletColor       = vehicleProperties['drone']['leafletColor'],
		...         cesiumColor        = vehicleProperties['drone']['cesiumColor'])
		... 
		>>> myAssignments


	Show the nodes and assignments on a map:
		>>> vrv.createLeaflet(nodes=myNodes, arcs=myAssignments)

	If you have saved your Cesium path as an environment variable, you may use `os.environ` to access it:
		>>> import os
		>>> CESIUM_DIR = os.environ['CESIUMDIR']
		>>> # Otherwise, you may specify the patch to Cesium here:
		>>> # CESIUM_DIR = '/provide/path/to/Cesium/' 

	Create a 3D movie of the drone deliveries:
		>>> vrv.createCesium(assignments = myAssignments, 
		...                  nodes       = myNodes, 
		...                  cesiumDir   = CESIUM_DIR, 
		...                  problemDir  = 'addAssignment3D_example1')


	Example 2 -- Coordinate deliveries with a drone launched from a truck
		>>> # Hard-code a solution.
		>>> # The truck will visit nodes 1->3->5->1
		>>> # The drone will launch from the truck at node 1, deliver to node 2, and return to the truck at node 3.
		>>> # The drone will then launch from the truck at 1, deliver to 4 and return to 5.
		>>> # The drone cannot land at nodes 3 and 5 until the truck has arrived.
		>>> mySolution = {
		...     'drone': [[1,2,3], [3,4,5]],
		...     'truck': [[1,3], [3,5], [5,1]]
		>>> }


	Define some information about our 2 vehicles, for use below:
		>>> vehicleProperties = {
		...     'drone': {'modelPackage': 'veroviz/models/drone_package.glb',
		...               'modelEmpty': 'veroviz/models/drone.glb',
		...               'leafletColor': 'red',
		...               'cesiumColor': 'red'},
		...     'truck': {'model': 'veroviz/models/ub_truck.glb',
		...               'leafletColor': 'blue',
		...               'cesiumColor': 'blue'}
		>>> }


		>>> # This example assumes the use of ORS as the data provider. 
		>>> # If you have saved your API key as an environment variable, you may use `os.environ` to access it:
		>>> import os
		>>> ORS_API_KEY = os.environ['ORSKEY']
		>>> # Otherwise, you may specify your key here:
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'

		>>> # Obtain the travel times for the truck:
		>>> [timeSecTruck, distMetersTruck] = vrv.getTimeDist2D(
		...     nodes            = myNodes,
		...     routeType        = 'fastest',
		...     dataProvider     = 'ORS-online',
		...     dataProviderArgs = {'APIkey': ORS_API_KEY})

		>>> # Obtain the travel times for the drone:
		>>> [timeSecDrone, groundDist, TotalDist] = vrv.getTimeDist3D(
		...     nodes            = myNodes,
		...     takeoffSpeedMPS    = vrv.convertSpeed(30, 'miles', 'hr', 'meters', 'sec'),
		...     cruiseSpeedMPS     = vrv.convertSpeed(80, 'miles', 'hr', 'meters', 'sec'),
		...     landSpeedMPS       = vrv.convertSpeed( 5, 'miles', 'hr', 'meters', 'sec'),
		...     cruiseAltMetersAGL = vrv.convertDistance(350, 'feet', 'meters'),
		...     routeType          = 'square')

		>>> # Find the coordination times for the truck and drone.
		>>> # These will be the earliest times that both the truck and drone can arrive at a node.
		>>> maxArrivalTime = {}
		>>> 
		>>> # 1) The truck travels from 1 to 3; the drone travels from 1 to 2 to 3:
		>>> truckArrivalTime = timeSecTruck[1,3]
		>>> droneArrivalTime = timeSecDrone[1,2] + timeSecDrone[2,3]
		>>> maxArrivalTime[3] = max(truckArrivalTime, droneArrivalTime)
		>>> 
		>>> # 2) The truck travels from 3 to 5; the drone travels from 3 to 4 to 5:
		>>> truckArrivalTime = maxArrivalTime[3] + timeSecTruck[3,5]
		>>> droneArrivalTime = maxArrivalTime[3] + timeSecDrone[3,4] + timeSecDrone[4,5]
		>>> maxArrivalTime[5] = max(truckArrivalTime, droneArrivalTime)
		>>> 
		>>> # 3) Let's also capture the time at which the truck will return to node 1:
		>>> maxArrivalTime[1] = maxArrivalTime[5] + timeSecTruck[5,1]
		>>> 
		>>> # maxArrival Time[1] is now the total time required to complete all of the deliveries
		>>> maxArrivalTime

	Build assignments for the drone deliveries:
		>>> myAssignments = vrv.initDataframe('assignments')
		>>>  
		>>> endTimeSec = 0.0
		>>> for arc in mySolution['drone']:
		...     # Fly from i to j with a package:
		...     [myAssignments, endTimeSec] = vrv.addAssignment3D(
		...         initAssignments    = myAssignments,
		...         objectID           = 'drone',
		...         modelFile          = vehicleProperties['drone']['modelPackage'],
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
		... 
		...     # Drop off a package
		...     myAssignments = vrv.addStaticAssignment(
		...             initAssignments  = myAssignments,
		...             objectID         = 'package %d' % (arc[1]),
		...             modelFile        = '/veroviz/models/box_yellow.gltf',
		...             loc              = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...             startTimeSec     = endTimeSec,
		...             endTimeSec       = -1)  
		...     
		...     # Fly from j to k empty:
		...     [myAssignments, endTimeSec] = vrv.addAssignment3D(
		...         initAssignments    = myAssignments,
		...         objectID           = 'drone',
		...         modelFile          = vehicleProperties['drone']['modelEmpty'],
		...         startLoc           = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...         endLoc             = list(myNodes[myNodes['id'] == arc[2]][['lat', 'lon']].values[0]),
		...         startTimeSec       = endTimeSec,
		...         takeoffSpeedMPS    = vrv.convertSpeed(30, 'miles', 'hr', 'meters', 'sec'),
		...         cruiseSpeedMPS     = vrv.convertSpeed(80, 'miles', 'hr', 'meters', 'sec'),
		...         landSpeedMPS       = vrv.convertSpeed( 5, 'miles', 'hr', 'meters', 'sec'),
		...         cruiseAltMetersAGL = vrv.convertDistance(350, 'feet', 'meters'),
		...         routeType          = 'square',
		...         earliestLandTime   = maxArrivalTime[arc[2]],
		...         loiterPosition     = 'arrivalAtAlt',
		...         leafletColor       = vehicleProperties['drone']['leafletColor'],
		...         cesiumColor        = vehicleProperties['drone']['cesiumColor'])
		... 
		>>> myAssignments


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
		...     
		...     # If necessary, wait for the drone to arrive:
		...     if (endTimeSec < maxArrivalTime[arc[1]]):
		...         myAssignments = vrv.addStaticAssignment(
		...             initAssignments  = myAssignments,
		...             objectID         = 'truck',
		...             modelFile        = vehicleProperties['truck']['model'],
		...             loc              = list(myNodes[myNodes['id'] == arc[1]][['lat', 'lon']].values[0]),
		...             startTimeSec     = endTimeSec,
		...             endTimeSec       = maxArrivalTime[arc[1]])
		... 
		...         endTimeSec = maxArrivalTime[arc[1]]  
		>>> myAssignments

	Show the nodes and assignments on a map:
		>>> vrv.createLeaflet(nodes=myNodes, arcs=myAssignments)

	Create a 3D movie of the drone deliveries:
		>>> vrv.createCesium(assignments = myAssignments, 
		...                  nodes       = myNodes, 
		...                  cesiumDir   = CESIUM_DIR, 
		...                  problemDir  = 'addAssignment3D_example1')

	"""	
	
	# validatation
	[valFlag, errorMsg, warningMsg] = valAddAssignment3D(initAssignments, odID, objectID, modelFile, startTimeSec, startLoc, endLoc, takeoffSpeedMPS, cruiseSpeedMPS, landSpeedMPS, cruiseAltMetersAGL, routeType, climbRateMPS, descentRateMPS, earliestLandTime, loiterPosition, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor)
	
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	assignmentsDF = None
	
	# if the user provided an initAssignments dataframe, add the new points after it
	if (type(initAssignments) is pd.core.frame.DataFrame):
		if (len(initAssignments) > 0):
			assignmentsDF = pd.DataFrame(initAssignments.copy(), columns = privInitDataframe('assignments').columns)
			odID = max(max(assignmentsDF['odID'])+1, odID)

	tmpShapepoints = privGetShapepoints3D(
		odID               = odID, 
		objectID           = objectID, 
		modelFile          = modelFile, 
		startTimeSec       = startTimeSec, 
		startLoc           = startLoc, 
		endLoc             = endLoc, 
		takeoffSpeedMPS    = takeoffSpeedMPS, 
		cruiseSpeedMPS     = cruiseSpeedMPS, 
		landSpeedMPS       = landSpeedMPS, 
		cruiseAltMetersAGL = cruiseAltMetersAGL, 
		routeType          = routeType, 
		climbRateMPS       = climbRateMPS, 
		descentRateMPS     = descentRateMPS, 
		earliestLandTime   = earliestLandTime, 
		loiterPosition     = loiterPosition, 
		leafletColor       = leafletColor, 
		leafletWeight      = leafletWeight, 
		leafletStyle       = leafletStyle, 
		leafletOpacity     = leafletOpacity, 
		leafletCurveType   = leafletCurveType, 
		leafletCurvature   = leafletCurvature, 
		useArrows          = useArrows, 
		modelScale         = modelScale, 
		modelMinPxSize     = modelMinPxSize, 
		cesiumColor        = stripCesiumColor(cesiumColor), 
		cesiumWeight       = cesiumWeight, 
		cesiumStyle        = cesiumStyle, 
		cesiumOpacity      = cesiumOpacity,
		ganttColor         = ganttColor, 
		popupText          = popupText)

	# Capture the end time
	endTimeSec = max(tmpShapepoints['endTimeSec'])

	# Update the assignments dataframe:
	if (assignmentsDF is not None):
		# Exclude all-NA columns before concatenation
		initCleaned = initAssignments.dropna(axis=1, how='all')	
		assignmentsDF = pd.concat([initCleaned, tmpShapepoints], ignore_index=True, sort=False)
	else:
		assignmentsDF = pd.DataFrame(tmpShapepoints, columns = privInitDataframe('assignments').columns)		
					
	return (assignmentsDF, endTimeSec)


def addStaticAssignment(initAssignments=None, odID=1, objectID=None, modelFile=None, modelScale=config['VRV_DEFAULT_CESIUMMODELSCALE'], modelMinPxSize=config['VRV_DEFAULT_CESIUMMODELMINPXSIZE'], loc=None, startTimeSec=None, endTimeSec=None, ganttColor=config['VRV_DEFAULT_GANTTCOLOR'], popupText=None):

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
	ganttColor: string, Optional, default as "darkgray"
		The color of this assignment when displayed in a Gantt chart. 
	popupText: string, Optional, default as None
		Text (or HTML) that will be displayed when a user clicks on the arc in either Leaflet or Cesium.  	

	Return
	------
	:ref:`Assignments` pandas.dataframe
		An assignments dataframe with a new row associated with this stationary object.

	Example
	-------
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
		...     modelFile      = 'veroviz/models/ub_truck.glb',
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
		...     modelFile       = 'veroviz/models/ub_truck.glb', 
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
	[valFlag, errorMsg, warningMsg] = valAddStaticAssignment(initAssignments, odID, objectID, modelFile, modelScale, modelMinPxSize, loc, startTimeSec, endTimeSec, ganttColor)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	# if the user provided an initAssignments dataframe, add the new points after it
	if (type(initAssignments) is pd.core.frame.DataFrame):
		# Increase odID as necessary:
		if (len(initAssignments) > 0):
			odID = max(max(initAssignments['odID'])+1, odID)
		
	assignments = privAddStaticAssignment(
		initAssignments = initAssignments, 
		odID            = odID, 
		objectID        = objectID, 
		modelFile       = modelFile, 
		modelScale      = modelScale, 
		modelMinPxSize  = modelMinPxSize, 
		loc             = loc, 
		startTimeSec    = startTimeSec, 
		endTimeSec      = endTimeSec, 
		ganttColor      = ganttColor, 
		popupText       = popupText)

	return assignments
	
def createAssignmentsFromArcs2D(initAssignments=None, arcs=None, serviceTimeSec=0.0, modelFile=None, modelScale=config['VRV_DEFAULT_CESIUMMODELSCALE'], modelMinPxSize=config['VRV_DEFAULT_CESIUMMODELMINPXSIZE'], startTimeSec=0.0, expDurationArgs=None, routeType='euclidean2D', speedMPS=None, leafletColor=None, leafletWeight=None, leafletStyle=None, leafletOpacity=None, leafletCurveType=None, leafletCurvature=None, useArrows=True, cesiumColor=None, cesiumWeight=None, cesiumStyle=None, cesiumOpacity=None, ganttColor=config['VRV_DEFAULT_GANTTCOLOR'], ganttColorService=config['VRV_DEFAULT_GANTTCOLORSERVICE'], popupText=None, dataProvider=None, dataProviderArgs=None):
	"""
	This function generates an "assignments" dataframe containing all of the "shapepoints" between successive arcs, including timestamps indicating the departure and arrival times for each shapepoint. Shapepoints are pairs of GPS coordinates that are connected by straight lines.  For a particular origin and destination, numerous individual shapepoints can be combined to define a travel route along a road network.  

	Note
	----
	This function is for vehicles traveling on a ground plane (2-dimensional).  For vehicles requiring an altitude component (e.g., drones), a 3D version of this function is provided by `createAssignmentsFromArcs3D()`.  This function creates an assignments dataframe from an arcs dataframe.  Similar functions are available to create an assignments dataframe from a sequence of nodes (`createShapepointsFromNodeSeq2D()`) or from a sequence of locations (`createShapepointsFromLocSeq2D()`).

	Parameters
	----------
	initAssignments: :ref:`Assignments` dataframe, Optional, default as None
		If provided, the function will append rows to this dataframe.
	arcs: :ref:`Arcs`, Required
		A :ref:`Arcs` dataframe, from which the assignments dataframe will be generated.
	serviceTimeSec: float, Optional, default as 0.0
		Specifies a duration, in seconds, that the vehicle will be stationary at each destination location in the arcs dataframe.
	modelFile: string, Optional, default as None
		The relative path and filename of the 3D model associated with the object described in the arcs dataframe.  The 3D model, typically in the format of `.gltf` or `.glb`, will be visualized in Cesium.  The path should be relative to the directory where Cesium is installed (i.e., the `modelFile` should exist within the Cesium root directory).	
	modelScale: int, Optional, default as 100
		The scale of the 3D model (specified by the `modelFile` argument) when displayed in Cesium, such that 100 represents 100%.
	modelMinPxSize: int, Optional, default as 75
		The minimum pixel size of the 3D model (specified by the `modelFile` argument) when displayed in Cesium.  When zooming out, the model will not be smaller than this size; zooming in can result in a larger model. 					
	startTimeSec: float, Optional, default as 0.0 
		The time, in seconds, at which the vehicle may leave the starting location.
	expDurationArgs: dictionary, Optional, default as None
		Sometimes there are inconsistencies between the travel times specified in the turn-by-turn navigation (i.e., shapepoints) and the travel matrices (i.e., from the getTimeDist functions).  The `expDurationArgs` field may take two different values.
		First, if `expDurationArgs` is `None` (default), the travel times will be based solely on the turn-by-turn times.  Second, if `expDurationArgs` is a dictionary with a key of `'getTravelTimes'` and a corresponding value of `True`, then this function will call the `getTimeDist2D()` function for each origin/destination pair (i.e., for each row of the arcs dataframe).  In this case, all shapepoint travel times will be adjusted/redistributed to match the resulting values.
	routeType: string, Optional, default as 'euclidean2D'
		This describes a characteristic of the travel mode.  Possible values are: 'euclidean2D', 'manhattan', 'fastest', 'shortest', 'pedestrian', 'cycling', and 'truck'.  The 'euclidean2D' and 'manhattan' options are calculated directly from GPS coordinates, without a road network.  Neither of these two options require a data provider.  However, the other options rely on road network information and require a data provider.  Furthermore, some of those other options are not supported by all data providers.  See :ref:`Data Providers` for details.
	speedMPS: float, Conditional, default as None
		Speed of the vehicle, in units of meters per second. For route types that are not road-network based (i.e., 'euclidean2D' and 'manhattan'), this field is required to calculate travel times. Otherwise, if a route type already incorporates travel speeds from road network data, (i.e., 'fastest', 'shortest', and 'pedestrain'), this input argument may be ignored.  If provided, `speedMPS` will override travel speed data used by the route type option.
	leafletColor: string, Optional, default as None
		Overrides the `leafletColor` column of the input :ref:`Arcs` dataframe.  If provided, all arcs will be displayed with this color.  See :ref:`Leaflet Style` for a list of available colors.
	leafletWeight: int, Optional, default as None
		Overrides the `leafletWeight` column of the input :ref:`Arcs` dataframe.  If provided, all arcs will be displayed with this line thickness (in pixels).  
	leafletStyle: string, Optional, default as None
		Overrides the `leafletStyle` column of the input :ref:`Arcs` dataframe. If provided, all arcs will be displayed with this type.  Valid options are 'solid', 'dotted', or 'dashed'.  See :ref:`Leaflet Style` for more information.
	leafletOpacity: float in [0, 1], Optional, default as None
		Overrides the `leafletOpacity` column of the input :ref:`Arcs` dataframe.  If provided, each arc will be displayed with this opacity.  Valid values are in the range from 0 (invisible) to 1 (no transparency).
	leafletCurveType: string, Optional, default as None
		Overrides the `leafletCurveType` column of the input :ref:`Arcs` dataframe, if provided. The type of curve to be shown on leaflet map for :ref:Arc dataframes (curves will not be applied to :ref:Assignments dataframes). The options are 'Bezier', 'greatcircle', and 'straight'. If Bezier is provided, the leafletCurvature is also required. If greatcircle is provided, the arc follow the curvature of the Earth.
	leafletCurvature: float in (-90, 90), Conditional, default as None
		Overrides the `leafletCurvature` column of the input :ref:`Arcs` dataframe, if provided.  If leafletCurveType is 'Bezier', then leafletCurvature is required; otherwise this argument will not be used. The curvature specifies the angle between a straight line connecting the two nodes and the curved arc emanating from those two nodes. Therefore, this value should be in the open interval (-90, 90), although values in the (-45, 45) range tend to work best.
	useArrows: boolean, Optional, default as None
		Overrides the `useArrows` column of the input :ref:`Arcs` dataframe. Indicates whether arrows should be shown on the route when displayed in Leaflet.
	cesiumColor: string, Optional, default as None
		Overrides the `cesiumColor` column of the input :ref:`Arcs` dataframe.  This will define the color of all arcs displayed in Cesium.  See :ref:`Cesium Style` for the collection of available colors.
	cesiumWeight: int, Optional, default as None
		Overrides the `cesiumWeight` column of the input :ref:`Arcs` dataframe. This will define the weight (in pixels) of all arcs displayed in Cesium. See :ref:`Cesium Style` for more information. 
	cesiumStyle: string, Optional, default as None
		Overrides the `cesiumStyle` column of the input :ref:`Arcs` dataframe. This will define the style of all arcs displayed in Cesium. See :ref:`Cesium Style` for available options.
	cesiumOpacity: float in [0, 1], Optional, default as None
		Overrides the `cesiumOpacity` column of the input :ref:`Arcs` dataframe.  This will define the opacity of all arcs displayed in Cesium.  See :ref:`Cesium Style` for more information.	
	ganttColor: string, Optional, default as "darkgray"
		The color of the route elements when displayed in a Gantt chart. 
	ganttColorService: string, Optional, default as "lightgray"
		The color of displayed in a Gantt chart for service activities.
	popupText: string, Optional, default as None
		Text (or HTML) that will be displayed when a user clicks on the arc in either Leaflet or Cesium. 		
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for obtaining the shapepoints. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.

	Return
	------
	:ref:`Assignments` dataframe
		An :ref:`Assignments` dataframe containing an ordered sequence of paired GPS coordinates describing the collection of straight-line segments required to travel through all arcs in the provided :ref:`Arcs` dataframe.

	Examples
	--------
	Import veroviz and check if it's the latest version:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Generate arcs from a given ordered list of coordinates:
		>>> arcs = vrv.createArcsFromLocSeq(
		...     locSeq=[[42.3538, -78.4253, 30], 
		...             [42.3465, -78.4234, 30], 
		...             [42.3343, -78.4146, 40]])
		>>> arcs

	Display the arcs on a Leaflet map:
		>>> vrv.createLeaflet(arcs=arcs)
		
	The following examples assume the use of ORS as the data provider. If you have saved your API key as an environment variable, you may use `os.environ` to access it:
		>>> import os
		>>> ORS_API_KEY = os.environ['ORSKEY']
		>>> # Otherwise, you may specify your key here:
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'
	
	Generate an assignments dataframe from the arcs dataframe:	
		>>> myAssignments = vrv.createAssignmentsFromArcs2D(
		...      arcs             = arcs, 
		...     modelFile        = 'veroviz/models/car_blue.gltf', 
		...     routeType        = 'fastest', 
		...     dataProvider     = 'ors-online',
		...     dataProviderArgs = {'APIkey': ORS_API_KEY},
		...     leafletColor     = 'blue')
		>>> myAssignments    

	Display the assignments on a map:	
		>>> vrv.createLeaflet(arcs=myAssignments)	
	"""
	
	# validatation
	[valFlag, errorMsg, warningMsg] = valCreateAssignmentsFromArcs2D(initAssignments, arcs, serviceTimeSec, modelScale, modelMinPxSize, expDurationArgs, modelFile, startTimeSec, routeType, speedMPS, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor, ganttColorService, dataProvider, dataProviderArgs)
	
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
		
	# Initialize an assignments dataframe:
	assignmentsDF = None

	# if the user provided an initAssignments dataframe, add the new points after it
	if (type(initAssignments) is pd.core.frame.DataFrame):
		if (len(initAssignments) > 0):
			assignmentsDF = pd.DataFrame(initAssignments.copy(), columns = privInitDataframe('assignments').columns)

	startTime = startTimeSec

	for i in arcs.index:		
		startLoc = [arcs['startLat'].at[i], arcs['startLon'].at[i]]
		endLoc   = [arcs['endLat'].at[i], arcs['endLon'].at[i]]

		if (expDurationArgs == None):
			expDurationSec = None
		elif ('getTravelTimes' in expDurationArgs):
			if (expDurationArgs['getTravelTimes']):
				# Call the data provider to get travel time
				[dicTime, dicDist] = getTimeDistFromLocs2D(fromLocs=[startLoc], fromRows=[0], toLocs=[endLoc], toCols=[0], outputDistUnits='meters', outputTimeUnits='seconds', routeType=routeType, speedMPS=speedMPS, dataProvider=dataProvider, dataProviderArgs=dataProviderArgs)

				[expDurationSec, distMeters] = [dicTime[0, 0], dicDist[0, 0]]

		odID     = arcs['odID'].at[i]
		objectID = arcs['objectID'].at[i]

		leafletColor = leafletColor if (leafletColor is not None) else arcs['leafletColor'].at[i]		 
		leafletWeight = leafletWeight if (leafletWeight is not None) else arcs['leafletWeight'].at[i]				
		leafletStyle = leafletStyle if (leafletStyle is not None) else arcs['leafletStyle'].at[i]
		leafletOpacity = leafletOpacity if (leafletOpacity is not None) else arcs['leafletOpacity'].at[i]
		leafletCurveType = leafletCurveType if (leafletCurveType is not None) else arcs['leafletCurveType'].at[i]
		leafletCurvature = leafletCurvature if (leafletCurvature is not None) else arcs['leafletCurvature'].at[i]
		useArrows = useArrows if (useArrows is not None) else arcs['useArrows'].at[i]
		cesiumColor = cesiumColor if (cesiumColor is not None) else arcs['cesiumColor'].at[i]
		cesiumWeight = cesiumWeight if (cesiumWeight is not None) else arcs['cesiumWeight'].at[i]
		cesiumStyle = cesiumStyle if (cesiumStyle is not None) else arcs['cesiumStyle'].at[i]
		cesiumOpacity = cesiumOpacity if (cesiumOpacity is not None) else arcs['cesiumOpacity'].at[i]
		
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
			leafletCurveType=leafletCurveType, 
			leafletCurvature=leafletCurvature, 
			useArrows=useArrows, 
			modelScale=modelScale, 
			modelMinPxSize=modelMinPxSize, 
			cesiumColor=stripCesiumColor(cesiumColor), 
			cesiumWeight=cesiumWeight, 
			cesiumStyle=cesiumStyle, 
			cesiumOpacity=cesiumOpacity,
			ganttColor=ganttColor,
			popupText=popupText,
			dataProvider=dataProvider, 
			dataProviderArgs=dataProviderArgs)

		# Update the assignments dataframe:
		if (assignmentsDF is not None):
			assignmentsDF = pd.concat([assignmentsDF, tmpShapepoints], ignore_index=True, sort=False)
		else:
			assignmentsDF = pd.DataFrame(tmpShapepoints, columns = privInitDataframe('assignments').columns)

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
				endTimeSec      = startTime + serviceTimeSec,
				ganttColor      = ganttColorService, 
				popupText       = popupText)

			odID += 1

			# Update the time again
			startTime = startTime + serviceTimeSec

    			
	return assignmentsDF

def createAssignmentsFromNodeSeq2D(initAssignments=None, nodeSeq=None, nodes=None, serviceTimeSec=0.0, odID=1, objectID=None, modelFile=None, modelScale=config['VRV_DEFAULT_CESIUMMODELSCALE'], modelMinPxSize=config['VRV_DEFAULT_CESIUMMODELMINPXSIZE'], startTimeSec=0.0, expDurationArgs=None, routeType='euclidean2D', speedMPS=None,   leafletColor=config['VRV_DEFAULT_LEAFLETARCCOLOR'], leafletWeight=config['VRV_DEFAULT_LEAFLETARCWEIGHT'], leafletStyle=config['VRV_DEFAULT_LEAFLETARCSTYLE'], leafletOpacity=config['VRV_DEFAULT_LEAFLETARCOPACITY'], leafletCurveType=config['VRV_DEFAULT_ARCCURVETYPE'], leafletCurvature=config['VRV_DEFAULT_ARCCURVATURE'], useArrows=True, cesiumColor=config['VRV_DEFAULT_CESIUMPATHCOLOR'], cesiumWeight=config['VRV_DEFAULT_CESIUMPATHWEIGHT'], cesiumStyle=config['VRV_DEFAULT_CESIUMPATHSTYLE'], cesiumOpacity=config['VRV_DEFAULT_CESIUMPATHOPACITY'], ganttColor=config['VRV_DEFAULT_GANTTCOLOR'], ganttColorService=config['VRV_DEFAULT_GANTTCOLORSERVICE'], popupText=None, dataProvider=None, dataProviderArgs=None):
	"""
	This function generates an "assignments" dataframe containing all of the "shapepoints" between successive node locations, including timestamps indicating the departure and arrival times for each shapepoint. Shapepoints are pairs of GPS coordinates that are connected by straight lines.  For a particular origin and destination, numerous individual shapepoints can be combined to define a travel route along a road network.  

	Note
	----
	This function is for vehicles traveling on a ground plane (2-dimensional).  For vehicles requiring an altitude component (e.g., drones), a 3D version of this function is provided by `createAssignmentsFromNodeSeq3D()`.
	This function creates an assignments dataframe from a sequence of nodes.  Similar functions are available to create an assignments dataframe from an arcs dataframe (`createShapepointsFromArcs2D()`) or from a sequence of locations (`createShapepointsFromLocSeq2D()`).
	
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
	leafletCurveType: string, Optional, default as 'straight'
		The type of curve to be shown on leaflet map for :ref:Arc dataframes (curves will not be applied to :ref:Assignments dataframes). The options are 'Bezier', 'greatcircle', and 'straight'. If Bezier is provided, the leafletCurvature is also required. If greatcircle is provided, the arc follow the curvature of the Earth.
	leafletCurvature: float in (-90, 90), Conditional, default as 45
		If leafletCurveType is 'Bezier', then leafletCurvature is required; otherwise this argument will not be used. The curvature specifies the angle between a straight line connecting the two nodes and the curved arc emanating from those two nodes. Therefore, this value should be in the open interval (-90, 90), although values in the (-45, 45) range tend to work best.
	useArrows: bool, Optional, default as True
		Indicates whether arrows should be shown on the route when displayed in Leaflet.
	modelScale: int, Optional, default as 100
		The scale of the 3D model (specified by the `modelFile` argument) when displayed in Cesium, such that 100 represents 100%.
	modelMinPxSize: int, Optional, default as 75
		The minimum pixel size of the 3D model (specified by the `modelFile` argument) when displayed in Cesium.  When zooming out, the model will not be smaller than this size; zooming in can result in a larger model. 
	cesiumColor: string, Optional, default as "orange"
		The color of the route when displayed in Cesium.  See :ref:`Cesium Style` for a list of available colors.
	cesiumWeight: int, Optional, default as 3
		The pixel width of the route when displayed in Cesium. 
	cesiumStyle: string, Optional, default as 'solid'
		The line style of the route when displayed in Cesium.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Cesium Style` for more information.
	cesiumOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the route when displayed in Cesium. Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	ganttColor: string, Optional, default as "darkgray"
		The color of the route elements when displayed in a Gantt chart. 
	ganttColorService: string, Optional, default as "lightgray"
		The color of displayed in a Gantt chart for service activities.
	popupText: string, Optional, default as None
		Text (or HTML) that will be displayed when a user clicks on the arc in either Leaflet or Cesium.		
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
			
	Example 3 - The vehicle will first wait at the starting location (node 1) for 65 seconds.  It will then visit nodes 3 and 2 before returning to node 1.  At each of those nodes, the vehicle will remain stationary for a 20-second service time.  The travel time between each pair of nodes will be determined by the times in the `timeSec` matrix.
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
		...     cesiumColor      = 'blue', 
		...     cesiumWeight     = 3, 
		...     cesiumStyle      = 'solid', 
		...     cesiumOpacity    = 0.8, 
		...     dataProvider     = 'ORS-online',
		...     dataProviderArgs = {'APIkey' : ORS_API_KEY})
		>>> newAssignmentsDF

	View the assignments in Leaflet:  
		>>> vrv.createLeaflet(arcs=newAssignmentsDF, nodes=exampleNodes)
	
	View the assignments in Cesium:
		>>> vrv.createCesium(
		...     assignments = newAssignmentsDF, 
		...     nodes       = exampleNodes, 
		...     startTime   = '08:00:00', 
		...     cesiumDir   = os.environ['CESIUMDIR'],
		...     problemDir  = 'createAssignments_example')
	"""	
	
	# validatation
	[valFlag, errorMsg, warningMsg] = valCreateAssignmentsFromNodeSeq2D(initAssignments, nodeSeq, nodes, serviceTimeSec, modelScale, modelMinPxSize, expDurationArgs, odID, objectID, modelFile, startTimeSec, routeType, speedMPS, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor, ganttColorService, dataProvider, dataProviderArgs)
	
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
		
	# Initialize an assignments dataframe:
	assignmentsDF = None

	# if the user provided an initAssignments dataframe, add the new points after it
	if (type(initAssignments) is pd.core.frame.DataFrame):
		if (len(initAssignments) > 0):
			assignmentsDF = pd.DataFrame(initAssignments.copy(), columns = privInitDataframe('assignments').columns)

			# Increase odID as necessary:
			odID = max(max(assignmentsDF['odID'])+1, odID)

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
			leafletCurveType=leafletCurveType, 
			leafletCurvature=leafletCurvature, 
			useArrows=useArrows, 
			modelScale=modelScale, 
			modelMinPxSize=modelMinPxSize, 
			cesiumColor=stripCesiumColor(cesiumColor), 
			cesiumWeight=cesiumWeight, 
			cesiumStyle=cesiumStyle, 
			cesiumOpacity=cesiumOpacity,
			ganttColor=ganttColor, 
			popupText=popupText,
			dataProvider=dataProvider, 
			dataProviderArgs=dataProviderArgs)

		# Update the assignments dataframe:
		if (assignmentsDF is not None):
			assignmentsDF = pd.concat([assignmentsDF, tmpShapepoints], ignore_index=True, sort=False)
		else:
			assignmentsDF = pd.DataFrame(tmpShapepoints, columns = privInitDataframe('assignments').columns)
			
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
				endTimeSec      = startTime + serviceTimeSec,
				ganttColor      = ganttColorService,
				popupText       = popupText)

			odID += 1

			# Update the time again
			startTime = startTime + serviceTimeSec

    			
	return assignmentsDF		
	
	

def createAssignmentsFromLocSeq2D(initAssignments=None, locSeq=None, serviceTimeSec=0.0, odID=1, objectID=None, modelFile=None, modelScale=config['VRV_DEFAULT_CESIUMMODELSCALE'], modelMinPxSize=config['VRV_DEFAULT_CESIUMMODELMINPXSIZE'], startTimeSec=0.0, expDurationArgs=None, routeType='euclidean2D', speedMPS=None, leafletColor=config['VRV_DEFAULT_LEAFLETARCCOLOR'], leafletWeight=config['VRV_DEFAULT_LEAFLETARCWEIGHT'], leafletStyle=config['VRV_DEFAULT_LEAFLETARCSTYLE'], leafletOpacity=config['VRV_DEFAULT_LEAFLETARCOPACITY'], leafletCurveType=config['VRV_DEFAULT_ARCCURVETYPE'], leafletCurvature=config['VRV_DEFAULT_ARCCURVATURE'], useArrows=True, cesiumColor=config['VRV_DEFAULT_CESIUMPATHCOLOR'], cesiumWeight=config['VRV_DEFAULT_CESIUMPATHWEIGHT'], cesiumStyle=config['VRV_DEFAULT_CESIUMPATHSTYLE'], cesiumOpacity=config['VRV_DEFAULT_CESIUMPATHOPACITY'], ganttColor=config['VRV_DEFAULT_GANTTCOLOR'], ganttColorService=config['VRV_DEFAULT_GANTTCOLORSERVICE'], popupText=None, dataProvider=None, dataProviderArgs=None):
	"""
	This function generates an "assignments" dataframe containing all of the "shapepoints" between successive locations, including timestamps indicating the departure and arrival times for each shapepoint. Shapepoints are pairs of GPS coordinates that are connected by straight lines.  For a particular origin and destination, numerous individual shapepoints can be combined to define a travel route along a road network.  

	Note
	----
	This function is for vehicles traveling on a ground plane (2-dimensional).  For vehicles requiring an altitude component (e.g., drones), a 3D version of this function is provided by `createAssignmentsFromLocSeq3D()`.
	This function creates an assignments dataframe from a sequence of [lat, lon] locations.  Similar functions are available to create an assignments dataframe from an arcs dataframe (`createShapepointsFromArcs2D()`) or from a sequence of nodes (`createShapepointsFromNodeSeq2D()`).
	
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
	leafletCurveType: string, Optional, default as 'straight'
		The type of curve to be shown on leaflet map for :ref:Arc dataframes (curves will not be applied to :ref:Assignments dataframes). The options are 'Bezier', 'greatcircle', and 'straight'. If Bezier is provided, the leafletCurvature is also required. If greatcircle is provided, the arc follow the curvature of the Earth.
	leafletCurvature: float in (-90, 90), Conditional, default as 45
		If leafletCurveType is 'Bezier', then leafletCurvature is required; otherwise this argument will not be used. The curvature specifies the angle between a straight line connecting the two nodes and the curved arc emanating from those two nodes. Therefore, this value should be in the open interval (-90, 90), although values in the (-45, 45) range tend to work best.
	useArrows: bool, Optional, default as True
		Indicates whether arrows should be shown on the route when displayed in Leaflet.
	modelScale: int, Optional, default as 100
		The scale of the 3D model (specified by the `modelFile` argument) when displayed in Cesium, such that 100 represents 100%.
	modelMinPxSize: int, Optional, default as 75
		The minimum pixel size of the 3D model (specified by the `modelFile` argument) when displayed in Cesium.  When zooming out, the model will not be smaller than this size; zooming in can result in a larger model. 
	cesiumColor: string, Optional, default as "orange"
		The color of the route when displayed in Cesium.  See :ref:`Cesium Style` for a list of available colors.
	cesiumWeight: int, Optional, default as 3
		The pixel width of the route when displayed in Cesium. 
	cesiumStyle: string, Optional, default as 'solid'
		The line style of the route when displayed in Cesium.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Cesium Style` for more information.
	cesiumOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the route when displayed in Cesium. Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	ganttColor: string, Optional, default as "darkgray"
		The color of the route elements when displayed in a Gantt chart. 
	ganttColorService: string, Optional, default as "lightgray"
		The color of displayed in a Gantt chart for service activities.
	popupText: string, Optional, default as None
		Text (or HTML) that will be displayed when a user clicks on the arc in either Leaflet or Cesium.		
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
		...     initAssignments   = assignmentsDF, 
		...     locSeq            = locs, 
		...     serviceTimeSec    = 20.0, 
		...     odID              = 1, 
		...     objectID          = 'Blue Car', 
		...     modelFile         = 'veroviz/models/car_blue.gltf', 
		...     modelScale        = 100,
		...     modelMinPxSize    = 75,
		...     startTimeSec      = 65.0, 
		...     expDurationArgs   = {'getTravelTimes': True}, 
		...     routeType         = 'fastest',
		...     speedMPS          = None,   
		...     leafletColor      = 'blue', 
		...     leafletWeight     = 3, 
		...     leafletStyle      = 'dashed', 
		...     leafletOpacity    = 0.8, 
		...     leafletCurveType  = 'straight',
		...     leafletCurvature  = None,
		...     useArrows         = True, 
		...     cesiumColor       = 'blue',
		...     ganttColorService = 'green',
		...     cesiumWeight      = 3, 
		...     cesiumStyle       = 'solid', 
		...     cesiumOpacity     = 0.8, 
		...     ganttColor        = 'blue',
		...     popupText         = 'Blue Car Route',
		...     dataProvider      = 'ORS-online',
		...     dataProviderArgs  = {'APIkey' : ORS_API_KEY})
		>>> newAssignmentsDF			

	Generate a :ref:`Nodes` dataframe from our first three locations (the fourth location is a duplicate of the first).  See :meth:`~veroviz.generateNodes.generateNodes` for other methods to generate "nodes" dataframes.
	    >>> exampleNodes = vrv.createNodesFromLocs(locs=locs[0:3])

	View the assignments in Leaflet:  
		>>> vrv.createLeaflet(arcs=newAssignmentsDF, nodes=exampleNodes)
	
	View the assignments in Cesium:
		>>> vrv.createCesium(
		...     assignments = newAssignmentsDF, 
		...     nodes       = exampleNodes, 
		...     startTime   = '08:00:00', 
		...     cesiumDir   = os.environ['CESIUMDIR'],
		...     problemDir  = 'createAssignments_example')
	"""	
	
	# validatation
	[valFlag, errorMsg, warningMsg] = valCreateAssignmentsFromLocSeq2D(initAssignments, locSeq, serviceTimeSec, modelScale, modelMinPxSize, expDurationArgs, odID, objectID, modelFile, startTimeSec, routeType, speedMPS, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor, ganttColorService, dataProvider, dataProviderArgs)
	
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
		
	assignmentsDF = None	
	# If the user provided an initAssignments dataframe, add the new points after it
	if (type(initAssignments) is pd.core.frame.DataFrame):
		if (len(initAssignments) > 0):
			assignmentsDF = pd.DataFrame(initAssignments.copy(), columns = privInitDataframe('assignments').columns)

			# Increase odID as necessary:
			odID = max(max(assignmentsDF['odID'])+1, odID)

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
			leafletCurveType=leafletCurveType, 
			leafletCurvature=leafletCurvature, 
			useArrows=useArrows, 
			modelScale=modelScale, 
			modelMinPxSize=modelMinPxSize, 
			cesiumColor=stripCesiumColor(cesiumColor), 
			cesiumWeight=cesiumWeight, 
			cesiumStyle=cesiumStyle, 
			cesiumOpacity=cesiumOpacity,
			ganttColor=ganttColor, 
			popupText=popupText,
			dataProvider=dataProvider, 
			dataProviderArgs=dataProviderArgs)


		# Update the assignments dataframe:
		if (assignmentsDF is not None):
			assignmentsDF = pd.concat([assignmentsDF, tmpShapepoints], ignore_index=True, sort=False)
		else:
			assignmentsDF = pd.DataFrame(tmpShapepoints, columns = privInitDataframe('assignments').columns)
			
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
				endTimeSec      = startTime + serviceTimeSec,
				ganttColor      = ganttColorService,
				popupText       = popupText)

			odID += 1

			# Update the time again
			startTime = startTime + serviceTimeSec

    			
	return assignmentsDF		
