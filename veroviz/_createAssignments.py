from veroviz._common import *
from veroviz._internal import loc2Dict
from veroviz.utilities import initDataframe
from veroviz._internal import replaceBackslashToSlash

def privAddStaticAssignment(initAssignments=None, odID=1, objectID=None, modelFile=None, modelScale=VRV_DEFAULT_CESIUMMODELSCALE, modelMinPxSize=VRV_DEFAULT_CESIUMMODELMINPXSIZE, loc=None, startTimeSec=None, endTimeSec=None):
				
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
	