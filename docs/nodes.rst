
.. _Nodes:

Nodes
=====

The `Nodes` dataframe type specifies information about single locations
(nodes or vertices). 
The :meth:`~veroviz.utilities.initDataframe` function may be used to 
create a blank/empty `Nodes` dataframe. 
This dataframe may also be populated from a list of lat/lon coordinates, 
using the :meth:`~veroviz.generateNodes.createNodesFromLocs` function.
The :meth:`~veroviz.generateNodes.generateNodes` function may be used 
to populate a `Nodes` dataframe with nodes generated from a distribution
(e.g., uniformly distributed over a region, or normally distributed 
about a central location).

The table below describes each of the fields/columns of a `Nodes` dataframe:

+------------------+-----------+--------------------------------------------+
| Field Name       | Data Type | Description                                |
+==================+===========+============================================+
| id               | int       | Unique identifier for each row of          |
|                  |           | the dataframe.                             |
+------------------+-----------+--------------------------------------------+
| lat              | float     | Latitude of the node, in [degrees].        |
|                  |           | 0-degrees latitude is the equator.         |
|                  |           | Negative latitudes are south of the        |
|                  |           | equator; positive latitudes are north.     |
|                  |           | The range is from -90 to +90.              |
+------------------+-----------+--------------------------------------------+
| lon              | float     | Longitude of the node, in [degrees].       |
|                  |           | 0-degrees longitude is Greenwich, England. |
|                  |           | Negative longitudes are west of Greenwich; |
|                  |           | positive longitudes are east. The range    |
|                  |           | is from -180 to +180.                      |
+------------------+-----------+--------------------------------------------+
| altMeters        | float     | Altitude of this node, in units of         |
|                  |           | [meters above ground level] (AGL).         |
+------------------+-----------+--------------------------------------------+
| nodeType         | string    | A text string that may be used to          |
|                  |           | categorize/classify a collection of nodes. |
|                  |           | This field is not used by VeRoViz          |
|                  |           | explicitly. Examples could include         |
|                  |           | "depots" or "customers".                   |
+------------------+-----------+--------------------------------------------+
| nodeName         | string    | A unique name for a particular node, such  |
|                  |           | as "depot 1" or "customer 32". The         | 
|                  |           | nodeName is not used by VeRoViz            |
|                  |           | explicitly.                                |
+------------------+-----------+--------------------------------------------+
| leafletIconPrefix| string    | There are a large number of Leaflet icons  |
|                  |           | available.  The IconPrefix identifies one  |
|                  |           | of two collections: "glyphicon" or "fa".   |
|                  |           | See :ref:`Leaflet Style` for more details. |
+------------------+-----------+--------------------------------------------+
| leafletIconType  | string    | The specific icon depends on the           |
|                  |           | leafletIconPrefix. See :ref:`Leaflet Style`|
|                  |           | for the options for different prefixes.    |
+------------------+-----------+--------------------------------------------+
| leafletColor     | string    | Color of the node marker when displayed in |
|                  |           | Leaflet. See :ref:`Leaflet Style` for      |
|                  |           | options of colors.                         |
+------------------+-----------+--------------------------------------------+
| leafletIconText  | string    | The text shown in the marker when displayed|
|                  |           | in Leaflet. See :ref:`Leaflet Style` for   |
|                  |           | more details.                              |
+------------------+-----------+--------------------------------------------+
| cesiumIconType   | string    | Describes the icon used to denote a node   |
|                  |           | when displayed in Cesium.                  |
|                  |           | See :ref:`Cesium Style` for options.       |
+------------------+-----------+--------------------------------------------+
| cesiumColor      | string    | Color of the node marker when displayed in |
|                  |           | Cesium. See :ref:`Cesium Style` for color  |
|                  |           | options.                                   |
+------------------+-----------+--------------------------------------------+
| cesiumIconText   | string    | The text shown in the marker when displayed|
|                  |           | in Cesium. See :ref:`Cesium Style` for more|
|                  |           | details.                                   |
+------------------+-----------+--------------------------------------------+

---------------------------------------------------------------------

A `Nodes` dataframe can be used in several functions. Here is a list of whether 
the field is required/optional/ignored in different functions.

.. note::
	Some explaination about "Required", "Optional", "Ignored":

	- "Required" means the function needs info from that field/column. That info can not be overridden by the function that uses the dataframe.
	- "Optional" means the function will use the info from that field/column as a default value.  However, some functions allow the user to temporarily "override" the optional values in the dataframe with different values provided in the function call.  
	- "Ignored" means the function neither needs nor uses info from that field/column.
	

In :meth:`~veroviz.snapNodesToRoad.snapNodesToRoad`  

+------------------+--------------+--------------+------------------+
| Field Name       | Required     |Optional      | Ignored          |
+==================+==============+==============+==================+
| id               |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| lat              | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| lon              | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| altMeters        |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| nodeName         |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| nodeType         |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconPrefix|              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconType  |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletColor     |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconText  |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumIconType   |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumColor      |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumIconText   |              |              | ✓                |
+------------------+--------------+--------------+------------------+

In :meth:`~veroviz.createCesium.createCesium`

+------------------+--------------+--------------+------------------+
| Field Name       | Required     |Optional      | Ignored          |
+==================+==============+==============+==================+
| id               | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| lat              | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| lon              | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| altMeters        | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| nodeName         | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| nodeType         |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconPrefix|              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconType  |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletColor     |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconText  |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumIconType   |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| cesiumColor      |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| cesiumIconText   |              | ✓            |                  |
+------------------+--------------+--------------+------------------+

In :meth:`~veroviz.createLeaflet.createLeaflet`

+------------------+--------------+--------------+------------------+
| Field Name       | Required     |Optional      | Ignored          |
+==================+==============+==============+==================+
| id               | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| lat              | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| lon              | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| altMeters        |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| nodeName         |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| nodeType         |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconPrefix|              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| leafletIconType  |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| leafletColor     |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| leafletIconText  |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| cesiumIconType   |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumColor      |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumIconText   |              |              | ✓                |
+------------------+--------------+--------------+------------------+

In :meth:`~veroviz.getTimeDist2D.getTimeDist2D`

+------------------+--------------+--------------+------------------+
| Field Name       | Required     |Optional      | Ignored          |
+==================+==============+==============+==================+
| id               | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| lat              | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| lon              | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| altMeters        |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| nodeName         |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| nodeType         |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconPrefix|              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconType  |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletColor     |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconText  |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumIconType   |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumColor      |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumIconText   |              |              | ✓                |
+------------------+--------------+--------------+------------------+

In :meth:`~veroviz.getTimeDist3D.getTimeDist3D`

+------------------+--------------+--------------+------------------+
| Field Name       | Required     |Optional      | Ignored          |
+==================+==============+==============+==================+
| id               | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| lat              | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| lon              | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| altMeters        | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| nodeName         |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| nodeType         |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconPrefix|              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconType  |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletColor     |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletIconText  |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumIconType   |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumColor      |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumIconText   |              |              | ✓                |
+------------------+--------------+--------------+------------------+