Install Dependencies
====================

Some *VeRoViz* functionality requires additional software or API keys. 

.. _install pgRouting:

Install pgRouting
-----------------

pgRouting is an extension to the PostGIS/PostgreSQL geospatial database, which provides geospatial routing functionality. In VeRoViz, installing pgRouting will enable the `pgRouting` option for generating nodes, building traveling matrices, querying shapepoints along routes, etc. 

pgRouting is not required for VeRoViz.  If it is not installed, other data providers may be used.

See https://veroviz.org/documentation.html for pgRouting installation instructions.


.. _apply for Cesium ion Key:

Install Cesium
--------------

Cesium is an open-source JavaScript library for rendering 3D maps.  The VeRoViz :meth:`~veroviz.createCesium.createCesium` function generates files to display solutions in Cesium.

See https://veroviz.org/documentation.html for Cesium installation instructions.


.. _apply for ORS APIkey:

Apply for ORS API key
---------------------

OpenRouteService (ORS) is currently the suggested data provider for VeRoViz. It uses data from OpenStreetMaps. ORS offers a free API key with a generous daily query limit. ORS also provides an open-source engine that can be installed locally, which VeRoViz now supports (as of version 0.4.0, in May, 2020).

Register for a free ORS API key here: https://openrouteservice.org/dev/#/signup.


.. _apply for MapQuest APIkey:

Apply for MapQuest API key
--------------------------

MapQuest is a commercial data source, but users may issue a limited number of requests for free. You may apply for a MapQuest API key here: https://developer.mapquest.com/documentation.

MapQuest provides perhaps the most detailed results of the data providers. However, keep in mind that the free API key has a monthly limit on the number of queries.

.. _apply for OpenWeatherMap APIkey:

Apply for OpenWeatherMap API key
--------------------------------

OWM provides current, forecast, and historical weather data, as well as map overlays for Leaflet.  Support for OWM integration is available in VeRoViz version 0.4.0.
						
You may register for a free API key at https://openweathermap.org/api.

.. _apply for ElevationAPI key:

Apply for Elevation-API key
---------------------------

Elevation-API provides elevation data for practically any location on the globe.  Elevations at 5km resolutions are available for free; higher-resolution data may be obtained for a nominal fee. Support for Elevation-API integration is available in VeRoViz version 0.4.0.
						
You may register for a free API key at https://elevation-api.io.
