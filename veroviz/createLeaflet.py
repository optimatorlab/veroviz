from veroviz._common import *
from veroviz._validation import valCreateLeaflet
from veroviz._validation import valAddLeafletCircle
from veroviz._validation import valAddLeafletMarker
from veroviz._validation import valAddLeafletPolygon
from veroviz._validation import valAddLeafletPolyline
from veroviz._validation import valAddLeafletText
from veroviz._validation import valAddLeafletIcon
from veroviz._validation import valAddLeafletIsochrones
from veroviz._validation import valAddLeafletWeather
from veroviz._internal import replaceBackslashToSlash
from veroviz._internal import splitLeafletCustomIconType

from veroviz._deconstructAssignments import deconstructAssignments

from veroviz._createEntitiesFromList import privCreateArcsFromLocSeq

from veroviz._utilities import privGetMapBoundary

from veroviz._geometry import geoDistancePath2D
from veroviz._geometry import geoMileageInPath2D
from veroviz._geometry import geoDistance2D
from veroviz._geometry import geoGetHeading
from veroviz._geometry import geoPointInDistance2D

foliumMaps = {
	'cartodb positron': {'attr': '&copy; CARTO'},  
	'cartodb dark_matter':  {'attr': '&copy; CARTO'}, 
	'openstreetmap':  {'attr': '&copy; OpenStreetMap contributors'},
	'stamen terrain':  {'attr': '&copy; Stadia Maps &copy; Stamen Design &copy; OpenMapTiles &copy; OpenStreetMap contributors'},
	'stamen toner':  {'attr': '&copy; Stadia Maps &copy; Stamen Design &copy; OpenMapTiles &copy; OpenStreetMap contributors'},
	'stamen watercolor':  {'attr': '&copy; Stadia Maps &copy; Stamen Design &copy; OpenStreetMap contributors'}
}

weatherMaps = {
	'clouds': {
		'tiles': 'https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=',
		'attr': 'openweathermap.org'
	},
	
	'precip': { 
		'tiles': 'https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=',
		'attr': 'openweathermap.org'
	},

	'pressure': { 
		'tiles': 'https://tile.openweathermap.org/map/pressure_new/{z}/{x}/{y}.png?appid=',
		'attr': 'openweathermap.org'
	},
		
	'wind': {
		'tiles': 'https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=',	
		'attr': 'openweathermap.org'
	},

	'temp': {
		'tiles': 'https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=',
		'attr': 'openweathermap.org'
	}
}



customMaps = {
	'arcgis aerial': {
		'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
		'attr': 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
	},

	'arcgis gray': {
		'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
		'attr': 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
	},

	'arcgis ocean': {
		'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}',
		'attr': 'Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri'
	},

	'arcgis roadmap': {
		'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
		'attr': 'Tiles &copy; Esri &mdash; Source: Esri'
	},

	'arcgis shaded relief': {
		'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}',
		'attr': 'Tiles &copy; Esri &mdash; Source: Esri'
	},

	'arcgis topo': {
		'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
		'attr': 'Tiles &copy; Esri &mdash; Source: Esri'
	},

	'open topo': {
		'tiles': 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
		'attr': 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
	},
}
	
