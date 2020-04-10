# Const for distance unit changing
VRV_CONST_METERS_PER_KILOMETER = 1000.0
VRV_CONST_METERS_PER_MILE = 1609.34
VRV_CONST_METERS_PER_YARD = 0.9144
VRV_CONST_METERS_PER_FEET = 0.3048
VRV_CONST_METERS_PER_NAUTICAL_MILE = 1852.0

# Const for speed unit changing
VRV_CONST_MPS_TO_KPH = 3.6
VRV_CONST_MPS_TO_MPH = 2.23694

# Const for time unit changing
VRV_CONST_SECONDS_PER_HOUR = 3600.0
VRV_CONST_SECONDS_PER_MINUTE = 60.0

# Defaults for adding Leaflet objects (e.g., circles, polygons, text)
VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE = 'red'
VRV_DEFAULT_LEAFLET_OBJECT_COLOR_FILL = 'red'
VRV_DEFAULT_LEAFLET_FONTSIZE = 24	# pt
VRV_DEFAULT_LEAFLET_FONTCOLOR = 'orange'
VRV_DEFAULT_LEAFLET_MAPTILES = 'CartoDB positron'

# Area conversions
VRV_CONST_SQKM_PER_SQMETER = 1e-6
VRV_CONST_SQMILES_PER_SQMETER = 3.861e-7 
VRV_CONST_SQFT_PER_SQMETER = 10.7639

# Default error tolerance of distance between origin/destin to snapped loc
VRV_DEFAULT_DISTANCE_ERROR_TOLERANCE = 10 # [meters]

# Standard const
VRV_CONST_RADIUS_OF_EARTH = 6378100.0	# [meters]

# Default Setting for leaflet
VRV_DEFAULT_LEAFLETICONPREFIX = 'glyphicon'
VRV_DEFAULT_LEAFLETICONTYPE = 'info-sign'
VRV_DEFAULT_LEAFLETICONCOLOR = 'blue'

VRV_DEFAULT_LEAFLETARCWEIGHT = 3
VRV_DEFAULT_LEAFLETARCSTYLE = 'solid'
VRV_DEFAULT_LEAFLETARCOPACITY = 0.8
VRV_DEFAULT_LEAFLETARCCOLOR = 'orange'

VRV_DEFAULT_LEAFLETBOUNDINGWEIGHT = 3
VRV_DEFAULT_LEAFLETBOUNDINGOPACITY = 0.6
VRV_DEFAULT_LEAFLETBOUNDINGSTYLE = 'dashed'
VRV_DEFAULT_LEAFLETBOUNDINGCOLOR = 'brown'

# Default Setting for Cesium
VRV_DEFAULT_CESIUMMODELSCALE = 100 # 100%
VRV_DEFAULT_CESIUMMODELMINPXSIZE = 75 # px

VRV_DEFAULT_CESIUMICONTYPE = 'pin'
VRV_DEFAULT_CESIUMICONSIZE = 40
VRV_DEFAULT_CESIUMICONCOLOR = 'Cesium.Color.BLUE'

VRV_DEFAULT_CESIUMPATHCOLOR = 'Cesium.Color.ORANGE'
VRV_DEFAULT_CESIUMPATHWEIGHT = 3
VRV_DEFAULT_CESIUMPATHSTYLE = 'solid'
VRV_DEFAULT_CESIUMPATHOPACITY = 0.8
VRV_DEFAULT_LEAFLET_ARROWSIZE = 6
# Global Setting
VRV_SETTING_PGROUTING_USERNAME = 'user'
VRV_SETTING_PGROUTING_HOST = 'localhost'
VRV_SETTING_PGROUTING_PASSWORD = ''

VRV_SETTING_SHOWOUTPUTMESSAGE = True
VRV_SETTING_SHOWWARNINGMESSAGE = True

# For validation

nodesColumnList = [
	'id', 
	'lat', 
	'lon', 
	'altMeters', 
	'nodeName', 
	'nodeType', 
	'leafletIconPrefix', 
	'leafletIconType', 
	'leafletColor', 
	'leafletIconText', 
	'cesiumIconType', 
	'cesiumColor', 
	'cesiumIconText'
]

arcsColumnList = [
	'odID',
	'objectID', 
	'startLat', 
	'startLon',
	'endLat', 
	'endLon',
	'leafletColor', 
	'leafletWeight', 
	'leafletStyle', 
	'leafletOpacity', 
	'useArrows', 
	'cesiumColor', 
	'cesiumWeight', 
	'cesiumStyle', 
	'cesiumOpacity'
]

