.. _Leaflet Style:

Leaflet Style
=============

Leaflet Map Background (Map Tiles)
----------------------------------

*VeRoViz* provides several options for the `mapBackground` field:

.. |Cartodb_Positron| image:: /_images/Cartodb_Positron.png
    :height: 200px

.. |Cartodb_Dark_matter| image:: /_images/Cartodb_Dark_matter.png
    :height: 200px

.. |Openstreetmap'| image:: /_images/Openstreetmap.png
    :height: 200px

.. |Stamen_Terrain| image:: /_images/Stamen_Terrain.png
    :height: 200px

.. |Stamen_Toner| image:: /_images/Stamen_Toner.png
    :height: 200px

.. |Stamen_Watercolor| image:: /_images/Stamen_Watercolor.png
    :height: 200px

.. |Arcgis_Aerial| image:: /_images/ArcGIS_Aerial.png
    :height: 200px

.. |Arcgis_Gray| image:: /_images/ArcGIS_Gray.png
    :height: 200px

.. |Arcgis_Ocean| image:: /_images/ArcGIS_Ocean.png
    :height: 200px

.. |Arcgis_Roadmap| image:: /_images/ArcGIS_Roadmap.png
    :height: 200px

.. |Arcgis_Shaded_Relief| image:: /_images/ArcGIS_Shaded_Relief.png
    :height: 200px

.. |Arcgis_Topo| image:: /_images/ArcGIS_Topo.png
    :height: 200px

.. |Open_Topo| image:: /_images/Open_Topo.png
    :height: 200px

+---------------------------+----------------------------------------------+
| `mapBackground` options   | Preview                                      |
+===========================+==============================================+
| 'Cartodb Positron'        | |Cartodb_Positron|                           |
+---------------------------+----------------------------------------------+
| 'Cartodb Dark_matter',    | |Cartodb_Dark_matter|                        |
+---------------------------+----------------------------------------------+
| 'Openstreetmap',          | |Openstreetmap'|                             |
+---------------------------+----------------------------------------------+
| 'Stamen Terrain',         | |Stamen_Terrain|                             |
+---------------------------+----------------------------------------------+
| 'Stamen Toner',           | |Stamen_Toner|                               |
+---------------------------+----------------------------------------------+
| 'Stamen Watercolor',      | |Stamen_Watercolor|                          |
+---------------------------+----------------------------------------------+
| 'Arcgis Aerial',          | |Arcgis_Aerial|                              |
+---------------------------+----------------------------------------------+
| 'Arcgis Gray',            | |Arcgis_Gray|                                |
+---------------------------+----------------------------------------------+
| 'Arcgis Ocean',           | |Arcgis_Ocean|                               |
+---------------------------+----------------------------------------------+
| 'Arcgis Roadmap',         | |Arcgis_Roadmap|                             |
+---------------------------+----------------------------------------------+
| 'Arcgis Shaded Relief',   | |Arcgis_Shaded_Relief|                       |
+---------------------------+----------------------------------------------+
| 'Arcgis Topo',            | |Arcgis_Topo|                                |
+---------------------------+----------------------------------------------+
| 'Open Topo'               | |Open_Topo|                                  |
+---------------------------+----------------------------------------------+


Leaflet Weather Map Overlays
----------------------------

Starting with version 0.4.0, *VeRoViz* also provides several weather condition "overlays" for Leaflet maps.  These options are enabled via the `mapType` field of the `addLeafletWeather()` function.

.. |clouds| image:: /_images/weather_clouds.png
    :height: 200px

.. |precip| image:: /_images/weather_precip.png
    :height: 200px

.. |pressure| image:: /_images/weather_pressure.png
    :height: 200px

.. |temp| image:: /_images/weather_temp.png
    :height: 200px

.. |wind| image:: /_images/weather_wind.png
    :height: 200px


+---------------------+------------------------------------+
| `mapType` options   | Preview                            |
+=====================+====================================+
| 'clouds'            | |clouds|                           |
+---------------------+------------------------------------+
| 'precip'            | |precip|                           |
+---------------------+------------------------------------+
| 'pressure'          | |pressure|                         |
+---------------------+------------------------------------+
| 'temp'              | |temp|                             |
+---------------------+------------------------------------+
| 'wind'              | |wind|                             |
+---------------------+------------------------------------+


Leaflet Colors
--------------

Leaflet supports the following colors: 'beige', 'black', 'blue', 'cadetblue', 'darkblue', 'darkgreen', 'gray',
'darkpurple', 'darkred',  'green', 'lightblue', 'lightgray', 
'lightgreen', 'lightred', 'orange', 'pink', 'purple', and 'red'.


Leaflet Prefix and Leaflet Type
-------------------------------

Leaflet provides numerous icons.  Both an `iconPrefix` and an
`iconType` are required to specify a particular icon.  Some of the available options 
for both of the icon prefixes are shown below:

+----------------------+----------------------------------------------+
| `iconPrefix` options | `iconType` options                           |
+======================+==============================================+
| 'glyphicon'          | 'info-sign', 'home', 'glass', 'flag',        |
|                      | 'star', 'user', 'cloud', 'bookmark', etc.    |
+----------------------+----------------------------------------------+
| 'fa'                 | 'ambulance', 'bicycle', 'bus', 'car',        |
|                      | 'flag', 'home', 'heartbeat', 'plane',        |
|                      | 'motorcycle', 'question', 'ship',            |
|                      | 'shopping-bag', 'shopping-basket',           |
|                      | 'shopping-cart', 'star', 'subway', 'taxi',   |
|                      | 'truck', 'university', 'user', 'users', etc. |
+----------------------+----------------------------------------------+
| 'custom'             | Specify a string with three fields separated |     
|                      | by a dash:  <circle radius in pixels>-<font  |
|                      | color>-<font size>.                          |
|                      | For example, '10-white-12' will produce a    |
|                      | circle icon of radius 10 pixels, with white  |
|                      | font of size 12 point.  The background color |
|                      | of the circle icon is specified by the       |
|                      | `iconColor` argument.                        |
+----------------------+---------------------------------------------+

Additional options may be available (but have not been tested):
- For 'glyphicon', see 
`https://www.w3schools.com/bootstrap/bootstrap_ref_comp_glyphs.asp <https://www.w3schools.com/bootstrap/bootstrap_ref_comp_glyphs.asp>`_ and
`https://getbootstrap.com/docs/3.3/components <https://getbootstrap.com/docs/3.3/components/>`_

For 'fa', see
`https://fontawesome.com/icons?d=gallery&m=free <https://fontawesome.com/icons?d=gallery&m=free>`_


Leaflet Line Styles
-------------------

The following line styles are available: 'solid', 'dashed', 'dotted'


Default settings for Leaflet
----------------------------

- Default colors
	- For Nodes (Icons): 'blue'
	- For Arcs/Assignments: 'orange'
	- For BoundingRegion: 'brown'

- Default icons
	- iconPrefix: 'glyphicon'
	- iconType: 'info-sign'

- Default arc style
	- style: 'solid'
	- weight: 3
	- opacity: 0.8

For more default settings, see :ref:`Global settings and defaults`