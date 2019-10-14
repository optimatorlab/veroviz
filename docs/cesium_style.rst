.. _Cesium Style:

Cesium Style
============

Cesium Colors
-------------

See the cesium color documentation `here <https://cesiumjs.org/Cesium/Build/Documentation/Color.html>`_
for all available color options.


Cesium Node Icons
-----------------

*VeRoViz* currently uses `PinBuilder` from Cesium, which only 
supports icons with short strings (e.g., a number, or a short symbol like "?" or "!"). 
These short strings should be denoted in the `cesiumIconText` column of a :ref:`Nodes` dataframe.  
Note that `cesiumIconText` differs from `leafletIconText`, in that the former will display text that is visible directly within the icon itself, while the latter will only be displayed if you click on the icon.


Cesium Assignment Models
------------------------

*VeRoViz* ships with the following 3D models, which may be specified in the `modelFile` column of an :ref:`Assignments` dataframe:

+---------------------------+---------------------------------------+
| Filename                  | Description                           |
+===========================+=======================================+
| "ub_truck.gltf"           | UB truck                              |
+---------------------------+---------------------------------------+
| "drone.gltf"              | drone (without package)               |
+---------------------------+---------------------------------------+
| "drone_package.gltf"      | drone (with package)                  |
+---------------------------+---------------------------------------+
| "car_red.gltf"            | red car                               |
+---------------------------+---------------------------------------+
| "car_green.gltf"          | green car                             |
+---------------------------+---------------------------------------+
| "car_blue.gltf"           | blue car                              |
+---------------------------+---------------------------------------+
| "box_blue.gltf"           | blue box                              |
+---------------------------+---------------------------------------+
| "box_yellow.gltf"         | yellow box                            |
+---------------------------+---------------------------------------+


Cesium Line Styles
------------------

The following line styles are available: 'solid', 'dashed', 'dotted'