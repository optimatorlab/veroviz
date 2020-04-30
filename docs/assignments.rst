
.. _Assignments:

Assignments
===========

The `Assignments` dataframe is used as the input for the :meth:`~veroviz.createCesium.createCesium` function to 
generate time-dynamic visualization of vehicle routes on a 3D map.

While there is no "standard" function for generating all of the rows of 
an `Assignments` dataframe, *VeRoViz* does provide some functions that 
can be used to construct individual rows of the dataframe.  Users may 
then append these rows into an `Assignments` dataframe.  For example, 
:meth:`~veroviz.getShapepoints2D.getShapepoints2D` returns an assignment 
dataframe describing the detailed navigation on a road network between 
a pair of origin/destination locations.  By iteratively calling that function 
for all O/D pairs of a route, a complete assignments dataframe can be constructed.
Similarly, :meth:`~veroviz.getShapepoints3D.getShapepoints3D` returns 
an assignment dataframe describing the flight profile/path for aircraft 
(e.g., drones) for a given O/D pair.

A blank/empty `Assignments` dataframe can be created by :meth:`~veroviz.utilites.initDataframe`.

+------------------+-----------+------------------------------------------+
| Field Name       | Data Type | Description                              |
+==================+===========+==========================================+
| odID             | int       | `odID` is an abbreviation for "origin/   |
|                  |           | destination identifier". It is           |
|                  |           | a group identifier.  Arc segments which  |
|                  |           | are part of the same origin/destination  |
|                  |           | share the same odID.                     |
+------------------+-----------+------------------------------------------+
| objectID         | string    | Identifier for each object (e.g. truck,  |
|                  |           | package, drone, etc.) shown in Cesium.   |
+------------------+-----------+------------------------------------------+
| modelFile        | string    | The 3D model used for the object. See    |
|                  |           | :ref:`Cesium Style` for a list of        |
|                  |           | available 3D Cesium models . You         |
|                  |           | can also generate your own `gltf` files. |
+------------------+-----------+------------------------------------------+
| modelScale       | int       | The scale of Cesium 3D model in percent. |
+------------------+-----------+------------------------------------------+
| modelMinPxSize   | int       | The minimum pixel size of Cesium 3D model|
+------------------+-----------+------------------------------------------+
| startTimeSec     | int       | In a sequence of coordinates that        |
|                  |           | navigates between origin and destination,|
|                  |           | the time  to arrive at the start         |
|                  |           | coordinate ([startLat,startLon]).        |
+------------------+-----------+------------------------------------------+
| startLat         | float     | Latitude of the start of the arc,        |
|                  |           | in [degrees].  0-degrees latitude is     |
|                  |           | the equator.  Negative latitudes are     |
|                  |           | south of the equator; positive           |
|                  |           | latitudes are north.  The range is from  |
|                  |           | -90 to +90.                              |
+------------------+-----------+------------------------------------------+
| startLon         | float     | Longitude of the start of the arc,       |
|                  |           | in [degrees].  0-degrees longitude is    |
|                  |           | Greenich, England.  Negative longitudes  |
|                  |           | are west of Greenich; positive           |
|                  |           | longitudes are east.  The range is from  |
|                  |           | -180 to +180.                            |
+------------------+-----------+------------------------------------------+
| startAltMeters   | float     | Altitude of the object at the start      |
|                  |           | time, in units of [meters above ground   |
|                  |           | level] (AGL).                            |
+------------------+-----------+------------------------------------------+
| endTimeSec       | int       | The arrival time (in seconds) to this    |
|                  |           | coordinate ([endLat,endLon]).            |
+------------------+-----------+------------------------------------------+
| endLat           | float     | Latitude of the end of the arc, in       |
|                  |           | [degrees].  The range is from -90 to +90.|
+------------------+-----------+------------------------------------------+
| endLon           | float     | Longitude of the end of the arc, in      |
|                  |           | [degrees].  The range is from -180 to    |
|                  |           | +180.                                    |
+------------------+-----------+------------------------------------------+
| endAltMeters     | float     | Altitude of the object at the end        |
|                  |           | time, in units of [meters AGL].          |
+------------------+-----------+------------------------------------------+
| leafletColor     | string    | Color of the arc when displayed in       |
|                  |           | Leaflet. See :ref:`Leaflet Style` for    |
|                  |           | options of colors.                       |
+------------------+-----------+------------------------------------------+
| leafletOpacity   | float in  | Amount of transparency for the arc.      |
|                  | [0, 1]    | A value of 1 indicates no transparency;  |
|                  |           | 0 indicates completely transparent.      |
+------------------+-----------+------------------------------------------+
| leafletStyle     | string    | Styling of the line, valid options are   |
|                  |           | "solid", "dotted" or "dashed". See       |
|                  |           | :ref:`Leaflet Style` for more details    |
+------------------+-----------+------------------------------------------+
| leafletCurveType | string    | The type of curve to be shown on a       |
|                  |           | leaflet map for :ref:Arc dataframes      |
|                  |           | (curves will not be applied to           |
|                  |           | :ref:Assignments dataframes). The        |
|                  |           | options are 'Bezier', 'greatcircle',     |
|                  |           | and 'straight'. If Bezier is provided,   |
|                  |           | the leafletCurvature is also required.   |
|                  |           | If greatcircle is provided, the arc      |
|                  |           | follows the curvature of the Earth.      |
+------------------+-----------+------------------------------------------+
| leafletCurvature | float in  | If leafletCurveType is 'Bezier', then    | 
|                  | (-90, 90) | leafletCurvature is required; otherwise  | 
|                  |           | this argument will not be used. The      |
|                  |           | curvature specifies the angle between a  |
|                  |           | straight line connecting the two nodes   |
|                  |           | and the curved arc emanating from those  |
|                  |           | two nodes. Therefore, this value should  |
|                  |           | be in the open interval (-90, 90),       |
|                  |           | although values in the (-45, 45) range   |
|                  |           | tend to work best.                       |  
+------------------+-----------+------------------------------------------+
| useArrows        | bool      | True if the arrows will be used when     |
|                  |           | creating Leaflet map, False otherwise.   |
+------------------+-----------+------------------------------------------+
| cesiumWeight     | int       | Pixel width of the line/arc.             |
+------------------+-----------+------------------------------------------+
| cesiumColor      | string    | Color of the arc when displayed in       |
|                  |           | Cesium. See :ref:`Cesium Style` for      |
|                  |           | color options.                           |
+------------------+-----------+------------------------------------------+
| cesiumOpacity    | float in  | The amount of transparency for the arc.  |
|                  | [0, 1]    | A value of 1 indicates no transparency;  |
|                  |           | 0 indicates completely transparent.      |
+------------------+-----------+------------------------------------------+
| cesiumStyle      | string    | Styling of the line, valid options are   |
|                  |           | "solid", "dotted" or "dashed". See       |
|                  |           | :ref:`Cesium Style` for options.         |
+------------------+-----------+------------------------------------------+
| cesiumWeight     | int       | Pixel width of the line/arc.             |
+------------------+-----------+------------------------------------------+
| ganttColor       | string    | The color to be displayed for this       |
|                  |           | assignment in a Gantt chart.  See the    |
|                  |           | `ganttColor()` function for details, and |
|                  |           | see :ref:`Cesium Style` for              |
|                  |           | color options.                           |
+------------------+-----------+------------------------------------------+
| popupText        | string    | Text (or HTML) that will be displayed    |
|                  |           | when a user clicks on the arc in         |
|                  |           | Leaflet or Cesium.                       |
+------------------+-----------+------------------------------------------+
| startElevMeters  | float     | Elevation of the start point, in units   |
|                  |           | of meters above ground level.            |
+------------------+-----------+------------------------------------------+
| endElevMeters    | float     | Elevation of the end point, in units     |
|                  |           | of meters above ground level.            |
+------------------+-----------+------------------------------------------+
| wayname          | string    | Name of the road segment between start   |
|                  |           | and end points.                          |
+------------------+-----------+------------------------------------------+
| waycategory      | string    | Classification of the road segment. May  |
|                  |           | include: 'No category', 'Highway',       |
|                  |           | 'Steps', 'Ferry', 'Unpaved road',        |
|                  |           | 'Track', 'Tunnel', 'Paved road', or      |
|                  |           | 'Ford'                                   |
+------------------+-----------+------------------------------------------+
| surface          | string    | Classification of the ground surface of  |
|                  |           | the road segment.  May include:          |
|                  |           | 'Unknown', 'Paved', 'Unpaved', 'Asphalt',|
|                  |           | 'Concrete', 'Cobblestone', 'Metal',      |
|                  |           | 'Wood', 'Compacted Gravel',              |
|                  |           | 'Fine Gravel', 'Gravel', 'Dirt',         |
|                  |           | 'Ground', 'Ice', 'Paving Stones', 'Sand',|
|                  |           | 'Woodchips', 'Grass', or  'Grass Paver'. |
+------------------+-----------+------------------------------------------+
| waytype          | string    | Classification of the road segment. May  |
|                  |           | include: 'Unknown', 'State Road', 'Road',|
|                  |           | 'Street', 'Path', 'Track', 'Cycleway',   |
|                  |           | 'Footway', 'Steps', 'Ferry', or          |
|                  |           | 'Construction'.                          |
+------------------+-----------+------------------------------------------+
| steepness        | int       | Varies from -5 to +5, with - (+)         |
|                  |           | values indicating a downward (upward)    |
|                  |           | slope.  The absolute scale is:           |
|                  |           | 0: '0%', 1: '1-3%', 2: '4-6%',           |
|                  |           | 3: '7-11%', 4: '12-15%', 5: '>16%'.      |
+------------------+-----------+------------------------------------------+
| tollway          | bool      | Indicates whether the road segment has   |
|                  |           | tolls.                                   |
+------------------+-----------+------------------------------------------+