assignmentsColumnList = [
	'odID', 
	'objectID', 
	'modelFile', 
	'modelScale',
	'modelMinPxSize',
	'startTimeSec', 
	'startLat', 
	'startLon', 
	'startAltMeters',
	'endTimeSec', 
	'endLat', 
	'endLon', 
	'endAltMeters',
	'leafletColor', 
	'leafletWeight', 
	'leafletStyle', 
	'leafletOpacity', 
	'useArrows', 
	'cesiumColor', 
	'cesiumWeight', 
	'cesiumStyle', 
	'cesiumOpacity'
]

timeUnitsDictionary = {
	'seconds': 's',
	'second': 's',
	'sec': 's',
	's': 's',

	'minutes': 'min',
	'minute': 'min',
	'mins': 'min', 
	'min': 'min', 

	'hours': 'h',
	'hour': 'h',
	'hrs': 'h',
	'hr': 'h',
	'h': 'h',
}

distanceUnitsDictionary = {
	'meters': 'm',
	'm': 'm',

	'kilometers': 'km',
	'km': 'km',

	'miles': 'mi',
	'mi': 'mi',

	'yard': 'yard',

	'feet': 'ft',
	'ft': 'ft',

	'nautical miles': 'nmi',
	'nmi': 'nmi',
	'nm': 'nmi'
}

areaUnitsDictionary = {
	'sf': 'sqft',
	'sqft': 'sqft',
	'sqfeet': 'sqft',
	
	'smi': 'sqmi',
	'sqmi': 'sqmi',
	'sqmiles': 'sqmi',
	
	'sm': 'sqm',
	'sqm': 'sqm',
	'sqmeters': 'sqm',

	'skm': 'sqkm',
	'sqkm': 'sqkm',
	'sqkilometers': 'sqkm'
}

mapBackgroundList = {
	'cartodb positron', 
	'cartodb dark_matter', 
	'openstreetmap', 
	'stamen terrain', 
	'stamen toner', 
	'stamen watercolor',
	'arcgis aerial', 
	'arcgis gray', 
	'arcgis ocean', 
	'arcgis roadmap', 
	'arcgis shaded relief', 
	'arcgis topo', 
	'open topo'
}

horizAlignList = {
	'left',
	'right',
	'center'
}

dataframeList = {
	'nodes',
	'arcs',
	'assignments'
}

loiterPositionList = [
	'beforeTakeoff',
	'takeoffAtAlt',
	'arrivalAtAlt',
	'afterLand'
]

routeType2DList = [
	'euclidean2d', 
	'manhattan', 
	'fastest', 
	'shortest', 
	'pedestrian',
	'cycling',
	'truck'
]

routeType3DList = [
	'square',
	'triangular',
	'trapezoidal',
	'straight'
]

isoTravelModeList = [
	'driving-car',
	'driving-hgv',
	'cycling-regular',
	'cycling-road',
	'cycling-mountain',
	'cycling-electric',
	'foot-walking',
	'foot-hiking',					
	'wheelchair'
]

dataProviderDictionary = {
	'mapquest': 'mapquest',
	'mq': 'mapquest',

	'pgrouting': 'pgrouting',
	'pgr': 'pgrouting',

	'osrm-online': 'osrm-online',
	'osrm-ol': 'osrm-online',

	'openrouteservice-online': 'ors-online',
	'openrouteservice-ol': 'ors-online',
	'ors-online': 'ors-online',
	'ors-ol': 'ors-online'
}

# NOTE:  The only valid dataProviders for the geocode()/reverseGeocode() functions are:
#        None, 'ors-online', and 'mapquest'
geoDataProviderDictionary = {
	'mapquest': 'mapquest',
	'mq': 'mapquest',

	'openrouteservice-online': 'ors-online',
	'openrouteservice-ol': 'ors-online',
	'ors-online': 'ors-online',
	'ors-ol': 'ors-online'
}

# NOTE: The only valid dataProvider for isochrones functions is:
#       ors-online
isoDataProviderDictionary = {
	'openrouteservice-online': 'ors-online',
	'openrouteservice-ol': 'ors-online',
	'ors-online': 'ors-online',
	'ors-ol': 'ors-online'
}