def createLeaflet(mapObject=None, mapFilename=None, mapBackground=config['VRV_DEFAULT_LEAFLET_MAPTILES'], mapBoundary=None, zoomStart=None, nodes=None, iconPrefix=None, iconType=None, iconColor=None, iconText=None, arcs=None, arcWeight=None, arcStyle=None, arcOpacity=None, arcCurveType=None, arcCurvature=None, arcColor=None, useArrows=None, arrowsPerArc=1, boundingRegion=None, boundingWeight=config['VRV_DEFAULT_LEAFLETBOUNDINGWEIGHT'], boundingOpacity=config['VRV_DEFAULT_LEAFLETBOUNDINGOPACITY'], boundingStyle=config['VRV_DEFAULT_LEAFLETBOUNDINGSTYLE'], boundingColor=config['VRV_DEFAULT_LEAFLETBOUNDINGCOLOR']):

	"""
	createLeaflet is used to generate Leaflet objects using folium. The function takes a boundingRegion polygon, `Nodes`, `Arcs`, and `Assignments` dataframes as inputs, and creates a folium/leaflet map showing boundings, nodes and/or arcs. 

	Parameters
	----------
	mapObject: Folium object, Optional, default as None
		If you already have a map (as a Folium object), you can provide that object and add content to that map.
	mapFilename: string, Optional, default as None
		This is the name of the map file that will be created (e.g., "../output/map.html" or "map.html").  The filename should have a `.html` extension.  If `mapFilename` is not provided, no map file will be generated.  The returned map object can be viewed within a Jupyter notebook.
	mapBackground: string, Optional, default as 'CartoDB positron'
		Sets the background tiles of the map.  See :ref:`Leaflet Style` for the list of options.
	mapBoundary: list of lists, Optional, default as None
		Allows customization of the zoom level.  If a map boundary is provided, the zoom level will correspond to the rectangle defined by the two map boundary points. This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  Must be in the form [[south lat, west lon], [north lat, east lon]].
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	nodes: :ref:`Nodes`, Conditional, `nodes`, `arcs`, and `boundingRegion` can not be None at the same time
		A Nodes dataframe describing the collection of nodes to be displayed on the Leaflet map.  See :ref:`Nodes` for documentation on this type of dataframe.
	iconPrefix: string, Optional, default as None
		Overrides the `leafletIconPrefix` column of an input :ref:`Nodes` dataframe.  If provided, all nodes will use this icon prefix.  Valid options are "glyphicon", "fa", or "custom". See :ref:`Leaflet Style` for details.
	iconType: string, Optional, default as None
		Overrides the `leafletIconType` column of an input :ref:`Nodes` dataframe.  If provided, all nodes will use this icon type.  The valid `iconType` options depend on the choice of `iconPrefix`.  See :ref:`Leaflet Style` for the collection of valid icon prefix/type combinations.
	iconColor: string, Optional, default as None
		Overrides the `leafletColor` column of an input :ref:`Nodes` dataframe.  If provided, all icons will use this color when displayed on this Leaflet map.  See :ref:`Leaflet Style` for the list of available color options.
	iconText: string, Optional, default as None
		Overrides the `leafletIconText` column of an input :ref:`Nodes` dataframe.  If provided, this text will be displayed within the node on a Leaflet map.  This text will only be shown if `leafletIconPrefix` is 'custom' and `leafletIconType` includes a font color and font size.  A value of None will result in the node ID being displayed in the node.  See :ref:`Leaflet style`.
	arcs: :ref:`Arcs` or :ref:`Assignments`, Conditional, `nodes`, `arcs` and `boundingRegion` can not be None at the same time
		An :ref:`Arcs` or :ref:`Assignments` dataframe describing vehicle routes.  Each row of this dataframe will be shown as a line on the Leaflet map.  See the documentation on :ref:`Arcs` and :ref:`Assignments` for more information.
	arcWeight: int, Optional, default as None
		Overrides the `leafletWeight` column of an input :ref:`Arcs` or :ref:`Assignments` dataframe.  If provided, all arcs will be displayed with this line thickness (in pixels).  
	arcStyle: string, Optional, default as None
		Overrides the `leafletStyle` column of an input :ref:`Arcs` or :ref:`Assignments` dataframe. If provided, all arcs will be displayed with this type.  Valid options are 'solid', 'dotted', or 'dashed'.  See :ref:`Leaflet Style` for more information.
	arcOpacity: float in [0, 1], Optional, default as None
		Overrides the `leafletOpacity` column of an input :ref:`Arcs` or :ref:`Assignments` dataframe.  If provided, each arc will be displayed with this opacity.  Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	arcColor: string, Optional, default as None
		Overrides the `leafletColor` column of an input :ref:`Arcs` or :ref:`Assignments` dataframe.  If provided, all arcs will be displayed with this color.  See :ref:`Leaflet Style` for a list of available colors.
	arcCurveType: string, Optional, default as 'straight'
		Choose the type of curve to be shown on leaflet map for :ref:`Arcs` dataframe (curves will not be applied to :ref:`Assignments` dataframes). The options are `Bezier`, `greatcircle`, and 'straight'. If `Bezier` is provided, the `arcCurvature` should not be None, leaflet will draw a Bezier curve between given nodes. If `greatcircle` is provided, the curve will go along with the surface of the Earth.
	arcCurvature: float in (-90, 90), Conditional, default as 45
		If choose `Bezier` as `arcCurveType`, then `arcCurvature` is required; otherwise this argument will not be used. The meaning of this argument is as following: link two nodes using straight line, the degrees between this straight line and the curve at two nodes is this argument, therefore it should be greater or equal to 0 and less than 90. A degree between -45 and 45 is recommended.		
	useArrows: boolean, Optional, default as None
		Indicates whether arrows should be shown on all arcs on the Leaflet map.
	arrowsPerArc: int, Optional, default as 1
		Number of arrows display on each arc, should be integer greater than 0. Each arc will have the same number of arrows, regardless of arc length. If useArrows is False, this parameter will be ignored (i.e., no arrows will be drawn).
	boundingRegion: list of lists, Conditional, `nodes`, `arcs` and `boundingRegion` can not be None at the same time
		A sequence of lat/lon coordinates defining a boundary polygon. The format is [[lat, lon], [lat, lon], ..., [lat, lon]].
	boundingWeight: int, Optional, default as 3
		Specifies the weight (in pixels) of the line defining the `boundingRegion` (if provided) when displayed in Leaflet.
	boundingStyle: string, Optional, default as 'dashed'
		Specifies the line style of the `boundingRegion` (if provided).  Valid options are 'solid', 'dotted', 'dashed'.  See :ref:`Leaflet Style` for more information.
	boundingOpacity: float in [0, 1], Optional, default as 0.6
		Specifies the opacity of the `boundingRegion` (if provided) when displayed in Leaflet.  Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	boundingColor: string, Optional, default as 'brown'
		Specifies the line color of the `boundingRegion` (if provided) when displayed in Leaflet. See :ref:`Leaflet Style` for a list of available colors.

	Return
	------
	Folium object
		A new/updated map that displays the nodes, arcs, and/or bounding region.

	Examples
	--------
	First, import veroviz and check the latest version
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Now, generate some example nodes inside a bounding region
		>>> bounding = [
		...     [42.98355351219673, -78.90518188476564], 
		...     [43.04731443361136, -78.83857727050783], 
		...     [43.02221961002041, -78.7108612060547], 
		...     [42.92777124914475, -78.68957519531251], 
		...     [42.866402688514626, -78.75343322753908], 
		...     [42.874957707517865, -78.82415771484375], 
		...     [42.90111863978987, -78.86878967285158], 
		...     [42.92224052343343, -78.8921356201172]]

		>>> exampleNodes = vrv.generateNodes(
		...     nodeType         = 'customer', 
		...     nodeDistrib      = 'normalBB', 
		...     nodeDistribArgs  = {
		...         'center'         : [42.90, -78.80], 
		...         'stdDev'         : 10000,
		...         'boundingRegion' : bounding
		...     },
		...     numNodes         = 3,
		...     leafletColor     = 'orange')

	The first example is using all default setting for generating a set of given nodes in Nodes dataframe.
		>>> vrv.createLeaflet(nodes=exampleNodes)

	Define some arcs based on the nodes we just generated:
		>>> exampleArcs = vrv.createArcsFromNodeSeq(
		...     nodes   = exampleNodes,
		...     nodeSeq = [1, 2, 3])
		>>> exampleArcs

	Display the nodes, arcs, and bounding region simultaneously:
		>>> vrv.createLeaflet(
		...     nodes          = exampleNodes,
		...     arcs           = exampleArcs,
		...     boundingRegion = bounding)

	The createLeaflet function provides options to override styles that were defined in the input nodes and/or arcs dataframes.  Note:  These overrides will not change the contents in the dataframes.
		>>> nodesAndArcsMap = vrv.createLeaflet(
		...     nodes      = exampleNodes,
		...     iconPrefix = 'fa',
		...     iconType   = 'car',
		...     iconColor  = 'blue',
		...     arcs       = exampleArcs,
		...     arcStyle   = 'dotted')
		>>> nodesAndArcsMap

	If you already have a folium map object, you can add more into it.
	Here, we add a bounding region to the `nodesAndArcsMap` object defined above.
		>>> nodesAndArcsMap = vrv.createLeaflet(
		...     mapObject      = nodesAndArcsMap,
		...     boundingRegion = bounding)
		>>> nodesAndArcsMap
		
	A new collection of nodes is defined here:
		>>> newNodes = vrv.generateNodes(
		...     nodeType        = 'customer', 
		...     nodeDistrib     = 'uniformBB', 
		...     nodeDistribArgs = {
		...         'boundingRegion' : bounding
		...     },
		...     numNodes        = 4,
		...     leafletColor    = 'red')
		>>> newNodes
		
	We will add these nodes to our existing map,
	but we're overriding these new nodes with a green color:	
	Notice that the addition of new entities will not change the style of previous entities that were already added into the map.
		>>> newMapWithArcsAndMoreNodes = vrv.createLeaflet(
		...     mapObject = nodesAndArcsMap,
		...     nodes     = newNodes,
		...     iconColor = 'green')
		>>> newMapWithArcsAndMoreNodes

	The following example includes all of the function arguments.
		>>> vrv.createLeaflet(
		...     mapObject       = None, 
		...     mapFilename     = 'example.html', 
		...     mapBackground   = 'CartoDB positron', 
		...     mapBoundary     = None, 
		...     zoomStart       = 10, 
		...     nodes           = exampleNodes, 
		...     iconPrefix      = 'fa', 
		...     iconType        = 'flag', 
		...     iconColor       = 'red', 
		...     iconText        = 'Here are some nodes', 
		...     arcs            = exampleArcs, 
		...     arcWeight       = 5, 
		...     arcStyle        = 'dashed', 
		...     arcOpacity      = 1, 
		...     arcColor        = 'green', 
		...     useArrows       = True, 
		...     boundingRegion  = bounding, 
		...     boundingWeight  = 1, 
		...     boundingOpacity = 0.8, 
		...     boundingStyle   = 'dotted', 
		...     boundingColor   = 'black')
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valCreateLeaflet(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, nodes, iconPrefix, iconType, iconColor, iconText, arcs, arcWeight, arcStyle, arcOpacity, arcColor, arcCurveType, arcCurvature, useArrows, arrowsPerArc, boundingRegion, boundingWeight, boundingOpacity, boundingStyle, boundingColor)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	# Replace backslash
	mapFilename = replaceBackslashToSlash(mapFilename)



	# If no mapObject exists, define a new mapObject
	if (mapObject == None):
		# Adjust the scope of the map to proper bounds
		if (nodes is None and arcs is None and boundingRegion is None):
			[midLat, midLon] = [0, 0]
		else:
			[[minLat, maxLon], [maxLat, minLon]] = privGetMapBoundary(nodes, arcs, boundingRegion)
			midLat = (maxLat + minLat) / 2.0
			midLon = (maxLon + minLon) / 2.0
		mapObject = _createLeafletMap(mapBackground=mapBackground, center=[midLat,midLon], zoomStart=zoomStart)

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)
		elif (mapBoundary is None):
			if (nodes is not None or arcs is not None or boundingRegion is not None):
				mapObject.fit_bounds(privGetMapBoundary(nodes, arcs, boundingRegion))
		
	# Plot arcs
	if (type(arcs) is pd.core.frame.DataFrame):
		mapObject = _createLeafletArcs(mapObject, arcs, arcWeight, arcOpacity, arcStyle, arcColor, arcCurveType, arcCurvature, useArrows, config['VRV_DEFAULT_LEAFLET_ARROWSIZE'], arrowsPerArc)	
	
	# Plot bounding
	if (type(boundingRegion) is list):
		mapObject = _createLeafletBoundingRegion(mapObject, boundingRegion, boundingWeight, boundingOpacity, boundingStyle, boundingColor)

	# Plot node markers
	if (type(nodes) is pd.core.frame.DataFrame):
		mapObject = _createLeafletNodes(mapObject, nodes, iconPrefix, iconType, iconColor, iconText)

	if (mapFilename is not None):		
		mapDirectory = ""
		strList = mapFilename.split("/")
		for i in range(len(strList) - 1):
			mapDirectory += strList[i] + "/"
		if (mapDirectory != ""):
			if (not os.path.exists(mapDirectory)):
				os.makedirs(mapDirectory, exist_ok=True)

		mapObject.save(mapFilename)
		if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
			print("Message: Map page written to %s." % (mapFilename))
	
	return mapObject

def _createLeafletMap(mapBackground=config['VRV_DEFAULT_LEAFLET_MAPTILES'], center=[0,0], zoomStart=None):

	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	# Define a new mapObject
	mapObject = folium.Map(
		location   = center, 
		zoom_start = zoomStart if (zoomStart != None) else 3, 
		tiles      = None)
	
	# Add the chosen map background first:
	if (mapBackground in foliumMaps):
		folium.TileLayer(mapBackground, attr=foliumMaps[mapBackground]['attr']).add_to(mapObject)
	elif (mapBackground in customMaps):
		folium.TileLayer(tiles=customMaps[mapBackground]['tiles'],
						 attr=customMaps[mapBackground]['attr']).add_to(mapObject)
	
	'''
	# Now, loop over our other map background options (excluding the chosen one):
	for (mBG in foliumMaps):
		if (mBG != mapBackground):
			folium.TileLayer(mBG).add_to(mapObject)
	for (mBG in customMaps):
		if (mBG != mapBackground):
			folium.TileLayer(tiles=customMaps[mBG]['tiles'],
							 attr=customMaps[mBG]['attr'],
							 name=mBG).add_to(mapObject)
	'''
	
	return mapObject

def _createLeafletNodes(mapObject=None, nodes=None, iconPrefix=None, iconType=None, iconColor=None, iconText=None):
	"""
	A sub-function to create leaflet nodes

	Parameters
	----------
	mapObject: Folium object, Required
		Add content to a folium map.
	nodes: :ref:`Nodes`, Required
		The Nodes dataframe to be generated in Leaflet
	iconPrefix: string, Optional
		The collection of Leaflet icons.  Options are "glyphicon", "fa", or "custom". See :ref:`Leaflet Style`
	iconType: string, Optional
		The specific icon to be used for all generated nodes.  The list of available options depends on the choice of the iconType. See :ref:`Leaflet Style`
	iconColor: string, Optional
		The icon color of the generated nodes when displayed in Leaflet.  One of a collection of pre-specified colors. See :ref:`Leaflet Style`
	iconText: string, Optional
		Text that will be displayed within the node on a Leaflet map.  This text will only be shown if `iconPrefix` is 'custom' and `iconType` includes a font color and font size.  A value of None will result in the node ID being displayed in the node.  See :ref:`Leaflet style`.

	return
	------
	Folium object
		A new/updated map that contains the nodes

	"""

	# Note: In nodes dataframe, we already checked 'leaflet-' columns, and those columns have default values, for sake of consistency in here I delete the 'failsafes'
	for i in range(0, len(nodes)):
		# If not overridden, use the info in nodes dataframe
		if (iconColor == None):
			newColor = nodes.iloc[i]['leafletColor']
		else:
			newColor = iconColor
			
		if ((iconPrefix == None) or (iconType == None)):
			newPrefix = nodes.iloc[i]['leafletIconPrefix']
			newType = nodes.iloc[i]['leafletIconType']
		else:
			newPrefix = iconPrefix
			newType = iconType

		if (iconText == None):
			newText = nodes.iloc[i]['leafletIconText']
		else:
			newText = iconText

		if (newColor != None):
			newColor = newColor.lower()
		if (newPrefix != None):
			newPrefix = newPrefix.lower()
		if (newType != None):
			newType = newType.lower()
			
		_drawLeafletNode(mapObject, [nodes.iloc[i]['lat'], nodes.iloc[i]['lon']], nodes.iloc[i]['popupText'], newPrefix, newType, newColor, newText)

	return mapObject


def _drawLeafletNode(mapObject, loc, popupText, iconPrefix, iconType, iconColor, iconText):
	
	# Format popup text
	if (popupText is not None):
		popupText = str(popupText)

	if (iconPrefix in ['fa', 'glyphicon']):
		# Folium draw nodes
		folium.Marker(
			loc, 
			icon=folium.Icon(
				color = iconColor.lower(), 
				prefix = iconPrefix.lower(), 
				icon = iconType.lower()), 
			popup=popupText
		).add_to(mapObject)
	else:
		[radius, fontColor, fontSize] = splitLeafletCustomIconType(iconType)
		
		# Add marker:
		folium.CircleMarker(
			loc, 
			radius = radius,  
			stroke = True, 
			weight = 1, 
			color = iconColor.lower(), 
			fill_color = iconColor.lower(),
			fill_opacity = 0.9,
			popup = popupText
			).add_to(mapObject)

		# Add text:
		if ((iconText is not None) and (fontColor is not None)):
			try:
				fontColor = fontColor.lower()
			except:
				pass

			iconSizeX = radius*2		# FIXME -- Not sure if this is good.
			iconAnchorX = iconSizeX / 2
				
			folium.map.Marker(loc, popup=popupText, icon=DivIcon(
				icon_size = (iconSizeX, fontSize), 
				icon_anchor = (iconAnchorX, fontSize), 
				html = "<div style=\"font-size: %dpt; color: %s; text-align: center;\">%s</div>" %  (fontSize, fontColor, iconText)
				)).add_to(mapObject)

	return

def _createLeafletArcs(mapObject=None, arcs=None, arcWeight=None, arcOpacity=None, arcStyle=None, arcColor=None, arcCurveType=None, arcCurvature=None, useArrows=None, arrowSize=6, arrowsPerArc=4):
	"""
	A sub-function to create leaflet arcs
	
	Parameters
	----------
	mapObject: Folium object, Required
		Add content to a folium map.
	arcs: ref:`Arcs`/:ref:`Assignments`, Required
		The Arc dataframe to be generated in Leaflet
	arcWeight: string, Optional
		The weight of generated route when displayed in Leaflet. See :ref:`Leaflet Style`
	arcStyle: string, Optional, default as 'solid'
		The line style of geneareted route, options are 'solid', 'dotted', 'dashed'. See :ref:`Leaflet Style`
	arcOpacity: string, Optional
		The opacity of generated route when displayed in Leaflet, range from 0 (invisible) to 1. See :ref:`Leaflet Style`
	arcColor: string, Optional
		The color of generated route when displayed in Leaflet.  One of a collection of pre-specified colors. See :ref:`Leaflet Style`
	arcCurveType: string, Optional
		Options are 'bezier', 'greatcircle' or None.
	arcCurvature: float in [-45,45], Optional
		Only used if arcCurveType=='bezier'.  	
	useArrows: boolean, Optional, default as None
		Whether or not to add arrows to leaflet map.
	arrowSize: int Optional, default as 
		Size of arrows

	return
	------
	Folium object
		A new/updated map that contains the arcs
	"""

	# In here "arcs" can be Arcs/Assignments, each path should have its own odID. Use lstPath as a list of Arcs/Assignments dataframe, each item in it is a path, with the same styles
	lstPath = []

	# For Arcs dataframe, each row is a path, i.e. each row should have different odID
	if (not {'startTimeSec'}.issubset(arcs.columns)):
		for i in range(0, len(arcs)):

			if (arcCurveType == None):
				newArcCurveType = arcs.iloc[i]['leafletCurveType'].lower()
			else:
				newArcCurveType = arcCurveType.lower()
			if (arcCurvature == None):
				newArcCurvature = arcs.iloc[i]['leafletCurvature']
			else:
				newArcCurvature = arcCurvature		


		
			newPath = pd.DataFrame(columns=['odID', 'startLat', 'startLon', 'endLat', 'endLon', 'leafletColor', 'leafletWeight', 'leafletStyle', 'leafletOpacity', 'useArrows'])
			newPathList = []
			if (newArcCurveType == 'greatcircle'):
				curvePoints = _getCurveGreatCircle([arcs.iloc[i]['startLat'], arcs.iloc[i]['startLon']], [arcs.iloc[i]['endLat'], arcs.iloc[i]['endLon']])
				for j in range(1, len(curvePoints)):		
					newPathList.append({
						'odID' : arcs.iloc[i]['odID'],
						'startLat' : curvePoints[j - 1][0],
						'startLon' : curvePoints[j - 1][1],
						'endLat' : curvePoints[j][0],
						'endLon' : curvePoints[j][1],
						'leafletColor' : arcs.iloc[i]['leafletColor'],
						'leafletWeight' : arcs.iloc[i]['leafletWeight'],
						'leafletStyle' : arcs.iloc[i]['leafletStyle'],
						'leafletOpacity' : arcs.iloc[i]['leafletOpacity'],
						'useArrows' : arcs.iloc[i]['useArrows'],
						'popupText' : arcs.iloc[i]['popupText']
						})
				newPath = pd.DataFrame(newPathList)
			elif (newArcCurveType == 'bezier'):
				curvePoints = _getCurveBezier([arcs.iloc[i]['startLat'], arcs.iloc[i]['startLon']], [arcs.iloc[i]['endLat'], arcs.iloc[i]['endLon']], newArcCurvature)
				for j in range(1, len(curvePoints)):		
					newPathList.append({
						'odID' : arcs.iloc[i]['odID'],
						'startLat' : curvePoints[j - 1][0],
						'startLon' : curvePoints[j - 1][1],
						'endLat' : curvePoints[j][0],
						'endLon' : curvePoints[j][1],
						'leafletColor' : arcs.iloc[i]['leafletColor'],
						'leafletWeight' : arcs.iloc[i]['leafletWeight'],
						'leafletStyle' : arcs.iloc[i]['leafletStyle'],
						'leafletOpacity' : arcs.iloc[i]['leafletOpacity'],
						'useArrows' : arcs.iloc[i]['useArrows'],
						'popupText' : arcs.iloc[i]['popupText']
						})
				newPath = pd.DataFrame(newPathList)						
			elif (newArcCurveType == 'straight'):
				newPathList.append({
					'odID' : arcs.iloc[i]['odID'],
					'startLat' : arcs.iloc[i]['startLat'],
					'startLon' : arcs.iloc[i]['startLon'],
					'endLat' : arcs.iloc[i]['endLat'],
					'endLon' : arcs.iloc[i]['endLon'],
					'leafletColor' : arcs.iloc[i]['leafletColor'],
					'leafletWeight' : arcs.iloc[i]['leafletWeight'],
					'leafletStyle' : arcs.iloc[i]['leafletStyle'],
					'leafletOpacity' : arcs.iloc[i]['leafletOpacity'],
					'useArrows' : arcs.iloc[i]['useArrows'],
					'popupText' : arcs.iloc[i]['popupText']
					})
				newPath = pd.DataFrame(newPathList)
					
			lstPath.append(newPath.copy())

	# For Assignments dataframe, use deconstructAssignments to generate a list of assignments dataframe
	if ({'objectID'}.issubset(arcs.columns) and {'startTimeSec'}.issubset(arcs.columns)):
		lstOD = deconstructAssignments(assignments=arcs)
		for i in range(len(lstOD)):
			if (arcCurveType == None):
				newArcCurveType = lstOD[i].iloc[0]['leafletCurveType'].lower()
			else:
				newArcCurveType = arcCurveType.lower()
			if (arcCurvature == None):
				newArcCurvature = lstOD[i].iloc[0]['leafletCurvature']
			else:
				newArcCurvature = arcCurvature

			newOrigin = [lstOD[i].iloc[0]['startLat'], lstOD[i].iloc[0]['startLon']]
			newDestine = [lstOD[i].iloc[len(lstOD[i]) - 1]['endLat'], lstOD[i].iloc[len(lstOD[i]) - 1]['endLon']]

			newPath = pd.DataFrame(columns=['odID', 'startLat', 'startLon', 'endLat', 'endLon', 'leafletColor', 'leafletWeight', 'leafletStyle', 'leafletOpacity', 'useArrows'])
			newPathList = []
			if (newArcCurveType == 'greatcircle'):
				curvePoints = _getCurveGreatCircle(newOrigin, newDestine)
				for j in range(1, len(curvePoints)):			  
					newPathList.append({
						'odID' : i,
						'startLat' : curvePoints[j - 1][0],
						'startLon' : curvePoints[j - 1][1],
						'endLat' : curvePoints[j][0],
						'endLon' : curvePoints[j][1],
						'leafletColor' : lstOD[i].iloc[0]['leafletColor'],
						'leafletWeight' : lstOD[i].iloc[0]['leafletWeight'],
						'leafletStyle' : lstOD[i].iloc[0]['leafletStyle'],
						'leafletOpacity' : lstOD[i].iloc[0]['leafletOpacity'],
						'useArrows' : lstOD[i].iloc[0]['useArrows'],
						'popupText' : lstOD[i].iloc[0]['popupText']
						})
				newPath = pd.DataFrame(newPathList)		
			elif (newArcCurveType == 'bezier'):
				curvePoints = _getCurveBezier(newOrigin, newDestine, newArcCurvature)
				for j in range(1, len(curvePoints)):			  
					newPathList.append({
						'odID' : i,
						'startLat' : curvePoints[j - 1][0],
						'startLon' : curvePoints[j - 1][1],
						'endLat' : curvePoints[j][0],
						'endLon' : curvePoints[j][1],
						'leafletColor' : lstOD[i].iloc[0]['leafletColor'],
						'leafletWeight' : lstOD[i].iloc[0]['leafletWeight'],
						'leafletStyle' : lstOD[i].iloc[0]['leafletStyle'],
						'leafletOpacity' : lstOD[i].iloc[0]['leafletOpacity'],
						'useArrows' : lstOD[i].iloc[0]['useArrows'],
						'popupText' : lstOD[i].iloc[0]['popupText']
						})
				newPath = pd.DataFrame(newPathList)	
			elif (newArcCurveType == 'straight'):
				newPath = lstOD[i]
				
			lstPath.append(newPath.copy())
			
	# For each path, generate the arcs and arrows accordingly
	for i in range(len(lstPath)):
		lstPath[i] = lstPath[i].reset_index(drop=True)
		arcPath = []
		arcPath.append([float(lstPath[i]['startLat'][0]), float(lstPath[i]['startLon'][0])])
		for j in range(len(lstPath[i])):
			arcPath.append([float(lstPath[i]['endLat'][j]), float(lstPath[i]['endLon'][j])])

		# FIXMELP -- Some of these values below aren't used anywhere that I can see.
		#            For example, curveType or curvature.
		# If not overridden, use the info in arcs dataframe
		if (arcColor == None):
			newColor = lstPath[i]['leafletColor'][0]
		else:
			newColor = arcColor
		if (arcWeight == None):
			newWeight = lstPath[i]['leafletWeight'][0]
		else:
			newWeight = arcWeight
		if (arcOpacity == None):
			newOpacity = lstPath[i]['leafletOpacity'][0]
		else:
			newOpacity = arcOpacity
		if (arcStyle == None):
			newStyle = lstPath[i]['leafletStyle'][0]
		else:
			newStyle = arcStyle.lower()
		if (arcCurveType == None):
			newArcCurveType = lstPath[i]['leafletStyle'][0]
		else:
			newArcCurveType = arcCurveType.lower()
		if (arcCurvature == None):
			newArcCurvature = lstPath[i]['leafletStyle'][0]
		else:
			newArcCurvature = arcCurvature

		# Interpret arc style
		if (newStyle == 'dashed'):
			dashArray = '30 10'
		elif (newStyle == 'dotted'):
			dashArray = '1 6'
		else:
			dashArray = None
		
		try:
			newColor = newColor.lower()
		except:
			pass

		for j in range(1, len(arcPath)):
			# Format popup text
			if (lstPath[i]['popupText'][j-1] is not None):
				popupText = str(lstPath[i]['popupText'][j-1])
			else:
				popupText = None	
			
			# '''
			# Folium draw arcs	
			folium.PolyLine(
				[arcPath[j-1], arcPath[j]], 
				color = newColor, 
				weight = float(newWeight), 
				opacity = float(newOpacity), 
				dash_array = dashArray,
				popup = popupText
			).add_to(mapObject)	
			# '''
			
		# Check if we add arrows
		arrowFlag = False
		if (useArrows == True):
			arrowFlag = True
		elif (useArrows == None):
			if ({'useArrows'}.issubset(lstPath[i].columns)):
				if (lstPath[i].iloc[0]['useArrows'] == True):
					arrowFlag = True
			else:
				arrowFlag = False
		elif (useArrows == False):
			arrowFlag = False			
		if (arrowFlag):
			mapObject = _createLeafletArrowsPathOnGround(mapObject, arcPath, newColor, arrowSize, mode='equal_division_spacing', arrowsPerArc=arrowsPerArc, arrowDistanceInMeters=1000)

	return mapObject

def _createLeafletBoundingRegion(mapObject=None, boundingRegion=None, boundingWeight=config['VRV_DEFAULT_LEAFLETBOUNDINGWEIGHT'], boundingOpacity=config['VRV_DEFAULT_LEAFLETBOUNDINGOPACITY'], boundingStyle=config['VRV_DEFAULT_LEAFLETBOUNDINGSTYLE'], boundingColor=config['VRV_DEFAULT_LEAFLETBOUNDINGCOLOR'], boundingIsFitEarthCurvature=False):
	"""
	A sub-function to create leaflet bounding region

	Parameters
	----------
	mapObject: Folium object, Required
		Add content to a folium map.
	boundingRegion: list of lists, Required
		A sequence of lat/lon coordinates defining the boundary of the objects.
	boundingWeight: string, Optional
		The weight of bounding region when displayed in Leaflet. See :ref:`Leaflet Style`
	boundingStyle: string, Optional, default as 'solid'
		The line style of bounding region, options are 'solid', 'dotted', 'dashed'. See :ref:`Leaflet Style`
	boundingOpacity: string, Optional
		The opacity of bounding region when displayed in Leaflet, range from 0 (invisible) to 1. See :ref:`Leaflet Style`
	boundingColor: string, Optional
		The color of bounding region when displayed in Leaflet.  One of a collection of pre-specified colors. See :ref:`Leaflet Style`

	return
	------
	Folium object
		A new/updated map that contains the boundings

	"""

	# Make the bounding region a closed circle
	boundings = boundingRegion[:]
	if (boundings[0] != boundings[len(boundings) - 1]):
		boundings.append(boundings[0])

	# Interpret bounding style
	try:
		boundingStyle = boundingStyle.lower()
	except:
		pass
		
	if (boundingStyle == 'dashed'):
		dashArray = '30 10'
	elif (boundingStyle == 'dotted'):
		dashArray = '1 6'
	else:
		dashArray = None

	try:
		boundingColor = boundingColor.lower()
	except:
		pass
		
	if (boundingIsFitEarthCurvature):
		tmpBoundings = boundings.copy()
		boundings = []
		for i in range(1, len(tmpBoundings)):
			boundings.extend(_getCurveGreatCircle(tmpBoundings[i - 1], tmpBoundings[i]))
			
	# Draw bounding region in folium (for now is not filled)
	folium.PolyLine(
		boundings, 
		color = boundingColor,
		weight = boundingWeight,
		opacity = boundingOpacity,
		dash_array = dashArray
	).add_to(mapObject)

	return mapObject

def _createLeafletArrowsPathOnGround(mapObject=None, path=None, color=None, size=7, mode='equal_division_spacing', arrowsPerArc=1, arrowDistanceInMeters=None):
	"""
	A sub-function to generate arrows for one path that curved to the Earth
	Parameters
	----------
	mapObject: Folium object, Required
		Add content to a folium map.
	lats: list, Required
		A list of latitudes
	lons: list, Required
		A list of longitudes
	color: string, Required
		The color for arrow, we are not providing any default value here because it has to be consistent with the color of arcs/assignments
	size: int, Optional, default as 7
		The size of the arrow
	mode: string, Optional, default as 'equal_division_spacing'
		For 'equal_division_spacing', divide the entire path equally in to several parts and add arrows accordingly. For 'equal_distance_spacing', add arrow for every given distance.
	arrowsPerArc: int, Optional, default as 1
		If we are using 'equal_division_spacing', it defines the number of arrows in the path, otherwise it will be ignored
	arrowDistanceInMeters: float, Optional
		If we are using 'equal_distance_spacing', it defines the distance between arrows
	Return
	------
	Folium object
		A map that contains arrows above the arcs
	"""

	# Calculate totalDistance
	totalDistance = geoDistancePath2D(path)

	# Use different modes to decide how many arrows to be generated and where are them
	lstMilages = []
	if (mode == 'equal_division_spacing'):
		for i in range(1, arrowsPerArc + 1):
			lstMilages.append(totalDistance * (i / (arrowsPerArc + 1)))
	elif (mode == 'equal_distance_spacing'):
		accuDistance = 0
		while accuDistance < totalDistance:
			accuDistance += arrowDistanceInMeters
			lstMilages.append(accuDistance)
		remainingDistance = totalDistance - accuDistance
		for i in range(len(lstMilages)):
			lstMilages[i] = lstMilages[i] + remainingDistance/2
	else:
		return

	try:
		color = color.lower()
	except:
		pass
		
	# Draw arrows
	for i in range(len(lstMilages)):
		arrowLoc = geoMileageInPath2D(path, lstMilages[i])
		folium.RegularPolygonMarker(
			location = arrowLoc['loc'],
			number_of_sides = 3,
			rotation = arrowLoc['bearingInDegree']-90,
			radius = size,
			color = color,
			fill_color = color,
			fill_opacity = 1.0
		).add_to(mapObject)
	
	return mapObject

def _createLeafletArrowsPathProjected(mapObject=None, path=None, color=None, size=7, mode='equal_division_spacing', arrowsPerArc=1, arrowDistanceInMeters=None):
	"""
	A sub-function to generate arrows for one path that curved to the Earth
	Parameters
	----------
	mapObject: Folium object, Required
		Add content to a folium map.
	lats: list, Required
		A list of latitudes
	lons: list, Required
		A list of longitudes
	color: string, Required
		The color for arrow, we are not providing any default value here because it has to be consistent with the color of arcs/assignments
	size: int, Optional, default as 7
		The size of the arrow
	mode: string, Optional, default as 'equal_division_spacing'
		For 'equal_division_spacing', divide the entire path equally in to several parts and add arrows accordingly. For 'equal_distance_spacing', add arrow for every given distance.
	arrowsPerArc: int, Optional, default as 1
		If we are using 'equal_division_spacing', it defines the number of arrows in the path, otherwise it will be ignored
	arrowDistanceInMeters: float, Optional
		If we are using 'equal_distance_spacing', it defines the distance between arrows
	Return
	------
	Folium object
		A map that contains arrows above the arcs
	"""

	# Calculate totalDistance
	totalDistance = geoDistancePath2D(path)

	# Use different modes to decide how many arrows to be generated and where are them
	lstMilages = []
	if (mode == 'equal_division_spacing'):
		for i in range(1, arrowsPerArc + 1):
			lstMilages.append(totalDistance * (i / (arrowsPerArc + 1)))
	elif (mode == 'equal_distance_spacing'):
		accuDistance = 0
		while accuDistance < totalDistance:
			accuDistance += arrowDistanceInMeters
			lstMilages.append(accuDistance)
		remainingDistance = totalDistance - accuDistance
		for i in range(len(lstMilages)):
			lstMilages[i] = lstMilages[i] + remainingDistance/2
	else:
		return

	try:
		color = color.lower()
	except:
		pass
		
	# Draw arrows
	for i in range(len(lstMilages)):
		arrowLoc = geoMileageInPath2D(path, lstMilages[i])
		folium.RegularPolygonMarker(
			location = arrowLoc['loc'],
			number_of_sides = 3,
			rotation = arrowLoc['bearingInDegree']-90,
			radius = size,
			color = color,
			fill_color = color,
			fill_opacity = 1.0
		).add_to(mapObject)
	
	return mapObject

def _getCurveBezier(startLoc, endLoc, curvature=45, numShapepoint=50):
	midLoc = [(startLoc[0] + endLoc[0]) / 2 + (startLoc[1] + endLoc[1]) / 2]
	distanceAwayFromStartLoc = (geoDistance2D(startLoc, endLoc)) / math.cos(math.radians(curvature)) / 2
	headingFromStartLocToRefLoc = geoGetHeading(startLoc, endLoc) - curvature
	refLoc = geoPointInDistance2D(startLoc, headingFromStartLocToRefLoc, distanceAwayFromStartLoc)
	headingFromRefLocToEndLoc = geoGetHeading(refLoc, endLoc)
	distStartLocToRefLoc = geoDistance2D(startLoc, refLoc)
	distRefLocToEndLoc = geoDistance2D(refLoc, endLoc) # Should be the same as distStartLocToRefLoc, in no curvature plane
	path = []
	for i in range(numShapepoint + 1):
		refStart = geoPointInDistance2D(startLoc, headingFromStartLocToRefLoc, i * distStartLocToRefLoc / float(numShapepoint))
		refEnd = geoPointInDistance2D(refLoc, headingFromRefLocToEndLoc, i * distRefLocToEndLoc / float(numShapepoint))
		refHeading = geoGetHeading(refStart, refEnd)
		refDist = geoDistance2D(refStart, refEnd)
		newLoc = geoPointInDistance2D(refStart, refHeading, i * refDist / float(numShapepoint))
		path.append(newLoc)
	return path

def _getCurveGreatCircle(startLoc, endLoc, numShapepoint=50):
	odPath = [startLoc, endLoc]
	direction = geoGetHeading(startLoc, endLoc)
	path = []
	totalDist = geoDistance2D(startLoc, endLoc)
	accDist = 0
	while (accDist < totalDist):
		path.append(geoPointInDistance2D(startLoc, direction, accDist))
		accDist = accDist + totalDist / float(numShapepoint)
	path.append(endLoc)
	return path

def addLeafletCircle(mapObject=None, mapFilename=None, mapBackground=config['VRV_DEFAULT_LEAFLET_MAPTILES'], mapBoundary=None, zoomStart=None, center=None, radius=None, text=None, fontSize=config['VRV_DEFAULT_LEAFLET_FONTSIZE'], fontColor=config['VRV_DEFAULT_LEAFLET_FONTCOLOR'], popupText=None, lineWeight=3, lineColor=None, lineOpacity=0.8, lineStyle='solid', fillColor=config['VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE'], fillOpacity=0.3):

	"""
	Add a circle, with a radius specified in [meters], to a Leaflet map.
	
	Note
	----
	This function differs from addLeafletMarker, in which the circle's radius is specified in [pixels].
	
	Parameters
	----------
	mapObject: Folium object, Optional, default None
		A Folium map object.  If provided, the circle will be added to an existing map.  Otherwise, a new map will be created.
	mapFilename: string, Optional, default as None
		This is the name of the map file that will be created (e.g., "../output/map.html" or "map.html").  The filename should have a `.html` extension.  If `mapFilename` is not provided, no map file will be generated.  The returned map object can be viewed within a Jupyter notebook.
	mapBackground: string, Optional, default as 'CartoDB positron'
		Sets the background tiles of the map.  See :ref:`Leaflet Style` for the list of options.
	mapBoundary: list of lists, Optional, default as None
		Allows customization of the zoom level.  If a map boundary is provided, the zoom level will correspond to the rectangle defined by the two map boundary points. This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  Must be in the form [[south lat, west lon], [north lat, east lon]].
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	center: list, Required, default None
		Specifies the center point of the circle.  Must be a list of the form `[lat, lon]` or `[lat, lon, alt]`.  If provided, the altitude component will be ignored (as all locations on Leaflet maps are assumed to be at ground level).
	radius: float, Required, default None
		The radius of the circle, in units of [meters]. 
	text: string, Optional, default None
		Specifies the text to be displayed on the map, centered as the `center` location.
	fontSize: float, Optional, default 24
		The size of the font, in units of [points].  The default is 24-point font.
	fontColor: string, Optional, default 'orange'
		The color of the text string.  `fontColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). 		
	popupText: string, Optional, default as None
		The circle will include this text as a popup label (you will need to click on the circle in the map to see this label).  		
	lineWeight: int, Optional, default 3
		The width of the circle's outline, in units of [pixels].  This value is ignored if `lineColor = None`. 
	lineColor: string, Optional, default None
		The color of the circle's outline.  `lineColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). No line will be drawn if `lineColor = None`. 
	lineOpacity: float in [0, 1], Optional, default 0.8
		Specifies the opacity of the circle's outline.  Valid values are in the range from 0 (invisible) to 1 (no transparency).
	lineStyle: string, Optional, default 'solid'
		The style of the circle's outline.  See :ref:`Leaflet Style` for a list of valid options.  
	fillColor: string, Optional, default 'red'
		The color of the interior of the circle. `fillColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). The circle will not be filled if `fillColor = None`.  
	fillOpacity: float in [0, 1], Optional, default 0.3
		Specifies the opacity of the circle's interior.  Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	
	Return
	------
	Folium object
		A Folium map object containing a circle (and pre-existing items previously specified in mapObject).
		
	Example
	-------
		>>> # Draw a circle of radius 10 meters, centered on the Univ. at Buffalo campus.
		>>> # Save this as "a_circle.html".
		>>> import veroviz as vrv
		>>> myMap = vrv.addLeafletCircle(
		...     zoomStart=18,
		...     center=[43.00154, -78.7871],
		...     radius=100,
		...     mapFilename="a_circle.html")
		>>> myMap

		>>> # Draw a circle of radius 2000 meters, centered on the Univ. at Buffalo campus.
		>>> # This example includes all of the available function arguments.
		>>> import veroviz as vrv
		>>> myMap = vrv.addLeafletCircle(
		...     mapObject = None,
		...     mapFilename = None,
		...     mapBackground = 'OpenStreetMap',
		...     mapBoundary = None,
		...     zoomStart = 13,
		...     center = [43.00154, -78.7871],
		...     radius = 2000,
		...     text = 'UB',
		...     fontSize = 24,
		...     fontColor = 'black',
		...     popupText = 'Univ. at Buffalo',
		...     lineWeight = 6,
		...     lineColor = '#ff66ff',
		...     lineOpacity = 0.7,
		...     lineStyle = 'dotted',
		...     fillColor = 'green',
		...     fillOpacity = 0.4)
		>>> myMap
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletCircle(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, center, radius, text, fontSize, fontColor, lineWeight, lineColor, lineOpacity, lineStyle, fillColor, fillOpacity)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)
	
	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	center = [center[0], center[1]]

	# If no mapObject exists, define a new mapObject
	if (mapObject == None):
		mapObject = _createLeafletMap(mapBackground=mapBackground, center=center, zoomStart=zoomStart)

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)

	try:
		lineStyle = lineStyle.lower()
	except:
		pass
	
	# Interpret line style
	if (lineStyle == 'dashed'):
		dashArray = '30 10'
	elif (lineStyle == 'dotted'):
		dashArray = '1 6'
	else:
		dashArray = None

	try:
		lineColor = lineColor.lower()
	except:
		pass
		
	try:
		fillColor = fillColor.lower()
	except:
		pass
		
	# Format popup text
	if (popupText is not None):
		popupText = str(popupText)
		
	# Draw circle:		
	folium.Circle(center, 
		radius = radius,  
		stroke = True, 
		weight = lineWeight, 
		color = lineColor, 
		opacity = lineOpacity, 
		dash_array = dashArray,
		fill_color = fillColor,
		fill_opacity = fillOpacity,
		popup = popupText
		).add_to(mapObject)
		
	# Add text:
	if (text is not None):
		try:
			fontColor = fontColor.lower()
		except:
			pass

		iconSizeX = 900		# FIXME -- Not sure if this is good.
		iconAnchorX = iconSizeX / 2
					
		folium.map.Marker(center, popup=popupText, icon=DivIcon(
			icon_size = (iconSizeX, fontSize), 
			icon_anchor = (iconAnchorX, fontSize), 
			html = "<div style=\"font-size: %dpt; color: %s; text-align: center;\">%s</div>" %  (fontSize, fontColor, text)
			)).add_to(mapObject)

	if (mapFilename is not None):
		mapObject.save(mapFilename)
		if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
			print("Message: Map page written to %s." % (mapFilename))

	return mapObject
	
def addLeafletMarker(mapObject=None, mapFilename=None, mapBackground=config['VRV_DEFAULT_LEAFLET_MAPTILES'], mapBoundary=None, zoomStart=None, center=None, radius=5, text=None, fontSize=config['VRV_DEFAULT_LEAFLET_FONTSIZE'], fontColor=config['VRV_DEFAULT_LEAFLET_FONTCOLOR'], popupText=None, lineWeight=3, lineColor=None, lineOpacity=0.8, lineStyle='solid', fillColor=config['VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE'], fillOpacity=0.3):

	"""
	Add a circle-shaped marker, with a radius specified in [pixels], to a Leaflet map.
	
	Note
	----
	This function differs from addLeafletCircle, in which the circle's radius is specified in [meters].
	
	Parameters
	----------
	mapObject: Folium object, Optional, default None
		A Folium map object.  If provided, the marker will be added to an existing map.  Otherwise, a new map will be created.
	mapFilename: string, Optional, default None 
		If provided, the map will be saved to this file, which should have a `.html` extension.  `mapFilename` can contain a filepath.  If `mapFilename` is not provided, no file will be generated.  The returned mapObject can be viewed within a Jupyter notebook. 
	mapBackground: string, Optional, default 'CartoDB positron'
		The tiles of the map, default to be 'CartoDB positron', for options, see :ref:`Leaflet Style`, also see folium documentation (https://python-visualization.github.io/folium/modules.html) for more options
	mapBoundary: list [LIST OF LISTS?], Optional, default None
		If provided, the mapBoundary coordinates are used to determine a zoom level such that these coordinates are contained within view when the map is opened.  This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  `mapBoundary` must be in the form [[south lat, west lon], [north lat, east lon]].	
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	center: list, Required, default None
		Specifies the center point of the circle marker.  Must be a list of the form `[lat, lon]` or `[lat, lon, alt]`.  If provided, the altitude component will be ignored (as all locations on Leaflet maps are assumed to be at ground level).
	radius: float, Required, default None
		The radius of the circle marker, in units of [pixels]. 
	text: string, Optional, default None
		Specifies the text to be displayed on the map, centered as the `center` location.
	fontSize: float, Optional, default 24
		The size of the font, in units of [points].  The default is 24-point font.
	fontColor: string, Optional, default 'orange'
		The color of the text string.  `fontColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). 		
	popupText: string, Optional, default as None
		The marker will include this text as a popup label (you will need to click on the marker in the map to see this label).  		
	lineWeight: int, Optional, default 3
		The width of the circle marker's outline, in units of [pixels].  This value is ignored if `line = False`. 
	lineColor: string, Optional, default 'red'
		The color of the circle marker's outline.  `lineColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). The line color is ignored if `line = False`. 
	lineOpacity: float in [0, 1], Optional, default 0.8
		The opacity of the circle marker's outline, where 0 is invisible and 1 represents no transparency.  See :ref:`Leaflet Style`
	lineStyle: string, Optional, default 'solid'
		The style of the circle marker's outline.  See :ref:`Leaflet Style` for a list of valid options.  
	fillColor: string, Optional, default None
		The color of the interior of the circle marker. `fillColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). The fill color is ignored if `fill = False`.  
	fillOpacity: float in [0, 1], Optional, default 0.3
		The opacity of the circle marker's interior, where 0 is invisible and 1 represents no transparency.  See :ref:`Leaflet Style`
	
	Return
	------
	Folium object
		A Folium map object containing a circle marker (and pre-existing items previously specified in mapObject).
		
	Example
	-------
		>>> # Draw a circle of radius 10 pixels, centered on the Univ. at Buffalo campus.
		>>> # Save this as "a_marker.html".
		>>> import veroviz as vrv
		>>> myMap = vrv.addLeafletMarker(
		...     center=[43.00154, -78.7871],
		...     radius=10,
		...     mapFilename="a_marker.html")
		>>> myMap

		>>> # Draw a circle of radius 30 pixels, centered on the Univ. at Buffalo campus.
		>>> # This example includes all of the available function arguments.
		>>> import veroviz as vrv
		>>> myMap = vrv.addLeafletMarker(
		...     mapObject = None, 
		...     mapFilename = None, 
		...     mapBackground = 'CartoDB positron', 
		...     mapBoundary = None, 
		...     zoomStart = 11, 
		...     center = [43.00154, -78.7871],
		...     radius = 30, 
		...     text = 'UB',
		...     fontSize = 24,
		...     fontColor = 'black',
		...     popupText = 'Univ. at Buffalo',
		...     lineWeight = 3, 
		...     lineColor = 'orange', 
		...     lineOpacity = 0.6, 
		...     lineStyle = 'dashed',
		...     fillColor = 'blue', 
		...     fillOpacity = 0.3)
		>>> myMap
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletMarker(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, center, radius, text, fontSize, fontColor, lineWeight, lineColor, lineOpacity, lineStyle, fillColor, fillOpacity)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	center = [center[0], center[1]]

	# If no mapObject exists, define a new mapObject
	if (mapObject == None):
		mapObject = _createLeafletMap(mapBackground=mapBackground, center=center, zoomStart=zoomStart)

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)
		
	try:
		lineStyle = lineStyle.lower()
	except:
		pass

	# Interpret line style
	if (lineStyle == 'dashed'):
		dashArray = '30 10'
	elif (lineStyle == 'dotted'):
		dashArray = '1 6'
	else:
		dashArray = None

	try:
		lineColor = lineColor.lower()
	except:
		pass
		
	try:
		fillColor = fillColor.lower()
	except:
		pass

	# Format popup text
	if (popupText is not None):
		popupText = str(popupText)

	# Add marker:
	folium.CircleMarker(center, 
		radius = radius,  
		stroke = True, 
		weight = lineWeight, 
		color = lineColor, 
		opacity = lineOpacity, 
		dash_array = dashArray,
		fill_color = fillColor,
		fill_opacity = fillOpacity,
		popup = popupText
		).add_to(mapObject)

	# Add text:
	if (text is not None):
		try:
			fontColor = fontColor.lower()
		except:
			pass

		iconSizeX = radius*2		# FIXME -- Not sure if this is good.
		iconAnchorX = iconSizeX / 2
										
		folium.map.Marker(center, popup=popupText, icon=DivIcon(
			icon_size = (iconSizeX, fontSize), 
			icon_anchor = (iconAnchorX, fontSize), 
			html = '<div style="font-size: %dpt; color: %s; text-align: center;">%s</div>' %  (fontSize, fontColor, text)
			)).add_to(mapObject)
		
	if (mapFilename is not None):
		mapObject.save(mapFilename)
		if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
			print("Message: Map page written to %s." % (mapFilename))

	return mapObject	

def addLeafletPolygon(mapObject=None, mapFilename=None, mapBackground=config['VRV_DEFAULT_LEAFLET_MAPTILES'], mapBoundary=None, zoomStart=None, points=None, popupText=None, lineWeight=3, lineColor=config['VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE'], lineOpacity=0.8, lineStyle='solid', fillColor=None, fillOpacity=0.3):
	"""
	Add a polygon, as defined by an ordered collection of lat/lon coordinates, to a Leaflet map.
		
	Note
	----
	There is also a "polyline" function, which does not assume a closed shape.
			
	Parameters
	----------
	mapObject: Folium object, Optional, default None
		A Folium map object.  If provided, the polygon will be added to an existing map.  Otherwise, a new map will be created.
	mapFilename: string, Optional, default as None
		This is the name of the map file that will be created (e.g., "../output/map.html" or "map.html").  The filename should have a `.html` extension.  If `mapFilename` is not provided, no map file will be generated.  The returned map object can be viewed within a Jupyter notebook.
	mapBackground: string, Optional, default as 'CartoDB positron'
		Sets the background tiles of the map.  See :ref:`Leaflet Style` for the list of options.
	mapBoundary: list of lists, Optional, default as None
		Allows customization of the zoom level.  If a map boundary is provided, the zoom level will correspond to the rectangle defined by the two map boundary points. This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  Must be in the form [[south lat, west lon], [north lat, east lon]].
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	points: list of lists, Required, default None
		Specifies the ordered collection of lat/lon coordinates comprising the polygon.  This must be a list of lists, of the form `[[lat1, lon1], [lat2, lon2], ..., [latn, lonn]]` or `[[lat1, lon1, alt1], [lat2, lon2, alt2], ..., [latn, lonn, altn]]`.  If an altitude is provided with each coordinate, this component will be ignored (as all Leaflet maps assume that objects are at ground level).  It is not necessary for `[lat1, lon1]` and `[latn, lonn]` to be the same point.  In other words, the polygon will automatically connect the first and last locations specified in the `points` list.	
	popupText: string, Optional, default as None
		The polygon will include this text as a popup label (you will need to click on the polygon in the map to see this label).  	
	lineWeight: int, Optional, default 3
		The width of the polygon's outline, in units of [pixels].  This value is ignored if `lineColor = None`. 
	lineColor: string, Optional, default 'red'
		The color of the polygon's outline.  `lineColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). No line will be drawn if `lineColor = None`. 
	lineOpacity: float in [0, 1], Optional, default 0.8
		Specifies the opacity of the polygon's outline.  Valid values are in the range from 0 (invisible) to 1 (no transparency).
	lineStyle: string, Optional, default 'solid'
		The style of the polygon's outline.  See :ref:`Leaflet Style` for a list of valid options.  
	fillColor: string, Optional, default None
		The color of the interior of the polygon. `fillColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). The polygon will not be filled if `fillColor = None`.  
	fillOpacity: float in [0, 1], Optional, default 0.3
		Specifies the opacity of the polygon's interior.  Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	
	Return
	------
	Folium object
		A Folium map object containing a polygon (and pre-existing items previously specified in mapObject).
		
	Example
	-------
		>>> # Draw a filled polygon around the Univ. at Buffalo campus.
		>>> # Save this as "a_polygon.html".
		>>> import veroviz as vrv
		>>> campusPoints = [[43.0121, -78.7858],
		...                 [43.0024, -78.7977],
		...                 [42.9967, -78.7921],
		...                 [42.9988, -78.7790]]
		>>> myMap = vrv.addLeafletPolygon(
		...     points=campusPoints,
		...     mapFilename="a_polygon.html")
		>>> myMap

		>>> # Draw a filled polygon around the Univ. at Buffalo campus.
		>>> # This example includes all of the available function arguments.
		>>> import veroviz as vrv
		>>> campusPoints = [[43.0121, -78.7858],
		...                 [43.0024, -78.7977],
		...                 [42.9967, -78.7921],
		...                 [42.9988, -78.7790]]
		>>> myMap = vrv.addLeafletPolygon(
		...     mapObject = None, 
		...     mapFilename = None, 
		...     mapBackground = 'OpenStreetMap', 
		...     mapBoundary = vrv.getMapBoundary(locs=campusPoints), 
		...     zoomStart = 15, 
		...     points = campusPoints, 
		...     popupText = 'Univ. at Buffalo',
		...     lineWeight = 7, 
		...     lineColor = '#ff00ff', 
		...     lineOpacity = 0.9, 
		...     lineStyle = 'solid', 
		...     fillColor = '#ff66ff', 
		...     fillOpacity = 0.3)    
		>>> myMap
	"""
 

	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletPolygon(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, points, lineWeight, lineColor, lineOpacity, lineStyle, fillColor, fillOpacity)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	# Do we have a rectangle?
	if (len(points) == 2):
		if ( (len(points[0]) == 2) & (len(points[1]) == 2)):
			points = [points[0], [points[0][0], points[1][1]], points[1], [points[1][0], points[0][1]]]
			if (config['VRV_SETTING_SHOWWARNINGMESSAGE']):
				print("NOTE: Only two pairs of coordinates were provided in 'points'.  This is being interpreted as a rectangle.")

	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	# If no mapObject exists, define a new mapObject
	if (mapObject == None):
		# Adjust the scope of the map to proper bounds
		[[minLat, maxLon], [maxLat, minLon]] = privGetMapBoundary(None, None, points)

		midLat = (maxLat + minLat) / 2.0
		midLon = (maxLon + minLon) / 2.0
		mapObject = _createLeafletMap(mapBackground=mapBackground, center=[midLat,midLon], zoomStart=zoomStart)

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)
		elif (mapBoundary is None):
			mapObject.fit_bounds(privGetMapBoundary(None, None, points))
	try:
		lineStyle = lineStyle.lower()
	except:
		pass
		
	# Interpret line style
	if (lineStyle == 'dashed'):
		dashArray = '30 10'
	elif (lineStyle == 'dotted'):
		dashArray = '1 6'
	else:
		dashArray = None

	try:
		lineColor = lineColor.lower()
	except:
		pass
		
	try:
		fillColor = fillColor.lower()
	except:
		pass

	points2D = []
	for i in range(len(points)):
		points2D.append([points[i][0], points[i][1]])

	# Format popup text
	if (popupText is not None):
		popupText = str(popupText)

	folium.Polygon(locations = points2D, 
		stroke = True, 
		weight = lineWeight, 
		color = lineColor, 
		opacity = lineOpacity, 
		dash_array = dashArray,
		fill_color = fillColor,
		fill_opacity = fillOpacity,
		popup = popupText
		).add_to(mapObject)


	if (mapFilename is not None):
		mapObject.save(mapFilename)
		if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
			print("Message: Map page written to %s." % (mapFilename))

	return mapObject

def addLeafletPolyline(mapObject=None, mapFilename=None, mapBackground=config['VRV_DEFAULT_LEAFLET_MAPTILES'], mapBoundary=None, zoomStart=None, points=None, popupText=None, lineWeight=3, lineColor=config['VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE'], lineOpacity=0.8, lineStyle='solid', lineCurveType='straight', lineCurvature=45, useArrows=False, arrowsPerArc=1):

	"""
	Add a polyline, as described by an ordered collection of lat/lon coordinates, to a Leaflet map.  
		
	Note
	----
	The polyline is an "open" shape, in the sense that there's nothing connecting the first and last locations.  By contrast, the "polygon" shape will automatically connect the first and last locations.

	Parameters
	----------
	mapObject: Folium object, Optional, default None
		A Folium map object.  If provided, the polyline will be added to an existing map.  Otherwise, a new map will be created.
	mapFilename: string, Optional, default as None
		This is the name of the map file that will be created (e.g., "../output/map.html" or "map.html").  The filename should have a `.html` extension.  If `mapFilename` is not provided, no map file will be generated.  The returned map object can be viewed within a Jupyter notebook.
	mapBackground: string, Optional, default as 'CartoDB positron'
		Sets the background tiles of the map.  See :ref:`Leaflet Style` for the list of options.
	mapBoundary: list of lists, Optional, default as None
		Allows customization of the zoom level.  If a map boundary is provided, the zoom level will correspond to the rectangle defined by the two map boundary points. This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  Must be in the form [[south lat, west lon], [north lat, east lon]].
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	points: list of lists, Required, default None
		Specifies the ordered collection of lat/lon coordinates comprising the polyline.   This must be a list of lists, of the form `[[lat1, lon1], [lat2, lon2], ..., [latn, lonn]]` or `[[lat1, lon1, alt1], [lat2, lon2, alt2], ..., [latn, lonn, altn]]`.  If an altitude is provided with each coordinate, this component will be ignored (as all Leaflet maps assume that objects are at ground level).  Note that the polyline will not automatically connect the first and last locations specified in the `points` list.  (By contrast the "polygon" function does connect those locatons.)
	popupText: string, Optional, default as None
		The polyline will include this text as a popup label (you will need to click on the polyline in the map to see this label).  		
	lineWeight: int, Optional, default 3
		The width of the polyline's outline, in units of [pixels].  This value is ignored if `lineColor = None`. 
	lineColor: string, Optional, default 'red'
		The color of the polyline's outline.  `lineColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). No line will be drawn if `lineColor = None`. 
	lineOpacity: float in [0, 1], Optional, default 0.8
		Specifies the opacity of the polyline.  Valid values are in the range from 0 (invisible) to 1 (no transparency).
	lineStyle: string, Optional, default 'solid'
		The style of the polyine.  See :ref:`Leaflet Style` for a list of valid options.  
	lineCurveType: string, Optional, default as 'straight'
		The type of curve to be shown on leaflet map for :ref:`Arcs` dataframes (curves will not be applied to :ref:Assignments dataframes). The options are 'Bezier', 'greatcircle', and 'straight'. If Bezier is provided, the leafletCurvature is also required. If greatcircle is provided, the arc follow the curvature of the Earth.
	lineCurvature: float in (-90, 90), Conditional, default as 45
		If leafletCurveType is 'Bezier', then leafletCurvature is required; otherwise this argument will not be used. The curvature specifies the angle between a straight line connecting the two nodes and the curved arc emanating from those two nodes. Therefore, this value should be in the open interval (-90, 90), although values in the (-45, 45) range tend to work best.
	useArrows: boolean, Optional, default as None
		Indicates whether arrows should be shown on all arcs on the Leaflet map.
	arrowsPerArc: int, Optional, default as 1
		Number of arrows display on each arc, should be integer greater than 0. Each arc will have the same number of arrows, regardless of arc length. If useArrows is False, this parameter will be ignored (i.e., no arrows will be drawn).
		
	
	Return
	------
	Folium object
		A Folium map object containing a polyline (and pre-existing items previously specified in mapObject).
		
	Example
	-------
		>>> # Draw a polyline around the northern portion of the Univ. at Buffalo campus.
		>>> # Save this as "a_polyline.html".
		>>> import veroviz as vrv
		>>> campusPoints = [[43.0024, -78.7977],
		...                 [43.0121, -78.7858],
		...                 [42.9988, -78.7790]]
		>>> myMap = vrv.addLeafletPolyline(
		...     points=campusPoints,
		...     mapFilename="a_polyline.html")
		>>> myMap

		>>> # Draw a polyline around the northern portion of the Univ. at Buffalo campus.
		>>> # This example includes all of the available function arguments.
		>>> import veroviz as vrv
		>>> campusPoints = [[43.0024, -78.7977],
		...                 [43.0121, -78.7858],
		...                 [42.9988, -78.7790]]
		>>> myMap = vrv.addLeafletPolyline(
		...     mapObject = None, 
		...     mapFilename = None, 
		...     mapBackground = 'CartoDB positron', 
		...     mapBoundary = vrv.getMapBoundary(locs=campusPoints),
		...     zoomStart = None, 
		...     points = campusPoints,
		...     popupText = 'Univ. at Buffalo',
		...     lineWeight = 3, 
		...     lineColor = '#0055ff', 
		...     lineOpacity = 0.8, 
		...     lineStyle = 'solid', 
		...     lineCurveType = 'bezier',
		...     lineCurvature = 30,
		...     useArrows = True,
		...     arrowsPerArc = 1)
		>>> myMap
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletPolyline(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, points, lineWeight, lineColor, lineOpacity, lineStyle, lineCurveType, lineCurvature, useArrows, arrowsPerArc)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	# If no mapObject exists, define a new mapObject
	if (mapObject == None):
		# Adjust the scope of the map to proper bounds
		[[minLat, maxLon], [maxLat, minLon]] = privGetMapBoundary(None, None, points)

		midLat = (maxLat + minLat) / 2.0
		midLon = (maxLon + minLon) / 2.0
		mapObject = _createLeafletMap(mapBackground=mapBackground, center=[midLat,midLon], zoomStart=zoomStart)

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)
		elif (mapBoundary is None):
			mapObject.fit_bounds(privGetMapBoundary(None, None, points))

	try:
		lineStyle = lineStyle.lower()
	except:
		pass
		
	# Interpret line style
	if (lineStyle == 'dashed'):
		dashArray = '30 10'
	elif (lineStyle == 'dotted'):
		dashArray = '1 6'
	else:
		dashArray = None

	try:
		lineColor = lineColor.lower()
	except:
		pass

	
	# print("FIXMELP -- DONE?  Your branch has some code here, but it cannot be implemented because it is missing some variables.  Please fix this appropriately.")

	arcs = privCreateArcsFromLocSeq(locSeq = points, popupText = popupText)	
	mapObject = _createLeafletArcs(mapObject=mapObject, arcs=arcs, arcWeight=lineWeight, arcOpacity=lineOpacity, arcStyle=lineStyle, arcColor=lineColor, arcCurveType=lineCurveType, arcCurvature=lineCurvature, useArrows=useArrows, arrowSize=config['VRV_DEFAULT_LEAFLET_ARROWSIZE'], arrowsPerArc=arrowsPerArc)
	
	if (mapFilename is not None):
		mapObject.save(mapFilename)
		if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
			print("Message: Map page written to %s." % (mapFilename))

	return mapObject

