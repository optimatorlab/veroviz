.. _Global Settings and Defaults:

Global Settings and Defaults
============================

The following items are found in `params.py`, which defines default
constants and settings for for the 'veroviz' package.  If you desire, 
you may modify these values (although this is not recommended).


Constants
---------

Distance conversions
    >>> VRV_CONST_METERS_PER_KILOMETER = 1000.0
    >>> VRV_CONST_METERS_PER_MILE = 1609.34
    >>> VRV_CONST_METERS_PER_YARD = 0.9144
    >>> VRV_CONST_METERS_PER_FEET = 0.3048
    >>> VRV_CONST_METERS_PER_NAUTICAL_MILE = 1852.0

Speed conversions
    >>> VRV_CONST_MPS_TO_KPH = 3.6
    >>> VRV_CONST_MPS_TO_MPH = 2.23694

Time conversions
    >>> VRV_CONST_SECONDS_PER_HOUR = 3600.0
    >>> VRV_CONST_SECONDS_PER_MINUTE = 60.0

Area conversions
    >>> VRV_CONST_SQKM_PER_SQMETER = 1e-6
    >>> VRV_CONST_SQMILES_PER_SQMETER = 3.861e-7 
    >>> VRV_CONST_SQFT_PER_SQMETER = 10.7639


Default Leaflet Styles
----------------------

Defaults for adding Leaflet objects (e.g., circles, polygons, text)
    >>> VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE = 'red'
    >>> VRV_DEFAULT_LEAFLET_OBJECT_COLOR_FILL = 'red'
    >>> VRV_DEFAULT_LEAFLET_FONTSIZE = 24	# pt
    >>> VRV_DEFAULT_LEAFLET_FONTCOLOR = 'orange'
    >>> VRV_DEFAULT_LEAFLET_MAPTILES = 'CartoDB positron'

For the nodes/icons
    >>> VRV_DEFAULT_LEAFLETICONPREFIX = 'glyphicon'
    >>> VRV_DEFAULT_LEAFLETICONTYPE = 'info-sign'
    >>> VRV_DEFAULT_LEAFLETICONCOLOR = 'blue'

For the arcs
    >>> VRV_DEFAULT_LEAFLETARCWEIGHT = 3
    >>> VRV_DEFAULT_LEAFLETARCSTYLE = 'solid'
    >>> VRV_DEFAULT_LEAFLETARCOPACITY = 0.8
    >>> VRV_DEFAULT_LEAFLETARCCOLOR = 'orange'

For the boundings
    >>> VRV_DEFAULT_LEAFLETBOUNDINGWEIGHT = 3
    >>> VRV_DEFAULT_LEAFLETBOUNDINGOPACITY = 0.6
    >>> VRV_DEFAULT_LEAFLETBOUNDINGSTYLE = 'dashed'
    >>> VRV_DEFAULT_LEAFLETBOUNDINGCOLOR = 'brown'

Default Cesium Styles
---------------------

For the nodes/icons
    >>> VRV_DEFAULT_CESIUMICONTYPE = 'pin'
    >>> VRV_DEFAULT_CESIUMICONSIZE = 40
    >>> VRV_DEFAULT_CESIUMICONCOLOR = 'Cesium.Color.BLUE'

For the assignments
    >>> VRV_DEFAULT_CESIUMPATHCOLOR = 'Cesium.Color.ORANGE'
    >>> VRV_DEFAULT_CESIUMPATHWEIGHT = 3
    >>> VRV_DEFAULT_CESIUMPATHSTYLE = 'solid'
    >>> VRV_DEFAULT_CESIUMPATHOPACITY = 0.8



Settings
--------

pgRouting database settings
    >>> VRV_SETTING_PGROUTING_USERNAME = 'user'
    >>> VRV_SETTING_PGROUTING_HOST = 'localhost'
    >>> VRV_SETTING_PGROUTING_PASSWORD = ''

Information and message settings
    >>> VRV_SETTING_SHOWWARNINGMESSAGE = True
    >>> VRV_SETTING_SHOWOUTPUTMESSAGE = True