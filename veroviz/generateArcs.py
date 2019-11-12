from veroviz._common import *
from veroviz._validation import valCreateArcsFromLocSeq
from veroviz._validation import valCreateArcsFromNodeSeq

from veroviz._createEntitiesFromList import privCreateArcsFromLocSeq

def createArcsFromLocSeq(locSeq=None, initArcs=None, startArc=1, objectID=None, leafletColor=VRV_DEFAULT_LEAFLETARCCOLOR, leafletWeight=VRV_DEFAULT_LEAFLETARCWEIGHT, leafletStyle=VRV_DEFAULT_LEAFLETARCSTYLE, leafletOpacity=VRV_DEFAULT_LEAFLETARCOPACITY, useArrows=True, cesiumColor=VRV_DEFAULT_CESIUMPATHCOLOR, cesiumWeight=VRV_DEFAULT_CESIUMPATHWEIGHT, cesiumStyle=VRV_DEFAULT_CESIUMPATHSTYLE, cesiumOpacity=VRV_DEFAULT_CESIUMPATHOPACITY):

	"""
	Create an "arcs" dataframe from an ordered list of coordinates.

	Parameters
	----------
	locSeq: list of lists, Required, default as None
		An ordered list of locations that will be converted into an :ref:`Arcs` dataframe. The list should be formated as [[lat1, lon1], [lat2, lon2], ..., [latn, lonn]].
	initArcs: :ref:`Arcs`, Optional, default as None
		An :ref:`Arcs` dataframe.  If provided, the arcs to be created will be appended to this dataframe.
	startArc: int, Optional, default as 1
		Specifies the starting index number for the arcs.  This will be reflected in the `odID` column of the resulting :ref:`Arcs` dataframe.  If `startArc` is less than the minimum value of the `odID` found in the dataframe specified by `initArcs`, the value of `startArc` will be ignored in favor of the smallest integer greater than the maximum existing `odID` value.
	objectID: int/string, Optional, default as None
		A descriptive name or index for a particular vehicle or object (e.g., 'truck 1', or 'red car'). 
	leafletColor: string, Optional, default as "orange"
		The color of the arcs when displayed in Leaflet.  See :ref:`Leaflet style` for a list of available colors.
	leafletWeight: int, Optional, default as 3
		The pixel width of the arcs when displayed in Leaflet. 
	leafletStyle: string, Optional, default as 'solid'
		The line style of the arcs when displayed in Leaflet.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Leaflet style` for more information.
	leafletOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the arcs when displayed in Leaflet. Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	useArrows: bool, Optional, default as True
		Indicates whether arrows should be shown on the arcs when displayed in Leaflet.
	cesiumColor: string, Optional, default as "Cesium.Color.ORANGE"
		The color of the arcs when displayed in Cesium.  See :ref:`Cesium Style` for a list of available colors.
	cesiumWeight: int, Optional, default as 3
		The pixel width of the arcs when displayed in Cesium. 
	cesiumStyle: string, Optional, default as 'solid'
		The line style of the arcs when displayed in Cesium.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Cesium Style` for more information.
	cesiumOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the arcs when displayed in Cesium. Valid values are in the range from 0 (invisible) to 1 (no transparency). 

	Return
	------
	:ref:`Arcs`
		An Arcs dataframe

	Examples
	--------
	First import veroviz and check if it is the latest version
	    >>> import veroviz as vrv
	    >>> vrv.checkVersion()

	Generate arcs from a given ordered list of coordinates:
	    >>> arcs = vrv.createArcsFromLocSeq(
	    ...     locSeq=[
	    ...         [42.1325, -78.2134], 
	    ...         [42.5341, -78.3252], 
	    ...         [42.3424, -78.6424]
	    ...     ])
	    >>> arcs
	    
	Display the arcs on a Leaflet map:
		>>> vrv.createLeaflet(arcs=arcs)	    


	This example includes all of the available function arguments.
		>>> arcs = vrv.createArcsFromLocSeq(
		...     locSeq         = [[42.1325, -78.2134],
		...                       [42.5341, -78.3252],
		...                       [42.3424, -78.6424]],
		...     initArcs       = None, 
		...     startArc       = 1, 
		...     objectID       = 'car', 
		...     leafletColor   = 'orange', 
		...     leafletWeight  = 5, 
		...     leafletStyle   = 'dashed', 
		...     leafletOpacity = 0.6, 
		...     useArrows      = False, 
		...     cesiumColor    = 'Cesium.Color.ORANGE', 
		...     cesiumWeight   = 5, 
		...     cesiumStyle    = 'dashed', 
		...     cesiumOpacity  = 0.6)
		>>> vrv.createLeaflet(arcs=arcs)
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valCreateArcsFromLocSeq(locSeq, initArcs, startArc, objectID, leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	arcs = privCreateArcsFromLocSeq(locSeq, initArcs, startArc, objectID, leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)

	return arcs

def createArcsFromNodeSeq(nodeSeq=None, nodes=None, initArcs=None, startArc=1, objectID=None, leafletColor=VRV_DEFAULT_LEAFLETARCCOLOR, leafletWeight=VRV_DEFAULT_LEAFLETARCWEIGHT, leafletStyle=VRV_DEFAULT_LEAFLETARCSTYLE, leafletOpacity=VRV_DEFAULT_LEAFLETARCOPACITY, useArrows=True,
	cesiumColor=VRV_DEFAULT_CESIUMPATHCOLOR, cesiumWeight=VRV_DEFAULT_CESIUMPATHWEIGHT, cesiumStyle=VRV_DEFAULT_CESIUMPATHSTYLE, cesiumOpacity=VRV_DEFAULT_CESIUMPATHOPACITY):

	"""
	Create an "arcs" dataframe from an ordered list of node IDs.  The "nodes" dataframe from which these node IDs are drawn must also be specified.

	Parameters
	----------
	nodeSeq: list, Required
		An ordered list of node IDs.  These IDs must be included in the `id` column of the :ref:`Nodes` dataframe specified in the `nodes` input argument to this function. The format for `nodeSeq` is [node_id_1, node_id_2, ...].
	nodes: :ref:`Nodes`, Required
		A :ref:`Nodes` dataframe, which must contain the individual node IDs specified in the `nodeSeq` input argument.
	initArcs: :ref:`Arcs`, Optional, default as None
		An :ref:`Arcs` dataframe.  If provided, the arcs to be created will be appended to this dataframe.
	startArc: int, Optional, default as 1
		Specifies the starting index number for the arcs.  This will be reflected in the `odID` column of the resulting :ref:`Arcs` dataframe.  If `startArc` is less than the minimum value of the `odID` found in the dataframe specified by `initArcs`, the value of `startArc` will be ignored in favor of the smallest integer greater than the maximum existing `odID` value.
	objectID: int/string, Optional, default as None
		A descriptive name or index for a particular vehicle or object (e.g., 'truck 1', or 'red car'). 
	leafletColor: string, Optional, default as "orange"
		The color of the arcs when displayed in Leaflet.  See :ref:`Leaflet style` for a list of available colors.
	leafletWeight: int, Optional, default as 3
		The pixel width of the arcs when displayed in Leaflet. 
	leafletStyle: string, Optional, default as 'solid'
		The line style of the arcs when displayed in Leaflet.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Leaflet style` for more information.
	leafletOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the arcs when displayed in Leaflet. Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	useArrows: bool, Optional, default as True
		Indicates whether arrows should be shown on the arcs when displayed in Leaflet.
	cesiumColor: string, Optional, default as "Cesium.Color.ORANGE"
		The color of the arcs when displayed in Cesium.  See :ref:`Cesium Style` for a list of available colors.
	cesiumWeight: int, Optional, default as 3
		The pixel width of the arcs when displayed in Cesium. 
	cesiumStyle: string, Optional, default as 'solid'
		The line style of the arcs when displayed in Cesium.  Valid options are 'solid', 'dotted', and 'dashed'. See :ref:`Cesium Style` for more information.
	cesiumOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of the arcs when displayed in Cesium. Valid values are in the range from 0 (invisible) to 1 (no transparency). 

	Return
	------
	:ref:`Arcs`
		An Arcs dataframe

	Examples
	--------
	First import veroviz and check if it is the latest version
	    >>> import veroviz as vrv
	    >>> vrv.checkVersion()

	Create a collection of 20 nodes:
	    >>> myNodes = vrv.generateNodes(
	    ...     numNodes        = 20,
	    ...     nodeType        = 'depot', 
	    ...     nodeDistrib     = 'normal', 
	    ...     nodeDistribArgs = {
	    ...         'center' : [42.30, 78.00], 
	    ...         'stdDev' : 1000
	    ...     })
	    >>> myNodes

	Generate arcs from nodes 2-to-15 and from 15-to-8.  These node IDs are found in the `id` column of the given Nodes dataframe.
	    >>> myArcs = vrv.createArcsFromNodeSeq(
	    ...     nodeSeq = [2, 15, 8],
	    ...     nodes   = myNodes)
	    >>> myArcs
	    
	Display the nodes and arcs on a Leaflet map:
	    >>> myMap = vrv.createLeaflet(arcs=myArcs, nodes=myNodes)
		>>> myMap
		
	This example includes all of the available function arguments:
		>>> moreArcs = vrv.createArcsFromNodeSeq(
		...     nodeSeq        = [3, 16, 9],
		...     nodes          = myNodes, 
		...     initArcs       = myArcs, 
		...     startArc       = 7, 
		...     objectID       = 'car',
		...     leafletColor   = 'cadetblue', 
		...     leafletWeight  = 3, 
		...     leafletStyle   = 'dotted', 
		...     leafletOpacity = 0.8, 
		...     useArrows      = False, 
		...     cesiumColor    = 'Cesium.Color.CADETBLUE', 
		...     cesiumWeight   = 3, 
		...     cesiumStyle    = 'dotted', 
		...     cesiumOpacity  = 0.8)
		>>> moreArcs
		
	Display the nodes and arcs on a Leaflet map:
		>>> vrv.createLeaflet(mapObject=myMap, arcs = moreArcs)
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valCreateArcsFromNodeSeq(nodeSeq, nodes, initArcs, startArc, objectID, leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	locSeq = []
	for i in range(len(nodeSeq)):
		locSeq.append([
				nodes.loc[nodes['id'] == nodeSeq[i]]['lat'].values[0],
				nodes.loc[nodes['id'] == nodeSeq[i]]['lon'].values[0],
			])

	arcs = privCreateArcsFromLocSeq(locSeq, initArcs, startArc, objectID, leafletColor, leafletWeight, leafletStyle, leafletOpacity, useArrows, cesiumColor, cesiumWeight, cesiumStyle, cesiumOpacity)

	return arcs