def addLeafletText(mapObject=None, mapFilename=None, mapBackground=config['VRV_DEFAULT_LEAFLET_MAPTILES'], mapBoundary=None, zoomStart=None, anchorPoint=None, text=None, fontSize=config['VRV_DEFAULT_LEAFLET_FONTSIZE'], fontColor=config['VRV_DEFAULT_LEAFLET_FONTCOLOR'], horizAlign='center'):
	"""
	Add a text label to a Leaflet map. 
		
	Parameters
	----------
	mapObject: Folium object, Optional, default None
		A Folium map object.  If provided, the text label will be added to an existing map.  Otherwise, a new map will be created.
	mapFilename: string, Optional, default as None
		This is the name of the map file that will be created (e.g., "../output/map.html" or "map.html").  The filename should have a `.html` extension.  If `mapFilename` is not provided, no map file will be generated.  The returned map object can be viewed within a Jupyter notebook.
	mapBackground: string, Optional, default as 'CartoDB positron'
		Sets the background tiles of the map.  See :ref:`Leaflet Style` for the list of options.
	mapBoundary: list of lists, Optional, default as None
		Allows customization of the zoom level.  If a map boundary is provided, the zoom level will correspond to the rectangle defined by the two map boundary points. This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  Must be in the form [[south lat, west lon], [north lat, east lon]].
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	anchorPoint: list, Required, default None
		Specifies an anchor point (location) for the text label.  Must be a list of the form `[lat, lon]` or `[lat, lon, alt]`.  If provided, the altitude component will be ignored (as all locations on Leaflet maps are assumed to be at ground level).  See also the `horizAlign` field below.
	text: string, Required, default None
		Specifies the text to be displayed on the map at the location of `anchorPoint`.
	fontSize: float, Optional, default 24
		The size of the font, in units of [points].  The default is 24-point font.
	fontColor: string, Optional, default 'orange'
		The color of the text string.  `fontColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). 
	horizAlign: string, Optional, default 'center'
		The horizontal alignment of the text string, relative to the location specified by the `anchorPoint` input argument.  Valid options are 'left' (the text begins at the `anchorPoint` location), 'right' (the text ends at the `anchorPoint` location), or 'center' (the text is centered at the 'anchorPoint' location).  		
	
	Return
	------
	Folium object
		A Folium map object containing a text string (and pre-existing items previously specified in mapObject).
		
	Example
	-------
		>>> # Draw a text label at the location of Bell Hall on the 
		>>> # Univ. at Buffalo campus.
		>>> # Save this as "a_text_label.html".
		>>> import veroviz as vrv
		>>> myMap = vrv.addLeafletText(
		...     anchorPoint=[43.00154, -78.7871],
		...     text="Bell Hall",
		...     mapFilename="a_text_label.html")

		>>> myMap

		>>> # Draw a text label at the location of Bell Hall on the
		>>> # Univ. at Buffalo campus.
		>>> # This example includes all of the available function arguments.
		>>> import veroviz as vrv
		>>> myMap = vrv.addLeafletText(
		...     mapObject=None, 
		...     mapFilename=None, 
		...     mapBackground='CartoDB positron', 
		...     mapBoundary=None, 
		...     zoomStart=10, 
		...     anchorPoint=[43.00154, -78.7871],
		...     text="Bell Hall",
		...     fontSize=34, 
		...     fontColor='black', 
		...     horizAlign='left')
		>>> myMap
	"""	
	
	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletText(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, anchorPoint, text, fontSize, fontColor, horizAlign)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	anchorPoint = [anchorPoint[0], anchorPoint[1]]

	# If no mapObject exists, define a new mapObject
	if (mapObject == None):
		mapObject = _createLeafletMap(mapBackground=mapBackground, center=anchorPoint, zoomStart=zoomStart)
		
	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)

	iconSizeX = 900		# FIXME -- Not sure if this is good.
	
	try:
		horizAlign = horizAlign.lower()
	except:
		pass
		
	if (horizAlign == 'left'):
		iconAnchorX = 0
	elif (horizAlign == 'right'):
		iconAnchorX = iconSizeX
	else:
		iconAnchorX = iconSizeX / 2
				
	try:
		fontColor = fontColor.lower()
	except:
		pass
							
	folium.map.Marker(anchorPoint, icon=DivIcon(
		icon_size = (iconSizeX, fontSize), 
		icon_anchor = (iconAnchorX, fontSize), 
		html = "<div style=\"font-size: %dpt; color: %s; text-align: %s;\">%s</div>" %  (fontSize, fontColor, horizAlign, text)
		)).add_to(mapObject)

	if (mapFilename is not None):
		mapObject.save(mapFilename)
		if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
			print("Message: Map page written to %s." % (mapFilename))

	return mapObject
	
	
