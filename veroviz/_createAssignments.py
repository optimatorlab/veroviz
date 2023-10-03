from veroviz._common import *
from veroviz._internal import loc2Dict
from veroviz._utilities import privInitDataframe
from veroviz._internal import replaceBackslashToSlash, addHeadSlash

def privAddStaticAssignment(initAssignments=None, odID=1, objectID=None, modelFile=None, modelScale=config['VRV_DEFAULT_CESIUMMODELSCALE'], modelMinPxSize=config['VRV_DEFAULT_CESIUMMODELMINPXSIZE'], loc=None, startTimeSec=None, endTimeSec=None, ganttColor=config['VRV_DEFAULT_GANTTCOLOR'], popupText=None):
				
	# Replace backslash
	modelFile = replaceBackslashToSlash(modelFile)

	# Ensure leading slash
	modelFile = addHeadSlash(modelFile)

	# assignment dataframe
	assignments = privInitDataframe('Assignments')

	dicLoc = loc2Dict(loc)
	
	assignments = pd.concat([assignments, pd.DataFrame({
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
		'ganttColor': ganttColor,
		'popupText': popupText,
		'leafletColor': None, 
		'leafletWeight': None,
		'leafletStyle': None,
		'leafletOpacity': None,
		'leafletCurveType': None,
		'leafletCurvature': None,
		'cesiumColor': None,
		'cesiumWeight': None,
		'cesiumStyle': None,
		'cesiumOpacity': None, 
		'useArrows': None,
		'startElevMeters' : None,
		'endElevMeters' : None,
		'wayname' : None,
		'waycategory' : None,
		'surface' : None,
		'waytype' : None, 
		'steepness' : None,
		'tollway' : None
		})], ignore_index=True, sort=False)

	if (type(initAssignments) is pd.core.frame.DataFrame):
		assignments = pd.concat([initAssignments, assignments], ignore_index=True)
				
	return assignments
	
