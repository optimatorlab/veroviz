### Change Log

### Version 0.4.3 (2020-12-30)

This minor release introduced five new functions, but was mostly about fixing some more bugs.

- New utility functions:
    - `assignmentsToPaths()`:  Returns a dictionary of lists of paths.  The dictionary's keys are objectIDs found in the 'assignments' dataframe.  For each 'objectID', a list is provided.  This list will contain one or more paths associated with that objectID.  If the objectID does not have any consecutive rows in the 'assignments' dataframe where the ending location differs from the starting location in the next row, then there will be only one path.  This function was created to make it easier to use functions like `closestPointLoc2Path()` and `minDistLoc2Path()`,  which require paths as inputs.
    - `arcsToPaths()`:  Like `assignmentsToPaths()`, but using an `arcs` dataframe as an input.
	- `nodesToLocs()`:  Returns a list of lists (i.e., locations) from a nodes dataframe, of the form [[lat,lon,alt], ..., [lat,lon,alt]].  
	- `closestPointLoc2Assignments()`:  Finds the point along each path of an assignments dataframe that is closest to a given location.
	- `closestPointLoc2Arcs()`:  Like `closestPointLoc2Assignments()`, but using an `arcs` dataframe as an input.

- Corrected an issue with the `nearestNodes()` function, where the wrong nodes were being returned if the nodes dataframe contained a subset of the nodes in the cost dictionary.

- Fixed bug in `createAssignments()` function where the `orsGetElevation()` function was not imported.

- Fixed bug in `createGantt()` function that was exposed by a recent update of `matplotlib`.  The number of y-axis tick marks now correctly matches the number of y-axis labels.

- Fixed bug in the `closestPointLoc2Path()` function, where an error would occur if two consecutive points in the path were actually the same location.

- Fixed bug in `createNodesFromLocs()`, where `startNode` was not allowed to equal zero.

- Updated docstring from the `addLeafletIsochrones()` function, which now provides a reference to the `isochrones()` function.
	
- Improved validation of inputs to `createAssignmentsFromLocSeq2D()` function.  It was not properly detecting if an invalid `dataProvider` was given.

- Increased DPI on Gantt charts (`createGantt()`) to improve image quality/size.

- Fixed two bugs in `createCesium()`:
    - The first was induced by Version 0.4.2, where the process of escaping single quotes was causing problems if the data were not of type `string`.
    - The second was related to the `cesiumIconText` field of a nodes dataframe was not being used to display text in the pins in Cesium.

- Corrected an issue in `getElevationDF()` where an error was thrown if there was no elevation data missing from the input dataframe.  The function now has a new input argument, `replaceOnlyNone`, which defaults to be `True`.  In this case, the user is warned if there's no missing elevation data (i.e., there's nothing to do).  If `False`, all elevation data will be updated.
    - FIXME -- Update example in Jupyter notebook

- Corrected an issue in calculating distances using geopy, where locations with differing altitudes were causing an error.

- Fixed an issue in `createLeaflet()`, `addLeafletCircle()`, and `addLeafletMarker()` where popup text wasn't being displayed.


### Version 0.4.2 (2020-07-22)

This minor release fixed some minor bugs.

- Associated with the `createCesium()` function:
    - Now checks for the existence of Cesium by looking for either `server.js` or `server.cjs`.
    - Escapes single quotes in `cesiumIconText` `popupText` fields.  These were causing javascript errors in Cesium.
- Associated with validation:
    - `createArcsFromNodeSeq` now requires the existence of a `nodes` dataframe.
    
### Version 0.4.1 (2020-06-18)

- Added `nearestNodes()` function to utilities.  Finds k nearest nodes (based on either time or distance) from a given node or location.
- Fixed bug associated with gathering road information when querying ORS (both online and local) for shapepoint info.
- Moved `initDataframe()`, `exportDataframe()`, `getMapBoundary()`, `convertDistance()`, `convertSpeed()`, and `convertTime()` to private functions within `_utilities.py`; pointed to these private functions when validation was not required.  This change was made to resolve circular references, where `utilities` imported a library that was also dependent upon `utilities`.
- Added new function, `setGlobal()`, to facilitate setting of global config values.  This function accepts a dictionary as an input. The key corresponds to a global VeRoViz setting parameter. This makes it easier for users to change default values for Leaflet entities and default settings. All the settings are saved in a dictionary named config.  Changes to default config settings are temporary (i.e., lasting only for a particular session).

### Version 0.4.0 (2020-05-01)

This major release focused on adding new data (including elevation and weather), and adding new functions.

- Added integration with new data providers:
    - Added 'ORS-local' as a valid dataProvider.  This is a locally-installed version of the OpenRouteService online API ('ORS-online').  See https://ask.openrouteservice.org/t/getting-started-with-ors-via-docker-and-localhost/1415/11 for more information on installing ORS locally.  The local version supports the following:
        - Snap to nearest road,
        - Isochrones (Note that 'total_pop' data is available from the online API, but is missing from the local implementation),
        - Find shapepoints (Note that 'wheelchair' routing is an option in the online API, but is not enabled in the local implementation), and 
        - Travel time/distance matrices (Note that there is no 'wheelchair' option in the local implementation)
            
    - The following functions are supported by 'ORS-online', but are not in 'ORS-local':	
        - `geocode()`
        - `reverseGeocode()`
        - `getElevation()`
	
	- OpenWeatherMap
	- Elevation-API
	- USGS