def addLeafletIcon(mapObject=None, mapFilename=None, mapBackground=config['VRV_DEFAULT_LEAFLET_MAPTILES'], mapBoundary=None, zoomStart=None, location=None, iconPrefix=config['VRV_DEFAULT_LEAFLETICONPREFIX'], iconType=config['VRV_DEFAULT_LEAFLETICONTYPE'], iconColor=config['VRV_DEFAULT_LEAFLETICONCOLOR'], iconText=None, popupText=None):

	"""
	Add a single icon/pin to a Leaflet map.

	Parameters
	----------
	mapObject: Folium object, Optional, default None
		A Folium map object.  If provided, the marker will be added to an existing map.  Otherwise, a new map will be created.
	mapFilename: string, Optional, default None 
		If provided, the map will be saved to this file, which should have a `.html` extension.  `mapFilename` can contain a filepath.  If `mapFilename` is not provided, no file will be generated.  The returned mapObject can be viewed within a Jupyter notebook. 
	mapBackground: string, Optional, default 'CartoDB positron'
		The tiles of the map, default to be 'CartoDB positron', for options, see :ref:`Leaflet Style`, also see folium documentation (https://python-visualization.github.io/folium/modules.html) for more options
	mapBoundary: list of lists, Optional, default None
		If provided, the mapBoundary coordinates are used to determine a zoom level such that these coordinates are contained within view when the map is opened.  This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  `mapBoundary` must be in the form [[south lat, west lon], [north lat, east lon]].	
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	location: list, Required, default as None
		Specifies the GPS coordinates of the icon/pin.  Must be a list of the form `[lat, lon]` or `[lat, lon, alt]`.  If provided, the altitude component will be ignored (as all locations on Leaflet maps are assumed to be at ground level).	
	iconPrefix: string, Optional, default as "glyphicon"
		There are a large number of Leaflet icons available. The `iconPrefix` identifies one of three collections: "glyphicon", "fa", or "custom".  See :ref:`Leaflet Style` for more information.
	iconType: string, Optional, default as "info-sign"
		Specifies the particular icon to be used for the icon/pin.  The list of available options depends on the choice of `iconPrefix`. See :ref:`Leaflet Style` for available options.
	iconColor: string, Optional, default as "blue"
		Defines the color of the icon/pin.  See :ref:`Leaflet Style` for the list of available color options.
	iconText: string, Optional, default as None
		Text that will be displayed within the node on a Leaflet map.  This text will only be shown if `iconPrefix` is 'custom' and `iconType` includes a font color and font size.  See :ref:`Leaflet style`.  
	popupText: string, Optional, default as None
		The icon/pin will include this text as a popup label (you will need to click on the pin in the map to see this label).
	
	Return
	------
	Folium object
		A Folium map object containing an icon/pin (and pre-existing items previously specified in mapObject).
		
	Example
	-------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Define a location:
		>>> whiteHouse = [38.8977, -77.0365]
		
	A minimal example, using mostly default parameters:
		>>> vrv.addLeafletIcon(location = whiteHouse)

	An example showing all function parameters:
		>>> vrv.addLeafletIcon(mapObject     = None, 
		...                    mapFilename   = None, 
		...                    mapBackground = 'arcgis aerial', 
		...                    mapBoundary   = None, 
		...                    zoomStart     = None, 
		...                    location      = whiteHouse, 
		...                    iconPrefix    = 'custom', 
		...                    iconType      = '18-yellow-12', 
		...                    iconColor     = 'purple', 
		...                    iconText      = 'WH', 
		...                    popupText     = '<nobr>click icon to see this single-line text</nobr>')
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletIcon(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, location, iconPrefix, iconType, iconColor, popupText)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	location = [location[0], location[1]]

	# If no mapObject exists, define a new mapObject
	if (mapObject == None):
		mapObject = _createLeafletMap(mapBackground=mapBackground, center=location, zoomStart=zoomStart)

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)

	_drawLeafletNode(mapObject, location, popupText, iconPrefix, iconType, iconColor, iconText)
	
	if (mapFilename is not None):
		mapObject.save(mapFilename)
		if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
			print("Message: Map page written to %s." % (mapFilename))

	return mapObject	
		
def addLeafletIsochrones(mapObject=None, mapFilename=None, mapBackground=config['VRV_DEFAULT_LEAFLET_MAPTILES'], mapBoundary=None, zoomStart=None, iso=None, showBoundingRegion=False, iconPrefix=config['VRV_DEFAULT_LEAFLETICONPREFIX'], iconType=config['VRV_DEFAULT_LEAFLETICONTYPE'], iconColor=config['VRV_DEFAULT_LEAFLETICONCOLOR'], iconText=None, popupText=None, lineWeight=3, lineOpacity=0.8, lineStyle='solid', fillOpacity=0.3):
	"""
	Easily draw isochrones on a Leaflet map.  Be sure to run the `isochrones()` function first.
		
	Parameters
	----------
	mapObject: Folium object, Optional, default None
		A Folium map object.  If provided, the marker will be added to an existing map.  Otherwise, a new map will be created.
	mapFilename: string, Optional, default None 
		If provided, the map will be saved to this file, which should have a `.html` extension.  `mapFilename` can contain a filepath.  If `mapFilename` is not provided, no file will be generated.  The returned mapObject can be viewed within a Jupyter notebook. 
	mapBackground: string, Optional, default 'CartoDB positron'
		The tiles of the map, default to be 'CartoDB positron', for options, see :ref:`Leaflet Style`, also see folium documentation (https://python-visualization.github.io/folium/modules.html) for more options
	mapBoundary: list of lists, Optional, default None
		If provided, the mapBoundary coordinates are used to determine a zoom level such that these coordinates are contained within view when the map is opened.  This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  `mapBoundary` must be in the form [[south lat, west lon], [north lat, east lon]].	
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	iso: isochrone object, Required, default as None
		See the `isochrones()` function for details on how to create this object.
	showBoundingRegion: boolean, Optional, default as False
		The isochrone object contains a bounding region, which is the smallest rectangle enclosing the isochrones.  If you wish to include this rectangle on the map, set `showBoundingRegion=True`.  
	iconPrefix: string, Optional, default as "glyphicon"
		There are a large number of Leaflet icons available. The `iconPrefix` identifies one of three collections: "glyphicon", "fa", or "custom".  See :ref:`Leaflet Style` for more information.
	iconType: string, Optional, default as "info-sign"
		Specifies the particular icon to be used for the icon/pin.  The list of available options depends on the choice of `iconPrefix`. See :ref:`Leaflet Style` for available options.
	iconColor: string, Optional, default as "blue"
		Defines the color of the icon/pin.  See :ref:`Leaflet Style` for the list of available color options.
	iconText: string, Optional, default as None
		Text that will be displayed within the node on a Leaflet map.  This text will only be shown if `iconPrefix` is 'custom' and `iconType` includes a font color and font size.  See :ref:`Leaflet style`.
	popupText: string, Optional, default as None
		The icon/pin will include this text as a popup label (you will need to click on the pin in the map to see this label).  
	lineWeight: int, Optional, default 3
		The width of the polygon's outline, in units of [pixels].  This value is ignored if `lineColor = None`. 
	lineOpacity: float in [0, 1], Optional, default 0.8
		Specifies the opacity of the polygon's outline.  Valid values are in the range from 0 (invisible) to 1 (no transparency).
	lineStyle: string, Optional, default 'solid'
		The style of the polygon's outline.  See :ref:`Leaflet Style` for a list of valid options.  
	fillOpacity: float in [0, 1], Optional, default 0.3
		Specifies the opacity of the polygon's interior.  Valid values are in the range from 0 (invisible) to 1 (no transparency). 

	Return
	------
	Folium object
		A Folium map object containing a polygon (and pre-existing items previously specified in mapObject).
		
	Example
	-------

	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	The following examples assume the use of ORS as the data provider.  If you have saved your API keys as environment variables, you may use `os.environ` to access them:
		>>> import os
		>>> 
		>>> ORS_API_KEY = os.environ['ORSKEY']
		>>> 
		>>> # Otherwise, you may specify your keys here:
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'

	Get isochrone data:
		>>> iso = vrv.isochrones(location         = [43.00154, -78.7871], 
		...                      locationType     = 'start', 
		...                      travelMode       = 'driving-car', 
		...                      rangeType        = 'time', 
		...                      rangeSize        = vrv.convertTime(5, 'minutes', 'seconds'), 
		...                      interval         = vrv.convertTime(2.5, 'minutes', 'seconds'), 
		...                      smoothing        = 5, 
		...                      dataProvider     ='ors-online', 
		...                      dataProviderArgs = {'APIkey': ORS_API_KEY})

	A minimal working example, using mostly default values:
		>>> vrv.addLeafletIsochrones(iso = iso)
		
	An example using all of the functional parameters:
		>>> vrv.addLeafletIsochrones(mapObject          = None, 
		...                          mapFilename        = None, 
		...                          mapBackground      = 'cartodb dark_matter', 
		...                          mapBoundary        = None, 
		...                          zoomStart          = None, 
		...                          iso                = iso, 
		...                          showBoundingRegion = True, 
		...                          iconPrefix         = 'custom', 
		...                          iconType           = '12-white-12', 
		...                          iconColor          = 'red', 
		...                          iconText           = '1', 
		...                          popupText          = None, 
		...                          lineWeight         = 3, 
		...                          lineOpacity        = 0.8, 
		...                          lineStyle          = 'solid', 
		...                          fillOpacity        = 0.3)		
	"""
	

	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletIsochrones(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, iso, showBoundingRegion, iconPrefix, iconType, iconColor, popupText, lineWeight, lineOpacity, lineStyle, fillOpacity)

	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	try:
		mapBackground = mapBackground.lower()
	except:
		pass


	# If no mapObject exists, define a new mapObject
	if (mapObject == None):
		# Adjust the scope of the map to properly show all objects
		[[minLat, maxLon], [maxLat, minLon]] = privGetMapBoundary(None, None, iso['boundingRegion'])

		midLat = (maxLat + minLat) / 2.0
		midLon = (maxLon + minLon) / 2.0
		mapObject = _createLeafletMap(mapBackground=mapBackground, center=[midLat,midLon], zoomStart=zoomStart)

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)
		elif (mapBoundary is None):
			mapObject.fit_bounds(privGetMapBoundary(None, None, iso['boundingRegion']))


	if (showBoundingRegion):
		folium.PolyLine(
			iso['boundingRegion'], 
			color = config['VRV_DEFAULT_LEAFLETBOUNDINGCOLOR'],
			weight = config['VRV_DEFAULT_LEAFLETBOUNDINGWEIGHT'],
			opacity = config['VRV_DEFAULT_LEAFLETBOUNDINGOPACITY'],
			dash_array = '30 10',
			popup = 'bounding region'
		).add_to(mapObject)


	_drawLeafletNode(mapObject, iso['location'], popupText, iconPrefix, iconType, iconColor, iconText)

	try:
		lineStyle = lineStyle.lower()
	except:
		pass
		
	# Interpret line style
	if (lineStyle == 'dashed'):
		dashArray = '30 10'
	elif (lineStyle == 'dotted'):
		dashArray = '1 6'
	else:
		dashArray = None
		
	try:
		fillColor = fillColor.lower()
	except:
		pass
	
	isoColorList = ['#9e0142', '#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#e6f598', '#abdda4', '#66c2a5', '#3288bd', '#5e4fa2']
	
	# Need to draw in reverse order (largest to smallest) so they are layered properly on map.  Otherwise, the big polygon will prevent clicking on smaller ones.
	for i in range(len(iso['isochrones'])-1, -1, -1):
		tmpText  = '<nobr>value: {} {}</nobr>\n'.format(iso['isochrones'][i]['value'], iso['isochrones'][i]['valueUnits'])
		tmpText += '<nobr>area: {} sq meters</nobr>\n'.format(iso['isochrones'][i]['area'])
		tmpText += '<nobr>pop: {}</nobr>\n'.format(iso['isochrones'][i]['pop'])
		tmpText += '<nobr>reachfactor: {}</nobr>\n'.format(iso['isochrones'][i]['reachfactor'])

		lineColor = isoColorList[i%len(isoColorList)]
		fillColor = lineColor
				
		# Each isochrone may have several polylines.
		for j in range(0, len(iso['isochrones'][i]['poly'])):
			folium.Polygon(locations = iso['isochrones'][i]['poly'][j], 
				stroke = True, 
				weight = lineWeight, 
				color = lineColor, 
				opacity = lineOpacity, 
				dash_array = dashArray,
				fill_color = fillColor,
				fill_opacity = fillOpacity,
				popup=str(tmpText)
				).add_to(mapObject)

	if (mapFilename is not None):
		mapObject.save(mapFilename)
		if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
			print("Message: Map page written to %s." % (mapFilename))

	return mapObject	
	
	
def addLeafletWeather(mapObject=None, mapType='precip', APIkey=None, mapFilename=None, mapBackground=config['VRV_DEFAULT_LEAFLET_MAPTILES']):
	"""
	Adds map tiles showing weather conditions to a Leaflet map.  Weather tiles are obtained via openweathermap.org (an API key is required).

	Parameters
	----------
	mapObject: Folium object, Optional, default as None
		If you already have a map (as a Folium object), you can provide that object and overlay weather on that map.
	mapType: string, Required, default as 'precip'
		Specifies the type of weather map to overlay on the mapObject.  Valid options are: 'clouds', 'precip', 'pressure', 'wind', and 'temp'.
	APIkey: string, Required, default at None
		These weather maps are hosted by openweathermap.org.  You may register for a free API key at their website.
	mapFilename: string, Optional, default as None
		This is the name of the map file that will be created (e.g., "../output/map.html" or "map.html").  The filename should have a `.html` extension.  If `mapFilename` is not provided, no map file will be generated.  The returned map object can be viewed within a Jupyter notebook.
	mapBackground: string, Optional, default as 'CartoDB positron'
		Sets the background tiles of the map.  See :ref:`Leaflet Style` for the list of options.
		
	Return
	------
	Folium object
		A Folium map object containing a text string (and pre-existing items previously specified in mapObject).
		
	Example
	-------

	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	If you have saved your API keys as environment variables, you may use `os.environ` to access them:
		>>> import os
		>>> 
		>>> OPENWEATHER_KEY = os.environ['OPENWEATHERKEY']
		>>> 
		>>> # Otherwise, you may specify your keys here:
		>>> # OPENWEATHER_KEY = 'YOUR_OPENWEATHERMAP_KEY_GOES_HERE'

	Display a map showing wind conditions.  This example includes all available function arguments.
		>>> vrv.addLeafletWeather(mapObject     = None,                          
		...                       mapType       = 'wind', 
		...                       APIkey        = OPENWEATHER_KEY, 
		...                       mapFilename   = None, 
		...                       mapBackground = 'cartodb dark_matter')
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletWeather(mapObject, mapType, APIkey, mapFilename, mapBackground)
	if (not valFlag):
		print (errorMsg)
		return
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	# Replace backslash
	mapFilename = replaceBackslashToSlash(mapFilename)

	try:
		mapType = mapType.lower()
	except:
		pass

	try:
		mapBackground = mapBackground.lower()
	except:
		pass
		
	# If no mapObject exists, define a new mapObject
	if (mapObject == None):
		mapObject = _createLeafletMap(mapBackground=mapBackground, center=[0,0])
	
	# Add the weather map layer:
	folium.TileLayer(
		tiles = '%s%s' % (weatherMaps[mapType]['tiles'], APIkey),
		attr  = weatherMaps[mapType]['attr']
	).add_to(mapObject)


	if (mapFilename is not None):		
		mapDirectory = ""
		strList = mapFilename.split("/")
		for i in range(len(strList) - 1):
			mapDirectory += strList[i] + "/"
		if (mapDirectory != ""):
			if (not os.path.exists(mapDirectory)):
				os.makedirs(mapDirectory, exist_ok=True)

		mapObject.save(mapFilename)
		if (config['VRV_SETTING_SHOWOUTPUTMESSAGE']):
			print("Message: Map page written to %s." % (mapFilename))
	
	return mapObject




	# weatherMaps	
	
	