matrixTypeList = [
	'all2all', 
	'one2many', 
	'many2one'
]

nodeDistribList = [
	"uniformBB", 
	"normalBB", 
	"normal"
	# "unifRoadBasedBB" 
] # Removed 'unifRoadBasedBB' for v.0.2.0

cesiumIconTypeList = [
	'pin'
]

cesiumColorList = [
	"Cesium.Color.ALICEBLUE",
	"Cesium.Color.ANTIQUEWHITE",
	"Cesium.Color.AQUA",
	"Cesium.Color.AQUAMARINE",
	"Cesium.Color.AZURE",
	"Cesium.Color.BEIGE",
	"Cesium.Color.BISQUE",
	"Cesium.Color.BLACK",
	"Cesium.Color.BLANCHEDALMOND",
	"Cesium.Color.BLUE",
	"Cesium.Color.BLUEVIOLET",
	"Cesium.Color.BROWN",
	"Cesium.Color.BURLYWOOD",
	"Cesium.Color.CADETBLUE",
	"Cesium.Color.CHARTREUSE",
	"Cesium.Color.CHOCOLATE",
	"Cesium.Color.CORAL",
	"Cesium.Color.CORNFLOWERBLUE",
	"Cesium.Color.CORNSILK",
	"Cesium.Color.CRIMSON",
	"Cesium.Color.CYAN",
	"Cesium.Color.DARKBLUE",
	"Cesium.Color.DARKCYAN",
	"Cesium.Color.DARKGOLDENROD",
	"Cesium.Color.DARKGRAY",
	"Cesium.Color.DARKGREEN",
	"Cesium.Color.DARKGREY",
	"Cesium.Color.DARKKHAKI",
	"Cesium.Color.DARKMAGENTA",
	"Cesium.Color.DARKOLIVEGREEN",
	"Cesium.Color.DARKORANGE",
	"Cesium.Color.DARKORCHID",
	"Cesium.Color.DARKRED",
	"Cesium.Color.DARKSALMON",
	"Cesium.Color.DARKSEAGREEN",
	"Cesium.Color.DARKSLATEBLUE",
	"Cesium.Color.DARKSLATEGRAY",
	"Cesium.Color.DARKSLATEGREY",
	"Cesium.Color.DARKTURQUOISE",
	"Cesium.Color.DARKVIOLET",
	"Cesium.Color.DEEPPINK",
	"Cesium.Color.DEEPSKYBLUE",
	"Cesium.Color.DIMGRAY",
	"Cesium.Color.DIMGREY",
	"Cesium.Color.DODGERBLUE",
	"Cesium.Color.FIREBRICK",
	"Cesium.Color.FLORALWHITE",
	"Cesium.Color.FORESTGREEN",
	"Cesium.Color.FUCHSIA",
	"Cesium.Color.GAINSBORO",
	"Cesium.Color.GHOSTWHITE",
	"Cesium.Color.GOLD",
	"Cesium.Color.GOLDENROD",
	"Cesium.Color.GRAY",
	"Cesium.Color.GREEN",
	"Cesium.Color.GREENYELLOW",
	"Cesium.Color.GREY",
	"Cesium.Color.HONEYDEW",
	"Cesium.Color.HOTPINK",
	"Cesium.Color.INDIANRED",
	"Cesium.Color.INDIGO",
	"Cesium.Color.IVORY",
	"Cesium.Color.KHAKI",
	"Cesium.Color.LAVENDAR_BLUSH",
	"Cesium.Color.LAVENDER",
	"Cesium.Color.LAWNGREEN",
	"Cesium.Color.LEMONCHIFFON",
	"Cesium.Color.LIGHTBLUE",
	"Cesium.Color.LIGHTCORAL",
	"Cesium.Color.LIGHTCYAN",
	"Cesium.Color.LIGHTGOLDENRODYELLOW",
	"Cesium.Color.LIGHTGRAY",
	"Cesium.Color.LIGHTGREEN",
	"Cesium.Color.LIGHTGREY",
	"Cesium.Color.LIGHTPINK",
	"Cesium.Color.LIGHTSEAGREEN",
	"Cesium.Color.LIGHTSKYBLUE",
	"Cesium.Color.LIGHTSLATEGRAY",
	"Cesium.Color.LIGHTSLATEGREY",
	"Cesium.Color.LIGHTSTEELBLUE",
	"Cesium.Color.LIGHTYELLOW",
	"Cesium.Color.LIME",
	"Cesium.Color.LIMEGREEN",
	"Cesium.Color.LINEN",
	"Cesium.Color.MAGENTA",
	"Cesium.Color.MAROON",
	"Cesium.Color.MEDIUMAQUAMARINE",
	"Cesium.Color.MEDIUMBLUE",
	"Cesium.Color.MEDIUMORCHID",
	"Cesium.Color.MEDIUMPURPLE",
	"Cesium.Color.MEDIUMSEAGREEN",
	"Cesium.Color.MEDIUMSLATEBLUE",
	"Cesium.Color.MEDIUMSPRINGGREEN",
	"Cesium.Color.MEDIUMTURQUOISE",
	"Cesium.Color.MEDIUMVIOLETRED",
	"Cesium.Color.MIDNIGHTBLUE",
	"Cesium.Color.MINTCREAM",
	"Cesium.Color.MISTYROSE",
	"Cesium.Color.MOCCASIN",
	"Cesium.Color.NAVAJOWHITE",
	"Cesium.Color.NAVY",
	"Cesium.Color.OLDLACE",
	"Cesium.Color.OLIVE",
	"Cesium.Color.OLIVEDRAB",
	"Cesium.Color.ORANGE",
	"Cesium.Color.ORANGERED",
	"Cesium.Color.ORCHID",
	"Cesium.Color.PALEGOLDENROD",
	"Cesium.Color.PALEGREEN",
	"Cesium.Color.PALETURQUOISE",
	"Cesium.Color.PALEVIOLETRED",
	"Cesium.Color.PAPAYAWHIP",
	"Cesium.Color.PEACHPUFF",
	"Cesium.Color.PERU",
	"Cesium.Color.PINK",
	"Cesium.Color.PLUM",
	"Cesium.Color.POWDERBLUE",
	"Cesium.Color.PURPLE",
	"Cesium.Color.RED",
	"Cesium.Color.ROSYBROWN",
	"Cesium.Color.ROYALBLUE",
	"Cesium.Color.SADDLEBROWN",
	"Cesium.Color.SALMON",
	"Cesium.Color.SANDYBROWN",
	"Cesium.Color.SEAGREEN",
	"Cesium.Color.SEASHELL",
	"Cesium.Color.SIENNA",
	"Cesium.Color.SILVER",
	"Cesium.Color.SKYBLUE",
	"Cesium.Color.SLATEBLUE",
	"Cesium.Color.SLATEGRAY",
	"Cesium.Color.SLATEGREY",
	"Cesium.Color.SNOW",
	"Cesium.Color.SPRINGGREEN",
	"Cesium.Color.STEELBLUE",
	"Cesium.Color.TAN",
	"Cesium.Color.TEAL",
	"Cesium.Color.THISTLE",
	"Cesium.Color.TOMATO",
	"Cesium.Color.TRANSPARENT",
	"Cesium.Color.TURQUOISE",
	"Cesium.Color.VIOLET",
	"Cesium.Color.WHEAT",
	"Cesium.Color.WHITE",
	"Cesium.Color.WHITESMOKE",
	"Cesium.Color.YELLOW",
	"Cesium.Color.YELLOWGREEN"
]

cesiumStyleList = [
	"dashed", 
	"dotted", 
	"solid"
]

leafletColorList = [
	'red',
	'blue',
	'gray',
	'darkred',
	'lightred',
	'orange',
	'beige',
	'green',
	'darkgreen',
	'lightgreen',
	'darkblue',
	'lightblue',
	'purple',
	'darkpurple',
	'pink',
	'cadetblue',
	'lightgray',
	'black',
	'white',
	'brown'
]

leafletIconPrefixList = [
	"glyphicon", 
	"fa"
]

leafletIconGlyphicon = [
	'info-sign',
	'home',
	'glass',
	'flag',
	'star',
	'bookmark',
	'user',
	'cloud'
]

leafletIconFa = [
	'ambulance',
	'bicycle',
	'bus',
	'car',
	'flag',
	'heartbeat',
	'home',
	'motorcycle',
	'plane',
	'question',
	'ship',
	'shopping-bag',
	'shopping-basket',
	'shopping-cart',
	'star',
	'subway',
	'taxi',
	'truck',
	'university',
	'user',
	'users'
]

leafletStyleList = [
	"dashed", 
	"dotted", 
	"solid"
]