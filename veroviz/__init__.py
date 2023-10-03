__version__ = '0.4.6'

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
from veroviz._utilities import *

# Visualize objects
from veroviz.createLeaflet import createLeaflet
from veroviz.createLeaflet import addLeafletCircle
from veroviz.createLeaflet import addLeafletMarker
from veroviz.createLeaflet import addLeafletPolygon
from veroviz.createLeaflet import addLeafletPolyline
from veroviz.createLeaflet import addLeafletText
from veroviz.createLeaflet import addLeafletIcon
from veroviz.createLeaflet import addLeafletIsochrones
from veroviz.createLeaflet import addLeafletWeather
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

# ORS-online related
from veroviz._queryORS import orsGetSnapToRoadLatLon
from veroviz._queryORS import orsGetShapepointsTimeDist
from veroviz._queryORS import orsGetTimeDistAll2All
from veroviz._queryORS import orsGetTimeDistOne2Many
from veroviz._queryORS import orsGetTimeDistMany2One
from veroviz._queryORS import orsGeocode
from veroviz._queryORS import orsReverseGeocode
from veroviz._queryORS import orsIsochrones
from veroviz._queryORS import orsGetElevation

# ORS-local related
from veroviz._queryORSlocal import orsLocalGetSnapToRoadLatLon
from veroviz._queryORSlocal import orsLocalGetShapepointsTimeDist
from veroviz._queryORSlocal import orsLocalGetTimeDistAll2All
from veroviz._queryORSlocal import orsLocalGetTimeDistOne2Many
from veroviz._queryORSlocal import orsLocalGetTimeDistMany2One
from veroviz._queryORSlocal import orsLocalIsochrones

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

# USGS related
from veroviz._queryUSGS import usgsGetElevation

# Elevation-API.io related
from veroviz._queryElevationapiio import elevapiGetElevation

# OpenWeather related
from veroviz._queryOpenWeather import owGetWeather

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

