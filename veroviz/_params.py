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

# Area conversions
VRV_CONST_SQKM_PER_SQMETER = 1e-6
VRV_CONST_SQMILES_PER_SQMETER = 3.861e-7 
VRV_CONST_SQFT_PER_SQMETER = 10.7639

# Standard const
VRV_CONST_RADIUS_OF_EARTH = 6378100.0	# [meters]

# # Default error tolerance of distance between origin/destin to snapped loc
# VRV_DEFAULT_DISTANCE_ERROR_TOLERANCE = 10 # [meters]

# # Defaults for adding Leaflet objects (e.g., circles, polygons, text)
# VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE = 'red'
# VRV_DEFAULT_LEAFLET_OBJECT_COLOR_FILL = 'red'
# VRV_DEFAULT_LEAFLET_FONTSIZE = 24	# pt
# VRV_DEFAULT_LEAFLET_FONTCOLOR = 'orange'
# VRV_DEFAULT_LEAFLET_MAPTILES = 'CartoDB positron'

# # Default Setting for leaflet
# VRV_DEFAULT_LEAFLETICONPREFIX = 'glyphicon'
# VRV_DEFAULT_LEAFLETICONTYPE = 'info-sign'
# VRV_DEFAULT_LEAFLETICONCOLOR = 'blue'

# VRV_DEFAULT_LEAFLETARCWEIGHT = 3
# VRV_DEFAULT_LEAFLETARCSTYLE = 'solid'
# VRV_DEFAULT_LEAFLETARCOPACITY = 0.8
# VRV_DEFAULT_LEAFLETARCCOLOR = 'orange'

# VRV_DEFAULT_LEAFLETBOUNDINGWEIGHT = 3
# VRV_DEFAULT_LEAFLETBOUNDINGOPACITY = 0.6
# VRV_DEFAULT_LEAFLETBOUNDINGSTYLE = 'dashed'
# VRV_DEFAULT_LEAFLETBOUNDINGCOLOR = 'brown'

# VRV_DEFAULT_ARCCURVETYPE = 'straight'
# VRV_DEFAULT_ARCCURVATURE = 0

# # Default Setting for Cesium
# VRV_DEFAULT_CESIUMMODELSCALE = 100 # 100%
# VRV_DEFAULT_CESIUMMODELMINPXSIZE = 75 # px

# VRV_DEFAULT_CESIUMICONTYPE = 'pin'
# VRV_DEFAULT_CESIUMICONSIZE = 40
# VRV_DEFAULT_CESIUMICONCOLOR = 'blue'

# VRV_DEFAULT_CESIUMPATHCOLOR = 'orange'
# VRV_DEFAULT_CESIUMPATHWEIGHT = 3
# VRV_DEFAULT_CESIUMPATHSTYLE = 'solid'
# VRV_DEFAULT_CESIUMPATHOPACITY = 0.8
# VRV_DEFAULT_LEAFLET_ARROWSIZE = 6

# # Default Settings for Gantt Chart
# VRV_DEFAULT_GANTTCOLOR = 'darkgray'
# VRV_DEFAULT_GANTTCOLORSERVICE = 'lightgray'
# VRV_DEFAULT_GANTTCOLORLOITER = 'lightgray'

# # Global Setting
# VRV_SETTING_PGROUTING_USERNAME = 'user'
# VRV_SETTING_PGROUTING_HOST = 'localhost'
# VRV_SETTING_PGROUTING_PASSWORD = ''

# VRV_SETTING_SHOWOUTPUTMESSAGE = True
# VRV_SETTING_SHOWWARNINGMESSAGE = True

