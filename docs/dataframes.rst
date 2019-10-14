Dataframes
==========

*VeRoViz* uses three particular pandas dataframes, as listed below. 
Each dataframe serves a specific purpose.  The columns of each dataframe 
that are used depend on the function that is referencing the dataframe. 
While each dataframe has a number of required columns, users are encouraged
to add new columns as necessary to support a particular research project.

+-------------------+----------------------------------------------------+
| Dataframe type    | Description                                        |
+===================+====================================================+
| :ref:`Nodes`      | Specifies information about single locations       |
|                   | (nodes or vertices).                               |
+-------------------+----------------------------------------------------+
| :ref:`Arcs`       | Used to draw lines between pairs of locations on a |
|                   | Leaflet map.                                       |
+-------------------+----------------------------------------------------+
| :ref:`Assignments`| Allows Cesium to generate 3D video for routing     |
|                   | visualization.                                     |
+-------------------+----------------------------------------------------+

The "Arcs" and "Assignments" dataframes are very similar.
See :ref:`Dataframes Comparison` for more information.


.. _Dataframes Comparison:

Dataframes Comparison
---------------------

The "Arcs" dataframe contains a subset of the "Assignments" dataframe 
columns.  Most notably, the "Arcs" dataframe does not contain information 
about timing, nor does it contain information related to the display of 
3D models in Cesium.

+-------------------+-----------+-----------------+
| Field Name        | Arcs      | Assignments     |
+===================+===========+=================+
| id                | ✓         | ✓               |
+-------------------+-----------+-----------------+
| objectID          |           | ✓               |
+-------------------+-----------+-----------------+
| modelFile         |           | ✓               |
+-------------------+-----------+-----------------+
| modelScale        |           | ✓               |
+-------------------+-----------+-----------------+
| modelMinPxSize    |           | ✓               |
+-------------------+-----------+-----------------+
| startTimeSec      |           | ✓               |
+-------------------+-----------+-----------------+
| startLat          | ✓         | ✓               |
+-------------------+-----------+-----------------+
| startLon          | ✓         | ✓               |
+-------------------+-----------+-----------------+
| startAltMeters    |           | ✓               |
+-------------------+-----------+-----------------+
| endTimeSec        |           | ✓               |
+-------------------+-----------+-----------------+
| endLat            | ✓         | ✓               |
+-------------------+-----------+-----------------+
| endLon            | ✓         | ✓               |
+-------------------+-----------+-----------------+
| endAltMeters      |           | ✓               |
+-------------------+-----------+-----------------+
| leafletColor      | ✓         | ✓               |
+-------------------+-----------+-----------------+
| leafletWeight     | ✓         | ✓               |
+-------------------+-----------+-----------------+
| leafletStyle      | ✓         | ✓               |
+-------------------+-----------+-----------------+
| leafletOpacity    | ✓         | ✓               |
+-------------------+-----------+-----------------+
| useArrows         | ✓         | ✓               |
+-------------------+-----------+-----------------+
| cesiumColor       | ✓         | ✓               |
+-------------------+-----------+-----------------+
| cesiumWeight      | ✓         | ✓               |
+-------------------+-----------+-----------------+
| cesiumStyle       | ✓         | ✓               |
+-------------------+-----------+-----------------+
| cesiumOpacity     | ✓         | ✓               |
+-------------------+-----------+-----------------+