__version__ = '0.4.0'

# Generate Objects
from veroviz.generateNodes import generateNodes
from veroviz.generateNodes import createNodesFromLocs
from veroviz.generateArcs import createArcsFromLocSeq
from veroviz.generateArcs import createArcsFromNodeSeq
from veroviz.snapNodesToRoad import snapNodesToRoad
from veroviz.snapNodesToRoad import getSnapLoc
from veroviz.snapNodesToRoad import getSnapLocBatch
from veroviz.getTimeDist2D import getTimeDist2D
from veroviz.getTimeDistScalar2D import getTimeDistScalar2D
from veroviz.getTimeDist3D import getTimeDist3D
from veroviz.getTimeDistScalar3D import getTimeDistScalar3D
from veroviz.getShapepoints2D import getShapepoints2D
from veroviz.getShapepoints3D import getShapepoints3D
from veroviz.createAssignments import addAssignment2D
from veroviz.createAssignments import addAssignment3D
from veroviz.createAssignments import addStaticAssignment
from veroviz.createAssignments import createAssignmentsFromArcs2D
from veroviz.createAssignments import createAssignmentsFromNodeSeq2D
from veroviz.createAssignments import createAssignmentsFromLocSeq2D

# Utilities
from veroviz.utilities import *

# Visualize objects
from veroviz.createLeaflet import createLeaflet
from veroviz.createLeaflet import addLeafletCircle
from veroviz.createLeaflet import addLeafletMarker
from veroviz.createLeaflet import addLeafletPolygon
from veroviz.createLeaflet import addLeafletPolyline
from veroviz.createLeaflet import addLeafletText
from veroviz.createLeaflet import addLeafletIcon
from veroviz.createLeaflet import addLeafletIsochrones
from veroviz.createCesium import createCesium

# Internal shared small functions/constants/validation
from veroviz._common import *
from veroviz._params import *
from veroviz._internal import *
from veroviz._validation import *
from veroviz._geometry import *

# pgRouting related
from veroviz._queryPgRouting import pgrGetSnapToRoadLatLon
from veroviz._queryPgRouting import pgrGetNearestStreet
from veroviz._queryPgRouting import pgrGetShapepointsTimeDist
from veroviz._queryPgRouting import pgrGetTimeDist

# ORS related
from veroviz._queryORS import orsGetSnapToRoadLatLon
from veroviz._queryORS import orsGetShapepointsTimeDist
from veroviz._queryORS import orsGetTimeDistAll2All
from veroviz._queryORS import orsGetTimeDistOne2Many
from veroviz._queryORS import orsGetTimeDistMany2One
from veroviz._queryORS import orsGeocode
from veroviz._queryORS import orsReverseGeocode
from veroviz._queryORS import orsIsochrones

# OSRM related
from veroviz._queryOSRM import osrmGetSnapToRoadLatLon
from veroviz._queryOSRM import osrmGetShapepointsTimeDist
from veroviz._queryOSRM import osrmGetTimeDistOnePair
from veroviz._queryOSRM import osrmGetTimeDist

# MapQuest related
from veroviz._queryMapQuest import mqGetSnapToRoadLatLon
from veroviz._queryMapQuest import mqGetSnapToRoadLatLonBatch
from veroviz._queryMapQuest import mqGetShapepointsTimeDist
from veroviz._queryMapQuest import mqGetTimeDistAll2All
from veroviz._queryMapQuest import mqGetTimeDistOne2Many
from veroviz._queryMapQuest import mqGetTimeDistMany2One
from veroviz._queryMapQuest import mqGeocode
from veroviz._queryMapQuest import mqReverseGeocode

# 3D function related
from veroviz._buildFlightProfile import buildNoLoiteringFlight
from veroviz._buildFlightProfile import getTimeDistFromFlight
from veroviz._buildFlightProfile import addLoiterTimeToFlight

# Function related to travel matrices generating
from veroviz._getTimeDistFromLocs2D import getTimeDistFromLocs2D

# Functions related to snapping nodes to road
from veroviz._getSnapLoc import privGetSnapLocBatch
from veroviz._getSnapLoc import privGetSnapLoc

# Functions that deconstruct an Assignments dataframe for `createLeaflet` and `createCesium`
from veroviz._deconstructAssignments import deconstructAssignments
from veroviz._createEntitiesFromList import privCreateNodesFromLocs
from veroviz._createEntitiesFromList import privCreateArcsFromLocSeq

# Functions related to assignments/shapepoints:
from veroviz._createAssignments import privAddStaticAssignment
from veroviz._getShapepoints import privGetShapepoints2D

# Check the current version and latest version of veroviz
def checkVersion():
	urllib3.disable_warnings()

	versionStatus = ""
	currentVersion = __version__
	latestVersion = ""
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', "https://pypi.python.org/pypi/veroviz/json")
		data = json.loads(response.data.decode('utf-8'))
		latestVersion = data['info']['version']
		if (currentVersion == latestVersion):
			versionStatus = "Your current installed version of veroviz is %s. You are up-to-date with the latest available version." % (currentVersion)
		else:
			versionStatus = "Your current installed version of veroviz is %s, the latest version available is %s. To update to the latest version, type `pip install --upgrade veroviz` at a command-line prompt." % (currentVersion, latestVersion)

	except:
		versionStatus = "Error: Cannot determine the latest version of veroviz. The most common cause is that your computer isn't connected to the network."

	return versionStatus

