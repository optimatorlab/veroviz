from veroviz._common import *
from veroviz._validation import valCreateCesium

from veroviz._deconstructAssignments import deconstructAssignments
from veroviz._internal import delTailSlash
from veroviz._internal import delHeadSlash
from veroviz._internal import addHeadSlash
from veroviz._internal import replaceBackslashToSlash
from veroviz._internal import expandCesiumColor

from veroviz._utilities import privGetMapBoundary
from veroviz._utilities import privExportDataframe

def createCesium(assignments=None, nodes=None, startDate=None, startTime='08:00:00', postBuffer=30, cesiumDir=None, problemDir=None, nodeColor=None, nodeStyle=None, pathColor=None, pathWeight=None, pathStyle=None, pathOpacity=None):
	"""
	This function generates several files required to view a solution in Cesium. The function requires assignments and/or nodes dataframes as input. 

	Parameters
	----------
	assignments: :ref:`Assignments`, Conditional, `assignments` and `nodes` can not be None at the same time
		An :ref:`Assignments` dataframe describing vehicle movement over time.  The assignments will be displayed as routes/paths in Cesium.  If a 3D model is defined in the `modelFile` column of the assignments dataframe, this object will also be displayed.
	nodes: :ref:`Nodes`, Conditional, `assignments` and `nodes` can not be None at the same time
		A :ref:`Nodes` dataframe describing the locations of nodes.  These nodes will be displayed on the map in Cesium.  
	startDate: string, Optional, format is "YYYY-MM-DD", default as today
		Defines the start date to be displayed in Cesium.
	startTime: string, Optional, format is "HH:MM:SS", default as '08:00:00'
		Defines the time at which the Cesium video begins, on the start date.
	postBuffer: int, Optional, default as 30
		Specifies the additional time (in seconds) that the Cesium video will continue to run after the last assignment is completed. 
	cesiumDir: string, Required, default as None
		This should be the full absolute path to the directory where Cesium is installed. For example, for Windows it might be "D:/Cesium"; for Linux it might be "/home/user/Cesium".
	problemDir: string, Required, default as None
		The path name of the generated problem directory. This path is relative to the root of Cesium. For example, if `cesiumDir = '/home/user/Cesium'` and `problemDir = 'veroviz/problems/TSP'` then the files will be generated in the directory `'/home/user/Cesium/veroviz/problems/TSP'`.
	nodeColor: string, Optional, default as None
		Overrides the `cesiumColor` column of the input `nodes` dataframe.  This will define the color of all nodes displayed in Cesium.  See :ref:`Cesium Style` for the collection of available colors. 
	nodeStyle: string, Optional, default as None
		Overrides the `cesiumIconType` column of the input `nodes` dataframe.  Currently, the only option is 'pin'.
	pathColor: string, Optional, default as None
		Overrides the `cesiumColor` column of the input `assignments` dataframe.  This will define the color of all arcs displayed in Cesium.  See :ref:`Cesium Style` for the collection of available colors.
	pathWeight: int, Optional, default as None
		Overrides the `cesiumWeight` column of the input `assignments` dataframe. This will define the weight (in pixels) of all arcs displayed in Cesium. See :ref:`Cesium Style` for more information.
	pathStyle: string, Optional, default as None
		Overrides the `cesiumStyle` column of the input `assignments` dataframe. This will define the style of all arcs displayed in Cesium. See :ref:`Cesium Style` for available options.
	pathOpacity: float in [0, 1], Optional, default as None
		Overrides the `cesiumOpacity` column of the input `assignments` dataframe.  This will define the opacity of all arcs displayed in Cesium.  See :ref:`Cesium Style` for more information.

	Return
	------
	N/A

	Note
	----
	This function generates the following files within the directory specified by input argument `problemDir`:

	- [problemDir].vrv (where [problemDir] is replaced by the value of `problemDir`);
	- config.js
	- displayNodes.js
	- displayPath.js
	- routes.czml

	Instructions for starting Cesium are provided at https://veroviz.org/documentation.html

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
		...     modelFile      = 'veroviz/models/ub_truck.glb',
		...     modelScale     = 80, 
		...     modelMinPxSize = 20, 
		...     startLoc       = list(myNodes.loc[0][['lat', 'lon']].values),
		...     endLoc         = list(myNodes.loc[1][['lat', 'lon']].values),
		...     routeType      = 'euclidean2D',
		...     dataProvider   = None,
		...     speedMPS       = vrv.convertSpeed(55, 'miles', 'hr', 'm', 's'))	
		
	Create Cesium output.
		>>> vrv.createCesium(
		...     assignments = myAssignments, 
		...     nodes       = myNodes, 
		...     startTime   = '08:00:00', 
		...     cesiumDir   = os.environ['CESIUMDIR'],
		...     problemDir  = 'createCesium_example')
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valCreateCesium(assignments, nodes, startDate, startTime, postBuffer, cesiumDir, problemDir, nodeColor, pathColor, pathWeight, pathStyle, pathOpacity)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	# Set default start date as today
	if (startDate is None):
		startDate = datetime.date.today()

	# Some modification about slashes:
	# cesiumDir - no tail slash
	# problemDir - no head slash and no tail slash
	# Change all backslash to slash
	cesiumDir = delTailSlash(cesiumDir)
	problemDir = delTailSlash(problemDir)
	problemDir = delHeadSlash(problemDir)
	cesiumDir = replaceBackslashToSlash(cesiumDir)
	problemDir = replaceBackslashToSlash(problemDir)

	# In case the problemDir does not exist
	fullDir = '%s/%s' % (cesiumDir, problemDir)
	if not os.path.exists(fullDir):
		os.makedirs(fullDir, exist_ok=True)

	# Mission duration, from time zero to endtime+postBuffer
	availStart = _getCesiumTime(startDate, startTime, 0)
	if (assignments is not None):
		availEnd   = _getCesiumTime(startDate, startTime, (max(assignments['endTimeSec']) + postBuffer))
	else:
		availEnd   = _getCesiumTime(startDate, startTime, postBuffer)
		
	# Decode Assignments dataframe to a Path dataframe (with details of a path) and a list of Assignments dataframes, and generate .js and .czml files
	if (assignments is not None):
		[path, lstSubAssignments] = _getPathsDetails(assignments)
		lstNonStationarySubAssignments = deconstructAssignments(assignments=assignments, includeVerticalFlag=True)

		# Update 'intervalStart' and 'intervalEnd' to cesiumTime
		for i in path.index:
			path.at[i, 'intervalStart'] = _getCesiumTime(startDate, startTime, path.at[i, 'startTimeSec'])
			path.at[i, 'intervalEnd'] = _getCesiumTime(startDate, startTime, path.at[i, 'endTimeSec']) if (path.at[i, 'endTimeSec'] >= 0) else availEnd
		path.drop(columns = ['startTimeSec', 'endTimeSec'])
	else:
		path = pd.DataFrame(columns=['objectID', 'czmlID', 'action'])

	# Write problem selector
	_writeSelector(fullDir, problemDir)

	# Write Configs
	mapBoundary = privGetMapBoundary(nodes=nodes, arcs=assignments, locs=None)
	_writeConfigs(mapBoundary, availStart, path, fullDir, problemDir)

	# Write Nodes
	_writeNodes(nodes, nodeColor, fullDir)

	# Write Assignments
	if (len(path) > 0):
		_writeAssignmentsJS(lstNonStationarySubAssignments, pathColor, pathWeight, pathStyle, pathOpacity, fullDir)
		_writeAssignmentsCZML(path, lstSubAssignments, availStart, availEnd, fullDir)
	else:
		_writeEmptyAssignments(fullDir)

	return

def _writeSelector(fullDir, problemDir):

	"""
	This script generates a .vrv file, in index.html, load [problemDir].vrv to load the other files

	Parameters
	----------
	fullDir: string
		The directory of cesium, including the name of the instance.
	problemDir: string
		The name of the instance
	"""

	# Replace "/" with ";"
	replacedDir = addHeadSlash(problemDir)
	replacedDir = replacedDir.replace("/", ";")

	# .vrv file path
	vrvFilePath = '%s/%s.vrv' % (fullDir, replacedDir)
	f = open(vrvFilePath, 'w')

	vrvStr = "~\n"

	f.write(vrvStr)
	f.close()
	if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
		print ("Message: File selector was written to %s ..." % (vrvFilePath))

	return

def _writeConfigs(mapBoundary, availStart, path, fullDir, problemDir):

	"""
	This script generates config.js file

	Parameters
	----------
	mapBoundary: list, the format is [minLon, minLat, maxLon, maxLat]
		The boundary of the map
	availStart: JulianDate
		The start time of entire routing visualization
	path: dataframe
		A list of detail information from `_getPathsDetails()`
	modelIDs: list
		`model` column from path dataframe
	actions: list
		`action` column from path dataframe
	fullDir: string
		The directory of cesium, including the name of the instance.
	problemDir: string
		The name of the instance
	"""
	# Decode
	allIDs = list(dict.fromkeys(path['czmlID'].tolist()))
	orientationIDs = list(dict.fromkeys(path.loc[path['action'] == "move", 'czmlID'].tolist()))
	[[minLat, maxLon], [maxLat, minLon]] = mapBoundary

	# .js file path
	jsFilePath = '%s/config.js' % (fullDir)
	f = open(jsFilePath, 'w')

	# Head description
	jsStr  =         "// This .js file is auto-generated by `createCesium()` from VeRoViz\n"
	jsStr +=         "// The configs for cesium application go to here\n\n"

	# Configuration and load czml file, runRoutes() is defined in index.html
	jsStr +=         "function setConfigs() {\n"

	# Set map boundary
	jsStr +=         "    viewer.camera.flyTo({\n"
	jsStr +=         "        destination: Cesium.Rectangle.fromDegrees(%f, %f, %f, %f) \n" % (minLon, minLat, maxLon, maxLat)
	jsStr +=         "    });\n"

	# Set clock
	jsStr +=         "    viewer.clock.currentTime = Cesium.JulianDate.addSeconds('%s', 0, new Cesium.JulianDate());\n" % (availStart)

	# allIDs and orientationIDs
	jsStr +=         "    allIDs = [\n"
	if (len(allIDs) > 0):
		for i in range(0, len(allIDs)):
			jsStr += "        '%s', \n" % (allIDs[i])
		jsStr = jsStr[:-3]
		jsStr +=     "    \n"
	jsStr +=         "    ];\n"

	jsStr +=         "    orientationIDs = [\n"
	if (len(orientationIDs) > 0):
		for i in range(0, len(orientationIDs)):
			jsStr += "        '%s', \n" % (orientationIDs[i])
		jsStr = jsStr[:-3]
		jsStr +=     "    \n"
	jsStr +=         "    ];\n"

	# load .czml, `runRoutes()` are writen in index.html 
	jsStr +=         "    czmlRouteFile = '%s/routes.czml';\n" % ("/" + problemDir)
	jsStr +=         "    runRoutes(czmlRouteFile, allIDs, orientationIDs);\n"

	# Get all unrepeated objectID, modelID, child model
	# The hierarchy is: objectID (one) - modelID (many), modelID (one) - child model (many)
	# E.g., For drones
	# objectID - UAV, 
	# model - UAV-drone.glb; UAV-drone_package.glb, 
	# child model - 'o-UAV-drone_package.glb-move'; 'o-UAV-drone_package.glb-vertical'; 'o-UAV-drone_package.glb-stationary'
	objectIDs = list(dict.fromkeys(path['objectID'].tolist()))
	for i in range(len(objectIDs)):
		models = list(dict.fromkeys(path.loc[path['objectID'] == objectIDs[i], 'modelFile'].tolist()))
		for j in range(len(models)):
			childModels = list(dict.fromkeys(path.loc[(path['objectID'] == objectIDs[i]) & (path['modelFile'] == models[j]), 'action'].tolist()))
			strChildModels = ""
			for k in range(len(childModels)):
				strChildModels += "'o-%s-%s-%s', " % (str(objectIDs[i]).replace("'", r""), str(models[j]).replace("'", r""), str(childModels[k]).replace("'", r""))
			if (strChildModels != ""):
				strChildModels = strChildModels[:-2]
			jsStr += "objectInfo['%s-%s'] = {\n" % (str(objectIDs[i]).replace("'", r""), str(models[j]).replace("'", r"\'"))
			jsStr += "    label : '%s (%s)', \n" % (str(objectIDs[i]).replace("'", r"\'"), str(models[j]).replace("'", r"\'"))
			jsStr += "    childModels : [%s],\n" % (strChildModels)
			jsStr += "    scale : %s, \n" % (path.loc[(path['objectID'] == objectIDs[i]) & (path['modelFile'] == models[j]), 'modelScale'].tolist()[0])
			jsStr += "    minPxSize : %s \n" %  (path.loc[(path['objectID'] == objectIDs[i]) & (path['modelFile'] == models[j]), 'modelMinPxSize'].tolist()[0])
			jsStr += "}; \n"

	# Register objects
	jsStr +=         "    registerObjects(objectInfo); \n"

	# End of the displayPaths function
	jsStr +=         "}"

	# Write contents and close file stream
	f.write(jsStr)
	f.close()

	if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
		print("Message: Configs were written to %s ..." % (jsFilePath))

	return

def _writeNodes(nodes, cesiumIconColor, fullDir):

	"""
	This script generates displayNodes.js file

	Parameters
	----------
	nodes: :ref:`Nodes`
		Nodes to be appeared in cesium
	cesiumIconColor: string
		The color of nodes when displayed in Cesium. If provided, it will overrides the color in nodes dataframe. One of a collection of pre-specified colors. See :ref:`Cesium Style`
	fullDir: string
		The directory of cesium, including the name of the instance.	
	"""

	# .js file path
	jsFilePath = '%s/displayNodes.js' % (fullDir)
	f = open(jsFilePath, 'w')

	# Head description
	jsStr  =     "// This .js file is auto-generated by `createCesium()` from VeRoViz\n"
	jsStr +=     "// Display nodes for cesium application\n\n"
	
	# Display the nodes
	jsStr +=     "function displayNodes() {\n"
	jsStr +=     "    var pin = new Array;\n"

	if (nodes is not None):
		# In case there are any skipped indices
		indNodes = nodes.copy().reset_index(drop=True)	
		indNodes['cesiumIconText'] = indNodes['cesiumIconText'].astype('string')
		indNodes['popupText'] = indNodes['popupText'].astype('string')
		

		for i in range(0, len(indNodes)):
			popupText = indNodes.iloc[i]['popupText']
			tmpIconText = str(indNodes.iloc[i]['cesiumIconText']).replace("'", r"")

			jsStr += "    pin[%s] = viewer.entities.add({\n" % (i)
			jsStr += "        name : '%s',\n" % (tmpIconText)
			jsStr += "        parent : nodePins,\n"
			if (popupText is not None):
				jsStr += "        description : '%s',\n" % (str(popupText).replace("'", r"\'"))	
			jsStr += "        position : Cesium.Cartesian3.fromDegrees(%s, %s),\n" % (indNodes.iloc[i]['lon'], indNodes.iloc[i]['lat'])
			jsStr += "        billboard : {\n"
			jsStr += "            image : pinBuilder.fromText('%s', %s, 40).toDataURL(),\n" % (tmpIconText, expandCesiumColor(cesiumIconColor) if (cesiumIconColor != None) else expandCesiumColor(indNodes.iloc[i]['cesiumColor']))
			jsStr += "            verticalOrigin : Cesium.VerticalOrigin.BOTTOM, \n"
			jsStr += "            heightReference : Cesium.HeightReference.RELATIVE_TO_GROUND \n"
			jsStr += "        }\n"
			jsStr += "    });\n\n"

	jsStr +=     "}"

	# Write contents and close file stream
	f.write(jsStr)
	f.close()

	if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
		print("Message: Nodes were written to %s ..." % (jsFilePath))

	return

def _writeEmptyAssignments(fullDir):
	"""
	This script generates "empty" routes.czml and displayPaths.js files

	Parameters
	----------
	fullDir: string
		The directory of cesium, including the name of the instance.
	"""
	
	# .czml file path
	czmlFilePath = '%s/routes.czml' % (fullDir)
	f = open(czmlFilePath, 'w')

	czmlStr  = '[ \n'
	czmlStr += '{ \n'
	czmlStr += '    "id": "document", \n'
	czmlStr += '    "version": "1.0" \n'
	czmlStr += '}\n'
	czmlStr += ']'

	# Write contents and close file stream
	f.write(czmlStr)
	f.close()


	# .js file path
	jsFilePath = '%s/displayPaths.js' % (fullDir)
	f = open(jsFilePath, 'w')

	jsStr  = "// This .js file is auto-generated by `createCesium` from VeRoViz\n"
	jsStr += "// Display paths for cesium application\n\n"
	jsStr += "function displayPaths() {\n"
	jsStr += "    // pass \n"
	jsStr += "}"

	# Write contents and close file stream
	f.write(jsStr)
	f.close()

	

def _writeAssignmentsCZML(path, lstSubAssignments, availStart, availEnd, fullDir):

	"""
	This script generates routes.czml file

	Parameters
	----------
	path: path dataframe
		A list of "path", defines the details of each sub-assignments. Each "path" has an origin coordinate and a destinate coordinate, represent a group of assignments (a sub-assignment) with same odID
	lstSubAssignments: list of :ref:`Assignments`
		A list of Assignments dataframe, each dataframe will have the same odID
	availStart: JulianDate
		Start time of entire .czml file
	availEnd: JulianDate
		End time of entire .czml file
	fullDir: string
		The directory of cesium, including the name of the instance.
	"""

	# .czml file path
	czmlFilePath = '%s/routes.czml' % (fullDir)
	f = open(czmlFilePath, 'w')

	# Group the path, so that the path with the same czmlID can ends up with the same block
	czmlIDList = path['czmlID'].tolist()
	czmlIDList = list(dict.fromkeys(czmlIDList))
	lstCzml = []

	for i in range(len(czmlIDList)):
		lstCzml.append(path.loc[path['czmlID'] == czmlIDList[i]])

	# Head of CZML file (can't comment on .czml file so there is no head description)
	czmlStr  =                 '[ \n'
	czmlStr +=                 '{ \n'
	czmlStr +=                 '    "id": "document", \n'
	czmlStr +=                 '    "version": "1.0" \n'
	czmlStr +=                 '}, \n'

	# For each combination of 'objectID', 'modelFile'. 'action', we have a section (in fact we treat a combination of those three fields as unique 'odID')
	for i in range(len(lstCzml)):
		czmlStr +=             '{ \n'
		czmlStr +=             '    "id": "%s", \n' % (str(czmlIDList[i]).replace("'", r""))
		czmlStr +=             '    "name": "%s", \n' % (str(czmlIDList[i]).replace("'", r""))
		czmlStr +=             '    "availability": "%s/%s", \n' % (availStart, availEnd)
		czmlStr +=             '    "model": { \n'
		czmlStr +=             '        "show": true, \n'
		czmlStr +=             '        "gltf": "%s", \n' % (lstCzml[i].iloc[0]['modelFile'])
		czmlStr +=             '        "scale": %d, \n' % (lstCzml[i].iloc[0]['modelScale']/100.0)
		czmlStr +=             '        "minimumPixelSize": %d, \n' % (lstCzml[i].iloc[0]['modelMinPxSize'])
		czmlStr +=             '        "heightReference": "RELATIVE_TO_GROUND" \n'		
		czmlStr +=             '    }, \n'
		czmlStr +=             '    "label": { \n'
		czmlStr +=             '        "fillColor":[{"rgba":[255,255,0,255]}], \n'
		czmlStr +=             '        "font":"bold 10pt Segoe UI Semibold", \n'
		czmlStr +=             '        "horizontalOrigin":"LEFT", \n'
		czmlStr +=             '        "outlineColor":{"rgba":[0,0,0,255]}, \n'
		czmlStr +=             '        "pixelOffset":{"cartesian2":[10.0,0.0]}, \n'
		czmlStr +=             '        "scale":1.0, \n'
		czmlStr +=             '        "show":[{"boolean":false}], \n'
		czmlStr +=             '        "style":"FILL", \n'
		czmlStr +=             '        "text":"Object %s", \n' % (str(lstCzml[i].iloc[0]['objectID']).replace('"', r'\"'))
		czmlStr +=             '        "verticalOrigin":"BOTTOM"\n'
		czmlStr +=             '    }, \n'
		czmlStr +=             '    "path":{ \n'
		czmlStr +=             '        "material":{"solidColor":{"color":{"rgba":[255,255,0,255]}}}, \n'
		czmlStr +=             '        "width":[{"number":2.0}], \n'
		czmlStr +=             '        "show":[{"boolean":false}] \n'
		czmlStr +=             '    }, \n'
		czmlStr +=             '    "position": [ \n'
		for j in range(len(lstCzml[i])):
			if (lstCzml[i].iloc[j]['action'] == "stationary"):
				czmlStr +=     '        { \n'
				czmlStr +=     '            "interval": "%s/%s", \n' % (lstCzml[i].iloc[j]['intervalStart'], lstCzml[i].iloc[j]['intervalEnd'])
				lat = lstSubAssignments[lstCzml[i].iloc[j]['indexInlstShapepoints']].iloc[0]['startLat']
				lon = lstSubAssignments[lstCzml[i].iloc[j]['indexInlstShapepoints']].iloc[0]['startLon']
				alt = lstSubAssignments[lstCzml[i].iloc[j]['indexInlstShapepoints']].iloc[0]['startAltMeters']
				czmlStr +=     '            "cartographicDegrees": [%s, %s, %s] \n' % (lon, lat, alt)
				czmlStr +=     '        }, \n'
			else:
				czmlStr +=     '        { \n'
				czmlStr +=     '            "interval": "%s/%s",\n' % (lstCzml[i].iloc[j]['intervalStart'], lstCzml[i].iloc[j]['intervalEnd'])
				czmlStr +=     '            "interpolationAlgorithm":"LAGRANGE", \n'
				czmlStr +=     '            "interpolationDegree": 1, \n'
				czmlStr +=     '            "epoch": "%s", \n' % (availStart)
				czmlStr +=     '            "cartographicDegrees": [ \n'
				# There will be a list of LLA
				time = lstSubAssignments[lstCzml[i].iloc[j]['indexInlstShapepoints']]['startTimeSec'].tolist()
				lats = lstSubAssignments[lstCzml[i].iloc[j]['indexInlstShapepoints']]['startLat'].tolist()
				lons = lstSubAssignments[lstCzml[i].iloc[j]['indexInlstShapepoints']]['startLon'].tolist()
				alts = lstSubAssignments[lstCzml[i].iloc[j]['indexInlstShapepoints']]['startAltMeters'].tolist()
				for k in range(0, len(lats)):
					czmlStr += '                %.2f, %f, %f, %f, \n' % (time[k], lons[k], lats[k], alts[k])
				lastTime = lstSubAssignments[lstCzml[i].iloc[j]['indexInlstShapepoints']].iloc[-1]['endTimeSec']
				lastLat = lstSubAssignments[lstCzml[i].iloc[j]['indexInlstShapepoints']].iloc[-1]['endLat']
				lastLon = lstSubAssignments[lstCzml[i].iloc[j]['indexInlstShapepoints']].iloc[-1]['endLon']
				lastAlt = lstSubAssignments[lstCzml[i].iloc[j]['indexInlstShapepoints']].iloc[-1]['endAltMeters']
				czmlStr +=     '                %.2f, %f, %f, %f \n' % (lastTime, lastLon, lastLat, lastAlt)

				czmlStr +=     '\n'
				czmlStr +=     '            ] \n'
				czmlStr +=     '        }, \n'
		czmlStr = czmlStr[:-3]
		czmlStr +=             '\n'
		czmlStr +=             '    ]\n'
		czmlStr +=             '}, \n'
	czmlStr = czmlStr[:-3]
	czmlStr +=                 '\n'

	# Closing bracket for entire .czml file
	czmlStr +=                 ']'

	# Write contents and close file stream
	f.write(czmlStr)
	f.close()

	if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
		print("Message: Assignments (.czml) were written to %s ..." % (czmlFilePath))

	return

def _writeAssignmentsJS(lstSubAssignments, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity, fullDir):

	"""
	This script generates the displayPaths.js file

	Parameters
	----------
	lstSubAssignments: list of :ref:`Assignments`
		A list of Assignments dataframes, each dataframe will have the same odID
	cesiumColor: string
		The color of arcs when displayed in Cesium. If provided, it will overrides the color in assignments dataframe. One of a collection of pre-specified colors. See :ref:`Cesium Style`
	cesiumWeight: int
		The weight of arcs when displayed in Cesium. If provided, it will overrides the weight in assignments dataframe. See :ref:`Cesium Style`
	cesiumStyle: string
		The style of arcs when displayed in Cesium. If provided, it will overrides the style in assignments dataframe. See :ref: `Cesium style`
	cesiumOpacity: string
		The opacity of arcs when displayed in Cesium. If provided, it will overrides the opacity in assignments dataframe. See :ref: `Cesium style`
	fullDir: string
		The directory of cesium, including the name of the instance.
	"""

	# .js file path
	jsFilePath = '%s/displayPaths.js' % (fullDir)
	f = open(jsFilePath, 'w')

	# Head description
	jsStr  =             "// This .js file is auto-generated by `createCesium` from VeRoViz\n"
	jsStr +=             "// Display paths for cesium application\n\n"

	# Begin of the displayPaths function
	jsStr +=             "function displayPaths() {\n"

	# Collect all moving objects ID for path names
	movingObjects = []
	for i in range(len(lstSubAssignments)):
		newObjectID = str(lstSubAssignments[i].iloc[0]['objectID'])
		newObjectID = newObjectID.replace("'", r"")
		newObjectID = newObjectID.replace('"', r'')
		if (newObjectID not in movingObjects):
			movingObjects.append(newObjectID)
	strMovingObjects = ""
	for i in range(len(movingObjects)):
		strMovingObjects += "'%s', " % (movingObjects[i])
	strMovingObjects = strMovingObjects[:-2]
	jsStr +=             "    var pathNames = [%s]; \n" % (strMovingObjects)

	# Register paths
	jsStr +=             "    registerPaths(pathNames); \n"

	# For each `odID`, draw a polyline
	for i in range(len(lstSubAssignments)):
		# Get the lat/lon/alt for each waypoint, (polygon in 3D)
		lstSubAssignments[i] = lstSubAssignments[i].reset_index(drop=True)
		assignmentLats = []
		assignmentLons = []
		assignmentAltMeters = []
		assignmentLats.append(lstSubAssignments[i]['startLat'][0])
		assignmentLons.append(lstSubAssignments[i]['startLon'][0])
		assignmentAltMeters.append(lstSubAssignments[i]['startAltMeters'][0])
		assignmentLats.extend(lstSubAssignments[i]['endLat'].tolist())
		assignmentLons.extend(lstSubAssignments[i]['endLon'].tolist())
		assignmentAltMeters.extend(lstSubAssignments[i]['endAltMeters'].tolist())

		assignmentDimension = 3
		if (max(assignmentAltMeters) == 0 and min(assignmentAltMeters) == 0):
			assignmentDimension = 2
		else:
			assignmentDimension = 3

		# Check if cesium styles have been overridden, if not, assume that for entire path the style is the same
		if (cesiumColor != None):
			color = expandCesiumColor(cesiumColor)
		else:
			color = expandCesiumColor(lstSubAssignments[i].iloc[0]['cesiumColor'])
		if (cesiumWeight != None):
			weight = cesiumWeight
		else:
			weight = lstSubAssignments[i].iloc[0]['cesiumWeight']
		if (cesiumOpacity != None):
			opacity = cesiumOpacity
		else:
			opacity = lstSubAssignments[i].iloc[0]['cesiumOpacity']
		if (cesiumStyle != None):
			style = cesiumStyle
		else:
			style = lstSubAssignments[i].iloc[0]['cesiumStyle']

		try:
			style = style.lower()
		except:
			pass
			
		if (style == 'dashed'):
			dashLength = 40
		elif (style == 'dotted'):
			dashLength = 10
		elif (style == 'solid'):
			dashLength = 0

		popupText = str(lstSubAssignments[i].iloc[0]['popupText']).replace("'", r"\'")
		tmpObjectID = str(lstSubAssignments[i].iloc[0]['objectID']).replace("'", r"")
		
		if (assignmentDimension == 3):
			# For each path, generate one polyline entity
			jsStr +=     "    paths[%d] = viewer.entities.add({\n" % (i)
			jsStr +=     "        parent: vehiclePolylines['%s'],\n" % (tmpObjectID)
			jsStr +=     "        name: 'Objects %s',\n" % (tmpObjectID)
			if (popupText is not None):
				jsStr +=     "        description: '%s',\n" % (popupText)
			jsStr +=     "        polyline: {\n"
			jsStr +=     "            positions: Cesium.Cartesian3.fromDegreesArrayHeights([\n"
			for j in range(0, len(assignmentLats)):
				jsStr += "                %f, %f, %f, \n" % (assignmentLons[j], assignmentLats[j], assignmentAltMeters[j])
			jsStr = jsStr[:-3]
			jsStr +=     "            \n"
			jsStr +=     "            ]),\n"
			jsStr +=     "            width: %d, \n" % (weight)
			jsStr +=     "            material: new Cesium.PolylineDashMaterialProperty({\n"
			jsStr +=     "                dashLength: %f,\n" % (dashLength)
			jsStr +=     "                color: %s.withAlpha(%f)\n" % (color, opacity)
			jsStr +=     "            })\n"
			jsStr +=     "        }\n"
			jsStr +=     "    });\n"
		elif (assignmentDimension == 2):
			# For each path, generate one polyline entity
			jsStr +=     "    paths[%d] = viewer.entities.add({\n" % (i)
			jsStr +=     "        parent: vehiclePolylines['%s'],\n" % (tmpObjectID)
			jsStr +=     "        name: 'Objects %s',\n" % (tmpObjectID)
			jsStr +=     "        polyline: {\n"
			jsStr +=     "            positions: Cesium.Cartesian3.fromDegreesArray([\n"
			for j in range(0, len(assignmentLats)):
				jsStr += "                %f, %f, \n" % (assignmentLons[j], assignmentLats[j])
			jsStr = jsStr[:-3]
			jsStr +=     "            \n"
			jsStr +=     "            ]),\n"
			jsStr +=     "            clampToGround: true, \n"
			jsStr +=     "            width: %d, \n" % (weight)
			jsStr +=     "            material: new Cesium.PolylineDashMaterialProperty({\n"
			jsStr +=     "                dashLength: %f,\n" % (dashLength)
			jsStr +=     "                color: %s.withAlpha(%f)\n" % (color, opacity)
			jsStr +=     "            })\n"
			jsStr +=     "        }\n"
			jsStr +=     "    });\n"

	# End of the displayPaths function
	jsStr +=             "}"

	# Write contents and close file stream
	f.write(jsStr)
	f.close()

	if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
		print("Message: Assignments (.js) were written to %s ..." % (jsFilePath))

	return

def _getCesiumTime(startDate, startTime, timeSec):
	"""
	This script gives a JulianDate format time for cesium

	Parameters
	----------
	startDate: string, format is "YYYY-MM-DD", default as today
		The start date of the video generated
	startTime: string, format is "HH:MM:SS", default as '08:00:00'
		The start time of the start date
	timeSec: float
		Time past after start time

	Return
	------
	JulianDate
		Time in JulianDate format
	"""

	# Set time zero
	timeZero = dateutil.parser.parse("%s %s" % (startDate, startTime))

	# Return timeSec in cesium format (semi-Julian format)
	cesiumTime = datetime.datetime.strftime(timeZero + datetime.timedelta(seconds = float(timeSec)), '%Y-%m-%dT%H:%M:%SZ')

	return cesiumTime

def _getAction(subAssignments):

	"""
	Given a group of assignments with same odID, find if this group is stationary/vertical/move.  Each will be treated differently in cesium and folium.

	Parameters
	----------
	subAssignments: :ref:`Assignments`
		An assignment dataframe with the same odID

	Return
	------
	string
		An enumerate string, out put can be 'stationary'/'vertical'/'move'
	"""

	# if it is static or vertical, there should (must) be one row for correspondence `odID`
	if (len(subAssignments) == 1):
		if (subAssignments.iloc[0]['startLat'] == subAssignments.iloc[0]['endLat']
			and subAssignments.iloc[0]['startLon'] == subAssignments.iloc[0]['endLon']
			and subAssignments.iloc[0]['startAltMeters'] == subAssignments.iloc[0]['endAltMeters']):
			action = "stationary"
		elif (subAssignments.iloc[0]['startLat'] == subAssignments.iloc[0]['endLat']
			and subAssignments.iloc[0]['startLon'] == subAssignments.iloc[0]['endLon']
			and subAssignments.iloc[0]['startAltMeters'] != subAssignments.iloc[0]['endAltMeters']):
			action = "vertical"
		else:
			action = "move"
	else:
		action = "move"

	return action

def _getPathsDetails(assignments):

	"""
	Given an Assignments dataframe, this script deconstruct it into a list of assignments(or called subAssignments) each subAssignment will have: the same odID; same type of movement(stationary/vertical/move)

	Parameters
	----------
	assignments: :ref:`Assignments`, Required
		The Assignments dataframe to be deconstructed into lists

	Returns
	-------
	path: Path dataframe
		A list of description of each subAssignment
	lstSubAssignments: list of :ref:`Assignments`
		A list of Assignments dataframe each with the same odID

	"""

	# Icon list
	modelWithDuplicates = assignments['modelFile'].tolist()
	uniqueIconList = list(dict.fromkeys(modelWithDuplicates))

	# Get path list from assignments dataframe
	lstSubAssignments = deconstructAssignments(assignments=assignments, includeStationaryFlag=True, includeVerticalFlag=True)

	# Now we prepare for .czml.
	# First, create a list of dictionaries, to eventually populate a Path Dataframe, which has the same length as lstSubAssignments
	pathList = []
	
	for i in range(len(lstSubAssignments)):
		tmpObjectID = str(lstSubAssignments[i].iloc[0]['objectID']).replace("'", r"")
		pathList.append({
			'odID': lstSubAssignments[i].iloc[0]['odID'],
			'czmlID': 'o-%s-%s-%s' % (tmpObjectID, lstSubAssignments[i].iloc[0]['modelFile'], _getAction(lstSubAssignments[i])),
			'objectID': lstSubAssignments[i].iloc[0]['objectID'],
			'modelFile': lstSubAssignments[i].iloc[0]['modelFile'],
			'action': _getAction(lstSubAssignments[i]),
			'modelScale': lstSubAssignments[i].iloc[0]['modelScale'],
			'modelMinPxSize': lstSubAssignments[i].iloc[0]['modelMinPxSize'],
			'startTimeSec': lstSubAssignments[i].iloc[0]['startTimeSec'],
			'endTimeSec': lstSubAssignments[i].iloc[-1]['endTimeSec'],
			'intervalStart': "",
			'intervalEnd': "",
			'indexInlstShapepoints': i
			})


	path = pd.DataFrame(pathList)
	path.sort_values('odID', ascending=True)

	return [path, lstSubAssignments]
