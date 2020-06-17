from veroviz._common import *
from veroviz._validation import valGetShapepoints2D

from veroviz._getShapepoints import privGetShapepoints2D

def getShapepoints2D(odID=1, objectID=None, modelFile=None, startLoc=None, endLoc=None, startTimeSec=0.0, expDurationSec=None, 
	routeType='euclidean2D', speedMPS=None,   
	leafletColor=config['VRV_DEFAULT_LEAFLETARCCOLOR'], leafletWeight=config['VRV_DEFAULT_LEAFLETARCWEIGHT'], leafletStyle=config['VRV_DEFAULT_LEAFLETARCSTYLE'], leafletOpacity=config['VRV_DEFAULT_LEAFLETARCOPACITY'], leafletCurveType=config['VRV_DEFAULT_ARCCURVETYPE'], leafletCurvature=config['VRV_DEFAULT_ARCCURVATURE'], useArrows=True, modelScale=config['VRV_DEFAULT_CESIUMMODELSCALE'], modelMinPxSize=config['VRV_DEFAULT_CESIUMMODELMINPXSIZE'], cesiumColor=config['VRV_DEFAULT_CESIUMPATHCOLOR'], cesiumWeight=config['VRV_DEFAULT_CESIUMPATHWEIGHT'], cesiumStyle=config['VRV_DEFAULT_CESIUMPATHSTYLE'], cesiumOpacity=config['VRV_DEFAULT_CESIUMPATHOPACITY'], ganttColor=config['VRV_DEFAULT_GANTTCOLOR'], popupText=None, dataProvider=None, dataProviderArgs=None):

	"""
	This function generates all of the "shapepoints" between two given GPS coordinates, including timestamps indicating the departure and arrival times for each shapepoint. Shapepoints are pairs of GPS coordinates that are connected by  straight lines.  For a given origin and destination, numerous individual shapepoints can be combined to define a travel route along a road network.   

	Note
	----
	This function is for vehicles traveling on a ground plane (2-dimensional).  For vehicles requiring an altitude component (e.g., drones), a 3D version of this function is provided by `getShapepoints3D()`.
	
	Parameters
	----------
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
	
	Example 1 - A minimal example, using the fastest car route.  The ORS-online data provider requires an API key.
		>>> shapepoints2D = vrv.getShapepoints2D(
		...     odID=1,
		...     startLoc=[42.80, -78.80],
		...     endLoc=[42.90, -78.80],
		...     routeType='fastest',
		...     dataProvider='ORS-online',
		...     dataProviderArgs = {'APIkey': 'YOUR_ORSKEY'})

	View the route in Leaflet.  The green marker is the start, the red marker is the end:
		>>> myMap = vrv.createLeaflet(arcs=shapepoints2D)
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=[42.80, -78.80], fillColor='green')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=[42.90, -78.80], fillColor='red')
		>>> myMap
	    
	Example 2 - Shapepoints with Euclidean travel can also be generated:
		>>> shapepoints2D = vrv.getShapepoints2D(
		...     odID             = 1,
		...     startLoc         = [42.80, -78.80],
		...     endLoc           = [42.90, -78.80],
		...     routeType        = 'euclidean2D',
		...     speedMPS         = vrv.convertSpeed(55, 'mi', 'hr', 'm', 's'),
		...     dataProvider     = None,
		...     dataProviderArgs = None)
		>>> shapepoints2D
	    
	View the route in Leaflet.  The green marker is the start, the red marker is the end:
		>>> myMap = vrv.createLeaflet(arcs=shapepoints2D)
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=[42.80, -78.80], fillColor='green')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=[42.90, -78.80], fillColor='red')
		>>> myMap

	Example 3 - Generate an Assignments dataframe that starts from 520 seconds and assumes the vehicle is driving at a constant constant speed of 16 m/s (or 35.8 mph).  The OSRM-online data provider does not require an API key.
	    >>> shapepoints2D = vrv.getShapepoints2D(
	    ...     odID         = 1, 
	    ...     startLoc     = [42.80, -78.80], 
	    ...     endLoc       = [42.90, -78.80], 
	    ...     startTimeSec = 520,
	    ...     routeType    = 'fastest',
	    ...     dataProvider = 'OSRM-online',
	    ...     speedMPS     = 16)

	View the route in Leaflet.  The green marker is the start, the red marker is the end:
		>>> myMap = vrv.createLeaflet(arcs=shapepoints2D)
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=[42.80, -78.80], fillColor='green')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=[42.90, -78.80], fillColor='red')
		>>> myMap

	Example 4 - The `expDurationSec` argument ensures that the vehicle reaches the ending location at time `startTimeSec + expDurationSec`. This is useful when you are using data from different sources (e.g., time matrix data from pgRouting and shapepoints created by ORS) and you want to maintain consistency in timing. If `expDurationSec` and `speedMPS` are both provided, `expDurationSec` will override the `speedMPS`.
	    >>> [travelTimeSec, travelDistMeters]  = vrv.getTimeDistScalar2D(
	    ...     startLoc         = [42.80, -78.80],
	    ...     endLoc           = [42.90, -78.80],
	    ...     outputDistUnits  = 'meters',
	    ...     outputTimeUnits  = 'seconds',
	    ...     routeType        = 'fastest',
	    ...     dataProvider     = 'ORS-online',
	    ...     dataProviderArgs = {'APIkey' : ORS_API_KEY})
	    >>> shapepoints2D = vrv.getShapepoints2D(
	    ...     odID             = 1, 
	    ...     startLoc         = [42.80, -78.80], 
	    ...     endLoc           = [42.90, -78.80], 
	    ...     startTimeSec     = 520,
	    ...     routeType        = 'fastest',
	    ...     dataProvider     = 'ORS-online',
	    ...     dataProviderArgs = {'APIkey' : ORS_API_KEY},
	    ...     expDurationSec   = travelTimeSec)
	    >>> shapepoints2D

	Example 5 - Note that `getShapepoints2D()` sometimes displays messages like "The origin/destination point is XXX meters away from the road".  This occurs if the start and/or end location provided is too far away from the nearest road.  VeRoViz does not attempt to find a path from an arbitrary location to the nearest road.  To avoid these warnings, one option is to snap the start/end locations to the road network before attempting to get the shapepoints.  In this case, it is highly recommended to use the same data provider for both the snapping and shapepoint activities.
	    >>> startLoc = vrv.getSnapLoc(loc              = [42.80, -78.80], 
	    ...                           dataProvider     = 'ORS-online',
	    ...                           dataProviderArgs = {'APIkey': ORS_API_KEY})
	    >>> endLoc   = vrv.getSnapLoc(loc              = [42.90, -78.80], 
	    ...                           dataProvider     = 'ORS-online',
	    ...                           dataProviderArgs = {'APIkey': ORS_API_KEY})
	    >>> shapepoints2D = vrv.getShapepoints2D(
	    ...          odID             = 1, 
	    ...          startLoc         = startLoc,
	    ...          endLoc           = endLoc,
	    ...          startTimeSec     = 520,
	    ...          routeType        = 'fastest',
	    ...          dataProvider     = 'ORS-online',
	    ...          dataProviderArgs = {'APIkey': ORS_API_KEY})
	    >>> shapepoints2D
	    
	View the route in Leaflet.  The green filled marker is the original start, the green outlined marker is the snapped start.  The red filled marker is the original end, the red outlined marker is the snapped end.
		>>> myMap = vrv.createLeaflet(arcs=shapepoints2D)
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=[42.80, -78.80], 
		...                              fillColor='green')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=[42.90, -78.80], 
		...                              fillColor='red')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=startLoc, 
		...                              fillColor=None, lineColor='green')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=endLoc, 
		...                              fillColor=None, lineColor='red')
		>>> myMap
		
	Example 6 - If you are constructing the Assignments dataframe for use with Cesium, then the `objectID` and `modelFile` arguments are required. If you are just using it to generate Leaflet maps, those arguments can be left as default (None).
		>>> shapepoints2D = vrv.getShapepoints2D(
		...     odID             = 1, 
		...     objectID         = 'Blue Car',
		...     modelFile        = '/veroviz/models/car_blue.gltf',
		...     startLoc         = vrv.getSnapLoc(
		...                          loc          = [42.80, -78.80], 
		...                          dataProvider = 'OSRM-online'),
		...     endLoc           = vrv.getSnapLoc(
		...                          loc          = [42.90, -78.80], 
		...                          dataProvider = 'OSRM-online'),
		...     startTimeSec     = 520,
		...     routeType        = 'shortest',
		...     dataProvider     = 'MapQuest',
		...     dataProviderArgs = {'APIkey': os.environ['MAPQUESTKEY']},
		...     expDurationSec   = 1500)
		>>> shapepoints2D
		
	Example 7 - This example includes all of the functional arguments:
		>>> start = [42.80, -78.80]
		>>> end   = [42.90, -78.80]
		>>> shapepoints2D = vrv.getShapepoints2D(
		...     odID             = 1, 
		...     objectID         = 'Blue Car', 
		...     modelFile        = 'veroviz/models/car_blue.gltf', 
		...     modelScale       = 100,
		...     modelMinPxSize   = 75,
		...     startLoc         = start, 
		...     endLoc           = end, 
		...     startTimeSec     = 30.0, 
		...     expDurationSec   = 90, 
		...     routeType        = 'shortest', 
		...     speedMPS         = 5.2, 
		...     leafletColor     = 'blue', 
		...     leafletWeight    = 3, 
		...     leafletStyle     = 'dashed', 
		...     leafletOpacity   = 0.8, 
		...     useArrows        = True, 
		...     cesiumColor      = 'blue', 
		...     cesiumWeight     = 3, 
		...     cesiumStyle      = 'solid', 
		...     cesiumOpacity    = 0.8, 
		...     ganttColor       = 'blue',
		...     popupText        = 'blue car route',
		...     dataProvider     = 'MapQuest',
		...     dataProviderArgs = {'APIkey': os.environ['MAPQUESTKEY']})
		>>> myMap = vrv.createLeaflet(arcs = shapepoints2D)
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=start, fillColor='green', lineColor='green')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=end, fillColor='red', lineColor='red')
		>>> myMap
		
	Generate a Cesium movie:	
		>>> vrv.createCesium(
		...     assignments = shapepoints2D, 
		...     cesiumDir   = os.environ['CESIUMDIR'],
		...     problemDir  = '/examples/shapepoints')
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valGetShapepoints2D(odID, objectID, modelFile, startLoc, endLoc, startTimeSec, expDurationSec, routeType, speedMPS, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	assignments = privGetShapepoints2D(odID=odID, objectID=objectID, modelFile=modelFile, startLoc=startLoc, endLoc=endLoc, startTimeSec=startTimeSec, expDurationSec=expDurationSec, routeType=routeType, speedMPS=speedMPS, leafletColor=leafletColor, leafletWeight=leafletWeight, leafletStyle=leafletStyle, leafletOpacity=leafletOpacity, leafletCurveType=leafletCurveType, leafletCurvature=leafletCurvature, useArrows=useArrows, modelScale=modelScale, modelMinPxSize=modelMinPxSize, cesiumColor=cesiumColor, cesiumWeight=cesiumWeight, cesiumStyle=cesiumStyle, cesiumOpacity=cesiumOpacity, ganttColor=ganttColor, popupText=popupText, dataProvider=dataProvider, dataProviderArgs=dataProviderArgs)
		
	return assignments
