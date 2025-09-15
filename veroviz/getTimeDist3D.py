from veroviz._common import *
from veroviz._validation import *

from veroviz._buildFlightProfile import buildNoLoiteringFlight
from veroviz._buildFlightProfile import getTimeDistFromFlight

from veroviz._utilities import privConvertDistance
from veroviz._utilities import privConvertTime

def getTimeDist3D(nodes=None, matrixType='all2all', fromNodeID=None, toNodeID=None, takeoffSpeedMPS=None, cruiseSpeedMPS=None, landSpeedMPS=None, cruiseAltMetersAGL=None,
	routeType='square',	climbRateMPS=None, descentRateMPS=None, outputDistUnits='meters', outputTimeUnits='seconds'):

	"""
	This function calculates travel time and distance for vehicles that travel in 3-dimensional space (e.g., drones).  The function returns three dictionaries; one for time, one for ground distance, and one for overall (3D) travel distance.

	Parameters
	----------
	nodes: :ref:`Nodes`, Required, default as None
		This :ref:`Nodes` dataframe contains the locations between which the travel time and distance will be calculated.
	matrixType: string, Optional, default as 'all2all'
		Specifies the structure of the travel matrices.  Valid options include 'all2all', 'many2one', and 'one2many'.  The default 'all2all' option will return square matrices (one for time, one for distance) describing the directed travel time and travel distance between all pairs of nodes.  The 'one2many' option will return vectors describing the directed travel from one node to all other nodes.  Similarly, the 'many2one' option will return vectors describing the directed travel from all nodes to a given node.  See the table in the note below for details.
	fromNodeID: int, Optional, default as None
		Specifies the node ID (from the `id` column of the input `nodes` dataframe) of the origin node.  This parameter is required for the 'one2many' matrix type; it is ignored by all other matrix types.  See the table in the note below for details.
	toNodeID: int, Optional, default as None
		Specifies the node ID (from the `id` column of the input `nodes` dataframe) of the destination node.  This parameter is required for the 'many2one' matrix type; it is ignored for all other matrix types.  See the table in the note below for details.
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
	outputDistUnits: string, Optional, default as 'meters'
		Specifies the desired distance units for the function's output.  Valid values are 'meters', 'm', 'kilometers', 'km', 'miles', 'mi', 'feet', 'ft', 'nm', and 'nmi' (nautical miles). See :ref:`Units` for options and abbreviations.
	outputTimeUnits: string, Optional, default as 'seconds'
		Specifies the desired time units for the function's output.  Valid values are 'seconds', 'hours', and 'minutes'. See :ref:`Units` for options and abbreviations.
	
	Returns
	-------
	totalTime: dictionary
		A Python dictionary containing travel times.  Time units are defined by `outputTimeUnits`.  The format of key values is: `(fromID, toID)`.  The travel time from ID 1 to ID 2 is provided by `time[1, 2]`. 
	totalGroundDistance: dictionary
		A Python dictionary containing ground travel distances (i.e., ignoring any vertical distances).  Distance units are defined by `outputDistUnits`.  The format of key values is: `(fromID, toID)`.  The horizontal-only travel distance from ID 1 to ID 2 is provided by `totalGroundDistance[1, 2]`.  
	totalFlightDistance: dictionary
		A Python dictionary containing total travel distances (i.e., including both the horizontal and vertical components of flight).  Distance units are defined by `outputDistUnits`.  The format of key values is: `(fromID, toID)`.  The total travel distance from ID 1 to ID 2 is provided by `totalFlightDistance[1, 2]`.  

	Note
	----
	For `matrixType`, the options are 'all2all', 'one2many', and 'many2one'.

	+----------------------+--------------+------------+------------------+
	| `matrixType` options | `fromNodeID` | `toNodeID` | Return type      |
	+======================+==============+============+==================+
	| 'all2all'            | ignored      | ignored    | Square matrices  |
	+----------------------+--------------+------------+------------------+
	| 'one2many'           | required     | ignored    | Row vectors      |
	+----------------------+--------------+------------+------------------+
	| 'many2one'           | ignored      | required   | Column vectors   |
	+----------------------+--------------+------------+------------------+

	In 'all2all', square matrices will be generated for all node pairs in the  
	provided `nodes` dataframe.

	In 'one2many', a node `id` will be assigned in the `fromNodeID` field, which 
	comes from the `id` column in the provided `nodes` dataframe.
	Row vectors will be returned for the time and distance from that node 
	to all the nodes in the provided `nodes` dataframe.

	In 'many2one', column vectors will be returned for the time and distance 
	from all nodes in the provided `nodes` dataframe to the node indicated 
	by `toNodeID`.


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

	Example 1 - Calculate 'all2all' travel matrices for a drone with a 'square' flight profile.  There are 3 nodes, so the matrices will be 3x3.  
		>>> [totalTime, totalGroundDistance, totalFlightDistance] = vrv.getTimeDist3D(
		...     nodes              = exampleNodes,
		...     routeType          = 'square',
		...     cruiseAltMetersAGL = 120,
		...     takeoffSpeedMPS    = 5,
		...     cruiseSpeedMPS     = 12,
		...     landSpeedMPS       = 2, 
		...     outputDistUnits    = 'meters', 
		...     outputTimeUnits    = 'seconds')
		>>> print("Travel time from node 2 to node 3 is %.2f seconds" % (totalTime[2, 3]))
		>>> print("Ground distance from node 2 to node 3 is %.2f meters" % (totalGroundDistance[2, 3]))
		>>> print("Total flight distance from node 2 to node 3 is %.2f meters" % (totalFlightDistance[2, 3]))

	Example 2 - Calculate 'one2many' travel matrices for a drone with a 'trapezoidal' flight profile, starting from node 2.  All functional arguments are included in this example.
		>>> [timeSec, groundDist, totalDist] = vrv.getTimeDist3D(
		...     nodes              = exampleNodes,
		...     matrixType         = 'one2many', 
		...     fromNodeID         = 2, 
		...     toNodeID           = None, 
		...     takeoffSpeedMPS    = 5, 
		...     cruiseSpeedMPS     = 12, 
		...     landSpeedMPS       = 5, 
		...     cruiseAltMetersAGL = 120, 
		...     routeType          = 'trapezoidal', 
		...     climbRateMPS       = 1, 
		...     descentRateMPS     = 1, 
		...     outputDistUnits    = 'meters', 
		...     outputTimeUnits    = 'seconds')
		>>> print("Travel time from node 2 to node 3 is %.2f seconds" % (timeSec[2, 3]))
		>>> print("Ground distance from node 2 to node 3 is %.2f meters" % (groundDist[2, 3]))
		>>> print("Total flight distance from node 2 to node 3 is %.2f meters" % (totalDist[2, 3]))
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valGetTimeDist3D(nodes, matrixType, fromNodeID, toNodeID, outputDistUnits, outputTimeUnits, routeType, takeoffSpeedMPS, climbRateMPS, cruiseSpeedMPS, cruiseAltMetersAGL, landSpeedMPS, descentRateMPS)
	if (not valFlag):
		print (errorMsg)
		return [None, None, None]
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	try:
		matrixType = matrixType.lower()
	except:
		pass

	# Specify the list of rows and columns of output dataframes
	fromIDs = []
	toIDs = []
	if (matrixType == "all2all"):
		fromIDs = nodes['id'].tolist()
		toIDs = nodes['id'].tolist()
	elif (matrixType == "one2many"):
		fromIDs = [fromNodeID]
		toIDs = nodes['id'].tolist()
	elif (matrixType == "many2one"):
		fromIDs = nodes['id'].tolist()
		toIDs = [toNodeID]
	else:
		return 

	# Specify the list of coordinations, for each coordinate, it is in [lat, lon, alt] format
	fromLocs = []
	toLocs = []
	for i in range(0, len(fromIDs)):
		fromLocs.append([
			float(nodes.loc[nodes['id'] == fromIDs[i], 'lat'].item()), 
			float(nodes.loc[nodes['id'] == fromIDs[i], 'lon'].item()), 
			float(nodes.loc[nodes['id'] == fromIDs[i], 'altMeters'].item())])
	for i in range(0, len(toIDs)):
		toLocs.append([
			float(nodes.loc[nodes['id'] == toIDs[i], 'lat'].item()), 
			float(nodes.loc[nodes['id'] == toIDs[i], 'lon'].item()), 
			float(nodes.loc[nodes['id'] == toIDs[i], 'altMeters'].item())])

	# Do queries to find DICTIONARIES of distance and time matrices
	totalTimeSec = {}
	totalGroundDistMeters = {}
	totalFlightDistMeters = {}
	for i in range(len(fromLocs)):
		for j in range(i, len(toLocs)):
			# Prepare for fields to generate flight
			startLoc = fromLocs[i]
			endLoc = toLocs[j]

			if (i != j):
				# The flight has no loitering
				flight = buildNoLoiteringFlight(routeType, startLoc, cruiseAltMetersAGL, endLoc, takeoffSpeedMPS, climbRateMPS, cruiseSpeedMPS, landSpeedMPS, descentRateMPS)
				
				# Time and ground/flight distance, notice the matrix is symmetric
				[time, groundDistance, flightDistance] = getTimeDistFromFlight(flight.copy())
				totalTimeSec[i, j] = time
				totalTimeSec[j, i] = time
				totalGroundDistMeters[i, j] = groundDistance
				totalGroundDistMeters[j, i] = groundDistance
				totalFlightDistMeters[i, j] = flightDistance
				totalFlightDistMeters[j, i] = flightDistance
			else:
				totalTimeSec[i, j] = 0
				totalGroundDistMeters[i, j] = 0
				totalFlightDistMeters[i, j] = 0

	# Rename the keyvalues by fromRows and toCols and reset output units
	totalTime = {}
	totalGroundDistance = {}
	totalFlightDistance = {}
	for i in range(len(fromIDs)):
		for j in range(len(toIDs)):
			totalTime[fromIDs[i], toIDs[j]] = totalTimeSec[i, j] * privConvertTime(1.0, 's', outputTimeUnits)
			totalGroundDistance[fromIDs[i], toIDs[j]] = totalGroundDistMeters[i, j] * privConvertDistance(1.0, 'm', outputDistUnits)
			totalFlightDistance[fromIDs[i], toIDs[j]] = totalFlightDistMeters[i, j] * privConvertDistance(1.0, 'm', outputDistUnits)

	return [totalTime, totalGroundDistance, totalFlightDistance]
