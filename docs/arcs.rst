
.. _Arcs:

Arcs
====

The `Arcs` dataframe is used to draw straight arcs between pairs of locations
on a Leaflet map. *VeRoViz* provides two functions to generate `Arcs` dataframes 
from a list of coordinates:  :meth:`~veroviz.generateArcs.createArcsFromLocSeq`
and :meth:`~veroviz.generateArcs.createArcsFromNodeSeq`.

The table below describes each of the fields/columns of an `Arcs` dataframe:

+------------------+-----------+----------------------------------------+
| Field Name       | Data Type | Description                            |
+==================+===========+========================================+
| odID             | int       | Each origin/destination pair should    |
|                  |           | have a unique odID.                    |
+------------------+-----------+----------------------------------------+
| objectID         | string    | Identifier for each object (e.g.,      |
|                  |           | truck, package, drone, etc.) shown in  |
|                  |           | Cesium.                                |
+------------------+-----------+----------------------------------------+
| startLat         | float     | Latitude of the start of the arc,      |
|                  |           | in [degrees].  0-degrees latitude is   |
|                  |           | the equator.  Negative latitudes are   |
|                  |           | south of the equator; positive         |
|                  |           | latitudes are north.  The range is from|
|                  |           | -90 to +90.                            |
+------------------+-----------+----------------------------------------+
| startLon         | float     | Longitude of the start of the arc,     |
|                  |           | in [degrees].  0-degrees longitude is  |
|                  |           | Greenich, England.  Negative longitudes|
|                  |           | are west of Greenich; positive         |
|                  |           | longitudes are east.  The range is from|
|                  |           | -180 to +180.                          |
+------------------+-----------+----------------------------------------+
| endLat           | float     | Latitude of the end of the arc, in     |
|                  |           | [degrees].  The range is from -90 to   |
|                  |           | +90.                                   |
+------------------+-----------+----------------------------------------+
| endLon           | float     | Longitude of the end of the arc, in    |
|                  |           | [degrees].  The range is from -180 to  |
|                  |           | +180.                                  |
+------------------+-----------+----------------------------------------+
| leafletColor     | string    | Color of the arc when displayed in     |
|                  |           | Leaflet. See :ref:`Leaflet Style` for  |
|                  |           | options of colors.                     |
+------------------+-----------+----------------------------------------+
| leafletOpacity   | float in  | Amount of transparency for the arc.    |
|                  | [0, 1]    | A value of 1 indicates no transparency;|
|                  |           | 0 indicates completely transparent.    |
+------------------+-----------+----------------------------------------+
| leafletStyle     | string    | Styling of the line, valid options are |
|                  |           | "solid", "dotted" or "dashed". See     |
|                  |           | :ref:`Leaflet Style` for more details  |
+------------------+-----------+----------------------------------------+
| leafletWeight    | int       | Pixel width of the line/arc.           |
+------------------+-----------+----------------------------------------+
| leafletCurveType | string    | The type of curve to be shown on a     |
|                  |           | leaflet map for :ref:Arc dataframes    |
|                  |           | (curves will not be applied to         |
|                  |           | :ref:Assignments dataframes). The      |
|                  |           | options are 'Bezier', 'greatcircle',   |
|                  |           | and 'straight'. If Bezier is provided, |
|                  |           | the leafletCurvature is also required. |
|                  |           | If greatcircle is provided, the arc    |
|                  |           | follows the curvature of the Earth.    |
+------------------+-----------+----------------------------------------+
| leafletCurvature | float in  | If leafletCurveType is 'Bezier', then  | 
|                  | (-90, 90) | leafletCurvature is required; otherwise| 
|                  |           | this argument will not be used. The    |
|                  |           | curvature specifies the angle between a|
|                  |           |  straight line connecting the two nodes|
|                  |           |  and the curved arc emanating from     |
|                  |           | those two nodes. Therefore, this value |
|                  |           | should be in the open interval         |
|                  |           | (-90, 90), although values in the      |
|                  |           | (-45, 45) range tend to work best.     | 
+------------------+-----------+----------------------------------------+
| useArrows        | bool      | True if the arrows will be used when   |
|                  |           | creating Leaflet map, false otherwise. |
|                  |           | When generating Arcs, this defaults to |
|                  |           | `True`.                                |
+------------------+-----------+----------------------------------------+
| cesiumColor      | string    | Color of the arc when displayed in     |
|                  |           | Cesium. See :ref:`Cesium Style` for    |
|                  |           | color options.                         |
+------------------+-----------+----------------------------------------+
| cesiumOpacity    | float in  | The amount of transparency for the arc.|
|                  | [0, 1]    | A value of 1 indicates no transparency;|
|                  |           | 0 indicates completely transparent.    |
+------------------+-----------+----------------------------------------+
| cesiumStyle      | string    | Styling of the line, valid options are |
|                  |           | "solid", "dotted" or "dashed". See     |
|                  |           | :ref:`Cesium Style` for options.       |
+------------------+-----------+----------------------------------------+
| cesiumWeight     | int       | Pixel width of the line/arc.           |
+------------------+-----------+----------------------------------------+
| popupText        | string    | Text (or HTML) that will be displayed  |
|                  |           | when a user clicks on the arc in       |
|                  |           | Leaflet.                               |
+------------------+-----------+----------------------------------------+
| startElevMeters  | float     | Elevation of the start point, in units |
|                  |           | of meters above ground level.          |
+------------------+-----------+----------------------------------------+
| endElevMeters    | float     | Elevation of the end point, in units   |
|                  |           | of meters above ground level.          |
+------------------+-----------+----------------------------------------+


:ref:`Arcs` and :ref:`Assignments` dataframes are similar,
see :ref:`Dataframes Comparison` for the similarity and differences between them.

---------------------------------------------------------------------

An `Arcs` dataframe can be used in :meth:`~veroviz.createLeaflet.createLeaflet`.  The table below indicates whether a field (column) is required/optional/ignored.

.. note::
	Some explaination about "Required", "Optional", "Ignored":

	- "Required" means the function needs info from that field/column. That info can not be overridden by the function that uses the dataframe.
	- "Optional" means the function will use the info from that field/column as a default value.  However, some functions allow the user to temporarily "override" the optional values in the dataframe with different values provided in the function call.  
	- "Ignored" means the function neither needs nor uses info from that field/column.


+------------------+--------------+--------------+------------------+
| Field Name       | Required     |Optional      | Ignored          |
+==================+==============+==============+==================+
| odID             | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| objectID         |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| startLat         | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| startLon         | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| endLat           | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| endLon           | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| leafletColor     |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| leafletOpacity   |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| leafletStyle     |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| leafletWeight    |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| leafletCurveType | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| leafletCurvature | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| useArrows        |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| cesiumColor      |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumOpacity    |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumStyle      |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumWeight     |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| popupText        |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| startElevMeters  |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| endElevMeters    |              |              | ✓                |
+------------------+--------------+--------------+------------------+
