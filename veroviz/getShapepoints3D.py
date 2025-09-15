from veroviz._common import *
from veroviz._validation import valGetShapepoints3D
from veroviz._getShapepoints import privGetShapepoints3D

def getShapepoints3D(odID=1, objectID=None, modelFile=None, startTimeSec=0.0, startLoc=None, endLoc=None, takeoffSpeedMPS=None, cruiseSpeedMPS=None, landSpeedMPS=None, cruiseAltMetersAGL=None, routeType='square', climbRateMPS=None, descentRateMPS=None, earliestLandTime=-1, loiterPosition='arrivalAtAlt', leafletColor=config['VRV_DEFAULT_LEAFLETARCCOLOR'], leafletWeight=config['VRV_DEFAULT_LEAFLETARCWEIGHT'], leafletStyle=config['VRV_DEFAULT_LEAFLETARCSTYLE'], leafletOpacity=config['VRV_DEFAULT_LEAFLETARCOPACITY'], leafletCurveType=config['VRV_DEFAULT_ARCCURVETYPE'], leafletCurvature=config['VRV_DEFAULT_ARCCURVATURE'],  useArrows=True, modelScale=config['VRV_DEFAULT_CESIUMMODELSCALE'], modelMinPxSize=config['VRV_DEFAULT_CESIUMMODELMINPXSIZE'], cesiumColor=config['VRV_DEFAULT_CESIUMPATHCOLOR'], cesiumWeight=config['VRV_DEFAULT_CESIUMPATHWEIGHT'], cesiumStyle=config['VRV_DEFAULT_CESIUMPATHSTYLE'], cesiumOpacity=config['VRV_DEFAULT_CESIUMPATHOPACITY'], ganttColor=config['VRV_DEFAULT_GANTTCOLOR'], ganttColorLoiter=config['VRV_DEFAULT_GANTTCOLORLOITER'], popupText=None):

	"""
	This function generates 3-dimensional "shapepoints" between two given GPS coordinates, including timestamps indicating the departure and arrival times for each shapepoint. Shapepoints are pairs of GPS coordinates (and altitudes) that are connected by  straight lines.  For a given origin and destination, numerous individual shapepoints can be combined to define movement in three dimensions.

	Note
	----
	This function is for vehicles whose travel path includes changes in altitude (e.g., drones).  For ground vehicles traveling on a ground plane, a 2-dimensional version of this function is provided by `getShapepoints2D()`.

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
	ganttColorLoiter: string, Optional, default as "lightgray"
		The color of displayed in a Gantt chart for loiter activities.
	popupText: string, Optional, default as None
		Text (or HTML) that will be displayed when a user clicks on the arc in either Leaflet or Cesium.

	Return
	-------
	:ref:`Assignments` dataframe
		An :ref:`Assignments` dataframe containing an ordered sequence of paired GPS coordinates and altitudes describing the collection of straight-line segments required to travel from a start location to an end location.

	Examples
	--------
	Import veroviz and check if a newer version exists:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Example 1 - Square profile (takeoff and land vertically, like a quadcopter).
		>>> shapepoints3D_1 = vrv.getShapepoints3D(
		...     odID               = 1,
		...     objectID           = 'square flight', 
		...     modelFile          = '/veroviz/models/drone.glb',
		...     startLoc           = [42.80, -78.80],
		...     endLoc             = [42.80, -78.77],
		...     cruiseAltMetersAGL = 220,
		...     takeoffSpeedMPS    = 15,
		...     cruiseSpeedMPS     = 20,
		...     landSpeedMPS       = 10,
		...     climbRateMPS       = None,
		...     descentRateMPS     = None,    
		...     routeType          = 'square',
		...     cesiumColor        = 'red')
		>>> shapepoints3D_1


	Example 2 - Straight profile (fly directly from start to end).
		>>> shapepoints3D_2 = vrv.getShapepoints3D(
		...     odID               = 2,
		...     objectID           = 'straight flight', 
		...     modelFile          = '/veroviz/models/drone.glb',
		...     startLoc           = [42.80, -78.80],
		...     endLoc             = [42.80, -78.77, 219],
		...     cruiseAltMetersAGL = None,
		...     takeoffSpeedMPS    = None, 
		...     cruiseSpeedMPS     = 20,
		...     landSpeedMPS       = None, 
		...     climbRateMPS       = None,
		...     descentRateMPS     = None,    
		...     routeType          = 'straight',
		...     cesiumColor        = 'green')
		>>> shapepoints3D_2


	Example 3 - Trapezoidal profiles (with different climb/descent rates).
		>>> shapepoints3D_3a = vrv.getShapepoints3D(
		...     odID               = 3,
		...     objectID           = 'trapezoid a', 
		...     modelFile          = '/veroviz/models/drone.glb',
		...     startLoc           = [42.80, -78.80],
		...     endLoc             = [42.80, -78.77],
		...     cruiseAltMetersAGL = 220,
		...     takeoffSpeedMPS    = 15,
		...     cruiseSpeedMPS     = 20,
		...     landSpeedMPS       = 10,
		...     climbRateMPS       = 10,
		...     descentRateMPS     = 5,    
		...     routeType          = 'trapezoidal',
		...     cesiumColor        = 'black')
		>>> shapepoints3D_3a

		>>> shapepoints3D_3b = vrv.getShapepoints3D(
		...     odID               = 4,
		...     objectID           = 'trapezoid b', 
		...     modelFile          = '/veroviz/models/drone.glb',
		...     startLoc           = [42.80, -78.80],
		...     endLoc             = [42.80, -78.77],
		...     cruiseAltMetersAGL = 220,
		...     takeoffSpeedMPS    = 15,
		...     cruiseSpeedMPS     = 20,
		...     landSpeedMPS       = 10,
		...     climbRateMPS       = 5,
		...     descentRateMPS     = 1,    
		...     routeType          = 'trapezoidal',
		...     cesiumColor        = 'black',
		...     cesiumStyle        = 'dashed')
		>>> shapepoints3D_3b


	Example 4 - Triangular profile
		>>> shapepoints3D_4 = vrv.getShapepoints3D(
		...     odID               = 5,
		...     objectID           = 'triangle', 
		...     modelFile          = '/veroviz/models/drone.glb',
		...     startLoc           = [42.80, -78.80],
		...     endLoc             = [42.80, -78.77],
		...     cruiseAltMetersAGL = 220,
		...     takeoffSpeedMPS    = None,
		...     cruiseSpeedMPS     = 20,
		...     landSpeedMPS       = None,
		...     climbRateMPS       = None,
		...     descentRateMPS     = None,    
		...     routeType          = 'triangular',
		...     cesiumColor        = 'lightpink')
		>>> shapepoints3D_4


	Example 5 - Compare the profiles from Examples 1-4.
		>>> # We'll need pandas to concatenate all of our dataframes.
		>>> import pandas as pd

		>>> # Initialize an empty "assignments" dataframe:
		>>> assignmentsDF = vrv.initDataframe('assignments')

		>>> # Initialize an "assignments" dataframe:
		>>> # The assignments dataframe will hold all shapepoints for all vehicles.
		>>> assignmentsDF = pd.DataFrame(shapepoints3D_1, columns = vrv.initDataframe('assignments').columns)
		
		>>> # Append to the assignments dataframe.
		>>> assignmentsDF = pd.concat([assignmentsDF, shapepoints3D_2], ignore_index=True, sort=False)
		>>> assignmentsDF = pd.concat([assignmentsDF, shapepoints3D_3a], ignore_index=True, sort=False)
		>>> assignmentsDF = pd.concat([assignmentsDF, shapepoints3D_3b], ignore_index=True, sort=False)
		>>> assignmentsDF = pd.concat([assignmentsDF, shapepoints3D_4], ignore_index=True, sort=False)
		>>> assignmentsDF

		>>> # Generate Cesium materials to view all flight profiles:
		>>> vrv.createCesium(
		...     assignments = assignmentsDF, 
		...     cesiumDir   = os.environ['CESIUMDIR'],
		...     problemDir  = '/examples/shapepoints3D')


	Example 6 - This example includes all of the functional arguments.
		>>> shapepoints3D = vrv.getShapepoints3D(
		...     odID               = 1,
		...     objectID           = 'drone', 
		...     modelFile          = '/veroviz/models/drone.glb', 
		...     startTimeSec       = 120.0, 
		...     startLoc           = [42.80, -78.90], 
		...     endLoc             = [42.85, -78.95], 
		...     takeoffSpeedMPS    = 25, 
		...     cruiseSpeedMPS     = 25, 
		...     landSpeedMPS       = 25, 
		...     cruiseAltMetersAGL = 120, 
		...     routeType          = 'trapezoidal', 
		...     climbRateMPS       = 6, 
		...     descentRateMPS     = 6, 
		...     earliestLandTime   = 500, 
		...     loiterPosition     = 'arrivalAtAlt', 
		...     leafletColor       = 'orange', 
		...     leafletWeight      = 3, 
		...     leafletStyle       = 'solid', 
		...     leafletOpacity     = 0.8, 
		...     useArrows          = True, 
		...     cesiumColor        = 'orange', 
		...     cesiumWeight       = 3, 
		...     cesiumStyle        = 'solid', 
		...     cesiumOpacity      = 0.8)

		>>> vrv.createCesium(
		...     assignments = shapepoints3D, 
		...     cesiumDir   = os.environ['CESIUMDIR'],
		...     problemDir  = 'examples/shapepoints3D/ex6')


	3D Shapepoints Demo - This final example combines several VeRoViz functions.  In this example, a truck and a drone start at the same location (node 1). The drone will travel to nodes 2 and 3; the truck will travel directly to node 3. The drone cannot land at node 3 until the truck arrives.
		>>> # Define 3 nodes
		>>> nodes = vrv.createNodesFromLocs(
		...    locs             = [[42.80, -78.80], 
		...                        [42.83, -78.75], 
		...                        [42.80, -78.70]], 
		...    snapToRoad       = True, 
		...    dataProvider     = 'ORS-online',
		...    dataProviderArgs = {'APIkey': os.environ['ORSKEY']})
		>>> nodes

		>>> # Find the truck's travel time from node 1 to node 3
		>>> [truckTimeSec, truckDistMeters] = vrv.getTimeDistScalar2D(
		...      startLoc         = list(nodes[nodes['id']==1][['lat', 'lon']].values[0]),
		...      endLoc           = list(nodes[nodes['id']==3][['lat', 'lon']].values[0]),
		...      routeType        = 'fastest',
		...      dataProvider     = 'ORS-online',
		...      dataProviderArgs = {'APIkey': os.environ['ORSKEY']})
		>>> truckTimeSec

		>>> # Get the truck shapepoints, using expected duration
		>>> truckShapepoints = vrv.getShapepoints2D(
		...        odID             = 1,
		...        objectID         = 'truck', 
		...        modelFile        = 'veroviz/models/ub_truck.glb', 
		...        modelScale       = 100,
		...        modelMinPxSize   = 75,
		...        startTimeSec     = 0,
		...        startLoc         = list(nodes[nodes['id']==1][['lat', 'lon']].values[0]),
		...        endLoc           = list(nodes[nodes['id']==3][['lat', 'lon']].values[0]),
		...        expDurationSec   = truckTimeSec, 
		...        routeType        = 'fastest', 
		...        dataProvider     = 'ORS-online',
		...        dataProviderArgs = {'APIkey': os.environ['ORSKEY']}, 
		...        leafletColor     = 'blue', 
		...        cesiumColor      = 'blue')

		>>> # Make the truck stay idle when it arrives at node 3:
		>>> truckShapepoints = vrv.addStaticAssignment(
		...    initAssignments = truckShapepoints, 
		...    odID            = 1, 
		...    objectID        = 'truck', 
		...    modelFile       = 'veroviz/models/ub_truck.glb', 
		...    modelScale      = 100,
		...    modelMinPxSize  = 75,
		...    loc             = list(nodes[nodes['id']==3][['lat', 'lon']].values[0]), 
		...    startTimeSec    = max(truckShapepoints['endTimeSec']),
		...    endTimeSec      = -1)

		>>> # Route the drone from 1 to 2:
		>>> droneShapepoints_1 = vrv.getShapepoints3D(
		...        odID               = 2,
		...        objectID           = 'drone', 
		...        modelFile          = '/veroviz/models/drone.glb',
		...        startTimeSec       = 0,
		...        startLoc           = list(nodes[nodes['id']==1][['lat', 'lon']].values[0]),
		...        endLoc             = list(nodes[nodes['id']==2][['lat', 'lon']].values[0]),
		...        cruiseAltMetersAGL = 220,
		...        takeoffSpeedMPS    = 15,
		...        cruiseSpeedMPS     = 20,
		...        landSpeedMPS       = 10,
		...        climbRateMPS       = None,
		...        descentRateMPS     = None,    
		...        routeType          = 'square',
		...        earliestLandTime   = -1,      # Can land as soon as it arrives.
		...        cesiumColor        = 'orange')

		>>> # Route the drone from 2 to 3, but wait for the truck before landing:
		>>> droneShapepoints_2 = vrv.getShapepoints3D(
		...        odID               = 2,
		...        objectID           = 'drone', 
		...        modelFile          = '/veroviz/models/drone.glb',
		...        startTimeSec       = max(droneShapepoints_1['endTimeSec']),
		...        startLoc           = list(nodes[nodes['id']==2][['lat', 'lon']].values[0]),
		...        endLoc             = list(nodes[nodes['id']==3][['lat', 'lon']].values[0]),
		...        cruiseAltMetersAGL = 220,
		...        takeoffSpeedMPS    = 15,
		...        cruiseSpeedMPS     = 20,
		...        landSpeedMPS       = 10,
		...        climbRateMPS       = None,
		...        descentRateMPS     = None,    
		...        routeType          = 'square',
		...        earliestLandTime   = truckTimeSec,    # Must wait for truck to arrive.
		...        loiterPosition     = 'arrivalAtAlt',
		...        cesiumColor        = 'orange')
		
		>>> # Create an assignments dataframe.
		>>> # The assignments dataframe will hold all shapepoints for both vehicles.
		>>> assignmentsDF = pd.concat([truckShapepoints, droneShapepoints_1, droneShapepoints_2], 
		...                          ignore_index=True, sort=False)
		>>> assignmentsDF	
		
		>>> # Look at the routes in Leaflet.
		>>> # We can't see timing or altitude changes here.
		>>> vrv.createLeaflet(nodes=nodes, arcs=assignmentsDF)
		
		>>> # Generate Cesium materials so we can watch the vehicle movements:
		>>> vrv.createCesium(
		...     assignments = assignmentsDF, 
		...     cesiumDir   = os.environ['CESIUMDIR'],
		...     problemDir  = '/examples/shapepoints3D/demo')
	
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valGetShapepoints3D(odID, objectID, modelFile, startTimeSec, startLoc, endLoc, takeoffSpeedMPS, cruiseSpeedMPS, landSpeedMPS, cruiseAltMetersAGL, routeType, climbRateMPS, descentRateMPS, earliestLandTime, loiterPosition, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor, ganttColorLoiter)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	assignments = privGetShapepoints3D(odID=odID, objectID=objectID, modelFile=modelFile, startTimeSec=startTimeSec, startLoc=startLoc, endLoc=endLoc, takeoffSpeedMPS=takeoffSpeedMPS, cruiseSpeedMPS=cruiseSpeedMPS, landSpeedMPS=landSpeedMPS, cruiseAltMetersAGL=cruiseAltMetersAGL, routeType=routeType, climbRateMPS=climbRateMPS, descentRateMPS=descentRateMPS, earliestLandTime=earliestLandTime, loiterPosition=loiterPosition, leafletColor=leafletColor, leafletWeight=leafletWeight, leafletStyle=leafletStyle, leafletOpacity=leafletOpacity, leafletCurveType=leafletCurveType, leafletCurvature=leafletCurvature, useArrows=useArrows, modelScale=modelScale, modelMinPxSize=modelMinPxSize, cesiumColor=cesiumColor, cesiumWeight=cesiumWeight, cesiumStyle=cesiumStyle, cesiumOpacity=cesiumOpacity, ganttColor=ganttColor, ganttColorLoiter=ganttColorLoiter, popupText=popupText)

	return assignments
