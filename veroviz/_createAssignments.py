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
	dicLoc = loc2Dict(loc)
	assignments = pd.DataFrame([{'odID': odID,
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
								'leafletColor': config['VRV_DEFAULT_LEAFLETARCCOLOR'],
								'leafletWeight': config['VRV_DEFAULT_LEAFLETARCWEIGHT'],
								'leafletStyle': config['VRV_DEFAULT_LEAFLETARCSTYLE'],
								'leafletOpacity': config['VRV_DEFAULT_LEAFLETARCOPACITY'],
								'leafletCurveType': config['VRV_DEFAULT_ARCCURVETYPE'],
								'leafletCurvature': config['VRV_DEFAULT_ARCCURVATURE'],
								'cesiumColor': None,
								'cesiumWeight': config['VRV_DEFAULT_CESIUMPATHWEIGHT'],
								'cesiumStyle': None,
								'cesiumOpacity': config['VRV_DEFAULT_CESIUMPATHOPACITY'], 
								'useArrows': False, # None,
								'startElevMeters' : 0, # None,
								'endElevMeters' : 0, # None,
								'wayname' : None,
								'waycategory' : None,
								'surface' : None,
								'waytype' : None, 
								'steepness' : 0, # None,
								'tollway' : False # None
								}], columns = privInitDataframe('Assignments').columns)
	
	assignments = assignments.astype(dtypeMapping['assignments'])
	if (type(initAssignments) is pd.core.frame.DataFrame):
		if (len(initAssignments) > 0):
			assignments = pd.concat([initAssignments, assignments], ignore_index=True)
				
	return assignments
	