config = {
	"VRV_DEFAULT_DISTANCE_ERROR_TOLERANCE" : 10,
	"VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE" : 'red',
	"VRV_DEFAULT_LEAFLET_OBJECT_COLOR_FILL" : 'red',
	"VRV_DEFAULT_LEAFLET_FONTSIZE" : 24,
	"VRV_DEFAULT_LEAFLET_FONTCOLOR" : 'orange',
	"VRV_DEFAULT_LEAFLET_MAPTILES" : 'CartoDB positron',
	"VRV_DEFAULT_LEAFLETICONPREFIX" : 'glyphicon',
	"VRV_DEFAULT_LEAFLETICONTYPE" : 'info-sign',
	"VRV_DEFAULT_LEAFLETICONCOLOR" : 'blue',
	"VRV_DEFAULT_LEAFLETARCWEIGHT" : 3,
	"VRV_DEFAULT_LEAFLETARCSTYLE" : 'solid',
	"VRV_DEFAULT_LEAFLETARCOPACITY" : 0.8,
	"VRV_DEFAULT_LEAFLETARCCOLOR" : 'orange',
	"VRV_DEFAULT_LEAFLETBOUNDINGWEIGHT" : 3,
	"VRV_DEFAULT_LEAFLETBOUNDINGOPACITY" : 0.6,
	"VRV_DEFAULT_LEAFLETBOUNDINGSTYLE" : 'dashed',
	"VRV_DEFAULT_LEAFLETBOUNDINGCOLOR" : 'brown',
	"VRV_DEFAULT_ARCCURVETYPE" : 'straight',
	"VRV_DEFAULT_ARCCURVATURE" : 0,
	"VRV_DEFAULT_CESIUMMODELSCALE" : 100,
	"VRV_DEFAULT_CESIUMMODELMINPXSIZE" : 75,
	"VRV_DEFAULT_CESIUMICONTYPE" : 'pin',
	"VRV_DEFAULT_CESIUMICONSIZE" : 40,
	"VRV_DEFAULT_CESIUMICONCOLOR" : 'blue',
	"VRV_DEFAULT_CESIUMPATHCOLOR" : 'orange',
	"VRV_DEFAULT_CESIUMPATHWEIGHT" : 3,
	"VRV_DEFAULT_CESIUMPATHSTYLE" : 'solid',
	"VRV_DEFAULT_CESIUMPATHOPACITY" : 0.8,
	"VRV_DEFAULT_LEAFLET_ARROWSIZE" : 6,
	"VRV_DEFAULT_GANTTCOLOR" : 'darkgray',
	"VRV_DEFAULT_GANTTCOLORSERVICE" : 'lightgray',
	"VRV_DEFAULT_GANTTCOLORLOITER" : 'lightgray',
	"VRV_SETTING_PGROUTING_USERNAME" : 'user',
	"VRV_SETTING_PGROUTING_HOST" : 'localhost',
	"VRV_SETTING_PGROUTING_PASSWORD" : '',
	"VRV_SETTING_SHOWOUTPUTMESSAGE" : True,
	"VRV_SETTING_SHOWWARNINGMESSAGE" : True
}

dtypeMapping = {'assignments': {
	'odID'             : int,       
	'objectID'         : str,
	'modelFile'        : str,
	'modelScale'       : int,
	'modelMinPxSize'   : int,
	'startTimeSec'     : int,
	'startLat'         : float,
	'startLon'         : float,
	'startAltMeters'   : float,
	'endTimeSec'       : int,
	'endLat'           : float,
	'endLon'           : float,
	'endAltMeters'     : float,
	'leafletColor'     : str,
	'leafletOpacity'   : float,
	'leafletStyle'     : str,
	'leafletCurveType' : str,
	'leafletCurvature' : float,
	'useArrows'        : bool,
	'cesiumWeight'     : int,
	'cesiumColor'      : str,
	'cesiumOpacity'    : float,
	'cesiumStyle'      : str,
	'cesiumWeight'     : int,
	'ganttColor'       : str,
	'popupText'        : str,
	'startElevMeters'  : float,
	'endElevMeters'    : float,
	'wayname'          : str,
	'waycategory'      : str,
	'surface'          : str,
	'waytype'          : str,
	'steepness'        : int,
	'tollway'          : bool
}}