:ref:`Arcs` and :ref:`Assignments` dataframes are similar,
see :ref:`Dataframes Comparison` for the similarity and differences between them.

---------------------------------------------------------------------

An `Assignments` dataframe can be used in :meth:`~veroviz.createLeaflet.createLeaflet`. The table below indicates whether a given field (column) of the dataframe is required/optional/ignored.

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
| objectID         | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| modelFile        |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| modelScale       |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| modelMinPxSize   |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| startTimeSec     |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| startLat         | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| startLon         | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| startAltMeters   |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| endTimeSec       |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| endLat           | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| endLon           | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| endAltMeters     |              |              | ✓                |
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
| wayname          |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| waycategory      |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| surface          |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| waytype          |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| steepness        |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| tollway          |              |              | ✓                |
+------------------+--------------+--------------+------------------+


An `Assignments` dataframe can be used in :meth:`~veroviz.createCesium.createCesium` to generate
a Cesium-based 4D WebGIS video. The video can be displayed on a 
Cesium web page.

+------------------+--------------+--------------+------------------+
| Field Name       | Required     |Optional      | Ignored          |
+==================+==============+==============+==================+
| odID             | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| objectID         | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| modelFile        | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| modelScale       | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| modelMinPxSize   | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| icon             | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| startTimeSec     | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| startLat         | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| startLon         | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| startAltMeters   | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| endTimeSec       | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| endLat           | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| endLon           | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| endAltMeters     | ✓            |              |                  |
+------------------+--------------+--------------+------------------+
| leafletColor     |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletOpacity   |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletStyle     |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletWeight    |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletCurveType |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| leafletCurvature |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| useArrows        |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| cesiumColor      |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| cesiumOpacity    |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| cesiumStyle      |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| cesiumWeight     |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| popupText        |              | ✓            |                  |
+------------------+--------------+--------------+------------------+
| startElevMeters  |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| endElevMeters    |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| wayname          |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| waycategory      |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| surface          |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| waytype          |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| steepness        |              |              | ✓                |
+------------------+--------------+--------------+------------------+
| tollway          |              |              | ✓                |
+------------------+--------------+--------------+------------------+

.. note::
	The `Assignments` dataframe may have duplicated `odID` values for different
	paths.  When `veroviz.createLeaflet` generates a Leaflet map, it will combine
	`odID` with `objectID` to form a new/unique `odID`.