- New Utility functions:
    - `isochrones()` - Finds isochrones (lines corresponding to points of equal distance or time from a given location) to or from a given location. 
    - `createGantt()` - Draws a Gantt chart from an `Assignments` dataframe.  This has the appearance of a horizontal bar chart.  The x-axis indicates the elapsed time.  Each `objectID` forms a horizontal bar.
    - `getElevationLocs()` - Finds the elevation, in units of meters above mean sea level (MSL), for a given location or list of locations. 
    - `getElevationDF()` - Replaces missing (`None`) values for elevation columns of the provided dataframe.  New values are in units of meters above mean sea level (MSL).  
    - `closestPointLoc2Path()` - Finds the point along a given line that is closest to a given location.  Returns the [lat, lon] coordinates of the point, and the corresponding distance (in [meters]) from that point to the line.
    - `closestNode2Loc()` - Returns the closest node in the dataframe to the given location.  Also returns the Euclidean distance (in [meters]) from the location to the nearest node.
    - `lengthFromNodeSeq()` - Calculate the total "length" (either in time or distance) along a path defined by a sequence of node IDs.
    - `calcArea()` - Calculate the area, in square meters, of a polygon.
    - `getWeather()` - Get weather information (current and forecasted) for a specified [lat, lon] location.

- New Leaflet-related functions:
    - `addLeafletIcon()` - Add a single icon/pin to a Leaflet map.
    - `addLeafletIsochrones()` - Easily draw isochrones on a Leaflet map.  Be sure to run the `isochrones()` function first.
    - `addLeafletWeather()` - Adds map tiles showing weather conditions to a Leaflet map.  Weather tiles are obtained via openweathermap.org (an API key is required).


- Dataframe Changes:  Several new columns were added to the existing VeRoViz dataframes.
    - Assignments:
        - Added `ganttColor` column.  Defaults to 'darkgray'.  Used to specify colors in `createGantt()` function.
        - Added `popupText` column.  Defaults to `None`.
        - Added `startElevMeters` and `endElevMeters` columns.  Default to `None`.
        - Added `wayname`, `waycategory`, `surface`, `waytype`, `steepness`, and `tollway` columns, from OSM data.

    - Nodes:
        - Added `popupText` column.  Defaults to `None`.
        - Added `elevMeters` column.  Defaults to `None`.

    - Arcs:		
        - Added `popupText` column.  Defaults to `None`.
        - Added `startElevMeters` and `endElevMeters` columns.  Default to `None`.
		
- Updates/Changes to existing functions:
    - Added 'wheelchair' and 'shortest' `routeType` options for 'ORS-online'.  

    - `addStaticAssignment()` - Now includes a parameter to specify `ganttColor`.

    - `createLeaflet()` - Now includes `popupText` for nodes, arcs, and assignments.  New node icons are now available (circular markers with text).
		
    - `createCesium()` - Now includes `popupText` for nodes and routes.

    - `addLeafletCircle()` - Added options to include displayed and "popup" text labels.  These are in the `popupText`, `text`, `fontSize`, and `fontColor` arguments.
		
    - `addLeafletMarker()` - Added options to include displayed and "popup" text labels.  These are in the `popupText`, `text`, `fontSize`, and `fontColor` arguments.
		
    - `addLeafletPolygon()` - Added `popupText` option to display text when the polygon is clicked.

    - `addLeafletPolyline()` - Added `popupText` option to display text when the polygon is clicked.

    - The following functions allow specification of curved arcs in Leaflet:
        - `addAssignment2D()`
        - `addAssignment3D()`
        - `createAssignmentsFromArcs2D()`
        - `createAssignmentsFromNodeSeq2D()`
        - `createAssignmentsFromLocSeq2D()`
        - `createArcsFromNodeSeq()`
        - `createArcsFromLocSeq()`
        - `getShapepoints2D()`
        - `getShapepoints3D()`

    - `generateNodes()` now includes an option for "roadBased".

- New imports/libraries:
    - Added matplotlib, as required by new `createGantt()` function.

- Bug fixes and minor changes:
    - Fixed bug in validation for `getConvexHull` (`valGetConvexHull()`).
    - In `createLeaflet()`, it is now OK if neither nodes, arcs, nor boundingRegion are specified.  
    - Added validation for all Utility functions.  Now checks for existence of required inputs.
    - Added validation for lists of lat/lon coordinates (`_valLatLonList()`).  Now checks for existence of list of lists.
    - Cesium colors no longer require the 'Cesium.Color' prefix.

 


#### Version 0.3.1 (2019-11-12)

- Corrected typo error in `findLocsAtTime()` function.

#### Version 0.3.0 (2019-11-11)

This version adds new functionality through several new functions:
- `createAssignmentsFromNodeSeq2D()`
- `createAssignmentsFromLocSeq2D()`
- `createAssignmentsFromArcs2D()`
- `geocode()`
- `reverseGeocode()`
- `addAssignment2D()`
- `addAssignment3D()`
- `findLocsAtTime()`

Important note:  `arcs` dataframes now include/require the `objectID` field, for better integration with `assignments` dataframes.  `arcs` dataframes saved with an older version of veroviz will throw an error when importing (due to the absence of the `objectID` column in those old dataframes).

This release also includes some minor bug fixes which do not affect functionality.

Note that the `buildAssignments` module has been renamed to `createAssignments`.

#### Version 0.2.2 (2019-10-19)

- Corrected error in createCesium() function that occurred if only stationary objects were added (no nodes).

#### Version 0.2.1 (2019-10-15)

- Replaced nonconforming double-quote character (\xe2) in the docstring of generateNodes.py.  This was causing installation issues for some users.  This change does not affect any functionality.

#### Version 0.2.0 (2019-10-14)

- First official release of veroviz. 

