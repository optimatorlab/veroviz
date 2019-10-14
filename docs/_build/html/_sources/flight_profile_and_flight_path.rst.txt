.. _Flight Profile and Flight Path:

Flight Profile and Flight Path
==============================

The :meth:`~veroviz.getTimeDist3D.getTimeDist3D` and 
:meth:`~veroviz.getShapepoints3D.getShapepoints3D` functions accommodate 
different types of flight profiles/paths, which are specified in the `routeType` 
input argument.  These profiles describe the aircraft's change 
in altitude over time, and are used to mimic certain types of flight.

Specifically, *VeRoViz* defines four pre-determined flight profiles/paths: 
- 'square' - The aircraft takes off vertically to a cruise altitude, flies at the cruise altitude to the destination, then lands vertically.  This type of profile is common with quadcopter drones.
- 'triangular' - The aircraft climbs to a cruising altitude and then immediately descends to the destination. 
- 'trapezoidal' - A hybrid of the 'square' and 'triangular' profiles, in the 'trapezoidal' profile the aircraft takes off while also moving toward the destination.  It then flies at the cruise altitude before descending while also moving toward the destination.
- 'straight' - The aircraft flies directly from the origin to the destination.  This would typically be useful if the origin and destination are at different altitudes, or if both locations have a positive altitude.

.. note::
	The "flight profiles" employed in *VeRoViz* are approximations, and do 
	not necessarily correspond to flight paths that are feasible for 
	certain aircraft.  These flight profiles are intended to be used for 
	visualization purposes.  

Each profile is fully characterized 
by a specific combination of parameters, as described in the table below.  
If a parameter is provided, but is not required, it will be ignored.


+--------------------+----------+--------------+---------------+------------+
|                    | `routeType` options                                  |
+--------------------+----------+--------------+---------------+------------+
| Field name         | 'square' | 'triangular' | 'trapezoidal' | 'straight' |
+====================+==========+==============+===============+============+
| takeoffSpeedMPS    | ✓        |              | ✓             |            |
+--------------------+----------+--------------+---------------+------------+
| climbRateMPS       |          |              | ✓             |            |
+--------------------+----------+--------------+---------------+------------+
| cruiseSpeedMPS     | ✓        | ✓            | ✓             | ✓          |
+--------------------+----------+--------------+---------------+------------+
| cruiseAltMetersAGL | ✓        | ✓            | ✓             |            |
+--------------------+----------+--------------+---------------+------------+
| landSpeedMPS       | ✓        |              | ✓             |            |
+--------------------+----------+--------------+---------------+------------+
| descentRateMPS     |          |              | ✓             |            |
+--------------------+----------+--------------+---------------+------------+


For problems involving coordinated vehicles, it is often necessary for one 
vehicle to wait for another.  The :meth:`~veroviz.getShapepoints3D.getShapepoints3D`
function includes `loiterPosition` and `earliestLandTime` arguments, 
which are used to specify where an aircraft would wait (loiter) and the 
earliest time at which the aircraft can land.  

The available loiter positions are specific to each flight profile.  The table below describes the `loiterPosition` options for each `routeType`.

+--------------------+----------+---------------+---------------+------------+
|                    | `routeType` options                                   |
+--------------------+----------+---------------+---------------+------------+
| `loiterPosition`   | 'square' | 'triangular'  | 'trapezoidal' | 'straight' |
+====================+==========+===============+===============+============+
| 'beforeTakeoff'    | ✓        | ✓             | ✓             | ✓          |
+--------------------+----------+---------------+---------------+------------+
| 'takeoffAtAlt'     | ✓        | ✓             | ✓             |            |
+--------------------+----------+---------------+---------------+------------+
| 'arrivalAtAlt'     | ✓        | ✓ (same as    | ✓             |            |
|                    |          | takeoffAtAlts)|               |            |
+--------------------+----------+---------------+---------------+------------+
| 'afterLand'        | ✓        | ✓             | ✓             | ✓          |
+--------------------+----------+---------------+---------------+------------+

- 'beforeTakeoff' - Loitering occurs before the aircraft leaves its starting location.
- 'takeoffAtAlt' - Loitering occurs when the aircraft reaches its cruise altitude.
- 'arrivalAtAlt' - Loitering occurs at the cruise altitude when the aircraft reaches the [lat,lon] coordinate of the destination.
- 'afterLand' - Loitering occurs after the aircraft completes its route to the destination.  The aircraft will then be held in place until `earliestLandTime` (the name of this parameter is misleading in this case, as the aircraft will have already landed before that time).