# For validation
nodesColumnList = [
	'id', 
	'lat', 
	'lon', 
	'altMeters', 
	'nodeName', 
	'nodeType', 
	'popupText',
	'leafletIconPrefix', 
	'leafletIconType', 
	'leafletColor', 
	'leafletIconText', 
	'cesiumIconType', 
	'cesiumColor', 
	'cesiumIconText',
	'elevMeters'
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
	'leafletCurveType',
	'leafletCurvature',	
	'useArrows', 
	'cesiumColor', 
	'cesiumWeight', 
	'cesiumStyle', 
	'cesiumOpacity',
	'popupText',
	'startElevMeters',
	'endElevMeters',	
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
	'leafletCurveType',
	'leafletCurvature',
	'useArrows', 
	'cesiumColor', 
	'cesiumWeight', 
	'cesiumStyle', 
	'cesiumOpacity', 
	'ganttColor',
	'popupText',
	'startElevMeters',
	'endElevMeters',
	'wayname',
	'waycategory',
	'surface',
	'waytype', 
	'steepness',
	'tollway'
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

weatherMapList = {
	'clouds', 
	'precip', 
	'pressure', 
	'wind', 
	'temp'
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
	'beforetakeoff',
	'takeoffatalt',
	'arrivalatalt',
	'afterland'
]

routeType2DList = [
	'euclidean2d', 
	'manhattan', 
	'fastest', 
	'shortest', 
	'pedestrian',
	'cycling',
	'truck',
	'wheelchair'
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
	'ors-ol': 'ors-online',
	
	'openrouteservice-local': 'ors-local',
	'openrouteservice-l': 'ors-local',
	'ors-local': 'ors-local',
	'ors-l': 'ors-local'
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

# NOTE: The only valid dataProvider options for isochrones functions are:
#       ors-online and ors-local
isoDataProviderDictionary = {
	'openrouteservice-online': 'ors-online',
	'openrouteservice-ol': 'ors-online',
	'ors-online': 'ors-online',
	'ors-ol': 'ors-online',

	'openrouteservice-local': 'ors-local',
	'openrouteservice-l': 'ors-local',
	'ors-local': 'ors-local',
	'ors-l': 'ors-local'
}

# NOTE: The only valid dataProvider options for elevation functions are:
#       ors-online
#       usgs
#		elevAPI
elevDataProviderDictionary = {
	'openrouteservice-online': 'ors-online',
	'openrouteservice-ol': 'ors-online',
	'ors-online': 'ors-online',
	'ors-ol': 'ors-online',
	
	'usgs': 'usgs',
	
	'elevapi': 'elevapi',
	'elev-api': 'elevapi',
	'elevation-api': 'elevapi',
	'elevationapi': 'elevapi'
}

weatherDataProviderDictionary = {
	'openweather': 'openweather',
	'openweathermap': 'openweather',
	'openweatherapi': 'openweather',
	'ow': 'openweather',
	'owm': 'openweather'
}

matrixTypeList = [
	'all2all', 
	'one2many', 
	'many2one'
]

nodeDistribList = [
	"uniformBB", 
	"normalBB", 
	"normal",
	"unifRoadBasedBB" 
] 

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

matplotlibColorDict = {
	'aliceblue':            '#F0F8FF',
	'antiquewhite':         '#FAEBD7',
	'aqua':                 '#00FFFF',
	'aquamarine':           '#7FFFD4',
	'azure':                '#F0FFFF',
	'beige':                '#F5F5DC',
	'bisque':               '#FFE4C4',
	'black':                '#000000',
	'blanchedalmond':       '#FFEBCD',
	'blue':                 '#0000FF',
	'blueviolet':           '#8A2BE2',
	'brown':                '#A52A2A',
	'burlywood':            '#DEB887',
	'cadetblue':            '#5F9EA0',
	'chartreuse':           '#7FFF00',
	'chocolate':            '#D2691E',
	'coral':                '#FF7F50',
	'cornflowerblue':       '#6495ED',
	'cornsilk':             '#FFF8DC',
	'crimson':              '#DC143C',
	'cyan':                 '#00FFFF',
	'darkblue':             '#00008B',
	'darkcyan':             '#008B8B',
	'darkgoldenrod':        '#B8860B',
	'darkgray':             '#A9A9A9',
	'darkgreen':            '#006400',
	'darkkhaki':            '#BDB76B',
	'darkmagenta':          '#8B008B',
	'darkolivegreen':       '#556B2F',
	'darkorange':           '#FF8C00',
	'darkorchid':           '#9932CC',
	'darkred':              '#8B0000',
	'darksalmon':           '#E9967A',
	'darkseagreen':         '#8FBC8F',
	'darkslateblue':        '#483D8B',
	'darkslategray':        '#2F4F4F',
	'darkturquoise':        '#00CED1',
	'darkviolet':           '#9400D3',
	'deeppink':             '#FF1493',
	'deepskyblue':          '#00BFFF',
	'dimgray':              '#696969',
	'dodgerblue':           '#1E90FF',
	'firebrick':            '#B22222',
	'floralwhite':          '#FFFAF0',
	'forestgreen':          '#228B22',
	'fuchsia':              '#FF00FF',
	'gainsboro':            '#DCDCDC',
	'ghostwhite':           '#F8F8FF',
	'gold':                 '#FFD700',
	'goldenrod':            '#DAA520',
	'gray':                 '#808080',
	'green':                '#008000',
	'greenyellow':          '#ADFF2F',
	'honeydew':             '#F0FFF0',
	'hotpink':              '#FF69B4',
	'indianred':            '#CD5C5C',
	'indigo':               '#4B0082',
	'ivory':                '#FFFFF0',
	'khaki':                '#F0E68C',
	'lavender':             '#E6E6FA',
	'lavenderblush':        '#FFF0F5',
	'lawngreen':            '#7CFC00',
	'lemonchiffon':         '#FFFACD',
	'lightblue':            '#ADD8E6',
	'lightcoral':           '#F08080',
	'lightcyan':            '#E0FFFF',
	'lightgoldenrodyellow': '#FAFAD2',
	'lightgreen':           '#90EE90',
	'lightgray':            '#D3D3D3',
	'lightpink':            '#FFB6C1',
	'lightsalmon':          '#FFA07A',
	'lightseagreen':        '#20B2AA',
	'lightskyblue':         '#87CEFA',
	'lightslategray':       '#778899',
	'lightsteelblue':       '#B0C4DE',
	'lightyellow':          '#FFFFE0',
	'lime':                 '#00FF00',
	'limegreen':            '#32CD32',
	'linen':                '#FAF0E6',
	'magenta':              '#FF00FF',
	'maroon':               '#800000',
	'mediumaquamarine':     '#66CDAA',
	'mediumblue':           '#0000CD',
	'mediumorchid':         '#BA55D3',
	'mediumpurple':         '#9370DB',
	'mediumseagreen':       '#3CB371',
	'mediumslateblue':      '#7B68EE',
	'mediumspringgreen':    '#00FA9A',
	'mediumturquoise':      '#48D1CC',
	'mediumvioletred':      '#C71585',
	'midnightblue':         '#191970',
	'mintcream':            '#F5FFFA',
	'mistyrose':            '#FFE4E1',
	'moccasin':             '#FFE4B5',
	'navajowhite':          '#FFDEAD',
	'navy':                 '#000080',
	'oldlace':              '#FDF5E6',
	'olive':                '#808000',
	'olivedrab':            '#6B8E23',
	'orange':               '#FFA500',
	'orangered':            '#FF4500',
	'orchid':               '#DA70D6',
	'palegoldenrod':        '#EEE8AA',
	'palegreen':            '#98FB98',
	'paleturquoise':        '#AFEEEE',
	'palevioletred':        '#DB7093',
	'papayawhip':           '#FFEFD5',
	'peachpuff':            '#FFDAB9',
	'peru':                 '#CD853F',
	'pink':                 '#FFC0CB',
	'plum':                 '#DDA0DD',
	'powderblue':           '#B0E0E6',
	'purple':               '#800080',
	'red':                  '#FF0000',
	'rosybrown':            '#BC8F8F',
	'royalblue':            '#4169E1',
	'saddlebrown':          '#8B4513',
	'salmon':               '#FA8072',
	'sandybrown':           '#FAA460',
	'seagreen':             '#2E8B57',
	'seashell':             '#FFF5EE',
	'sienna':               '#A0522D',
	'silver':               '#C0C0C0',
	'skyblue':              '#87CEEB',
	'slateblue':            '#6A5ACD',
	'slategray':            '#708090',
	'snow':                 '#FFFAFA',
	'springgreen':          '#00FF7F',
	'steelblue':            '#4682B4',
	'tan':                  '#D2B48C',
	'teal':                 '#008080',
	'thistle':              '#D8BFD8',
	'tomato':               '#FF6347',
	'turquoise':            '#40E0D0',
	'violet':               '#EE82EE',
	'wheat':                '#F5DEB3',
	'white':                '#FFFFFF',
	'whitesmoke':           '#F5F5F5',
	'yellow':               '#FFFF00',
	'yellowgreen':          '#9ACD32'
}

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
	"fa",
	"custom"
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

# Mapping from ORS ID numbers to more descriptive explanations.
# See https://github.com/GIScience/openrouteservice-docs#routing-response for more info
orsWaycategoryDict = {
	0: 'No category',
	1: 'Highway',
	2: 'Steps',
	4: 'Ferry',
	8: 'Unpaved road',
	16: 'Track',
	32: 'Tunnel',
	64: 'Paved road',
	128: 'Ford'
}

# https://github.com/GIScience/openrouteservice-docs#surface
orsSurfaceDict = {
	0: 'Unknown',
	1: 'Paved',
	2: 'Unpaved',
	3: 'Asphalt',
	4: 'Concrete',
	5: 'Cobblestone',
	6: 'Metal',
	7: 'Wood',
	8: 'Compacted Gravel',
	9: 'Fine Gravel',
	10: 'Gravel',
	11: 'Dirt',
	12: 'Ground',
	13: 'Ice',
	14: 'Paving Stones',
	15: 'Sand',
	16: 'Woodchips',
	17: 'Grass',
	18: 'Grass Paver'
}

orsWaytypeDict = {
	0: 'Unknown',
	1: 'State Road',
	2: 'Road',
	3: 'Street',
	4: 'Path',
	5: 'Track',
	6: 'Cycleway',
	7: 'Footway',
	8: 'Steps',
	9: 'Ferry',
	10: 'Construction'
}

# https://github.com/GIScience/openrouteservice-docs#steepness
orsSteepnessDict = {
	-5: '>16%',
	-4: '12-15%',
	-3: '7-11%',
	-2: '4-6%',
	-1: '1-3%',
	0: '0%',
	1: '1-3%',
	2: '4-6%',
	3: '7-11%',
	4: '12-15%',
	5: '>16%'
}