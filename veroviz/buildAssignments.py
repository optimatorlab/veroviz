from veroviz._common import *

from veroviz._validation import valAddStaticAssignment

from veroviz._internal import loc2Dict
from veroviz._internal import replaceBackslashToSlash
from veroviz.utilities import initDataframe

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

	# Replace backslash
	modelFile = replaceBackslashToSlash(modelFile)

	# assignment dataframe
	assignments = initDataframe('Assignments')

	dicLoc = loc2Dict(loc)
	assignments = assignments.append({
		'odID': odID,
		'objectID': objectID,
		'modelFile': modelFile,
		'modelScale': modelScale,
		'modelMinPxSize': modelMinPxSize,
		'startTimeSec': startTimeSec,
		'startLat': dicLoc['lat'],
		'startLon': dicLoc['lon'],
		'startAltMeters': dicLoc['alt'],
		'endTimeSec': endTimeSec,
		'endLat': dicLoc['lat'],
		'endLon': dicLoc['lon'],
		'endAltMeters': dicLoc['alt'],
		'leafletColor': None, 
		'leafletWeight': None,
		'leafletStyle': None,
		'leafletOpacity': None,
		'cesiumColor': None,
		'cesiumWeight': None,
		'cesiumStyle': None,
		'cesiumOpacity': None, 
		'useArrows': None
		}, ignore_index=True, sort=False)

	if (type(initAssignments) is pd.core.frame.DataFrame):
		assignments = pd.concat([initAssignments, assignments], ignore_index=True)

	return assignments