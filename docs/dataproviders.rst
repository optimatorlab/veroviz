.. _Data Providers:

Data Providers
==============

*VeRoViz* supports the use of several data providers for querying travel directions, travel time/distance matrices, and snapping nodes to a road network.  Integration with additional data providers is planned for a future *VeRoViz* release.

Functions that employ data from these providers require specification of the `dataProvider` itself, as well as additional arguments that are unique to the chosen `dataProvider` (e.g., an `APIkey` or a `databaseName`).  The `routeType` field can be used to differentiate between a 'fastest' route, a 'shortest' route, 'pedestrian' routes, etc. 

The following table summarizes the options and requirements for each data provider currently supported by *VeRoViz*:

+-------------------+-----------------+------+------------+-----------+---------------+--------------+
|                                     | `dataProvider` field options                                 |
+-------------------+-----------------+------+------------+-----------+---------------+--------------+
|                                     | None | 'pgRouting'| 'MapQuest'| 'OSRM-online' | 'ORS-online' |
+===================+=================+======+============+===========+===============+==============+
| required key      | "databaseName"  |      | ✓          |           |               |              |
| in                +-----------------+------+------------+-----------+---------------+--------------+
| `dataProviderArgs`| "APIkey"        |      |            | ✓         |               | ✓            |
+-------------------+-----------------+------+------------+-----------+---------------+--------------+
| allowed?          | snapNodesToRoad |      | ✓          | ✓         | ✓             | ✓            |
+-------------------+-----------------+------+------------+-----------+---------------+--------------+
| `routetype`       | "fastest"       |      | ✓          | ✓         | ✓             | ✓            |
| field             +-----------------+------+------------+-----------+---------------+--------------+
| options           | "shortest"      |      |            | ✓         |               |              |
|                   +-----------------+------+------------+-----------+---------------+--------------+
|                   | "pedestrian"    |      |            | ✓         |               | ✓            |
|                   +-----------------+------+------------+-----------+---------------+--------------+
|                   | "cycling"       |      |            |           |               | ✓            |
|                   +-----------------+------+------------+-----------+---------------+--------------+
|                   | "truck"         |      |            |           |               | ✓            |
|                   +-----------------+------+------------+-----------+---------------+--------------+
|                   | "euclidean2d"   | ✓    |            |           |               |              |
|                   +-----------------+------+------------+-----------+---------------+--------------+
|                   | "manhattan"     | ✓    |            |           |               |              |
+-------------------+-----------------+------+------------+-----------+---------------+--------------+

None
----

No data provider is chosen. Nodes and arcs are generated without consideration of any underlying road networks. Only simple types of node distributions or route types can be applied without a data provider.

pgRouting
---------

pgRouting is an open-source database application that must be installed locally on the user's computer.  You will need to :ref:`install pgRouting` before 
using related functions. 

We recommend that users update their local pgRouting database frequently, as the source data (from OpenStreetMap) changes over time.

If you find odd results when using pgRouting, (e.g. unexpected values of "0" 
from :meth:`~veroviz.getTravelMatrice2D.getTravelMatrice2D`) or if nodes are not being snapped properly to road, please check if the data in the pgRouting database is sufficient 
to cover the region of interest. VeRoViz can not calculate the coordinates outside
the boundary of pgRouting data.

See the `pgRouting documentation`_ for more details.

MapQuest
--------

MapQuest is a commercial data source, but users may issue a limited number of requests for free.  You will need to :ref:`apply for MapQuest APIkey`
before using related functions.  MapQuest provides perhaps the most detailed results of the data providers.  However, keep in mind that the free API key has a monthly limit on the number of queries.

See the `MapQuest documentation`_ for more details.

OSRM
----

The Open Source Routing Machine is available via both an online API (in which case no installation is required) or as a local installation.  Currently, however, VeRoViz only supports the online API.  

For the online API, no API key is required.  Please note, though, that this API is hosted on a "demo" server, which is not intended for high-volume user requests.  It is recommended that users use OSRM only for small-scale testing/evaluation; please don't overload the OSRM demo server with large-scale problems.  Be advised that excessive OSRM requests will often result in server timeouts.

The routes and travel matrix data provided by OSRM are based on OpenStreetMaps.  OSRM's results are typically less detailed than those provided by MapQuest. 

See the `OSRM documentation`_ for more details.

ORS
---

OpenRouteService is currently the suggested data provider for VeRoViz.  Like OSRM, it uses data from OpenStreetMaps.  ORS offers a free API key with a generous daily query limit.  Although ORS also provides an open-source engine that can be installed locally, this option is not currently enabled in VeRoViz.

See the `ORS documentation`_ for more information.

.. _pgRouting documentation: http://docs.pgrouting.org/latest/en/index.html
.. _MapQuest documentation: https://developer.mapquest.com/documentation/
.. _OSRM documentation: http://project-osrm.org/docs/v5.22.0/api/#general-options
.. _ORS documentation: https://openrouteservice.org