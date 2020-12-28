from veroviz._common import *
from veroviz._geometry import *
from veroviz._internal import *

def valGenerateNodes(initNodes, nodeType, nodeName, numNodes, startNode, incrementName, incrementStart, nodeDistrib, nodeDistribArgs, snapToRoad, popupText, leafletIconPrefix, leafletIconType, leafletColor, leafletIconText, cesiumIconType, cesiumColor, cesiumIconText, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (initNodes is not None):
		[valFlag, errorMsg, newWarningMsg] = valNodes(initNodes)
		warningMsg += newWarningMsg

	if (valFlag):
		if (nodeName is None):
			if (incrementName == True):
				valFlag = False
				errorMsg = "Error: `incrementName` cannot be `True` if `nodeName` is not provided. There is no name on which to increment."

	if (valFlag):
		if (incrementName == True):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(incrementStart, 'incrementStart')
			warningMsg += newWarningMsg

	if (valFlag):
		if (numNodes is None):
			valFlag = False
			errorMsg = "Error: `numNodes` is required. Please enter the number of nodes to be generated."

	if (valFlag):
		if (startNode is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(startNode, "startNode")
			warningMsg += newWarningMsg

		if (valFlag and initNodes is not None):
			if (len(initNodes) > 0):
				maxID = max(initNodes['id'])
				if (maxID >= startNode):
					warningMsg += "Warning: 'id' in `initNodes` is already larger than `startNode`. Overriding `startNode` with maximum `id` + 1."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valNodeDistribArgs(nodeDistrib, nodeDistribArgs)
		warningMsg += newWarningMsg

	if (valFlag and (snapToRoad or nodeDistrib == 'unifRoadBasedBB')):
		if (dataProvider == None):
			valFlag = False
			errorMsg = "Error: A `dataProvider` is required if `snapToRoad = True`. Valid `dataProvider` options are 'pgRouting', 'MapQuest', 'ORS-online',  'OSRM-online', and 'ORS-local'."
		else:
			if (valFlag):
				locs = []
				if (nodeDistribArgs is not None):
					if ('boundingRegion' in nodeDistribArgs):
						locs.extend(nodeDistribArgs['boundingRegion'])
					if ('center' in nodeDistribArgs):
						locs.append(nodeDistribArgs['center'])
				[valFlag, errorMsg, newWarningMsg] = _valDatabase(locs, dataProvider, dataProviderArgs)
				warningMsg += newWarningMsg

	if (valFlag and nodeDistrib == 'normalBB' and nodeDistribArgs is not None):
		if ('boundingRegion' in nodeDistribArgs and 'center' in nodeDistribArgs):
			center = nodeDistribArgs['center']
			boundingRegion = nodeDistribArgs['boundingRegion']
			if (not geoIsPointInPoly(center, boundingRegion)):
				valFlag = False
				errorMsg = "Error: `center` of truncated normal distributed nodes should be within the `boundingRegion`."

	if (valFlag and nodeDistrib == 'normal' and nodeDistribArgs is not None):
		if ('boundingRegion' in nodeDistribArgs and 'center' in nodeDistribArgs):
			center = nodeDistribArgs['center']
			boundingRegion = nodeDistribArgs['boundingRegion']
			if (not geoIsPointInPoly(center, boundingRegion)):
				valFlag = False
				errorMsg = "Error: A `boundingRegion` was provided in `nodeDistribArgs`. The `nodeDistrib` is being treated as `normalBB` instead of `normal`.  With the truncated normal distribution, the `center` point must also be within the `boundingRegion`."

	if (valFlag):
		if ((leafletIconPrefix != None) or (leafletIconType != None) or (leafletColor != None)):
			try:
				leafletIconPrefix = leafletIconPrefix.lower()
			except:
				pass
				
			try:
				leafletIconType = leafletIconType.lower()
			except:
				pass
				
			try:
				leafletColor = leafletColor.lower()
			except:
				pass
		
			[valFlag, errorMsg, newWarningMsg] = _valLeafletNodeInputs(leafletIconPrefix, leafletIconType, leafletColor)
			warningMsg += newWarningMsg

	if (valFlag):
		if ((cesiumIconType != None) or (cesiumIconText != None) or (cesiumColor != None)):
			[valFlag, errorMsg, newWarningMsg] = _valCesiumNodeInputs(cesiumIconType, cesiumColor)
			warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valSnapNodesToRoad(nodes, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (nodes is not None):
		[valFlag, errorMsg, newWarningMsg] = valNodes(nodes)
		warningMsg += newWarningMsg
	else:
		valFlag = False
		errorMsg = "Error: `nodes` dataframe is required for `snapNodesToRoad()`."

	if (valFlag):
		locs = list(zip(nodes.lat, nodes.lon))
		[valFlag, errorMsg, newWarningMsg] = _valDatabase(locs, dataProvider, dataProviderArgs)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valGetTimeDist2D(nodes, matrixType, fromNodeID, toNodeID, outputDistUnits, outputTimeUnits, routeType, speedMPS, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		routeType = routeType.lower()
	except:
		pass

	if (nodes is not None):
		[valFlag, errorMsg, newWarningMsg] = valNodes(nodes)
		warningMsg += newWarningMsg
	else:
		valFlag = False
		errorMsg = "Error: `nodes` should not be None."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valMatrixType(matrixType, fromNodeID, toNodeID)
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			outputDistUnits = outputDistUnits.lower()
		except:
			pass
			
		[valFlag, errorMsg, newWarningMsg] = _valDistanceUnits(outputDistUnits, "output")
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			outputTimeUnits = outputTimeUnits.lower()
		except:
			pass

		[valFlag, errorMsg, newWarningMsg] = _valTimeUnits(outputTimeUnits, "output")
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valRouteType2DForScalar(routeType, speedMPS, dataProvider)
		warningMsg += newWarningMsg

	if (valFlag and routeType != 'euclidean2d' and routeType != 'manhattan'):
		locs = list(zip(nodes.lat, nodes.lon))
		[valFlag, errorMsg, newWarningMsg] = _valDatabase(locs, dataProvider, dataProviderArgs)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valGetTimeDistScalar2D(startLoc, endLoc, outputDistUnits, outputTimeUnits, routeType, speedMPS, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		routeType = routeType.lower()
	except:
		pass

	if (valFlag):
		if (startLoc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(startLoc)
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `startLoc` is required."

	if (valFlag):
		if (endLoc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(endLoc)
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `endLoc` is required."

	if (valFlag):
		try:
			outputDistUnits = outputDistUnits.lower()
		except:
			pass
			
		[valFlag, errorMsg, newWarningMsg] = _valDistanceUnits(outputDistUnits, "output")
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			outputTimeUnits = outputTimeUnits.lower()
		except:
			pass
			
		[valFlag, errorMsg, newWarningMsg] = _valTimeUnits(outputTimeUnits, "output")
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valRouteType2DForScalar(routeType, speedMPS, dataProvider)
		warningMsg += newWarningMsg

	if (valFlag and routeType != 'euclidean2d' and routeType != 'manhattan'):
		locs = [startLoc, endLoc]
		[valFlag, errorMsg, newWarningMsg] = _valDatabase(locs, dataProvider, dataProviderArgs)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valGetTimeDist3D(nodes, matrixType, fromNodeID, toNodeID, outputDistUnits, outputTimeUnits, routeType, takeoffSpeedMPS, climbRateMPS, cruiseSpeedMPS, cruiseAltMetersAGL, landSpeedMPS, descentRateMPS):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		routeType = routeType.lower()
	except:
		pass

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = valNodes(nodes)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valMatrixType(matrixType, fromNodeID, toNodeID)
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			outputDistUnits = outputDistUnits.lower()
		except:
			pass
			
		[valFlag, errorMsg, newWarningMsg] = _valDistanceUnits(outputDistUnits, "output")
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			outputTimeUnits = outputTimeUnits.lower()
		except:
			pass
			
		[valFlag, errorMsg, newWarningMsg] = _valTimeUnits(outputTimeUnits, "output")
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valRouteType3D(routeType, takeoffSpeedMPS, climbRateMPS, cruiseSpeedMPS, landSpeedMPS, descentRateMPS)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valGetTimeDistScalar3D(startLoc, endLoc, outputDistUnits, outputTimeUnits, takeoffSpeedMPS, cruiseSpeedMPS, landSpeedMPS, cruiseAltMetersAGL, routeType, climbRateMPS, descentRateMPS):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		routeType = routeType.lower()
	except:
		pass

	if (valFlag):
		if (startLoc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(startLoc)
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `startLoc` is required."

	if (valFlag):
		if (endLoc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(endLoc)
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `endLoc` is required."

	if (valFlag):
		try:
			outputDistUnits = outputDistUnits.lower()
		except:
			pass
			
		[valFlag, errorMsg, newWarningMsg] = _valDistanceUnits(outputDistUnits, "output")
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			outputTimeUnits = outputTimeUnits.lower()
		except:
			pass
			
		[valFlag, errorMsg, newWarningMsg] = _valTimeUnits(outputTimeUnits, "output")
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valRouteType3D(routeType, takeoffSpeedMPS, climbRateMPS, cruiseSpeedMPS, landSpeedMPS, descentRateMPS)
		warningMsg += newWarningMsg

	if (valFlag and routeType != 'straight'):
		if (len(startLoc)==3):
			startAlt = startLoc[2]
		else:
			startAlt = 0
		if (len(endLoc)==3):
			endAlt = endLoc[2]
		else:
			endAlt = 0
		[valFlag, errorMsg, newWarningMsg] = _valAltitude(startAlt, cruiseAltMetersAGL, endAlt)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valGetShapepoints2D(odID, objectID, modelFile, startLoc, endLoc, startTimeSec, expDurationSec, routeType, speedMPS, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		routeType = routeType.lower()
	except:
		pass

	if (valFlag):
		if (odID is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(odID, 'odID')
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `odID` is required for `getShapepoints2D()`."

	if (valFlag):
		if (objectID == None):
			warningMsg += "Warning: `objectID` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		if (modelFile == None):
			warningMsg += "Warning: `modelFile` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		if (startLoc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(startLoc)
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `startLoc` is required for `getShapepoints2D()`."

	if (valFlag):
		if (endLoc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(endLoc)
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `endLoc` is required for `getShapepoints2D()`."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(startTimeSec, 'startTimeSec')
		warningMsg += newWarningMsg

	if (valFlag):
		if (startLoc != endLoc):
			[valFlag, errorMsg, newWarningMsg] = _valRouteType2DForShapepoints(routeType, speedMPS, expDurationSec, dataProvider)
			warningMsg += newWarningMsg

	if (valFlag and routeType not in ['euclidean2d', 'manhattan']):
		if (startLoc != endLoc):
			locs = [startLoc, endLoc]
			[valFlag, errorMsg, newWarningMsg] = _valDatabase(locs, dataProvider, dataProviderArgs)
			warningMsg += newWarningMsg

	if (valFlag):
		if ((leafletColor != None) or (leafletWeight != None) or (leafletStyle != None) or (leafletOpacity != None)):
			try:
				leafletColor = leafletColor.lower()
			except:
				pass
				
			try:
				leafletStyle = leafletStyle.lower()
			except:
				pass
									
			[valFlag, errorMsg, newWarningMsg] = _valLeafletArcInputs(leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, leafletCurveType, leafletCurvature)
			warningMsg += newWarningMsg

	# print("FIXMELP -- DONE?  Need to validate `leafletCurveType` and `leafletCurvature`.")

	if (valFlag):
		if ((cesiumColor != None) or (cesiumWeight != None) or (cesiumStyle != None) or (cesiumOpacity != None)):
			try:
				cesiumStyle = cesiumStyle.lower()
			except:
				pass
				
			[valFlag, errorMsg, newWarningMsg] = _valCesiumArcInputs(cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)
			warningMsg += newWarningMsg

	if (valFlag):
		if (ganttColor is not None):
			if (ganttColor.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(ganttColor)
				warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valGetShapepoints3D(odID, objectID, modelFile, startTimeSec, startLoc, endLoc, takeoffSpeedMPS, cruiseSpeedMPS, landSpeedMPS, cruiseAltMetersAGL, routeType, climbRateMPS, descentRateMPS, earliestLandTime, loiterPosition, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor, ganttColorLoiter):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		routeType = routeType.lower()
	except:
		pass

	if (valFlag):
		if (odID is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(odID, 'odID')
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `odID` is required for `getShapepoints3D()`."

	if (valFlag):
		if (startLoc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(startLoc)
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `startLoc` is required for `getShapepoints3D()`."

	if (valFlag):
		if (endLoc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(endLoc)
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `endLoc` is required for `getShapepoints3D()`."

	if (valFlag):
		if (objectID == None):
			warningMsg += "Warning: `objectID` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		if (modelFile == None):
			warningMsg += "Warning: `modelFile` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag and startTimeSec is not None):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(startTimeSec, 'startTimeSec')
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valRouteType3D(routeType, takeoffSpeedMPS, climbRateMPS, cruiseSpeedMPS, landSpeedMPS, descentRateMPS)
		warningMsg += newWarningMsg

	if (valFlag and routeType != 'straight'):
		if (len(startLoc)==3):
			startAlt = startLoc[2]
		else:
			startAlt = 0
		if (len(endLoc)==3):
			endAlt = endLoc[2]
		else:
			endAlt = 0
		[valFlag, errorMsg, newWarningMsg] = _valAltitude(startAlt, cruiseAltMetersAGL, endAlt)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLoiterPosition(loiterPosition)
		warningMsg += newWarningMsg

	if (valFlag):
		if ((leafletColor != None) or (leafletWeight != None) or (leafletStyle != None) or (leafletOpacity != None)):
			try:
				leafletColor = leafletColor.lower()
			except:
				pass
				
			try:
				leafletStyle = leafletStyle.lower()
			except:
				pass
		
			[valFlag, errorMsg, newWarningMsg] = _valLeafletArcInputs(leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, leafletCurveType, leafletCurvature)
			warningMsg += newWarningMsg

	# print("FIXMELP -- DONE?  Need to validate `leafletCurveType` and `leafletCurvature`.")

	if (valFlag):
		if ((cesiumColor != None) or (cesiumWeight != None) or (cesiumStyle != None) or (cesiumOpacity != None)):
			[valFlag, errorMsg, newWarningMsg] = _valCesiumArcInputs(cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)
			warningMsg += newWarningMsg

	if (valFlag):
		if (ganttColor is not None):
			if (ganttColor.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(ganttColor)
				warningMsg += newWarningMsg

	if (valFlag):
		if (ganttColorLoiter is not None):
			if (ganttColorLoiter.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(ganttColorLoiter)
				warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valCreateLeaflet(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, nodes, leafletIconPrefix, leafletIconType, leafletIconColor, leafletIconText, arcs, leafletArcWeight, leafletArcStyle, leafletArcOpacity, leafletArcColor, arcCurveType, arcCurvature, useArrows, arrowsPerArc, boundingRegion, leafletBoundingWeight, leafletBoundingOpacity, leafletBoundingStyle, leafletBoundingColor): 
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valMapBoundary(mapBoundary, zoomStart)
		warningMsg += newWarningMsg

	'''
	if (valFlag):
		if (nodes is None and arcs is None and boundingRegion is None):
			valFlag = False
			errorMsg = "Error:  Please input nodes, arcs, and/or boundingRegion.  No object can be created without at least one of these."
	'''
	
	if (valFlag):
		try:
			mapBackground = mapBackground.lower()
		except:
			pass

		if (mapBackground not in mapBackgroundList):
			valFlag = False
			errorMsg = "Error: Invalid `mapBackground` value. Valid options include 'CartoDB positron', 'CartoDB dark_matter', 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'arcGIS Aerial', 'arcGIS Gray', 'arcGIS Ocean', 'arcGIS Roadmap', 'arcGIS Shaded Relief', 'arcGIS Topo', 'Open Topo'"

	if (valFlag and nodes is not None):
		if (valFlag):
			[valFlag, errorMsg, newWarningMsg] = valNodes(nodes)
			warningMsg += newWarningMsg

		if (valFlag and (leafletIconPrefix is not None or leafletIconType is not None or leafletIconColor is not None or leafletIconText is not None)):
			[valFlag, errorMsg, newWarningMsg] = _valLeafletNodeInputs(leafletIconPrefix, leafletIconType, leafletIconColor)
			warningMsg += newWarningMsg

	if (valFlag and arcs is not None):
		if (valFlag):
			[valFlag, errorMsg, newWarningMsg] = valArcs(arcs)
			warningMsg += newWarningMsg

		if (valFlag and (leafletArcWeight is not None or leafletArcStyle is not None or leafletArcColor is not None or leafletArcOpacity is not None or useArrows is not None)):
			[valFlag, errorMsg, newWarningMsg] = _valLeafletArcInputs(leafletArcColor, leafletArcWeight, leafletArcStyle, leafletArcOpacity, useArrows, arcCurveType, arcCurvature)
			warningMsg += newWarningMsg

	# print("FIXMELP -- DONE?  Need to validate `arcCurveType` and `arcCurvature`.")
	# print("FIXMELP -- DONE?  Need to validate `arrowsPerArc`.")
	
	if (valFlag and useArrows):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(arrowsPerArc, 'arrowsPerArc')
		warningMsg += newWarningMsg
		
	if (valFlag and boundingRegion is not None):
		if (valFlag):
			[valFlag, errorMsg, newWarningMsg] = _valBoundingRegion(boundingRegion)
			warningMsg += newWarningMsg

		if (valFlag and (leafletBoundingWeight is not None or leafletBoundingStyle is not None or leafletBoundingColor is not None or leafletBoundingOpacity is not None)):
			[valFlag, errorMsg, newWarningMsg] = _valLeafletBoundingInputs(leafletBoundingColor, leafletBoundingWeight, leafletBoundingStyle, leafletBoundingOpacity)
			warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valAddLeafletCircle(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, center, radius, text, fontSize, fontColor, lineWeight, lineColor, lineOpacity, lineStyle, fillColor, fillOpacity):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valMapBoundary(mapBoundary, zoomStart)
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			mapBackground = mapBackground.lower()
		except:
			pass

		if (mapBackground not in mapBackgroundList):
			valFlag = False
			errorMsg = "Error: Invalid `mapBackground` value. Valid options include 'CartoDB positron', 'CartoDB dark_matter', 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'arcGIS Aerial', 'arcGIS Gray', 'arcGIS Ocean', 'arcGIS Roadmap', 'arcGIS Shaded Relief', 'arcGIS Topo', 'Open Topo'"

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(center)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(radius, 'radius')
		warningMsg += newWarningMsg

	if (text is not None):
		if (valFlag):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(fontSize, 'fontSize')
			warningMsg += newWarningMsg

		if (valFlag):
			try:
				fontColor = fontColor.lower()
			except:
				pass

			if (fontColor not in leafletColorList):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(fontColor)
				warningMsg += newWarningMsg
	
	if (valFlag and lineWeight is not None):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(lineWeight, 'lineWeight')
		warningMsg += newWarningMsg

	if (valFlag and lineColor is not None):
		try:
			lineColor = lineColor.lower()
		except:
			pass
			
		if (lineColor not in leafletColorList):
			[valFlag, errorMsg, newWarningMsg] = _valHexColor(lineColor)
			warningMsg += newWarningMsg

	if (valFlag and lineOpacity is not None):
		[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 1, lineOpacity, 'lineOpacity')
		warningMsg += newWarningMsg

	if (valFlag and lineStyle is not None):
		try:
			lineStyle = lineStyle.lower()
		except:
			pass
			
		if (lineStyle not in leafletStyleList):
			valFlag = False
			errorMsg = "Error: Invalid `lineStyle` value. Valid options are 'solid', 'dotted', and 'dashed'."

	if (valFlag and fillColor is not None):
		try:
			fillColor = fillColor.lower()
		except:
			pass
			
		if (fillColor not in leafletColorList):
			[valFlag, errorMsg, newWarningMsg] = _valHexColor(fillColor)
			warningMsg += newWarningMsg

	if (valFlag and fillOpacity is not None):
		[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 1, fillOpacity, 'fillOpacity')
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valAddLeafletIcon(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, location, iconPrefix, iconType, iconColor, popupText):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valMapBoundary(mapBoundary, zoomStart)
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			mapBackground = mapBackground.lower()
		except:
			pass

		if (mapBackground not in mapBackgroundList):
			valFlag = False
			errorMsg = "Error: Invalid `mapBackground` value. Valid options include 'CartoDB positron', 'CartoDB dark_matter', 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'arcGIS Aerial', 'arcGIS Gray', 'arcGIS Ocean', 'arcGIS Roadmap', 'arcGIS Shaded Relief', 'arcGIS Topo', 'Open Topo'"

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(location)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] =_valLeafletNodeInputs(iconPrefix, iconType, iconColor) 
		warningMsg += newWarningMsg
		
	if (valFlag):
		if (iconColor is None):
			valFlag = False
			errorMsg = "Error: A valid `iconColor` is required."

	return [valFlag, errorMsg, warningMsg]
	
def valAddLeafletIsochrones(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, iso, showBoundingRegion, iconPrefix, iconType, iconColor, popupText, lineWeight, lineOpacity, lineStyle, fillOpacity):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valMapBoundary(mapBoundary, zoomStart)
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			mapBackground = mapBackground.lower()
		except:
			pass

		if (mapBackground not in mapBackgroundList):
			valFlag = False
			errorMsg = "Error: Invalid `mapBackground` value. Valid options include 'CartoDB positron', 'CartoDB dark_matter', 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'arcGIS Aerial', 'arcGIS Gray', 'arcGIS Ocean', 'arcGIS Roadmap', 'arcGIS Shaded Relief', 'arcGIS Topo', 'Open Topo'"

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valIso(iso)
		warningMsg += newWarningMsg

	if (valFlag):
		if (type(showBoundingRegion) is not bool):
			valFlag = False
			errorMsg = "Error: `showBoundingRegion` must be a boolean value (True or False)."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] =_valLeafletNodeInputs(iconPrefix, iconType, iconColor) 
		warningMsg += newWarningMsg
		
	if (valFlag):
		if (iconColor is None):
			valFlag = False
			errorMsg = "Error: A valid `iconColor` is required."

	if (valFlag):
		[valFlag, warningMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(lineWeight, "lineWeight")
		warningMsg += newWarningMsg
		
	if (valFlag):
		if (lineStyle is None):
			valFlag = False
			errorMsg = "Error: A valid `lineStyle` is required."
		elif (lineStyle.lower() not in leafletStyleList):
			valFlag = False
			errorMsg = "Error: Choose `lineStyle` from 'solid', 'dashed', and 'dotted'."

	if (valFlag):
		if (lineOpacity is None):
			valFlag = False
			errorMsg = "Error: A valid `lineOpacity` is required."		
		else:
			[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 1, lineOpacity, 'lineOpacity')
			warningMsg += newWarningMsg

	if (valFlag):
		if (fillOpacity is None):
			valFlag = False
			errorMsg = "Error: A valid `fillOpacity` is required."		
		else:
			[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 1, fillOpacity, 'fillOpacity')
			warningMsg += newWarningMsg
	
	return [valFlag, errorMsg, warningMsg]


	
def valAddLeafletMarker(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, center, radius, text, fontSize, fontColor, lineWeight, lineColor, lineOpacity, lineStyle, fillColor, fillOpacity):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valMapBoundary(mapBoundary, zoomStart)
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			mapBackground = mapBackground.lower()
		except:
			pass

		if (mapBackground not in mapBackgroundList):
			valFlag = False
			errorMsg = "Error: Invalid `mapBackground` value. Valid options include 'CartoDB positron', 'CartoDB dark_matter', 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'arcGIS Aerial', 'arcGIS Gray', 'arcGIS Ocean', 'arcGIS Roadmap', 'arcGIS Shaded Relief', 'arcGIS Topo', 'Open Topo'"

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(center)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(radius, 'radius')
		warningMsg += newWarningMsg

	if (text is not None):
		if (valFlag):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(fontSize, 'fontSize')
			warningMsg += newWarningMsg

		if (valFlag):
			try:
				fontColor = fontColor.lower()
			except:
				pass

			if (fontColor not in leafletColorList):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(fontColor)
				warningMsg += newWarningMsg

	if (valFlag and lineWeight is not None):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(lineWeight, 'lineWeight')
		warningMsg += newWarningMsg

	if (valFlag and lineColor is not None):
		try:
			lineColor = lineColor.lower()
		except:
			pass
			
		if (lineColor not in leafletColorList):
			[valFlag, errorMsg, newWarningMsg] = _valHexColor(lineColor)
			warningMsg += newWarningMsg

	if (valFlag and lineOpacity is not None):
		[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 1, lineOpacity, 'lineOpacity')
		warningMsg += newWarningMsg

	if (valFlag and lineStyle is not None):
		try:
			lineStyle = lineStyle.lower()
		except:
			pass

		if (lineStyle not in leafletStyleList):
			valFlag = False
			errorMsg = "Error: Invalid `lineStyle` value. Valid options are 'solid', 'dotted', and 'dashed'."

	if (valFlag and fillColor is not None):
		try:
			fillColor = fillColor.lower()
		except:
			pass

		if (fillColor not in leafletColorList):
			[valFlag, errorMsg, newWarningMsg] = _valHexColor(fillColor)
			warningMsg += newWarningMsg

	if (valFlag and fillOpacity is not None):
		[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 1, fillOpacity, 'fillOpacity')
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valAddLeafletPolygon(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, points, lineWeight, lineColor, lineOpacity, lineStyle, fillColor, fillOpacity):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valMapBoundary(mapBoundary, zoomStart)
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			mapBackground = mapBackground.lower()
		except:
			pass

		if (mapBackground not in mapBackgroundList):
			valFlag = False
			errorMsg = "Error: Invalid `mapBackground` value. Valid options include 'CartoDB positron', 'CartoDB dark_matter', 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'arcGIS Aerial', 'arcGIS Gray', 'arcGIS Ocean', 'arcGIS Roadmap', 'arcGIS Shaded Relief', 'arcGIS Topo', 'Open Topo'"

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(points)
		warningMsg += newWarningMsg

	if (valFlag and lineWeight is not None):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(lineWeight, 'lineWeight')
		warningMsg += newWarningMsg

	if (valFlag and lineColor is not None):
		try:
			lineColor = lineColor.lower()
		except:
			pass

		if (lineColor not in leafletColorList):
			[valFlag, errorMsg, newWarningMsg] = _valHexColor(lineColor)
			warningMsg += newWarningMsg

	if (valFlag and lineOpacity is not None):
		[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 1, lineOpacity, 'lineOpacity')
		warningMsg += newWarningMsg

	if (valFlag and lineStyle is not None):
		try:
			lineStyle = lineStyle.lower()
		except:
			pass

		if (lineStyle not in leafletStyleList):
			valFlag = False
			errorMsg = "Error: Invalid `lineStyle` value. Valid options are 'solid', 'dotted', and 'dashed'."

	if (valFlag and fillColor is not None):
		try:
			fillColor = fillColor.lower()
		except:
			pass

		if (fillColor not in leafletColorList):
			[valFlag, errorMsg, newWarningMsg] = _valHexColor(fillColor)
			warningMsg += newWarningMsg

	if (valFlag and fillOpacity is not None):
		[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 1, fillOpacity, 'fillOpacity')
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valAddLeafletPolyline(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, points, lineWeight, lineColor, lineOpacity, lineStyle, lineCurveType, lineCurvature, useArrows, arrowsPerArc):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valMapBoundary(mapBoundary, zoomStart)
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			mapBackground = mapBackground.lower()
		except:
			pass

		if (mapBackground not in mapBackgroundList):
			valFlag = False
			errorMsg = "Error: Invalid `mapBackground` value. Valid options include 'CartoDB positron', 'CartoDB dark_matter', 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'arcGIS Aerial', 'arcGIS Gray', 'arcGIS Ocean', 'arcGIS Roadmap', 'arcGIS Shaded Relief', 'arcGIS Topo', 'Open Topo'"

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(points)
		warningMsg += newWarningMsg


	if (valFlag and lineWeight is not None):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(lineWeight, 'lineWeight')
		warningMsg += newWarningMsg

	if (valFlag and lineColor is not None):
		try:
			lineColor = lineColor.lower()
		except:
			pass

		if (lineColor not in leafletColorList):
			[valFlag, errorMsg, newWarningMsg] = _valHexColor(lineColor)
			warningMsg += newWarningMsg

	if (valFlag and lineOpacity is not None):
		[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 1, lineOpacity, 'lineOpacity')
		warningMsg += newWarningMsg

	if (valFlag and lineStyle is not None):
		try:
			lineStyle = lineStyle.lower()
		except:
			pass

		if (lineStyle not in leafletStyleList):
			valFlag = False
			errorMsg = "Error: Invalid `lineStyle` value. Valid options are 'solid', 'dotted', and 'dashed'."

	return [valFlag, errorMsg, warningMsg]

def valAddLeafletText(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, anchorPoint, text, fontSize, fontColor, horizAlign):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valMapBoundary(mapBoundary, zoomStart)
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			mapBackground = mapBackground.lower()
		except:
			pass

		if (mapBackground not in mapBackgroundList):
			valFlag = False
			errorMsg = "Error: Invalid `mapBackground` value. Valid options include 'CartoDB positron', 'CartoDB dark_matter', 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'arcGIS Aerial', 'arcGIS Gray', 'arcGIS Ocean', 'arcGIS Roadmap', 'arcGIS Shaded Relief', 'arcGIS Topo', 'Open Topo'"

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(anchorPoint)
		warningMsg += newWarningMsg

	if (valFlag and fontSize is not None):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(fontSize, 'fontSize')
		warningMsg += newWarningMsg

	if (valFlag and fontColor is not None):
		try:
			fontColor = fontColor.lower()
		except:
			pass

		if (fontColor not in leafletColorList):
			[valFlag, errorMsg, newWarningMsg] = _valHexColor(fontColor)
			warningMsg += newWarningMsg

	if (valFlag and horizAlign is not None):
		try:
			horizAlign = horizAlign.lower()
		except:
			pass

		if (horizAlign not in horizAlignList):
			valFlag = False
			errorMsg = "Error: Invalid `horizAlign` value.  Valid options are 'left', 'right', and 'center'."

	return [valFlag, errorMsg, warningMsg]


def valAddLeafletWeather(mapObject, mapType, APIkey, mapFilename, mapBackground):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (mapObject is not None):
		if (type(mapObject) is not folium.folium.Map):
			valFlag = False
			errorMsg = "Error: Invalid `mapObject`."
			
	if (valFlag):
		try:
			mapType = mapType.lower()
		except:
			pass
			
		if (mapType not in weatherMapList):
			valFlag = False
			errorMsg = "Error: Invalid `mapType` value.  Valid options include 'clouds', 'precip', 'pressure', 'wind', and 'temp'."	
			
	if (valFlag):
		if (mapFilename is not None):
			if (type(mapFilename) is not str):
				valFlag = False
				errorMsg = "Error: filename should be a string."

	if (valFlag):
		try:
			mapBackground = mapBackground.lower()
		except:
			pass

		if (mapBackground not in mapBackgroundList):
			valFlag = False
			errorMsg = "Error: Invalid `mapBackground` value. Valid options include 'CartoDB positron', 'CartoDB dark_matter', 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'arcGIS Aerial', 'arcGIS Gray', 'arcGIS Ocean', 'arcGIS Roadmap', 'arcGIS Shaded Relief', 'arcGIS Topo', 'Open Topo'"

	return [valFlag, errorMsg, warningMsg]


def valCreateCesium(assignments, nodes, startDate, startTime, postBuffer, cesiumDir, problemDir, cesiumIconColor, cesiumPathColor, cesiumPathWeight, cesiumPathStyle, cesiumPathOpacity):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag and assignments is not None):
		[valFlag, errorMsg, newWarningMsg] = valAssignments(assignments)
		warningMsg += newWarningMsg

	if (valFlag and nodes is not None):
		[valFlag, errorMsg, newWarningMsg] = valNodes(nodes)
		warningMsg += newWarningMsg

	if (assignments is None and nodes is None):
		valFlag = False
		errorMsg = "Error: `assignments` and `nodes` cannot be None at the same time."

	if (valFlag and startDate is not None):
		[valFlag, errorMsg, newWarningMsg] = _valDate(startDate)
		warningMsg += newWarningMsg

	if (valFlag and startTime is not None):
		[valFlag, errorMsg, newWarningMsg] = _valTime(startTime)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(postBuffer, 'postBuffer')
		warningMsg += newWarningMsg

	if (valFlag):
		if (cesiumDir == None):
			valFlag = False
			errorMsg = "Error: `cesiumDir` is required for `createCesium()`. Please provide the full absolute directory for cesium, e.g., `cesiumDir = '/home/user/cesium'` for Linux or `cesiumDir = 'D:/cesium'` for Windows.  Note that shortcuts to home directories, such as in `cesiumDir = '~/cesium'`, are not allowed."
		else:
			cesiumServerJsDir  = addTailSlash(cesiumDir) + 'server.js'
			cesiumServerCjsDir = addTailSlash(cesiumDir) + 'server.cjs'
			if ((not os.path.exists(cesiumServerJsDir)) and (not os.path.exists(cesiumServerCjsDir))):
				valFlag = False
				errorMsg = "Error: Cannot find Cesium application in '%s'. Please provide the full absolute path for cesium, and input as `cesiumDir = CESIUMDIRECTORY`, e.g., `cesiumDir = '/home/user/cesium'` for Linux or `cesiumDir = 'D:/cesium'` for Windows.  Note that shortcuts to home directories, such as in `cesiumDir = '~/cesium'`, are not allowed." % (cesiumDir)

	if (valFlag):
		if (problemDir == None):
			valFlag = False
			errorMsg = "Error: `problemDir` is required for `createCesium()`. Please provide a relative path to the root directory of cesium, e.g., `problemDir = 'veroviz/problems/TSP'`."

	if (valFlag and assignments is not None):
		modelFiles = list(dict.fromkeys(assignments['modelFile'].tolist()))
		for i in range(len(modelFiles)):
			if (not os.path.isfile(cesiumDir + modelFiles[i])):
				valFlag = False
				errorMsg = "Error: modelFile %s cannot be found within the %s directory. Please edit the 'modelFile' column of the assignments dataframe to include the proper path and filename." % (modelFiles[i], cesiumDir + modelFiles[i])

	if (valFlag == True):
		if (cesiumIconColor != None):
			if (expandCesiumColor(cesiumIconColor) not in cesiumColorList):
				warningMsg += "Warning: cesiumColor is not recognized; it may not be displayed properly.\n"

	if (valFlag):
		if ((cesiumPathColor != None) or (cesiumPathWeight != None) or (cesiumPathStyle != None) or (cesiumPathOpacity != None)):
			[valFlag, errorMsg, newWarningMsg] = _valCesiumArcInputs(cesiumPathColor, cesiumPathWeight, cesiumPathStyle, cesiumPathOpacity)
			warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valGetSnapLoc(loc, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valDatabase([loc], dataProvider, dataProviderArgs)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valGetSnapLocBatch(locs, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(locs)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valDatabase(locs, dataProvider, dataProviderArgs)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valCalcPerimeter2D(path, closeLoop, distUnits):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(path)
		warningMsg += newWarningMsg

	if (valFlag):
		if (type(closeLoop) is not bool):
			valFlag = False
			errorMsg = "Error: `closeLoop` must be boolean (True or False)."

	if (valFlag):
		try:
			distUnits = distUnits.lower()
		except:
			pass

		[valFlag, errorMsg, newWarningMsg] = _valDistanceUnits(distUnits, "distUnits")
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valCalcArea(poly):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (poly is None):
		valFlag = False
		errorMsg = "Error: Function `calcArea()` requires a polygon as an input."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(poly)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]


def valLengthFromNodeSeq(nodeSeq, lengthDict):

	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (nodeSeq == None):
		valFlag = False
		errorMsg = "Error: `nodeSeq` is required.  Please enter the sequence of locations in the format of [nodeID1, nodeID2, ...]."

	if (valFlag):
		if (lengthDict == None):
			valFlag = False
			errorMsg = "Error: `lengthDict` is required.  Please provide either a distance or time matrix, in the form of a dictionary."

	if (valFlag):
		if (type(nodeSeq) is not list):
			valFlag = False
			errorMsg = "Error: `nodeSeq` must be a sequence of locations in the format of [nodeID1, nodeID2, ...]."

	if (valFlag):
		if (len(nodeSeq) <= 1):
			valFlag = False
			errorMsg = "Error: `nodeSeq` must be a sequence of locations, in the format of [nodeID1, nodeID2, ...], with at least 2 nodes."

	if (valFlag):
		if (type(lengthDict) is not dict):
			valFlag = False
			errorMsg = "Error: `lengthDict` must be a distance or time matrix, in the form of a dictionary."

	if (valFlag):
		for i in range(0, len(nodeSeq)-1):
			if (not valFlag):
				break
			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(nodeSeq[i], 'nodeSeq')
			if (valFlag):
				if ((nodeSeq[i], nodeSeq[i+1]) not in lengthDict):
					valFlag = False
					errorMsg = "Error: (%d, %d) is not a key in the `lengthDict` dictionary." % (nodeSeq[i], nodeSeq[i+1])

	return [valFlag, errorMsg, warningMsg]

def valConvertSpeed(speed, fromUnitsDist, fromUnitsTime, toUnitsDist, toUnitsTime):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	
	if ((speed is None) or (fromUnitsDist is None) or (fromUnitsTime is None) or (toUnitsDist is None) or (toUnitsTime is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 5 required input parameters to function `convertSpeed()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(speed, 'speed')
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			fromUnitsDist = fromUnitsDist.lower()
		except:
			pass
	
		[valFlag, errorMsg, newWarningMsg] = _valDistanceUnits(fromUnitsDist, "input")
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			toUnitsDist = toUnitsDist.lower()
		except:
			pass
			
		[valFlag, errorMsg, newWarningMsg] = _valDistanceUnits(toUnitsDist, "output")
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			fromUnitsTime = fromUnitsTime.lower()
		except:
			pass

		[valFlag, errorMsg, newWarningMsg] = _valTimeUnits(fromUnitsTime, "input")
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			toUnitsTime = toUnitsTime.lower()
		except:
			pass

		[valFlag, errorMsg, newWarningMsg] = _valTimeUnits(toUnitsTime, "output")
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valConvertDistance(distance, fromUnitsDist, toUnitsDist):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((distance is None) or (fromUnitsDist is None) or (toUnitsDist is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 3 required input parameters to function `convertDistance()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(distance, 'distance')
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			fromUnitsDist = fromUnitsDist.lower()
		except:
			pass
	
		[valFlag, errorMsg, newWarningMsg] = _valDistanceUnits(fromUnitsDist, "input")
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			toUnitsDist = toUnitsDist.lower()
		except:
			pass

		[valFlag, errorMsg, newWarningMsg] = _valDistanceUnits(toUnitsDist, "output")
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valConvertArea(area, fromUnits, toUnits):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((area is None) or (fromUnits is None) or (toUnits is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 3 required input parameters to function `convertArea()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(area, 'area')
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			fromUnits = fromUnits.lower()
		except:
			pass

		[valFlag, errorMsg, newWarningMsg] = _valAreaUnits(fromUnits, "input")
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			toUnits = toUnits.lower()
		except:
			pass

		[valFlag, errorMsg, newWarningMsg] = _valAreaUnits(toUnits, "output")
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valConvertTime(time, fromUnitsTime, toUnitsTime):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((time is None) or (fromUnitsTime is None) or (toUnitsTime is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 3 required input parameters to function `convertTime()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(time, 'time')
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			fromUnitsTime = fromUnitsTime.lower()
		except:
			pass

		[valFlag, errorMsg, newWarningMsg] = _valTimeUnits(fromUnitsTime, "input")
		warningMsg += newWarningMsg

	if (valFlag):
		try:
			toUnitsTime = toUnitsTime.lower()
		except:
			pass

		[valFlag, errorMsg, newWarningMsg] = _valTimeUnits(toUnitsTime, "output")
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valExportDataframe(filename, dataframe):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (type(filename) is not str):
		valFlag = False
		errorMsg = "Error: filename should be a string."

	elif (type(dataframe) is not pd.core.frame.DataFrame):
		valFlag = False
		errorMsg = "Error: dataframe should be a pandas dataframe."

	return [valFlag, errorMsg, warningMsg]

def valImportDataframe(filename, intCols, useIndex):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (type(filename) is not str):
		valFlag = False
		errorMsg = "Error: filename should be a string."

	return [valFlag, errorMsg, warningMsg]

def valInitDataframe(dataframe):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		dataframe = dataframe.lower()
	except:
		pass

	if (dataframe not in dataframeList):
		valFlag = False
		errorMsg = "Error: No dataframe could be created. The initDataframe function accepts 'nodes', 'arcs', or 'assignments' as inputs."

	return [valFlag, errorMsg, warningMsg]

def valCreateArcsFromLocSeq(locSeq, initArcs, startArc, objectID, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (locSeq == None):
		valFlag = False
		errorMsg = "Error: `locSeq` is required.  Please enter the sequence of locations in the format of [[lat, lon], [lat, lon], ...]."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(locSeq)
		warningMsg += newWarningMsg

	if (valFlag and initArcs is not None):
		[valFlag, errorMsg, newWarningMsg] = valArcs(initArcs)
		warningMsg += newWarningMsg

	if (valFlag):
		if (startArc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(startArc, "startArc")
			warningMsg += newWarningMsg

		if (valFlag and initArcs is not None):
			if (len(initArcs) > 0):
				maxID = max(initArcs['odID'])
				if (maxID >= startArc):
					# 2019-11-07 -- removed warning message
					# warningMsg += "Warning: 'odID' in `initArcs` is already larger than `startArc`.  Overriding `startArc` with maximum `odID` + 1.\n"
					pass

	if (valFlag):
		if ((leafletColor != None) or (leafletWeight != None) or (leafletStyle != None) or (leafletOpacity != None)):
			try:
				leafletColor = leafletColor.lower()
			except:
				pass
				
			try:
				leafletStyle = leafletStyle.lower()
			except:
				pass

			[valFlag, errorMsg, newWarningMsg] = _valLeafletArcInputs(leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, leafletCurveType, leafletCurvature)
			warningMsg += newWarningMsg

	# print("FIXMELP -- DONE? Need to validate `leafletCurveType` and `leafletCurvature`.")

	if (valFlag):
		if ((cesiumColor != None) or (cesiumWeight != None) or (cesiumStyle != None) or (cesiumOpacity != None)):
			try:
				cesiumStyle = cesiumStyle.lower()
			except:
				pass

			[valFlag, errorMsg, newWarningMsg] = _valCesiumArcInputs(cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)
			warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valCreateArcsFromNodeSeq(nodeSeq, nodes, initArcs, startArc, objectID, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (nodeSeq == None):
		valFlag = False
		errorMsg = "Error: `nodeSeq` is required.  Please enter the sequence of locations in the format of [nodeID1, nodeID2, ...]."

	if (valFlag):
		if (nodes is None):
			valFlag = False
			errorMsg = "Error: A `nodes` dataframe is required."
			
	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = valNodes(nodes)
		warningMsg += newWarningMsg

	if (valFlag):
		for i in range(len(nodeSeq)):
			if (not valFlag):
				break
			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(nodeSeq[i], 'nodeSeq')
			if (valFlag):
				if (nodeSeq[i] not in nodes['id'].tolist()):
					valFlag = False
					errorMsg = "Error: 'nodes' dataframe does not contain a node with `id = %s`." % (nodeSeq[i])

	if (valFlag and initArcs is not None):
		[valFlag, errorMsg, newWarningMsg] = valArcs(initArcs)
		warningMsg += newWarningMsg

	if (valFlag):
		if (startArc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(startArc, "startArc")
			warningMsg += newWarningMsg

		if (valFlag and initArcs is not None):
			if (len(initArcs) > 0):
				maxID = max(initArcs['odID'])
				if (maxID >= startArc):
					# 2019-11-07 -- removed warning message
					# warningMsg += "Warning: 'odID' in `initArcs` is already larger than `startArc`.  Overriding `startArc` with maximum `odID` + 1.\n"
					pass

	if (valFlag):
		if ((leafletColor != None) or (leafletWeight != None) or (leafletStyle != None) or (leafletOpacity != None)):
			try:
				leafletColor = leafletColor.lower()
			except:
				pass
				
			try:
				leafletStyle = leafletStyle.lower()
			except:
				pass

			[valFlag, errorMsg, newWarningMsg] = _valLeafletArcInputs(leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, leafletCurveType, leafletCurvature)
			warningMsg += newWarningMsg

	# print("FIXMELP -- DONE?  Need to validate `leafletCurveType` and `leafletCurvature`.")

	if (valFlag):
		if ((cesiumColor != None) or (cesiumWeight != None) or (cesiumStyle != None) or (cesiumOpacity != None)):
			try:
				cesiumStyle = cesiumStyle.lower()
			except:
				pass

			[valFlag, errorMsg, newWarningMsg] = _valCesiumArcInputs(cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)
			warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valCreateNodesFromLocs(locs, initNodes, nodeType, nodeName, startNode, incrementName, incrementStart, snapToRoad, dataProvider, dataProviderArgs, popupText, leafletIconPrefix, leafletIconType, leafletColor, leafletIconText, cesiumIconType, cesiumColor, cesiumIconText):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (locs == None):
		valFlag = False
		errorMsg = "Error: `locs` is required.  Please enter the sequence of location in the format of [[lat, lon], [lat, lon], ...]."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(locs)
		warningMsg += newWarningMsg

	if (valFlag and initNodes is not None):
		[valFlag, errorMsg, newWarningMsg] = valNodes(initNodes)
		warningMsg += newWarningMsg

	if (valFlag):
		if (startNode is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(startNode, "startNode")
			warningMsg += newWarningMsg

		if (valFlag and initNodes is not None):
			if (len(initNodes) > 0):
				maxID = max(initNodes['id'])
				if (maxID >= startNode):
					warningMsg += "Warning: 'id' in `initNodes` is already larger than `startNode`.  Overriding `startNode` with maximum `id` + 1.\n"

	if (valFlag):
		if (nodeName is None):
			if (incrementName == True):
				valFlag = False
				errorMsg = "Error: `incrementName` cannot be `True` if `nodeName` is not provided. There is no name on which to increment."

	if (valFlag and snapToRoad):
		if (dataProvider == None):
			valFlag = False
			errorMsg = "Error: A `dataProvider` is required if `snapToRoad = True`. Valid `dataProvider` options are 'pgRouting', 'MapQuest', 'ORS-online',  'OSRM-online', and 'ORS-local'."
		else:
			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valDatabase(locs, dataProvider, dataProviderArgs)
				warningMsg += newWarningMsg

	if (valFlag):
		if ((leafletIconPrefix != None) or (leafletIconType != None) or (leafletColor != None)):
			try:
				leafletIconPrefix = leafletIconPrefix.lower()
			except:
				pass
				
			try:
				leafletIconType = leafletIconType.lower()
			except:
				pass
				
			try:
				leafletColor = leafletColor.lower()
			except:
				pass
				
			[valFlag, errorMsg, newWarningMsg] = _valLeafletNodeInputs(leafletIconPrefix, leafletIconType, leafletColor)
			warningMsg += newWarningMsg

	if (valFlag):
		if ((cesiumIconType != None) or (cesiumIconText != None) or (cesiumColor != None)):
			[valFlag, errorMsg, newWarningMsg] = _valCesiumNodeInputs(cesiumIconType, cesiumColor)
			warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]


def valCreateAssignmentsFromArcs2D(initAssignments, arcs, serviceTimeSec, modelScale, modelMinPxSize, expDurationArgs, modelFile, startTimeSec, routeType, speedMPS, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor, ganttColorService, dataProvider, dataProviderArgs):

	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		routeType = routeType.lower()
	except:
		pass

	if (initAssignments is not None):
		[valFlag, errorMsg, newWarningMsg] = valAssignments(initAssignments)
		warningMsg += newWarningMsg

	if (valFlag):
		if (arcs is None):
			valFlag = False
			errorMsg = "Error: The 'arcs' dataframe is required."
			
	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = valArcs(arcs)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(modelScale, 'modelScale')
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(modelMinPxSize, 'modelMinPxSize')
		warningMsg += newWarningMsg

	dummyExpDurationSec = None
	
	if (valFlag):
		if (expDurationArgs is not None):
			if ('getTravelTimes' in expDurationArgs):
				if (type(expDurationArgs['getTravelTimes']) is not bool):
					valFlag = False
					errorMsg = "Error: `expDurationArgs['getTravelTimes']` must have a boolean (True or False) value." 
				else:
					if (expDurationArgs['getTravelTimes']):
						dummyExpDurationSec = 1.23		# dummy positive value
					else:
						dummyExpDurationSec = None		# won't use exp duration
			else:
				valFlag = False
				errorMsg = "Error: Invalid `expDurationArgs` value provided.  See the documentation for allowable options."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(serviceTimeSec, 'serviceTimeSec')
		warningMsg += newWarningMsg


	if (valFlag):
		if (modelFile == None):
			warningMsg += "Warning: `modelFile` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(startTimeSec, 'startTimeSec')
		warningMsg += newWarningMsg

	if (valFlag):
		for i in arcs.index:
			if (not valFlag):
				break

			startLoc = [arcs['startLat'].at[i], arcs['startLon'].at[i]]
			endLoc   = [arcs['endLat'].at[i], arcs['endLon'].at[i]]
	
			if (startLoc != endLoc):
				[valFlag, errorMsg, newWarningMsg] = _valRouteType2DForShapepoints(routeType, speedMPS, dummyExpDurationSec, dataProvider)
				warningMsg += newWarningMsg

			if (valFlag and routeType not in ['euclidean2d', 'manhattan']):
				if (startLoc != endLoc):
					locs = [startLoc, endLoc]
					[valFlag, errorMsg, newWarningMsg] = _valDatabase(locs, dataProvider, dataProviderArgs)
					warningMsg += newWarningMsg

	if (valFlag):
		if ((leafletColor != None) or (leafletWeight != None) or (leafletStyle != None) or (leafletOpacity != None)):
			try:
				leafletColor = leafletColor.lower()
			except:
				pass
				
			try:
				leafletStyle = leafletStyle.lower()
			except:
				pass
				
			[valFlag, errorMsg, newWarningMsg] = _valLeafletArcInputs(leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, leafletCurveType, leafletCurvature)
			warningMsg += newWarningMsg

	# print("FIXMELP -- DONE?  Need to validate `leafletCurveType` and `leafletCurvature`.")

	if (valFlag):
		if ((cesiumColor != None) or (cesiumWeight != None) or (cesiumStyle != None) or (cesiumOpacity != None)):
			try:
				cesiumStyle = cesiumStyle.lower()
			except:
				pass
				
			[valFlag, errorMsg, newWarningMsg] = _valCesiumArcInputs(cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)
			warningMsg += newWarningMsg

	if (valFlag):
		if (ganttColor is not None):
			if (ganttColor.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(ganttColor)
				warningMsg += newWarningMsg

	if (valFlag):
		if (ganttColorService is not None):
			if (ganttColorService.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(ganttColorService)
				warningMsg += newWarningMsg
			
	return [valFlag, errorMsg, warningMsg]	


def valCreateAssignmentsFromNodeSeq2D(initAssignments, nodeSeq, nodes, serviceTimeSec, modelScale, modelMinPxSize, expDurationArgs, odID, objectID, modelFile, startTimeSec, routeType, speedMPS, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor, ganttColorService, dataProvider, dataProviderArgs):

	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		routeType = routeType.lower()
	except:
		pass

	if (initAssignments is not None):
		[valFlag, errorMsg, newWarningMsg] = valAssignments(initAssignments)
		warningMsg += newWarningMsg

	if (nodeSeq == None):
		valFlag = False
		errorMsg = "Error: `nodeSeq` is required.  Please enter the sequence of locations in the format of [nodeID1, nodeID2, ...]."

	if (valFlag):
		if (nodes is None):
			valFlag = False
			errorMsg = "Error: `nodes` dataframe is required."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = valNodes(nodes)
		warningMsg += newWarningMsg

	if (valFlag):
		for i in range(len(nodeSeq)):
			if (not valFlag):
				break
			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(nodeSeq[i], 'nodeSeq')
			if (valFlag):
				if (nodeSeq[i] not in nodes['id'].tolist()):
					valFlag = False
					errorMsg = "Error: 'nodes' dataframe does not contain a node with `id = %s`." % (nodeSeq[i])

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(modelScale, 'modelScale')
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(modelMinPxSize, 'modelMinPxSize')
		warningMsg += newWarningMsg

	dummyExpDurationSec = None
	
	if (valFlag):
		if (expDurationArgs is not None):
			if ('timeSecDict' in expDurationArgs):
				dummyExpDurationSec = 1.23		# dummy positive value
				
				# make sure there are valid times here
				if (type(expDurationArgs['timeSecDict']) is not dict):
					valFlag = False
					errorMsg = "Error: `expDurationArgs['timeSecDict']` must be a travel time dictionary, with travel times in units of seconds."
				else:
					for i in range(0, len(nodeSeq)-1):
						if (not valFlag):
							break
						if ((nodeSeq[i], nodeSeq[i+1]) not in expDurationArgs['timeSecDict']):
							valFlag = False
							errorMsg = "Error: `expDurationArgs['timeSecDict']` does not contain a travel time from node %d to node %d" % (nodeSeq[i], nodeSeq[i+1])
						else:
							[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(expDurationArgs['timeSecDict'][nodeSeq[i], nodeSeq[i+1]], "expDurationArgs['timeSecDict'][%d, %d]" % (nodeSeq[i], nodeSeq[i+1]))
								
			elif ('getTravelTimes' in expDurationArgs):
				if (type(expDurationArgs['getTravelTimes']) is not bool):
					valFlag = False
					errorMsg = "Error: `expDurationArgs['getTravelTimes']` must have a boolean (True or False) value." 
				else:
					if (expDurationArgs['getTravelTimes']):
						dummyExpDurationSec = 1.23		# dummy positive value
					else:
						dummyExpDurationSec = None		# won't use exp duration
			else:
				valFlag = False
				errorMsg = "Error: Invalid `expDurationArgs` value provided.  See the documentation for allowable options."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(serviceTimeSec, 'serviceTimeSec')
		warningMsg += newWarningMsg

	if (valFlag):
		if (odID is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(odID, 'odID')
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `odID` is required."

	if (valFlag):
		if (objectID == None):
			warningMsg += "Warning: `objectID` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		if (modelFile == None):
			warningMsg += "Warning: `modelFile` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(startTimeSec, 'startTimeSec')
		warningMsg += newWarningMsg

	if (valFlag):
		for i in range(0, len(nodeSeq)-1):
			if (not valFlag):
				break

			startLoc = [nodes.loc[nodes['id'] == nodeSeq[i]]['lat'].values[0],
						nodes.loc[nodes['id'] == nodeSeq[i]]['lon'].values[0]]
			endLoc   = [nodes.loc[nodes['id'] == nodeSeq[i+1]]['lat'].values[0],
						nodes.loc[nodes['id'] == nodeSeq[i+1]]['lon'].values[0]]
	
			if (startLoc != endLoc):
				[valFlag, errorMsg, newWarningMsg] = _valRouteType2DForShapepoints(routeType, speedMPS, dummyExpDurationSec, dataProvider)
				warningMsg += newWarningMsg

			if (valFlag and routeType not in ['euclidean2d', 'manhattan']):
				if (startLoc != endLoc):
					locs = [startLoc, endLoc]
					[valFlag, errorMsg, newWarningMsg] = _valDatabase(locs, dataProvider, dataProviderArgs)
					warningMsg += newWarningMsg

	if (valFlag):
		if ((leafletColor != None) or (leafletWeight != None) or (leafletStyle != None) or (leafletOpacity != None)):
			try:
				leafletColor = leafletColor.lower()
			except:
				pass
				
			try:
				leafletStyle = leafletStyle.lower()
			except:
				pass
				
			[valFlag, errorMsg, newWarningMsg] = _valLeafletArcInputs(leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, leafletCurveType, leafletCurvature)
			warningMsg += newWarningMsg

	# print("FIXMELP -- DONE?  Need to validate `leafletCurveType` and `leafletCurvature`.")

	if (valFlag):
		if ((cesiumColor != None) or (cesiumWeight != None) or (cesiumStyle != None) or (cesiumOpacity != None)):
			try:
				cesiumStyle = cesiumStyle.lower()
			except:
				pass
				
			[valFlag, errorMsg, newWarningMsg] = _valCesiumArcInputs(cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)
			warningMsg += newWarningMsg

	if (valFlag):
		if (ganttColor is not None):
			if (ganttColor.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(ganttColor)
				warningMsg += newWarningMsg

	if (valFlag):
		if (ganttColorService is not None):
			if (ganttColorService.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(ganttColorService)
				warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]	

def valCreateAssignmentsFromLocSeq2D(initAssignments, locSeq, serviceTimeSec, modelScale, modelMinPxSize, expDurationArgs, odID, objectID, modelFile, startTimeSec, routeType, speedMPS, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor, ganttColorService, dataProvider, dataProviderArgs):

	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		routeType = routeType.lower()
	except:
		pass

	if (initAssignments is not None):
		[valFlag, errorMsg, newWarningMsg] = valAssignments(initAssignments)
		warningMsg += newWarningMsg

	if (locSeq == None):
		valFlag = False
		errorMsg = "Error: `locSeq` is required.  Please enter the sequence of locations in the format of [[lat, lon], [lat, lon], ...] or [[lat, lon, alt], [lat, lon, alt], ...]."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(locSeq)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(modelScale, 'modelScale')
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(modelMinPxSize, 'modelMinPxSize')
		warningMsg += newWarningMsg

	dummyExpDurationSec = None
	
	if (valFlag):
		if (expDurationArgs is not None):
			if ('getTravelTimes' in expDurationArgs):
				if (type(expDurationArgs['getTravelTimes']) is not bool):
					valFlag = False
					errorMsg = "Error: `expDurationArgs['getTravelTimes']` must have a boolean (True or False) value." 
				else:
					if (expDurationArgs['getTravelTimes']):
						dummyExpDurationSec = 1.23		# dummy positive value
					else:
						dummyExpDurationSec = None		# won't use exp duration
			else:
				valFlag = False
				errorMsg = "Error: Invalid `expDurationArgs` value provided.  See the documentation for allowable options."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(serviceTimeSec, 'serviceTimeSec')
		warningMsg += newWarningMsg

	if (valFlag):
		if (odID is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(odID, 'odID')
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `odID` is required."

	if (valFlag):
		if (objectID == None):
			warningMsg += "Warning: `objectID` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		if (modelFile == None):
			warningMsg += "Warning: `modelFile` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(startTimeSec, 'startTimeSec')
		warningMsg += newWarningMsg

	if (valFlag):
		for i in range(0, len(locSeq)-1):
			if (not valFlag):
				break

			startLoc = locSeq[i]
			endLoc   = locSeq[i+1]
	
			if (valFlag and routeType not in ['euclidean2d', 'manhattan']):
				if (startLoc != endLoc):
					locs = [startLoc, endLoc]
					[valFlag, errorMsg, newWarningMsg] = _valDatabase(locs, dataProvider, dataProviderArgs)
					warningMsg += newWarningMsg

			if (valFlag and startLoc != endLoc):
				[valFlag, errorMsg, newWarningMsg] = _valRouteType2DForShapepoints(routeType, speedMPS, dummyExpDurationSec, dataProvider)
				warningMsg += newWarningMsg


	if (valFlag):
		if ((leafletColor != None) or (leafletWeight != None) or (leafletStyle != None) or (leafletOpacity != None)):
			try:
				leafletColor = leafletColor.lower()
			except:
				pass
				
			try:
				leafletStyle = leafletStyle.lower()
			except:
				pass
				
			[valFlag, errorMsg, newWarningMsg] = _valLeafletArcInputs(leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, leafletCurveType, leafletCurvature)
			warningMsg += newWarningMsg

	# print("FIXMELP -- DONE?  Need to validate `leafletCurveType` and `leafletCurvature`.")

	if (valFlag):
		if ((cesiumColor != None) or (cesiumWeight != None) or (cesiumStyle != None) or (cesiumOpacity != None)):
			try:
				cesiumStyle = cesiumStyle.lower()
			except:
				pass
				
			[valFlag, errorMsg, newWarningMsg] = _valCesiumArcInputs(cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)
			warningMsg += newWarningMsg

	if (valFlag):
		if (ganttColor is not None):
			if (ganttColor.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(ganttColor)
				warningMsg += newWarningMsg

	if (valFlag):
		if (ganttColorService is not None):
			if (ganttColorService.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(ganttColorService)
				warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]	

def valAddAssignment2D(initAssignments, odID, objectID, modelFile, startLoc, endLoc, startTimeSec, expDurationSec, routeType, speedMPS, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor, dataProvider, dataProviderArgs):

	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (initAssignments is not None):
		[valFlag, errorMsg, newWarningMsg] = valAssignments(initAssignments)
		warningMsg += newWarningMsg

	try:
		routeType = routeType.lower()
	except:
		pass

	if (valFlag):
		if (odID is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(odID, 'odID')
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `odID` is required for `addAssignment2D()`."

	if (valFlag):
		if (objectID == None):
			warningMsg += "Warning: `objectID` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		if (modelFile == None):
			warningMsg += "Warning: `modelFile` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		if (startLoc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(startLoc)
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `startLoc` is required for `addAssignment2D()`."

	if (valFlag):
		if (endLoc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(endLoc)
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `endLoc` is required for `addAssignment2D()`."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(startTimeSec, 'startTimeSec')
		warningMsg += newWarningMsg

	if (valFlag):
		if (startLoc != endLoc):
			[valFlag, errorMsg, newWarningMsg] = _valRouteType2DForShapepoints(routeType, speedMPS, expDurationSec, dataProvider)
			warningMsg += newWarningMsg

	if (valFlag and routeType not in ['euclidean2d', 'manhattan']):
		if (startLoc != endLoc):
			locs = [startLoc, endLoc]
			[valFlag, errorMsg, newWarningMsg] = _valDatabase(locs, dataProvider, dataProviderArgs)
			warningMsg += newWarningMsg

	if (valFlag):
		if ((leafletColor != None) or (leafletWeight != None) or (leafletStyle != None) or (leafletOpacity != None)):
			try:
				leafletColor = leafletColor.lower()
			except:
				pass
				
			try:
				leafletStyle = leafletStyle.lower()
			except:
				pass
				
			[valFlag, errorMsg, newWarningMsg] = _valLeafletArcInputs(leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, leafletCurveType, leafletCurvature)
			warningMsg += newWarningMsg

	# print("FIXMELP -- DONE?  Need to validate `leafletCurveType` and `leafletCurvature`.")

	if (valFlag):
		if ((cesiumColor != None) or (cesiumWeight != None) or (cesiumStyle != None) or (cesiumOpacity != None)):
			try:
				cesiumStyle = cesiumStyle.lower()
			except:
				pass
				
			[valFlag, errorMsg, newWarningMsg] = _valCesiumArcInputs(cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)
			warningMsg += newWarningMsg

	if (valFlag):
		if (ganttColor is not None):
			if (ganttColor.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(ganttColor)
				warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]
	

def valAddAssignment3D(initAssignments, odID, objectID, modelFile, startTimeSec, startLoc, endLoc, takeoffSpeedMPS, cruiseSpeedMPS, landSpeedMPS, cruiseAltMetersAGL, routeType, climbRateMPS, descentRateMPS, earliestLandTime, loiterPosition, leafletColor, leafletWeight, leafletStyle, leafletOpacity, leafletCurveType, leafletCurvature, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, ganttColor):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (initAssignments is not None):
		[valFlag, errorMsg, newWarningMsg] = valAssignments(initAssignments)
		warningMsg += newWarningMsg

	try:
		routeType = routeType.lower()
	except:
		pass

	if (valFlag):
		if (odID is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(odID, 'odID')
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `odID` is required for `addAssignment3D()`."

	if (valFlag):
		if (startLoc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(startLoc)
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `startLoc` is required for `addAssignment3D()`."

	if (valFlag):
		if (endLoc is not None):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(endLoc)
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `endLoc` is required for `addAssignment3D()`."

	if (valFlag):
		if (objectID == None):
			warningMsg += "Warning: `objectID` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		if (modelFile == None):
			warningMsg += "Warning: `modelFile` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag and startTimeSec is not None):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(startTimeSec, 'startTimeSec')
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valRouteType3D(routeType, takeoffSpeedMPS, climbRateMPS, cruiseSpeedMPS, landSpeedMPS, descentRateMPS)
		warningMsg += newWarningMsg

	if (valFlag and routeType != 'straight'):
		if (len(startLoc)==3):
			startAlt = startLoc[2]
		else:
			startAlt = 0
		if (len(endLoc)==3):
			endAlt = endLoc[2]
		else:
			endAlt = 0
		[valFlag, errorMsg, newWarningMsg] = _valAltitude(startAlt, cruiseAltMetersAGL, endAlt)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLoiterPosition(loiterPosition)
		warningMsg += newWarningMsg

	if (valFlag):
		if ((leafletColor != None) or (leafletWeight != None) or (leafletStyle != None) or (leafletOpacity != None)):
			try:
				leafletColor = leafletColor.lower()
			except:
				pass
				
			try:
				leafletStyle = leafletStyle.lower()
			except:
				pass
		
			[valFlag, errorMsg, newWarningMsg] = _valLeafletArcInputs(leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, leafletCurveType, leafletCurvature)
			warningMsg += newWarningMsg

	# print("FIXMELP -- DONE?  Need to validate `leafletCurveType` and `leafletCurvature`.")

	if (valFlag):
		if ((cesiumColor != None) or (cesiumWeight != None) or (cesiumStyle != None) or (cesiumOpacity != None)):
			[valFlag, errorMsg, newWarningMsg] = _valCesiumArcInputs(cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)
			warningMsg += newWarningMsg

	if (valFlag):
		if (ganttColor is not None):
			if (ganttColor.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(ganttColor)
				warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valAddStaticAssignment(initAssignments, odID, objectID, modelFile, modelScale, modelMinPxSize, loc, startTimeSec, endTimeSec, ganttColor):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (initAssignments is not None):
		[valFlag, errorMsg, newWarningMsg] = valAssignments(initAssignments)
		warningMsg += newWarningMsg

	if (valFlag):
		if (odID is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(odID, 'odID')
			warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error: `odID` is required for `addStaticAssignment()`."

	if (valFlag):
		if (objectID == None):
			warningMsg += "Warning: `objectID` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		if (modelFile == None):
			warningMsg += "Warning: `modelFile` is None; the Assignments dataframe can not be visualized by Cesium.\n"

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(modelScale, 'modelScale')
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroInteger(modelMinPxSize, 'modelMinPxSize')
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc)
		warningMsg += newWarningMsg

	if (valFlag):
		if (startTimeSec == None):
			valFlag = False
			errorMsg = "Error: `startTimeSec` is required for `addStaticAssignment()`."
		else:
			[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(startTimeSec, 'startTimeSec')
			warningMsg += newWarningMsg

	if (valFlag):
		if (endTimeSec == None):
			valFlag = False
			errorMsg = "Error: `endTimeSec` is required for `addStaticAssignment()`, if there is no specified ending time, input `endTimeSec = -1`."
		elif (endTimeSec != -1):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(endTimeSec, 'endTimeSec')
			warningMsg += newWarningMsg

	if (valFlag):
		if (startTimeSec > endTimeSec and endTimeSec != -1):
			valFlag = False
			errorMsg = "Error: 'startTimeSec' cannot be greater than 'endTimeSec'."

	if (valFlag):
		if (ganttColor is not None):
			if (ganttColor.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(ganttColor)
				warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valNodes(nodes):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (nodes is None):
		warningMsg += "Warning: No initial nodes provided.\n"
	elif (type(nodes) is not pd.core.frame.DataFrame):
		valFlag = False
		errorMsg = "Error: Initial nodes is not a pandas dataframe."
	else:
		for col in nodesColumnList:
			if (valFlag):
				if (not {col}.issubset(nodes.columns)):
					valFlag = False
					errorMsg = "Error: %s is missing from nodes dataframe.  To see all required columns, call 'initDataframe('nodes')'." % (col)
					break

	if (valFlag and nodes is not None):
		if (len(nodes) > 0):
			[valFlag, errorMsg, newWarningMsg] = _valLatLonList(list(map(list, zip(nodes.lat, nodes.lon))))
			warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valAssignments(assignments):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (assignments is None):
		warningMsg = "Warning: No initial assignments provided."
	elif (type(assignments) is not pd.core.frame.DataFrame):
		valFlag = False
		errorMsg = "Error: Initial assignments is not a pandas dataframe."
	else:
		for col in assignmentsColumnList:
			if (valFlag):
				if (not {col}.issubset(assignments.columns)):
					valFlag = False
					errorMsg = "Error: %s is missing from assignments dataframe.  To see all required columns, call 'initDataframe('assignments')'." % (col)
					break

	if (valFlag and assignments is not None):
		if (len(assignments) > 0):
			[valFlag, errorMsg, newWarningMsg] = _valLatLonList(list(map(list, zip(assignments.startLat, assignments.startLon))))
			warningMsg += newWarningMsg

	if (valFlag and assignments is not None):
		if (len(assignments) > 0):
			[valFlag, errorMsg, newWarningMsg] = _valLatLonList(list(map(list, zip(assignments.endLat, assignments.endLon))))
			warningMsg += newWarningMsg

	if (valFlag):
		for i in assignments.index:
			assignments.at[i, 'modelFile'] = addHeadSlash(assignments.at[i, 'modelFile'])

	return [valFlag, errorMsg, warningMsg]

def valArcs(arcs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (arcs is None):
		warningMsg = "Warning: No initial arcs provided."
	elif (type(arcs) is not pd.core.frame.DataFrame):
		valFlag = False
		errorMsg = "Error: Initial arcs is not a pandas dataframe."
	else:
		for col in arcsColumnList:
			if (valFlag):
				if (not {col}.issubset(arcs.columns)):
					valFlag = False
					errorMsg = "Error: %s is missing from arcs dataframe.  To see all required columns, call 'initDataframe('arcs')'." % (col)
					break

	if (valFlag and arcs is not None):
		if (len(arcs) > 0):
			[valFlag, errorMsg, newWarningMsg] = _valLatLonList(list(map(list, zip(arcs.startLat, arcs.startLon))))
			warningMsg += newWarningMsg

	if (valFlag and arcs is not None):
		if (len(arcs) > 0):
			[valFlag, errorMsg, newWarningMsg] = _valLatLonList(list(map(list, zip(arcs.endLat, arcs.endLon))))
			warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valGetConvexHull(locs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (locs is None):
		valFlag = False
		errorMsg = "Error: Missing required input for function `getConvexHull()`."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(locs)
		warningMsg += newWarningMsg

	if (valFlag):
		if (len(locs) < 4):
			valFlag = False
			errorMsg = "Error: Need at least 4 locations to find convex hull."

	return [valFlag, errorMsg, warningMsg]

def valIsPointInPoly(loc, poly):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((loc is None) or (poly is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 2 required input parameters to function `isPointInPoly()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(poly)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valBoundingRegion(poly)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valIsPathInPoly(path, poly):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((path is None) or (poly is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 2 required input parameters to function `isPathInPoly()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(path)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(poly)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valBoundingRegion(poly)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valIsPathCrossPoly(path, poly):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((path is None) or (poly is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 2 required input parameters to function `isPathCrossPoly()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(path)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(poly)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valBoundingRegion(poly)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valIsPassPath(loc, path, tolerance):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((loc is None) or (path is None) or (tolerance is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 3 required input parameters to function `isPassPath()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(path)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(tolerance, "tolerance")
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valMinDistLoc2Path(loc, path):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((loc is None) or (path is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 2 required input parameters to function `minDistLoc2Path()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(path)
		warningMsg += newWarningMsg
		
	return [valFlag, errorMsg, warningMsg]

def valDistance2D(loc1, loc2):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((loc1 is None) or (loc2 is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 2 required input parameters to function `distance2D()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc1)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc2)
		warningMsg += newWarningMsg
		
	return [valFlag, errorMsg, warningMsg]

def valDistance3D(loc1, loc2):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((loc1 is None) or (loc2 is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 2 required input parameters to function `distance3D()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc1)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc2)
		warningMsg += newWarningMsg
		
	return [valFlag, errorMsg, warningMsg]

def valDistancePath2D(path):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (path is None):
		valFlag = False
		errorMsg = "Error: Missing required input parameter to function `distancePath2D()`."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(path)
		warningMsg += newWarningMsg
		
	return [valFlag, errorMsg, warningMsg]

def valPointInDistance2D(loc, direction, distMeters):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((loc is None) or (direction is None) or (distMeters is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 3 required input parameters to function `pointInDistance2D()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 360, direction, "degrees of direction")
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(distMeters, "distMeters")
		warningMsg += newWarningMsg
		
	return [valFlag, errorMsg, warningMsg]

def valGetHeading(currentLoc, goalLoc):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((currentLoc is None) or (goalLoc is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 2 required input parameters to function `getHeading()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(currentLoc)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(goalLoc)
		warningMsg += newWarningMsg
		
	return [valFlag, errorMsg, warningMsg]

def valGetMapBoundary(nodes, arcs, locs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (nodes is None and arcs is None and locs is None):
		valFlag = False
		errorMsg = "Error: nodes, arcs, locs can not be None at the same time."

	if (valFlag and nodes is not None):
		[valFlag, errorMsg, newWarningMsg] = valNodes(nodes)
		warningMsg += newWarningMsg

	if (valFlag and arcs is not None):
		[valFlag, errorMsg, newWarningMsg] = valArcs(arcs)
		warningMsg += newWarningMsg

	if (valFlag and locs is not None):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(locs)
		warningMsg += newWarningMsg
		
	return [valFlag, errorMsg, warningMsg]


def valFindLocsAtTime(assignments, timeSec):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (assignments is None):
		valFlag = False
		errorMsg = "Error: An assignments dataframe is required."
		
	if (valFlag and assignments is not None):
		[valFlag, errorMsg, newWarningMsg] = valAssignments(assignments)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(timeSec, 'timeSec')
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]
	
	
def valGeocode(location, dataProvider, dataProviderArgs):    
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (location == None):
		valFlag = False
		errorMsg = "Error: A location (as a text string) is required for `geocode()`."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGeoDataProvider(dataProvider, dataProviderArgs)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]    
	
def valReverseGeocode(location, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	[valFlag, errorMsg, newWarningMsg] = _valLatLon(location)
	warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGeoDataProvider(dataProvider, dataProviderArgs)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]    

def valIsochrones(location, locationType, travelMode, rangeType, rangeSize, interval, smoothing, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	[valFlag, errorMsg, newWarningMsg] = _valLatLon(location)
	warningMsg += newWarningMsg

	if (valFlag):
		try:
			locationType = locationType.lower()
		except:
			pass

		if (locationType not in ['start', 'destination']):
			valFlag = False
			errorMsg = "Error: `locationType` must be either 'start' or 'destination'."
						
	if (valFlag):
		try:
			rangeType = rangeType.lower()
		except:
			pass

		if (rangeType not in ['distance', 'time']):
			valFlag = False
			errorMsg = "Error: `rangeType` must be either 'distance' or 'time'."
		
	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(rangeSize, 'rangeSize')
		warningMsg += newWarningMsg

	if (valFlag):
		if (interval is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(interval, 'interval')
			warningMsg += newWarningMsg
		
	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 100, smoothing, 'smoothing')
		warningMsg += newWarningMsg


	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valIsoDataProvider(travelMode, dataProvider, dataProviderArgs)
		warningMsg += newWarningMsg
	
	return [valFlag, errorMsg, warningMsg]    

def valGetElevationLocs(locs, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (locs is None):
		valFlag = False
		errorMsg = "Error: Must provide `locs`, as a list of lists."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(locs)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGetElevationDataProvider(dataProvider, dataProviderArgs)
		warningMsg += newWarningMsg
	
	return [valFlag, errorMsg, warningMsg]    


def valGetElevationDF(dataframe, replaceOnlyNone, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (dataframe is None):
		valFlag = False
		errorMsg = "Error: Must provide `dataframe` as pandas dataframe."

	if (valFlag):
		if (type(replaceOnlyNone) is not bool):
			valFlag = False
			errorMsg = "Error: `replaceOnlyNone` must be boolean (either `True` or `False`)."
	
	
	if (valFlag):
		# dataframe must be either a nodes, arcs, or assignments dataframe
		[tmpValFlag, tmpErrorMsg, newWarningMsg] = valNodes(dataframe)
		warningMsg += newWarningMsg

		if (not tmpValFlag):
			[tmpValFlag, tmpErrorMsg, newWarningMsg] = valArcs(dataframe)
			warningMsg += newWarningMsg

		if (not tmpValFlag):
			[tmpValFlag, tmpErrorMsg, newWarningMsg] = valAssignments(dataframe)
			warningMsg += newWarningMsg

		valFlag  = tmpValFlag
		errorMsg = tmpErrorMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGetElevationDataProvider(dataProvider, dataProviderArgs)
		warningMsg += newWarningMsg
	
	return [valFlag, errorMsg, warningMsg]    


def valClosestNode2Loc(loc, nodes):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((loc is None) or (nodes is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 2 required input parameters to function `closestNode2Loc()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = valNodes(nodes)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def valClosestPointLoc2Path(loc, path):

	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if ((loc is None) or (path is None)):
		valFlag = False
		errorMsg = "Error: 1 or more of the 2 required input parameters to function `closestPointLoc2Path()` are missing."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(path)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]
	
def valClosestPointLoc2Assignments(loc, assignments, objectID, ignoreStaticPoints):	

	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (loc is None):
		valFlag = False
		errorMsg = "Error: A location (loc) is required."

	if (valFlag):
		if (assignments is None):
			valFlag = False
			errorMsg = "Error: An assignments dataframe is required."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc)
		warningMsg += newWarningMsg
	
	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = valAssignments(assignments)
		warningMsg += newWarningMsg

	if (valFlag):
		if (len(assignments) == 0):
			valFlag = False
			errorMsg = "Error: The assignments dataframe is empty."
	
	if (objectID is not None):
		if (valFlag):
			if (type(objectID) is not str):
				valFlag = False
				errorMsg = "Error: `objectID` must be either `None` or a string."
		if (valFlag):
			if (objectID not in list(assignments['objectID'])):
				valFlag = False
				errorMsg = "Error: `objectID` {} is not found in the `objectID` column of the assignments dataframe.".format(objectID)

	if (valFlag):
		if (type(ignoreStaticPoints) is not bool):
			valFlag = False
			errorMsg = "Error: `ignoreStaticPoints` must be boolean (either `True` or `False`)."
				
	return [valFlag, errorMsg, warningMsg]	


def valClosestPointLoc2Arcs(loc, arcs, objectID, ignoreStaticPoints):	

	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (loc is None):
		valFlag = False
		errorMsg = "Error: A location (loc) is required."

	if (valFlag):
		if (arcs is None):
			valFlag = False
			errorMsg = "Error: An arcs dataframe is required."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLon(loc)
		warningMsg += newWarningMsg

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = valArcs(arcs)
		warningMsg += newWarningMsg

	if (valFlag):
		if (len(arcs) == 0):
			valFlag = False
			errorMsg = "Error: The arcs dataframe is empty."
	
	if (objectID is not None):
		if (valFlag):
			if (type(objectID) is not str):
				valFlag = False
				errorMsg = "Error: `objectID` must be either `None` or a string."
		if (valFlag):
			if (objectID not in list(arcs['objectID'])):
				valFlag = False
				errorMsg = "Error: `objectID` {} is not found in the `objectID` column of the arcs dataframe.".format(objectID)

	if (valFlag):
		if (type(ignoreStaticPoints) is not bool):
			valFlag = False
			errorMsg = "Error: `ignoreStaticPoints` must be boolean (either `True` or `False`)."
				
	return [valFlag, errorMsg, warningMsg]	


def valNearestNodes(origin, nodes, k, costDict, metric, routeType, speedMPS, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	routeTypeReqd = False

	# We'll check nodes first.  If nodes is valid, we can do some 
	# other checks on origin later.
	if (valFlag):
		if (nodes is None):
			valFlag = False
			errorMsg = "Error: `nodes` cannot be None."
		else:    
			[valFlag, errorMsg, warningMsg] = valNodes(nodes)

	if (valFlag):
		if (len(nodes) == 0):
			valFlag = False
			errorMsg = "Error: `nodes` cannot be an empty dataframe."

	if (type(origin) is list):
		[valFlag, errorMsg, warningMsg] = _valLatLon(origin)  
		routeTypeReqd = True
	else:
		# origin is assumed to be a nodeID
		[valFlag, errorMsg, warningMsg] = _valInteger(origin, 'origin')
		if (valFlag):
			if (origin not in nodes['id'].tolist()):
				valFlag = False
				errorMsg = "Error: `origin` %d is not a value in the 'id' column of the `nodes` dataframe." % (origin)
	
	if (valFlag):
		[valFlag, errorMsg, warningMsg] = _valInteger(k, 'k')

	# NOTE: We're not doing any validation on the structure of costDict.

	if ((costDict is None) or (routeTypeReqd)):
		if (valFlag):
			if (type(metric) is not str):
				valFlag = False
				errorMsg = "Error: `metric` must be either 'distance' or 'time'."
			elif (metric.lower() not in ['distance', 'time']):
				valFlag = False
				errorMsg = "Error: `metric` must be either 'distance' or 'time'."

		if (valFlag):
			try:
				routeType = routeType.lower()
			except:
				pass
		
			if (metric.lower() == 'distance' and routeType in ['euclidean2d', 'manhatan']):
				if (speedMPS is None):
					speedMPS = 1  # dummy value

			[valFlag, errorMsg, warningMsg] = _valRouteType2DForScalar(routeType, speedMPS, dataProvider)
		
		# FIXME -- Need to check for valid dataProviderArgs
	
	return [valFlag, errorMsg, warningMsg]

def valArcsToPaths(arcs, objectID, ignoreStaticPoints):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (arcs is None):
		valFlag = False
		errorMsg = "Error: An arcs dataframe is required."
	
	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = valArcs(arcs)
		warningMsg += newWarningMsg

	if (valFlag):
		if (len(arcs) == 0):
			valFlag = False
			errorMsg = "Error: The arcs dataframe is empty."
	
	if (objectID is not None):
		if (valFlag):
			if (type(objectID) is not str):
				valFlag = False
				errorMsg = "Error: `objectID` must be either `None` or a string."
		if (valFlag):
			if (objectID not in list(arcs['objectID'])):
				valFlag = False
				errorMsg = "Error: `objectID` {} is not found in the `objectID` column of the arcs dataframe.".format(objectID)

	if (valFlag):
		if (type(ignoreStaticPoints) is not bool):
			valFlag = False
			errorMsg = "Error: `ignoreStaticPoints` must be boolean (either `True` or `False`)."
				
	return [valFlag, errorMsg, warningMsg]	

	
def valAssignmentsToPaths(assignments, objectID, ignoreStaticPoints):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (assignments is None):
		valFlag = False
		errorMsg = "Error: An assignments dataframe is required."
	
	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = valAssignments(assignments)
		warningMsg += newWarningMsg

	if (valFlag):
		if (len(assignments) == 0):
			valFlag = False
			errorMsg = "Error: The assignments dataframe is empty."
	
	if (objectID is not None):
		if (valFlag):
			if (type(objectID) is not str):
				valFlag = False
				errorMsg = "Error: `objectID` must be either `None` or a string."
		if (valFlag):
			if (objectID not in list(assignments['objectID'])):
				valFlag = False
				errorMsg = "Error: `objectID` {} is not found in the `objectID` column of the assignments dataframe.".format(objectID)

	if (valFlag):
		if (type(ignoreStaticPoints) is not bool):
			valFlag = False
			errorMsg = "Error: `ignoreStaticPoints` must be boolean (either `True` or `False`)."
				
	return [valFlag, errorMsg, warningMsg]	
	
def valNodesToLocs(nodes, includeAlt):
	valFlag = True
	errorMsg = ""
	warningMsg = ""
	
	if (nodes is None):
		valFlag = False
		errorMsg = "Error: A nodes dataframe is required."
	
	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = valNodes(nodes)
		warningMsg += newWarningMsg

	if (valFlag):
		if (type(includeAlt) is not bool):
			valFlag = False
			errorMsg = "Error: `includeAlt` must be boolean (either `True` or `False`)."
				
	return [valFlag, errorMsg, warningMsg]	
	
		
def valCreateGantt(assignments, objectIDorder, separateByModelFile, mergeByodID, splitOnColorChange, title, xAxisLabel, xGrid, yGrid, xMin, xMax, xGridFreq, timeFormat, overlayColumn, missingColor, filename):
	valFlag = True
	errorMsg = ""
	warningMsg = ""


	if (assignments is None):
		valFlag = False
		errorMsg = "Error: An assignments dataframe is required."
		
	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = valAssignments(assignments)
		warningMsg += newWarningMsg

	if (valFlag):
		if (len(assignments) == 0):
			valFlag = False
			errorMsg = "Error: The assignments dataframe is empty."
	
	if (objectIDorder is not None):
		if (valFlag):
			if (type(objectIDorder) is not list):
				valFlag = False
				errorMsg = "Error: `objectIDorder` must be either `None` or a list."
		if (valFlag):
			for objectID in objectIDorder:
				if (objectID not in list(assignments['objectID'])):
					valFlag = False
					errorMsg = "Error: `objectIDorder` contains a value ({}) that is not found in the `objectID` column of the assignments dataframe.".format(objectID)
					break
	
	if (valFlag):
		if (type(separateByModelFile) is not bool):
			valFlag = False
			errorMsg = "Error: `separateByModelFile` must be boolean (either `True` or `False`)."

	if (valFlag):
		if (type(mergeByodID) is not bool):
			valFlag = False
			errorMsg = "Error: `mergeByodID` must be boolean (either `True` or `False`)."
			
	if (valFlag):
		if (type(splitOnColorChange) is not bool):
			valFlag = False
			errorMsg = "Error: `splitOnColorChange` must be boolean (either `True` or `False`)."

	# title -- not checked
	# xAxisLabel -- not checked
	
	if (valFlag):
		if (type(xGrid) is not bool):
			valFlag = False
			errorMsg = "Error: `xGrid` must be boolean (either `True` or `False`)."

	if (valFlag):
		if (type(yGrid) is not bool):
			valFlag = False
			errorMsg = "Error: `yGrid` must be boolean (either `True` or `False`)."
		
	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(xMin, 'xMin')
		warningMsg += newWarningMsg
		
	if (xMax is not None):
		if (valFlag):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(xMax, 'xMax')
			warningMsg += newWarningMsg
		if (valFlag):
			if (xMax <= xMin):
				valFlag = False
				errorMsg = "Error: `xMax` must be greater than or equal to `xMin` (or `xMax` may be left at its default value of `None`)."
		
	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(xGridFreq, 'xGridFreq')
		warningMsg += newWarningMsg

	if (valFlag):
		if (type(timeFormat) is not str):
			valFlag = False
			errorMsg = "Error: `timeFormat` must be a string.  Valid options are 'dhms', 'hms', 'ms', 'd', 'h', 'm', or 's'."
	
	if (valFlag):		
		if (timeFormat.lower() not in ['dhms', 'hms', 'ms', 'd', 'h', 'm', 's']):
			valFlag = False
			errorMsg = "Error: `timeFormat` must be either 'dhms', 'hms', 'ms', 'd', 'h', 'm', or 's'."

	# Not sure if we want to add these warnings...
    # [d, h, m, s] = getDHMS(max(assignments['endTimeSec']))
    # if ((d > 0) and timeFormat.lower() in ['hms', 'ms']):
    #    print("Warning: The time exceeds 24 hours.  Consider using the 'DHMS' format.")
    # elif((h > 0) and timeFormat.lower() in ['ms']):
    #     print("Warning: The time exceeds 60 minutes.  Consider using the 'HMS' format.")

	if (valFlag):
		if (overlayColumn not in [None, 'odID', 'index']):
			valFlag = False
			errorMsg = "Error: `overlayColumn` must be either None (default), 'odID', or 'index'."

	if (missingColor is not None):
		if (valFlag):
			if (missingColor.lower() not in matplotlibColorDict.keys()):
				[valFlag, errorMsg, newWarningMsg] = _valHexColor(missingColor)
				warningMsg += newWarningMsg
	
	if (filename is not None):	
		if (valFlag):	
			if (type(filename) is not str):
				valFlag = False
				errorMsg = "Error: `filename` must be either `None` or a string."

	if (valFlag):
		if (overlayColumn == 'index' and mergeByodID):
			warningMsg += "Warning: Combining `overlayColumn='index'` with `mergeByodID=True` is not recommended."
		if (overlayColumn == 'odID' and not mergeByodID):
			warningMsg += "Warning: Combining `overlayColumn='odID'` with `mergeByodID=False` is not recommended."

	return [valFlag, errorMsg, warningMsg]
		
def valGetWeather(location, id, initDF, metricUnits, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	
	[valFlag, errorMsg, newWarningMsg] = _valLatLon(location)
	warningMsg += newWarningMsg
	
	if (valFlag):
		if (id is not None):
			[valFlag, warningMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(id, "id")
			warningMsg += newWarningMsg
	
	if (valFlag):
		if (initDF is not None):
			if (type(initDF) is not pd.core.frame.DataFrame):
				valFlag = False
				errorMsg = "Error: initDF should be a pandas dataframe or None."
			
	if (valFlag):
		if (type(metricUnits) is not bool):
			valFlag = False
			errorMsg = "Error: `metricUnits` must be boolean (True or False)."

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGetWeatherDataProvider(dataProvider, dataProviderArgs)
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

	
def _valMapBoundary(mapBoundary, zoomStart):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (mapBoundary is not None and zoomStart is not None):
		warningMsg += "Warning: `mapBoundary` and `zoomStart` are both provided, but `zoomStart` will override `mapBoundary`.  To use `mapBoundary` alone, please remove the `zoomStart` field. "

	if (mapBoundary is not None):
		if (len(mapBoundary) != 2):
			valFlag = False
			errorMsg = "Error: mapBoundary should be in [[minLat, maxLon], [maxLat, minLon]] format."
		elif (len(mapBoundary[0]) != 2 or len(mapBoundary[1]) != 2):
			valFlag = False
			errorMsg = "Error: mapBoundary should be in [[minLat, maxLon], [maxLat, minLon]] format."
		if (valFlag):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(mapBoundary[0])
		if (valFlag):
			[valFlag, errorMsg, newWarningMsg] = _valLatLon(mapBoundary[1])

	if (valFlag and zoomStart is not None):
		if (type(zoomStart) is not int):
			valFlag = False
			errorMsg = "Error: zoomStart should be integer."
		elif (zoomStart < 1 or zoomStart > 18):
			valFlag = False
			errorMsg = "Error: zoomStart must be between 1 and 18 (inclusive), 1 --> global view, 18 --> max zoom."

	return [valFlag, errorMsg, warningMsg]

def _valBoundingRegion(boundingRegion):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (len(boundingRegion) < 3):
		valFlag = False
		errorMsg = "Error: At least 3 coordinates are required to form a polygon."
	
	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valLatLonList(boundingRegion)

	if (valFlag):
		boundingRegion2D = []
		for i in range(len(boundingRegion)):
			boundingRegion2D.append([boundingRegion[i][0], boundingRegion[i][1]])
		lstLineSegment = [boundingRegion2D[0], boundingRegion2D[len(boundingRegion2D) - 1]]
		for i in range(1, len(boundingRegion2D) - 1):
			lstLineSegment.append([boundingRegion2D[i - 1], boundingRegion2D[i]])
		for i in range(len(lstLineSegment)):
			if (geoIsLineCrossPoly(lstLineSegment, boundingRegion2D)):
				valFlag = False
				errorMsg = "Error: Invalid `boundingRegion`; cannot have crossed line segments."
				break

	return [valFlag, errorMsg, warningMsg]

def _valNodeDistribArgs(nodeDistrib, nodeDistribArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		if (nodeDistrib is None):
			valFlag = False
			errorMsg = "Error: `nodeDistrib` is required. Valid options are 'uniformBB', 'normalBB', and 'normal'.  Note that these options are case sensitive." # Removed 'unifRoadBasedBB' for v.0.2.0

	if (valFlag):
		if (nodeDistrib not in nodeDistribList):
			valFlag = False
			errorMsg = "Error: Invalid `nodeDistrib` value. Valid options are 'uniformBB', 'normalBB', and 'normal'.  Note that these options are case sensitive." # Removed 'unifRoadBasedBB' for v.0.2.0
		elif (nodeDistribArgs is None):
			valFlag = False
			errorMsg = "Error: `nodeDistribArgs` is required. Key values are varied for different `nodeDistrib`."
		else:
			if (nodeDistrib == 'uniformBB'):
				if ('boundingRegion' not in nodeDistribArgs):
					valFlag = False
					errorMsg = "Error: 'boundingRegion' is a required key in `nodeDistribArgs` if `nodeDistrib = 'uniformBB'`."
				else:
					[valFlag, errorMsg, newWarningMsg] = _valBoundingRegion(nodeDistribArgs['boundingRegion'])
					warningMsg += newWarningMsg

			if (nodeDistrib == 'normalBB'):
				if ('center' not in nodeDistribArgs):
					valFlag = False
					errorMsg = "Error: 'center' is a required key in `nodeDistribArgs` if `nodeDistrib = 'normalBB'`.  Please provide the center location in the  form of [lat, lon]."
				elif ('stdDev' not in nodeDistribArgs):
					valFlag = False
					errorMsg = "Error: 'stdDev' is a required key in `nodeDistribArgs` if `nodeDistrib = 'normalBB'`."
				elif ('boundingRegion' not in nodeDistribArgs):
					valFlag = False
					errorMsg = "Error: 'boundingRegion' is a required key in `nodeDistribArgs` if `nodeDistrib = 'normalBB'`."

				if (valFlag):
					[valFlag, errorMsg, newWarningMsg] = _valBoundingRegion(nodeDistribArgs['boundingRegion'])
					warningMsg += newWarningMsg

				if (valFlag):
					[valFlag, errorMsg, newWarningMsg] = _valLatLon(nodeDistribArgs['center'])
					warningMsg += newWarningMsg

				if (valFlag):
					[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(nodeDistribArgs['stdDev'], "standard deviation")
					warningMsg += newWarningMsg

			if (nodeDistrib == 'normal'):
				if ('center' not in nodeDistribArgs):
					valFlag = False
					errorMsg = "Error: 'center' is a required key in `nodeDistribArgs` if `nodeDistrib = 'normal'`.  Please provide the center location in the form of [lat, lon]."
				elif ('stdDev' not in nodeDistribArgs):
					valFlag = False
					errorMsg = "Error: 'stdDev' is a required key in `nodeDistribArgs` if `nodeDistrib = 'normal'`."

				if ('boundingRegion' in nodeDistribArgs):
					warningMsg += "Warning: A `boundingRegion` was provided in `nodeDistribArgs`. The `nodeDistrib` is being treated as 'normalBB' instead of 'normal'. To use a 'normal' `nodeDistrib`, simply remove the `boundingRegion`.\n"

				if (valFlag):
					[valFlag, errorMsg, newWarningMsg] = _valLatLon(nodeDistribArgs['center'])
					warningMsg += newWarningMsg

				if (valFlag):
					[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(nodeDistribArgs['stdDev'], "standard deviation")
					warningMsg += newWarningMsg

			if (nodeDistrib == 'unifRoadBasedBB'):
				if ('boundingRegion' not in nodeDistribArgs):
					valFlag = False
					errorMsg = "Error: 'boundingRegion' is a required key in `nodeDistribArgs` if `nodeDistrib = 'unifRoadBasedBB'`."
				elif ('distToRoad' not in nodeDistribArgs):
					valFlag = False
					errorMsg = "Error: 'distToRoad' is a required key in `nodeDistribArgs` if `nodeDistrib = 'unifRoadBasedBB'`."

				if (valFlag):
					[valFlag, errorMsg, newWarningMsg] = _valBoundingRegion(nodeDistribArgs['boundingRegion'])
					warningMsg += newWarningMsg

				if (valFlag):
					[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(nodeDistribArgs['distToRoad'], "distance to road")
					warningMsg += newWarningMsg



	return [valFlag, errorMsg, warningMsg]

def _valLatLonList(locs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (locs is None):
		valFlag = False
		errorMsg = "Error: `locs` should not be None."
	else:
		if (type(locs) is not list):
			valFlag = False
			errorMsg = "Error: A list of lists was expected to describe a sequence of locations, in the format of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...]."
		if (valFlag):
			if (len(locs) == 0):
				valFlag = False
				errorMsg = "Error: A list of lists was expected to describe a sequence of locations, in the format of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...]."
	
		if (valFlag):
			for i in range(len(locs)):
				if (valFlag):
					[valFlag, errorMsg, newWarningMsg] = _valLatLon(locs[i])
					warningMsg += newWarningMsg
				else:
					break

	return [valFlag, errorMsg, warningMsg]

def _valLatLon(loc):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (loc is None):
		valFlag = False
		errorMsg = "Error: `loc` should not be None."
	elif (type(loc) is not list):
		valFlag = False
		errorMsg = "Error: `loc` should be a list, of the form [lat, lon] or [lat, lon, alt]."	
	else:
		if (len(loc) == 2 or len(loc) == 3):
			if (valFlag):
				if (loc[0] < -90 or loc[0] > 90):
					valFlag = False
					errorMsg = "Error: latitude is out of range.  The valid range is [-90, +90] degrees."
			if (valFlag):
				if (loc[1] < -180 or loc[1] > 180):
					valFlag = False
					errorMsg = "Error: longitude is out of range.  The valid range is [-180, +180] degrees."
			if (valFlag and len(loc) == 3):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(loc[2], "altitude")
				warningMsg += newWarningMsg
		else:
			valFlag = False
			errorMsg = "Error:  location must be in the format of [lat, lon] or [lat, lon, alt]."

	return [valFlag, errorMsg, warningMsg]

def _valDatabase(locs, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	if (dataProvider not in dataProviderDictionary.keys()):
		errorMsg = "Error: Invalid `dataProvider` value. Valid options include 'pgRouting', 'MapQuest', 'ORS-online', 'OSRM-online', and 'ORS-local'."
		valFlag = False
	else:
		if (dataProviderDictionary[dataProvider] == "pgrouting"):
			if (dataProviderArgs is None):
				valFlag = False
				errorMsg = "Error: `dataProviderArgs` is a required parameter if `dataprovider = 'pgRouting'`."
			elif ('databaseName' not in dataProviderArgs):
				valFlag = False
				errorMsg = "Error: 'databaseName' is a required key in `dataProviderArgs` if `dataProvider = 'pgRouting'`."
			else:
				databaseName = dataProviderArgs['databaseName']
				try:
					conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (databaseName, config['VRV_SETTING_PGROUTING_USERNAME'], config['VRV_SETTING_PGROUTING_HOST'], config['VRV_SETTING_PGROUTING_PASSWORD']))
					cur = conn.cursor()
					sqlCommand = "select min(lat), max(lat), min(lon), max(lon) from ways_vertices_pgr;"
					cur.execute(sqlCommand)
					row = cur.fetchone()
					minLat = row[0]
					maxLat = row[1]
					minLon = row[2]
					maxLon = row[3]
					for i in range(len(locs)):
						if (locs[i][0] < minLat or locs[i][0] > maxLat or locs[i][1] < minLon or locs[i][1] > maxLon):
							warningMsg += "Warning: The database contains coordinates between latitude: %s to %s and longitude: %s to %s, the coordinates (%s, %s) you provided is not inside. \n" % (minLat, maxLat, minLon, maxLon, locs[i][0], locs[i][1])
					conn.close()
				except:
					valFlag = False
					errorMsg = "Error: Bad request. Database '%s' doesn't exist." % (databaseName)

		if (dataProviderDictionary[dataProvider] == "mapquest"):
			if (dataProviderArgs is None):
				valFlag = False
				errorMsg = "Error: `dataProviderArgs` is a required parameter if `dataprovider = 'MapQuest'`."
			elif ('APIkey' not in dataProviderArgs):
				valFlag = False
				errorMsg = "Error: 'APIkey' is a required key in `dataProviderArgs` if `dataProvider = 'MapQuest'`."

		if (dataProviderDictionary[dataProvider] == "ors-online"):
			if (dataProviderArgs is None):
				valFlag = False
				errorMsg = "Error: `dataProviderArgs` is a required parameter if `dataprovider = 'ORS-online'`."
			elif ('APIkey' not in dataProviderArgs):
				valFlag = False
				errorMsg = "Error: 'APIkey' is a required key in `dataProviderArgs` if `dataProvider = 'ORS-online'`."

		if (dataProviderDictionary[dataProvider] == "ors-local"):
			if (dataProviderArgs is None):
				valFlag = False
				errorMsg = "Error: `dataProviderArgs` is a required parameter if `dataprovider = 'ORS-local'`."
			elif ('port' not in dataProviderArgs):
				valFlag = False
				errorMsg = "Error: 'port' is a required key in `dataProviderArgs` if `dataProvider = 'ORS-local'`."

		if (dataProviderDictionary[dataProvider] == "osrm-online"):
			if (dataProviderArgs is not None):
				warningMsg += "Warning: `dataProviderArgs` will be ignored if `dataProvider = 'OSRM-online'`.\n"

	return [valFlag, errorMsg, warningMsg]


def _valGeoDataProvider(dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	if (dataProvider == None):
		pass
	elif (dataProvider not in geoDataProviderDictionary.keys()):
		errorMsg = "Error: Invalid `dataProvider` value. Valid options include 'MapQuest', and 'ORS-online'."
		valFlag = False
	else:
		if (geoDataProviderDictionary[dataProvider] == "mapquest"):
			if ('APIkey' not in dataProviderArgs):
				valFlag = False
				errorMsg = "Error: 'APIkey' is a required key in `dataProviderArgs` if `dataProvider = 'MapQuest'`."

		if (geoDataProviderDictionary[dataProvider] == "ors-online"):
			if ('APIkey' not in dataProviderArgs):
				valFlag = False
				errorMsg = "Error: 'APIkey' is a required key in `dataProviderArgs` if `dataProvider = 'ORS-online'`."

	return [valFlag, errorMsg, warningMsg]
	
def _valGetElevationDataProvider(dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	if (dataProvider not in elevDataProviderDictionary.keys()):
		valFlag = False
		errorMsg = "Error: Invalid `dataProvider` value. Currently, the only valid option is 'ORS-online'."
	else:
		if (elevDataProviderDictionary[dataProvider] == "ors-online"):
			if ('APIkey' not in dataProviderArgs):
				valFlag = False
				errorMsg = "Error: 'APIkey' is a required key in `dataProviderArgs` if `dataProvider = 'ORS-online'`."

	return [valFlag, errorMsg, warningMsg]

	
def _valIsoDataProvider(travelMode, dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		travelMode = travelMode.lower()
	except:
		pass

	if (travelMode not in isoTravelModeList):
		valFlag = False
		errorMsg = "Error: Invalid `travelMode` value."
	
	if (valFlag):
		try:
			dataProvider = dataProvider.lower()
		except:
			pass

		if (dataProvider not in isoDataProviderDictionary.keys()):
			valFlag = False
			errorMsg = "Error: Invalid `dataProvider` value. Currently, the only valid options are 'ORS-online' and 'ors-local."
		else:
			if (isoDataProviderDictionary[dataProvider] == "ors-online"):
				if ('APIkey' not in dataProviderArgs):
					valFlag = False
					errorMsg = "Error: 'APIkey' is a required key in `dataProviderArgs` if `dataProvider = 'ORS-online'`."
			elif (isoDataProviderDictionary[dataProvider] == "ors-local"):
				if ('port' not in dataProviderArgs):
					valFlag = False
					errorMsg = "Error: 'port' is a required key in `dataProviderArgs` if `dataProvider = 'ORS-local'`."

	return [valFlag, errorMsg, warningMsg]

def _valIso(iso):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (type(iso) is not dict):
		valFlag = False
		errorMsg = "Error: `iso` must be a dictionary."

	if (valFlag):
		if ('location' not in iso):
			valFlag = False
			errorMsg = "Error: `iso` dictionary must include `location` key."

	if (valFlag):
		if ('boundingRegion' not in iso):
			valFlag = False
			errorMsg = "Error: `iso` dictionary must include `boundingRegion` key."

	if (valFlag):
		if (type(iso['boundingRegion']) is not list):
			valFlag = False
			errorMsg = "Error: `iso['boundingRegion]` must be a list."

	if (valFlag):
		if (len(iso['boundingRegion']) != 5):
			valFlag = False
			errorMsg = "Error: `iso['boundingRegion]` must be a list with 5 [lat, lon] pairs."
						
	if (valFlag):
		if ('isochrones' not in iso):
			valFlag = False
			errorMsg = "Error: `iso` dictionary must include `isochrones` key."
			
	if (valFlag):
		if (type(iso['isochrones']) is not list):
			valFlag = False
			errorMsg = "Error: `iso['isochrones]` must be a list."
			
	if (valFlag):
		for i in range(0, len(iso['isochrones'])):
			if (type(iso['isochrones'][i]) is not dict):
				valFlag = False
				errorMsg = "Error: Each element of `iso['isochrones]` must be a dictionary."
				break
	
			if ('value' not in iso['isochrones'][i]):
				valFlag = False
				errorMsg = "Error: Each element of `iso['isochrones]` must include a 'value' key."
				break

			if ('valueUnits' not in iso['isochrones'][i]):
				valFlag = False
				errorMsg = "Error: Each element of `iso['isochrones]` must include a 'valueUnits' key."
				break

			if ('area' not in iso['isochrones'][i]):
				valFlag = False
				errorMsg = "Error: Each element of `iso['isochrones]` must include an 'area' key."
				break
				
			if ('pop' not in iso['isochrones'][i]):
				valFlag = False
				errorMsg = "Error: Each element of `iso['isochrones]` must include a 'pop' key."
				break

			if ('reachfactor' not in iso['isochrones'][i]):
				valFlag = False
				errorMsg = "Error: Each element of `iso['isochrones]` must include a 'reachfactor' key."
				break
				
			if ('poly' not in iso['isochrones'][i]):
				valFlag = False
				errorMsg = "Error: Each element of `iso['isochrones]` must include a 'poly' key."
				break
		
			if (type(iso['isochrones'][i]['poly']) is not list):
				valFlag = False
				errorMsg = "Error: Each element of `iso['isochrones]` must include a 'poly' key with a list structure."
				break

			# FIXME -- Could continue to drill down into poly structure,
			#          but this already seems like overkill at this point.


	return [valFlag, errorMsg, warningMsg]


def _valGetWeatherDataProvider(dataProvider, dataProviderArgs):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	if (dataProvider not in weatherDataProviderDictionary.keys()):
		valFlag = False
		errorMsg = "Error: Invalid `dataProvider` value. Currently, the only valid option is 'openweather'."
	else:
		if (weatherDataProviderDictionary[dataProvider] == "openweather"):
			if ('APIkey' not in dataProviderArgs):
				valFlag = False
				errorMsg = "Error: 'APIkey' is a required key in `dataProviderArgs` if `dataProvider = 'openweather'`."

	return [valFlag, errorMsg, warningMsg]
	
	
def _valRouteType2DForScalar(routeType, speedMPS, dataProvider):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	try:
		routeType = routeType.lower()
	except:
		pass
		
	if (routeType not in routeType2DList):
		errorMsg = "Error: Invalid `routeType` value. Valid options include 'euclidean2D', 'manhattan', 'fastest', 'shortest', 'pedestrian', 'cycling', 'truck', and 'wheelchair'."
		valFlag = False
	else:
		if (routeType == 'euclidean2d'):
			if (speedMPS is None):
				valFlag = False
				errorMsg = "Error: For 'euclidean2D' routeType, speedMPS is required."
		elif (routeType == 'manhattan'):
			if (speedMPS is None):
				valFlag = False
				errorMsg = "Error: For 'manhattan' routeType, speedMPS is required."
		elif (routeType == 'fastest'):
			if (dataProvider not in dataProviderDictionary.keys()):
				errorMsg = "Error: A valid dataProvider is required if routeType = 'fastest'. Valid data providers supporting the 'fastest' routeType are 'ORS-online', 'OSRM-online', 'pgRouting', MapQuest', and 'ORS-local'."
				valFlag = False
			elif (speedMPS is not None):
				warningMsg += "Warning:  An explicit constant vehicle speed was specified by speedMPS.  Speeds from the data provider will be ignored. \n"
		elif (routeType == 'shortest'):
			if (dataProviderDictionary[dataProvider] not in ['ors-online', 'mapquest']):
				errorMsg = "Error: 'ors-online' and 'MapQuest' are currently the only dataProvider options for routeType = 'shortest'."
				valFlag = False
			elif (speedMPS is not None):
				warningMsg += "Warning:  An explicit constant vehicle speed was specified by speedMPS.  Speeds from the data provider will be ignored.\n"
		elif (routeType == 'pedestrian'):
			if (dataProviderDictionary[dataProvider] not in ['ors-online', 'mapquest', 'ors-local']):
				errorMsg = "Error: 'ors-online', 'MapQuest', and 'ORS-local' are currently the only dataProvider options for routeType = 'pedestrian'."
				valFlag = False
			elif (speedMPS is not None):
				warningMsg += "Warning:  An explicit constant vehicle speed was specified by speedMPS.  Speeds from the data provider will be ignored.\n"
		elif (routeType == 'cycling'):
			if (dataProviderDictionary[dataProvider] not in ['ors-online', 'ors-local']):
				errorMsg = "Error: 'ORS-online' and 'ORS-local' are currently the only dataProvider options for routeType = 'cycling'."
				valFlag = False
			elif (speedMPS is not None):
				warningMsg += "Warning:  An explicit constant vehicle speed was specified by speedMPS.  Speeds from the data provider will be ignored.\n"
		elif (routeType == 'truck'):
			if (dataProviderDictionary[dataProvider] not in ['ors-online', 'ors-local']):
				errorMsg = "Error: 'ORS-online' and 'ORS-local' are currently the only dataProvider options for routeType = 'truck'."
				valFlag = False
			elif (speedMPS is not None):
				warningMsg += "Warning:  An explicit constant vehicle speed was specified by speedMPS.  Speeds used by the data provider will be ignored.\n"
		elif (routeType == 'wheelchair'):
			if (dataProviderDictionary[dataProvider] not in ['ors-online']):
				errorMsg = "Error: 'ORS-online' is currently the only dataProvider option for routeType = 'wheelchair'."
				valFlag = False
			elif (speedMPS is not None):
				warningMsg += "Warning:  An explicit constant vehicle speed was specified by speedMPS.  Speeds used by the data provider will be ignored.\n"
				
	return [valFlag, errorMsg, warningMsg]

def _valRouteType2DForShapepoints(routeType, speedMPS, expDurationSec, dataProvider):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	try:
		routeType = routeType.lower()
	except:
		pass
		
	if (routeType not in routeType2DList):
		errorMsg = "Error: Invalid `routeType` value. Valid options include 'euclidean2D', 'manhattan', 'fastest', 'shortest', 'pedestrian', 'cycling', 'truck', and 'wheelchair'."
		valFlag = False
	else:
		if (valFlag and speedMPS is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(speedMPS, 'speedMPS')
			warningMsg += newWarningMsg

		if (valFlag and expDurationSec is not None):
			[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(expDurationSec, 'expDurationSec')
			warningMsg += newWarningMsg
		
		if (routeType in ['euclidean2d', 'manhattan']):
			if (speedMPS is None and expDurationSec is None):
				valFlag = False
				errorMsg = "Error: Please provide `expDurationSec` or `speedMPS` for calculating shapepoints."
			
			elif (speedMPS is not None and expDurationSec is not None):
				warningMsg += "Warning: `speedMPS` and `expDurationSec` are both provided, but `expDurationSec` will override `speedMPS`. To calculate by `speedMPS` (rather than by an expected duration), leave `expDurationSec` at its default value (None).\n"

			if (valFlag and dataProvider is not None):
				warningMsg += "Warning: For 'euclidean2d' and 'manhattan', it is not using data provider, therefore `dataProvider` is ignored.\n"

		elif (routeType in ['greatcircle', 'curve']):
			# FIXMELP -- Where are these new "routeType" options defined?
			#            Also, these are not in `routeType2DList`, so they will throw an error above. 
			if (expDurationSec is None):
				valFlag = False
				errorMsg = "Error: Please provide `expDurationSec` to be evenly distributed to the arc"

			if (speedMPS is not None):
				warningMsg += "Warning: `speedMPS` will not be used for calculation. \n"
				
		elif (routeType in ['fastest', 'shortest', 'pedestrian', 'cycling', 'truck', 'wheelchair']):
			if (routeType == 'fastest'):
				if (dataProvider not in dataProviderDictionary.keys()):
					errorMsg = "Error: A valid dataProvider is required if routeType = 'fastest'. Valid data providers supporting the 'fastest' routeType are 'ORS-online', 'OSRM-online', 'pgRouting', 'MapQuest', and 'ORS-local'."
					valFlag = False
			elif (routeType == 'shortest'):
				if (dataProviderDictionary[dataProvider] not in ['ors-online', 'mapquest']):
					errorMsg = "Error: 'ors-online' and 'MapQuest' are currently the only dataProvider options for routeType = 'shortest'."
					valFlag = False
			elif (routeType == 'pedestrian'):
				if (dataProviderDictionary[dataProvider] not in ['ors-online', 'mapquest', 'ors-local']):
					errorMsg = "Error: Invalid `dataProvider` value.  'ORS-online',  'MapQuest', and 'ORS-local' are currently the only data providers supporting the 'pedestrian' routeType option."
					valFlag = False
			elif (routeType == 'cycling'):
				if (dataProviderDictionary[dataProvider] not in ['ors-online', 'ors-local']):
					errorMsg = "Error: Invalid `dataProvider` value.  'ORS-online' and 'ORS-local' are currently the only data providers supporting the 'cycling' routeType option."
					valFlag = False
			elif (routeType == 'truck'):
				if (dataProviderDictionary[dataProvider] not in ['ors-online', 'ors-local']):
					errorMsg = "Error: Invalid `dataProvider` value.  'ORS-online' and 'ORS-local' are currently the only data providers supporting the 'truck' routeType option."
					valFlag = False
			elif (routeType == 'wheelchair'):
				if (dataProviderDictionary[dataProvider] not in ['ors-online']):
					errorMsg = "Error: 'ORS-online' is currently the only dataProvider option for routeType = 'wheelchair'."
					valFlag = False

			if (valFlag):
				if (speedMPS != None and expDurationSec == None):
					warningMsg += "Warning:  A constant speed for the vehicle has been provided.  Speed from data provider will be ignored. To calculate based on data from the data provider, leave `speedMPS` at its default value (None).\n"

				elif (speedMPS == None and expDurationSec != None):
					warningMsg += "Warning: Expected duration time has been provided; speed from data provider will be ignored. To calculate based on data from the data provider, leave `expDurationSec` at its default value (None).\n"

				elif (speedMPS != None and expDurationSec != None):
					warningMsg += "Warning: `speedMPS` and `expDurationSec` are both provided, but `expDurationSec` will override `speedMPS` and speed from the data provider. To calculate by `speedMPS` (rather than by an expected duration), leave `expDurationSec` at its default value (None). To calculate based on data from the data provider, leave both `speedMPS` and `expDurationSec` at their default values (None).\n"

	return [valFlag, errorMsg, warningMsg]

def _valMatrixType(matrixType, fromNodeID, toNodeID):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		matrixType = matrixType.lower()
	except:
		pass
		
	if (matrixType not in matrixTypeList):
		valFlag = False
		errorMsg = "Error: matrixType not included"
	elif (matrixType == 'all2all' and (fromNodeID is not None or toNodeID is not None)):
		warningMsg += "Warning: `fromNodeID` and `toNodeID` will be ignored.\n"
	elif (matrixType == 'one2many'):
		if (fromNodeID is None):
			valFlag = False
			errorMsg = "Error: `fromNodeID` is needed for 'one2many' option; the origin node is required."
		if (toNodeID is not None):
			warningMsg += "Warning: `toNodeID` is ignored.  Time/distance values will be generated from the start node to all given nodes.\n"
	elif (matrixType == 'many2one'):
		if (fromNodeID is not None):
			warningMsg += "Warning: `fromNodeID` is ignored.  Time/distance values will be generated from all given nodes to the target node.\n"
		if (toNodeID is None):
			valFlag = False
			errorMsg = "Error: `toNodeID` is needed for 'many2one' option; the destination node is required."

	return [valFlag, errorMsg, warningMsg]

def _valDistanceUnits(distUnits, parameterName):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		distUnits = distUnits.lower()
	except:
		pass

	if (distUnits not in distanceUnitsDictionary.keys()):
		valFlag = False
		errorMsg = "Error: Invalid units for %s distance. Valid distance options include 'meters', 'm', 'kilometers', 'km', 'miles', 'mi', 'yard', 'feet', 'ft', 'nm', 'nmi'." % (parameterName)

	return [valFlag, errorMsg, warningMsg]

def _valTimeUnits(timeUnits, parameterName):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		timeUnits = timeUnits.lower()
	except:
		pass

	if (timeUnits not in timeUnitsDictionary.keys()):
		valFlag = False
		errorMsg = "Error: Invalid units for %s time. Valid time options include 'seconds', 'second', 'sec', 's', 'minutes', 'mins', 'min', 'hours', 'hour', 'hrs', 'hr', 'h'." % (parameterName)

	return [valFlag, errorMsg, warningMsg]

def _valAreaUnits(areaUnits, parameterName):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		areaUnits = areaUnits.lower()
	except:
		pass
		
	if (areaUnits not in areaUnitsDictionary.keys()):
		valFlag = False
		errorMsg = "Error: Invalid units for %s area. Valid area options include 'sf', 'sqft', 'sqfeet', 'smi', 'sqmi', 'sqmiles', 'sm', 'sqm', 'sqmeters', 'skm', 'sqkm', 'sqkilometers'." % (parameterName)

	return [valFlag, errorMsg, warningMsg]

def _valDate(date):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		time.strptime(date, '%Y-%m-%d')
	except ValueError:
		valFlag = False
		errorMsg = "Error: Date format should be 'YYYY-MM-DD'."

	return [valFlag, errorMsg, warningMsg]

def _valTime(t):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		time.strptime(t, '%H:%M:%S')
	except ValueError:
		valFlag = False
		errorMsg = "Error: Time format should be 'HH:MM:SS'."

	return [valFlag, errorMsg, warningMsg]

def _valHexColor(hexColor):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hexColor)

	if (not match):
		valFlag = False
		errorMsg = "Error: Invalid Hex color string."

	return [valFlag, errorMsg, warningMsg]

def _valRouteType3D(routeType, takeoffSpeedMPS, climbRateMPS, cruiseSpeedMPS, landSpeedMPS, descentRateMPS):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		routeType = routeType.lower()
	except:
		pass

	if (routeType not in routeType3DList):
		errorMsg = "Error: Invalid `routeType` value.  Valid options include 'square', 'triangular', 'trapezoidal', and 'straight'"
		valFlag = False
	else:
		if (routeType == 'square'):
			if (cruiseSpeedMPS is None):
				valFlag = False
				errorMsg = "Error: For `square` routeType, cruiseSpeedMPS is required."

			if (takeoffSpeedMPS is None):
				valFlag = False
				errorMsg = "Error: For `square` routeType, takeoffSpeedMPS is required."

			if (landSpeedMPS is None):
				valFlag = False
				errorMsg = "Error: For `square` routeType, landSpeedMPS is required."

			if (climbRateMPS != None):
				warningMsg += "Warning: climbRateMPS will be overridden.\n"

			if (descentRateMPS != None):
				warningMsg += "Warning: descentRateMPS will be overridden.\n"

			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(takeoffSpeedMPS, 'takeoffSpeedMPS')

			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(cruiseSpeedMPS, 'cruiseSpeedMPS')

			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(landSpeedMPS, 'landSpeedMPS')

		elif (routeType == 'triangular'):
			if (cruiseSpeedMPS is None):
				valFlag = False
				errorMsg = "Error: For `triangular` routeType, cruiseSpeedMPS is required."

			if (takeoffSpeedMPS != None):
				warningMsg += "Warning: takeoffSpeedMPS will be ignored.\n"

			if (landSpeedMPS != None):
				warningMsg += "Warning: landSpeedMPS will be ignored.\n"

			if (climbRateMPS != None):
				warningMsg += "Warning: climbRateMPS will be ignored.\n"

			if (descentRateMPS != None):
				warningMsg += "Warning: descentRateMPS will be ignored.\n"

			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(cruiseSpeedMPS, 'cruiseSpeedMPS')

		elif (routeType == 'trapezoidal'):
			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(takeoffSpeedMPS, 'takeoffSpeedMPS')

			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(climbRateMPS, 'climbRateMPS')

			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(cruiseSpeedMPS, 'cruiseSpeedMPS')

			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(landSpeedMPS, 'landSpeedMPS')

			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(descentRateMPS, 'descentRateMPS')

			if (valFlag):
				if (climbRateMPS > takeoffSpeedMPS):
					valFlag = False
					errorMsg = "Error: Rate of climb can not be greater than takeoff speed."

			if (valFlag):
				if (descentRateMPS > landSpeedMPS):
					valFlag = False
					errorMsg = "Error: Rate of descent can not be greater than landing speed."

		elif (routeType == 'straight'):
			if (cruiseSpeedMPS is None):
				valFlag = False
				errorMsg = "Error: For `straight` routeType, cruiseSpeedMPS is required."

			if (takeoffSpeedMPS != None):
				warningMsg += "Warning: takeoffSpeedMPS will be ignored.\n"

			if (landSpeedMPS != None):
				warningMsg += "Warning: landSpeedMPS will be ignored.\n"

			if (climbRateMPS != None):
				warningMsg += "Warning: climbRateMPS will be ignored.\n"

			if (descentRateMPS != None):
				warningMsg += "Warning: descentRateMPS will be ignored.\n"

			if (valFlag):
				[valFlag, errorMsg, newWarningMsg] = _valGreaterThanZeroFloat(cruiseSpeedMPS, 'cruiseSpeedMPS')

	return [valFlag, errorMsg, warningMsg]

def _valAltitude(startAltMetersAGL, cruiseAltMetersAGL, endAltMetersAGL):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(startAltMetersAGL, 'startAltMetersAGL')

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(cruiseAltMetersAGL, 'cruiseAltMetersAGL')

	if (valFlag):
		[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(endAltMetersAGL, 'endAltMetersAGL')

	if (valFlag):
		if (startAltMetersAGL >= cruiseAltMetersAGL):
			valFlag = False
			errorMsg = "Error: startAltMetersAGL should be lower than cruiseAltMetersAGL."

	if (valFlag):
		if (endAltMetersAGL >= cruiseAltMetersAGL):
			valFlag = False
			errorMsg = "Error: endAltMetersAGL should be lower than cruiseAltMetersAGL."

	return [valFlag, errorMsg, warningMsg]

def _valLoiterPosition(loiterPosition):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		loiterPosition = loiterPosition.lower()
	except:
		pass

	if (loiterPosition not in loiterPositionList):
		valFlag = False
		errorMsg = "Error: Invalid loiterPosition.  Valid options include 'beforeTakeoff', 'takeoffAtAlt', 'arrivalAtAlt', and 'afterLand'."

	return [valFlag, errorMsg, warningMsg]

def _valLeafletNodeInputs(leafletIconPrefix, leafletIconType, leafletColor):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		leafletIconPrefix = leafletIconPrefix.lower()
	except:
		pass
			
	try:
		leafletIconType = leafletIconType.lower()
	except:
		pass
				
	if (valFlag == True):
		if (leafletIconPrefix is not None and leafletIconType is not None):
			if (leafletIconPrefix not in leafletIconPrefixList):
				valFlag = False
				errorMsg = "Error: Choose leafletIconPrefix from 'glyphyicon', 'fa', or 'custom'."
			elif (leafletIconPrefix == 'glyphicon'):
				if (leafletIconType not in leafletIconGlyphicon):
					warningMsg += "Warning: leafletIconType value (%s) is not recognized.  It may not be displayed properly.\n" % (leafletIconType)
			elif (leafletIconPrefix == 'fa'):
				if (leafletIconType not in leafletIconFa):
					warningMsg += "Warning: leafletIconType value (%s) is not recognized.  It may not be displayed properly.\n" % (leafletIconType)
			elif (leafletIconPrefix == 'custom'):
				[valFlag, errorMsg, newWarningMsg] = _valLeafletCustomIconType(leafletIconType)
				warningMsg += newWarningMsg
		elif ((leafletIconPrefix is None and leafletIconType is not None) or (leafletIconPrefix is not None and leafletIconType is None)):
			warningMsg += "Warning: Both leafletIconPrefix and leafletIconType must be valid.\n"

	if (valFlag == True and leafletColor is not None):
		if (leafletIconPrefix in ['fa', 'glyphicon']):
			if (leafletColor.lower() not in leafletColorList):
				warningMsg += "Warning: Leaflet color value (%s) is not recognized; it may not be displayed properly.\n" % (leafletColor)
		elif (leafletIconPrefix == 'custom'):
			if (leafletColor.lower() not in matplotlibColorDict.keys()):
				warningMsg += "Warning: Leaflet color value (%s) is not recognized; it may not be displayed properly.\n" % (leafletColor)
			
	return [valFlag, errorMsg, warningMsg]

def _valLeafletArcInputs(leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, leafletCurveType, leafletCurvature):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag == True and leafletColor is not None):
		if (leafletColor.lower() not in leafletColorList):
			[valFlag, errorMsg, newWarningMsg] = _valHexColor(leafletColor)
			warningMsg += newWarningMsg

	if (valFlag == True and leafletWeight is not None):
		[valFlag, warningMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(leafletWeight, "leafletWeight")
		warningMsg += newWarningMsg
	
	if (valFlag == True and leafletStyle is not None):
		if (leafletStyle.lower() not in leafletStyleList):
			valFlag = False
			errorMsg = "Error: Choose leafletStyle from 'solid', 'dashed', and 'dotted'."

	if (valFlag == True and leafletOpacity is not None):
		[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 1, leafletOpacity, 'leafletOpacity')
		warningMsg += newWarningMsg

	if (valFlag == True and useArrows is not None):
		if (type(useArrows) is not bool):
			valFlag = False
			errorMsg = "Error: `useArrows` must be boolean (True or False)."

	if (valFlag and leafletCurveType is not None):
		if (leafletCurveType.lower() not in ['bezier', 'greatcircle', 'straight']):
			valFlag = False
			errorMsg = "Error: curveType must be either 'bezier', 'greatcircle', or 'straight'."

	if (valFlag and leafletCurvature is not None):
		[valFlag, errorMsg, newWarningMsg] = _valBetweenFloat(-90, 90, leafletCurvature, 'leafletCurvature')
		warningMsg += newWarningMsg
			
	return [valFlag, errorMsg, warningMsg]

def _valLeafletBoundingInputs(leafletColor, leafletWeight, leafletStyle, leafletOpacity):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag == True and leafletColor is not None):
		if (leafletColor.lower() not in leafletColorList):
			[valFlag, errorMsg, newWarningMsg] = _valHexColor(leafletColor)
			warningMsg += newWarningMsg

	if (valFlag == True and leafletWeight is not None):
		[valFlag, warningMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(leafletWeight, "leafletWeight")
		warningMsg += newWarningMsg
	
	if (valFlag == True and leafletStyle is not None):
		if (leafletStyle.lower() not in leafletStyleList):
			valFlag = False
			errorMsg = "Error: Choose leafletStyle from 'solid', 'dashed', and 'dotted'."

	if (valFlag == True and leafletOpacity is not None):
		[valFlag, errorMsg, newWarningMsg] = _valBetweenOrEqualToFloat(0, 1, leafletOpacity, 'leafletOpacity')
		warningMsg += newWarningMsg

	return [valFlag, errorMsg, warningMsg]

def _valCesiumNodeInputs(cesiumIconType, cesiumColor):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	try:
		cesiumIconType = cesiumIconType.lower()
	except:
		pass

	if (valFlag == True):
		if (cesiumIconType not in cesiumIconTypeList):
			warningMsg = "Warning: cesiumIconType is not recognized; it may not be displayed properly."

	if (valFlag == True):
		if (expandCesiumColor(cesiumColor) not in cesiumColorList):
			warningMsg = "Warning: cesiumColor is not recognized; it may not be displayed properly."

	return [valFlag, errorMsg, warningMsg]

def _valCesiumArcInputs(cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (valFlag == True):
		if (expandCesiumColor(cesiumColor) not in cesiumColorList):
			warningMsg = "Warning: cesiumColor is not recognized; it may not be displayed properly."

	if (valFlag == True):
		[valFlag, warningMsg, newWarningMsg] = _valGreaterOrEqualToZeroInteger(cesiumWeight, "cesiumWeight")
		warningMsg += newWarningMsg
	
	if (valFlag == True):
		try:
			cesiumStyle = cesiumStyle.lower()
		except:
			pass
			
		if (cesiumStyle not in cesiumStyleList):
			valFlag = False
			errorMsg = "Error: Choose cesiumStyle from 'solid', 'dashed', and 'dotted'."

	if (valFlag == True):
		if not (cesiumOpacity > 0 and cesiumOpacity <=1):
			valFlag = False
			errorMsg = "Error: cesiumOpacity should between 0 and 1."

	return [valFlag, errorMsg, warningMsg]

def _valLeafletCustomIconType(leafletIconType):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	parts = splitLeafletCustomIconType(leafletIconType)

	# first element describes marker size
	[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(parts[0], "iconType first element")

	# second element should be either None or a valid matplotlib color
	if (parts[1] is not None):
		if (valFlag):
			if (parts[1] not in matplotlibColorDict.keys()):
				warningMsg += "Warning: Leaflet color value (%s) is not recognized; it may not be displayed properly.\n" % (parts[1])

			# last element should be a non-negative number
			# only checked if second element is not None
			[valFlag, errorMsg, newWarningMsg] = _valGreaterOrEqualToZeroFloat(parts[2], "iconType third element")

	return [valFlag, errorMsg, warningMsg]

def _valGreaterOrEqualToZeroInteger(number, parameterName):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (number is None):
		valFlag = False
		errorMsg = "Error: %s should not be None." % (parameterName)
	else:
		try:
			float(number)
		except ValueError:
			valFlag = False
			errorMsg = "Error: %s should be an integer number and greater than or equal to 0." % (parameterName)

	if (valFlag):
		if (float(number).is_integer() == False):
			valFlag = False
			errorMsg = "Error: %s should be an integer number and greater than or equal to 0." % (parameterName)	

	if (valFlag):
		if (number < 0):
			valFlag = False
			errorMsg = "Error: %s should be greater or equal to 0." % (parameterName)
	return [valFlag, errorMsg, warningMsg]

def _valGreaterOrEqualToZeroFloat(number, parameterName):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (number is None):
		valFlag = False
		errorMsg = "Error: %s should not be None." % (parameterName)
	else:
		try:
			float(number)
		except ValueError:
			valFlag = False
			errorMsg = "Error: %s should be a float number and greater than or equal to 0." % (parameterName)

	if (valFlag):
		if (number < 0):
			valFlag = False
			errorMsg = "Error: %s should be greater than or equal to 0." % (parameterName)

	return [valFlag, errorMsg, warningMsg]

def _valGreaterThanZeroInteger(number, parameterName):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (number is None):
		valFlag = False
		errorMsg = "Error: %s should not be None." % (parameterName)
	else:
		try:
			float(number)
		except ValueError:
			valFlag = False
			errorMsg = "Error: %s should be an integer number and greater than 0." % (parameterName)

	if (valFlag):
		if (float(number).is_integer() == False):
			valFlag = False
			errorMsg = "Error: %s should be an integer number and greater than 0." % (parameterName)	

	if (valFlag):
		if (number <= 0):
			valFlag = False
			errorMsg = "Error: %s should be greater than 0" % (parameterName)
	return [valFlag, errorMsg, warningMsg]

def _valGreaterThanZeroFloat(number, parameterName):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (number is None):
		valFlag = False
		errorMsg = "Error: %s should not be None." % (parameterName)
	else:
		try:
			float(number)
		except ValueError:
			valFlag = False
			errorMsg = "Error: %s should be a float number and greater than 0." % (parameterName)

	if (valFlag):
		if (number <= 0):
			valFlag = False
			errorMsg = "Error: %s should be greater than 0." % (parameterName)

	return [valFlag, errorMsg, warningMsg]

def _valBetweenOrEqualToInteger(lower, upper, number, parameterName):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (number is None):
		valFlag = False
		errorMsg = "Error: %s should not be None." % (parameterName)
	else:
		try:
			float(number)
		except ValueError:
			valFlag = False
			errorMsg = "Error: %s should be an integer number and greater than 0." % (parameterName)

	if (valFlag):
		if (float(number).is_integer() == False):
			valFlag = False
			errorMsg = "Error: %s should be an integer number and greater than 0." % (parameterName)	

	if (valFlag):
		if (number < lower):
			valFlag = False
			errorMsg = "Error: %s should be an integer number and  greater than or equal to %s." % (parameterName, lower)

	if (valFlag):
		if (number > upper):
			valFlag = False
			errorMsg = "Error: %s should be an integer number and less than or equal to %s." % (parameterName, upper)		

	return [valFlag, errorMsg, warningMsg]

def _valBetweenInteger(lower, upper, number, parameterName):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (number is None):
		valFlag = False
		errorMsg = "Error: %s should not be None." % (parameterName)
	else:
		try:
			float(number)
		except ValueError:
			valFlag = False
			errorMsg = "Error: %s should be an integer number and greater than 0." % (parameterName)

	if (valFlag):
		if (float(number).is_integer() == False):
			valFlag = False
			errorMsg = "Error: %s should be an integer number and greater than 0." % (parameterName)	

	if (valFlag):
		if (number <= lower):
			valFlag = False
			errorMsg = "Error: %s should be an integer number and greater than %s." % (parameterName, lower)

	if (valFlag):
		if (number >= upper):
			valFlag = False
			errorMsg = "Error: %s should be an integer number and less than %s." % (parameterName, upper)		

	return [valFlag, errorMsg, warningMsg]

def _valBetweenOrEqualToFloat(lower, upper, number, parameterName):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (number is None):
		valFlag = False
		errorMsg = "Error: %s should not be None." % (parameterName)
	else:
		try:
			float(number)
		except ValueError:
			valFlag = False
			errorMsg = "Error: %s should be a float number and greater than 0." % (parameterName)

	if (valFlag):
		if (number < lower):
			valFlag = False
			errorMsg = "Error: %s should be a float number and greater than or equal to %s." % (parameterName, lower)

	if (valFlag):
		if (number > upper):
			valFlag = False
			errorMsg = "Error: %s should be a float number and less than or equal to %s." % (parameterName, upper)		

	return [valFlag, errorMsg, warningMsg]

def _valBetweenFloat(lower, upper, number, parameterName):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (number is None):
		valFlag = False
		errorMsg = "Error: %s should not be None." % (parameterName)
	else:
		try:
			float(number)
		except ValueError:
			valFlag = False
			errorMsg = "Error: %s should be float number and greater than 0." % (parameterName)

	if (valFlag):
		if (number <= lower):
			valFlag = False
			errorMsg = "Error: %s should be a float number and greater than %s." % (parameterName, lower)

	if (valFlag):
		if (number >= upper):
			valFlag = False
			errorMsg = "Error: %s should be a float number and less than %s." % (parameterName, upper)		

	return [valFlag, errorMsg, warningMsg]
	
def _valInteger(number, parameterName):
	valFlag = True
	errorMsg = ""
	warningMsg = ""

	if (number is None):
		valFlag = False
		errorMsg = "Error: %s should not be None." % (parameterName)
	else:
		try:
			float(number)
		except ValueError:
			valFlag = False
			errorMsg = "Error: %s should be an integer number." % (parameterName)

	if (valFlag):
		if (float(number).is_integer() == False):
			valFlag = False
			errorMsg = "Error: %s should be an integer number." % (parameterName)

	return [valFlag, errorMsg, warningMsg] 
