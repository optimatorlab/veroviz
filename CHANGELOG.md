### Change Log

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