def setGlobal(newConfig):
	"""
	This function accepts a dictionary as an input. The key corresponds to a global VeRoViz setting parameter.  This makes it easier for users to change default values for Leaflet entities and default settings.  All the settings are saved in a dictionary named config.  Changes to default config settings are temporary (i.e., lasting only for a particular session).

	Parameters
	----------
	newConfig: Dictionary
		New configurations for default values and global settings, the keys are the same as the global variable `config`. See :ref:`Global Settings and Defaults` for more details.
	"""
	global config
	if ('VRV_DEFAULT_DISTANCE_ERROR_TOLERANCE' in newConfig):
		config['VRV_DEFAULT_DISTANCE_ERROR_TOLERANCE'] = newConfig['VRV_DEFAULT_DISTANCE_ERROR_TOLERANCE']
	if ('VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE' in newConfig):
		config['VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE'] = newConfig['VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE']
	if ('VRV_DEFAULT_LEAFLET_OBJECT_COLOR_FILL' in newConfig):
		config['VRV_DEFAULT_LEAFLET_OBJECT_COLOR_FILL'] = newConfig['VRV_DEFAULT_LEAFLET_OBJECT_COLOR_FILL']
	if ('VRV_DEFAULT_LEAFLET_FONTSIZE' in newConfig):
		config['VRV_DEFAULT_LEAFLET_FONTSIZE'] = newConfig['VRV_DEFAULT_LEAFLET_FONTSIZE']
	if ('VRV_DEFAULT_LEAFLET_FONTCOLOR' in newConfig):
		config['VRV_DEFAULT_LEAFLET_FONTCOLOR'] = newConfig['VRV_DEFAULT_LEAFLET_FONTCOLOR']
	if ('VRV_DEFAULT_LEAFLET_MAPTILES' in newConfig):
		config['VRV_DEFAULT_LEAFLET_MAPTILES'] = newConfig['VRV_DEFAULT_LEAFLET_MAPTILES']
	if ('VRV_DEFAULT_LEAFLETICONPREFIX' in newConfig):
		config['VRV_DEFAULT_LEAFLETICONPREFIX'] = newConfig['VRV_DEFAULT_LEAFLETICONPREFIX']
	if ('VRV_DEFAULT_LEAFLETICONTYPE' in newConfig):
		config['VRV_DEFAULT_LEAFLETICONTYPE'] = newConfig['VRV_DEFAULT_LEAFLETICONTYPE']
	if ('VRV_DEFAULT_LEAFLETICONCOLOR' in newConfig):
		config['VRV_DEFAULT_LEAFLETICONCOLOR'] = newConfig['VRV_DEFAULT_LEAFLETICONCOLOR']
	if ('VRV_DEFAULT_LEAFLETARCWEIGHT' in newConfig):
		config['VRV_DEFAULT_LEAFLETARCWEIGHT'] = newConfig['VRV_DEFAULT_LEAFLETARCWEIGHT']
	if ('VRV_DEFAULT_LEAFLETARCSTYLE' in newConfig):
		config['VRV_DEFAULT_LEAFLETARCSTYLE'] = newConfig['VRV_DEFAULT_LEAFLETARCSTYLE']
	if ('VRV_DEFAULT_LEAFLETARCOPACITY' in newConfig):
		config['VRV_DEFAULT_LEAFLETARCOPACITY'] = newConfig['VRV_DEFAULT_LEAFLETARCOPACITY']
	if ('VRV_DEFAULT_LEAFLETARCCOLOR' in newConfig):
		config['VRV_DEFAULT_LEAFLETARCCOLOR'] = newConfig['VRV_DEFAULT_LEAFLETARCCOLOR']
	if ('VRV_DEFAULT_LEAFLETBOUNDINGWEIGHT' in newConfig):
		config['VRV_DEFAULT_LEAFLETBOUNDINGWEIGHT'] = newConfig['VRV_DEFAULT_LEAFLETBOUNDINGWEIGHT']
	if ('VRV_DEFAULT_LEAFLETBOUNDINGOPACITY' in newConfig):
		config['VRV_DEFAULT_LEAFLETBOUNDINGOPACITY'] = newConfig['VRV_DEFAULT_LEAFLETBOUNDINGOPACITY']
	if ('VRV_DEFAULT_LEAFLETBOUNDINGSTYLE' in newConfig):
		config['VRV_DEFAULT_LEAFLETBOUNDINGSTYLE'] = newConfig['VRV_DEFAULT_LEAFLETBOUNDINGSTYLE']
	if ('VRV_DEFAULT_LEAFLETBOUNDINGCOLOR' in newConfig):
		config['VRV_DEFAULT_LEAFLETBOUNDINGCOLOR'] = newConfig['VRV_DEFAULT_LEAFLETBOUNDINGCOLOR']
	if ('VRV_DEFAULT_ARCCURVETYPE' in newConfig):
		config['VRV_DEFAULT_ARCCURVETYPE'] = newConfig['VRV_DEFAULT_ARCCURVETYPE']
	if ('VRV_DEFAULT_ARCCURVATURE' in newConfig):
		config['VRV_DEFAULT_ARCCURVATURE'] = newConfig['VRV_DEFAULT_ARCCURVATURE']
	if ('VRV_DEFAULT_CESIUMMODELSCALE' in newConfig):
		config['VRV_DEFAULT_CESIUMMODELSCALE'] = newConfig['VRV_DEFAULT_CESIUMMODELSCALE']
	if ('VRV_DEFAULT_CESIUMMODELMINPXSIZE' in newConfig):
		config['VRV_DEFAULT_CESIUMMODELMINPXSIZE'] = newConfig['VRV_DEFAULT_CESIUMMODELMINPXSIZE']
	if ('VRV_DEFAULT_CESIUMICONTYPE' in newConfig):
		config['VRV_DEFAULT_CESIUMICONTYPE'] = newConfig['VRV_DEFAULT_CESIUMICONTYPE']
	if ('VRV_DEFAULT_CESIUMICONSIZE' in newConfig):
		config['VRV_DEFAULT_CESIUMICONSIZE'] = newConfig['VRV_DEFAULT_CESIUMICONSIZE']
	if ('VRV_DEFAULT_CESIUMICONCOLOR' in newConfig):
		config['VRV_DEFAULT_CESIUMICONCOLOR'] = newConfig['VRV_DEFAULT_CESIUMICONCOLOR']
	if ('VRV_DEFAULT_CESIUMPATHCOLOR' in newConfig):
		config['VRV_DEFAULT_CESIUMPATHCOLOR'] = newConfig['VRV_DEFAULT_CESIUMPATHCOLOR']
	if ('VRV_DEFAULT_CESIUMPATHWEIGHT' in newConfig):
		config['VRV_DEFAULT_CESIUMPATHWEIGHT'] = newConfig['VRV_DEFAULT_CESIUMPATHWEIGHT']
	if ('VRV_DEFAULT_CESIUMPATHSTYLE' in newConfig):
		config['VRV_DEFAULT_CESIUMPATHSTYLE'] = newConfig['VRV_DEFAULT_CESIUMPATHSTYLE']
	if ('VRV_DEFAULT_CESIUMPATHOPACITY' in newConfig):
		config['VRV_DEFAULT_CESIUMPATHOPACITY'] = newConfig['VRV_DEFAULT_CESIUMPATHOPACITY']
	if ('VRV_DEFAULT_LEAFLET_ARROWSIZE' in newConfig):
		config['VRV_DEFAULT_LEAFLET_ARROWSIZE'] = newConfig['VRV_DEFAULT_LEAFLET_ARROWSIZE']
	if ('VRV_DEFAULT_GANTTCOLOR' in newConfig):
		config['VRV_DEFAULT_GANTTCOLOR'] = newConfig['VRV_DEFAULT_GANTTCOLOR']
	if ('VRV_DEFAULT_GANTTCOLORSERVICE' in newConfig):
		config['VRV_DEFAULT_GANTTCOLORSERVICE'] = newConfig['VRV_DEFAULT_GANTTCOLORSERVICE']
	if ('VRV_DEFAULT_GANTTCOLORLOITER' in newConfig):
		config['VRV_DEFAULT_GANTTCOLORLOITER'] = newConfig['VRV_DEFAULT_GANTTCOLORLOITER']
	if ('VRV_SETTING_PGROUTING_USERNAME' in newConfig):
		config['VRV_SETTING_PGROUTING_USERNAME'] = newConfig['VRV_SETTING_PGROUTING_USERNAME']
	if ('VRV_SETTING_PGROUTING_HOST' in newConfig):
		config['VRV_SETTING_PGROUTING_HOST'] = newConfig['VRV_SETTING_PGROUTING_HOST']
	if ('VRV_SETTING_PGROUTING_PASSWORD' in newConfig):
		config['VRV_SETTING_PGROUTING_PASSWORD'] = newConfig['VRV_SETTING_PGROUTING_PASSWORD']
	if ('VRV_SETTING_SHOWOUTPUTMESSAGE' in newConfig):
		config['VRV_SETTING_SHOWOUTPUTMESSAGE'] = newConfig['VRV_SETTING_SHOWOUTPUTMESSAGE']
	if ('VRV_SETTING_SHOWWARNINGMESSAGE' in newConfig):
		config['VRV_SETTING_SHOWWARNINGMESSAGE'] = newConfig['VRV_SETTING_SHOWWARNINGMESSAGE']
	return
