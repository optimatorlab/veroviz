from veroviz._common import *
from veroviz._validation import valGetTimeDistScalar3D

from veroviz._utilities import privConvertDistance
from veroviz._utilities import privConvertTime

from veroviz._buildFlightProfile import buildNoLoiteringFlight
from veroviz._buildFlightProfile import getTimeDistFromFlight

def getTimeDistScalar3D(startLoc=None, endLoc=None, outputDistUnits='meters', outputTimeUnits='seconds', takeoffSpeedMPS=None, cruiseSpeedMPS=None, landSpeedMPS=None, cruiseAltMetersAGL=None, routeType='square', climbRateMPS=None, descentRateMPS=None):
	"""
	Returns scalar values of time, ground distance, and total distance between 2 points in 3 dimensions.
	

	Parameters
	----------
	startLoc: list, Required, default as 'None'
		The starting location, expressed as either [lat, lon, alt] or [lat, lon]. If no altitude is provided, it will be assumed to be 0 meters above ground level.
	endLoc: list, Required, default as 'None'
		The ending location, expressed as either [lat, lon, alt] or [lat, lon]. If no altitude is provided, it will be assumed to be 0 meters above ground level.
	outputDistUnits: string, Optional, default as 'meters'
		Specifies the desired distance units for the function's output.  Valid values are 'meters', 'm', 'kilometers', 'km', 'miles', 'mi', 'feet', 'ft', 'nm', and 'nmi' (nautical miles). See :ref:`Units` for options and abbreviations.
	outputTimeUnits: string, Optional, default as 'seconds'
		Specifies the desired time units for the function's output.  Valid values are 'seconds', 'hours', and 'minutes'. See :ref:`Units` for options and abbreviations.
	routeType: string, Optional, default as 'square'
		Specifies the basic shape of the flight profile.  Valid options include 'square', 'triangular', 'trapezoidal', and 'straight'.  The square profile involves a vertical takeoff to a cruising altitude, horizontal travel at the cruising altitude, and a vertical landing.  The trapezoidal profile describes a takeoff phase in which the aircraft increases altitude and travels horizontally towards the destination until reaching the cruising altitude, horizontal travel at the cruising altitude, and a landing phase in which the aircraft decreases altitude and travels horizontally until reaching the destination.  For the trapezoidal profile, the horizontal movement during the takeoff and landing phases is a function of the `climbRateMPS` and `descentRateMPS`, respectively.  The triangular profile describes an ascent to the cruising altitude followed immediately by a descent to the destination.  Finally, the straight profile describes straight-line flight directly from the starting location to the ending location; the altitudes of these two locations may differ.  See :ref:`Flight Profile and Flight Path` for a description of these flight profiles.
	takeoffSpeedMPS: float, Conditional, default as None
		The speed of the aircraft, in meters per second, during the "takeoff" phase.  This will apply only to 'square' and 'trapezoidal' route types.  The takeoff phase is the first component of these route types, and is associated with an increase in altitude.  The takeoff speed is assumed to be constant, and ignores acceleration.  See :ref:`Flight Profile and Flight Path` for additional information.
	cruiseSpeedMPS: float, Conditional, default as None
		The speed of the aircraft, in meters per second, during the "cruising" phase.  This will apply to all of the route options.  Typically, the cruising phase occurs at a constant altitude, as specified by `cruiseAltMetersAGL`.  However, for the 'triangular' route type, cruiseSpeedMPS specifies the constant travel speed during both the ascent to, and immediate descent from, the cruise altitude.  In the 'triangle' route type, the aircraft has no horizontal travel at the cruise altitude.  In all cases, the cruise speed is assumed to be constant, and ignores acceleration.  See :ref:`Flight Profile and Flight Path` for additional information.
	landSpeedMPS: float, Conditional, default as None
		The speed of the aircraft, in meters per second, during the "landing" phase. This will apply to only the 'square' and 'trapezoidal' route types.  The landing phase is the last component of these route types, and is associated with a decrease in altitude.  The landing speed is assumed to be constant, and ignore deceleration.  See :ref:`Flight Profile and Flight Path` for additional information.
	cruiseAltMetersAGL: float, Conditional, default as None
		The altitude, in meters above ground level, at which the aircraft is in the "cruise" phase.  This phase is typically associated with horizontal movement at a fixed altitude.  The exception is for the 'triangular' route type, in which case the aircraft instantaneously transitions from ascent to descent at the cruise altitude (i.e., there is no horizontal travel at this altitude).  All but the 'straight' route type require/use the cruise altitude.  See :ref:`Flight Profile and Flight Path` for additional details.
	climbRateMPS: float, Conditional, default as None
		This parameter is used only for the 'trapezoidal' route type, and is in units of meters per second.  It describes the rate at which the aircraft increases its altitude, relative to the value of `takeoffSpeedMPS`.  If `climbRateMPS == takeoffSpeedMPS`, then the takeoff phase will be purely vertical.  If `climbRateMPS` is close to zero, then the takeoff phase will be characterized by a slow increase in altitude (and longer horizontal flight).  The aircraft's actual travel speed during the climb will be `takeoffSpeedMPS`.  See :ref:`Flight Profile and Flight Path` for additional details.
	descentRateMPS: float, Conditional, default as None
		This parameter is used only for the 'trapezoidal' route type, and is in units of meters per second.  It describes the rate at which the aircraft decreases its altitude, relative to the value of `landSpeedMPS`.  If `descentRateMPS == landSpeedMPS`, then the landing phase will be purely vertical.  If `descentRateMPS` is close to zero, then the landing phase will be characterized by a slow decrease in altitude (and longer horizontal flight).  The aircraft's actual travel speed during the descent will be `landSpeedMPS`.  See :ref:`Flight Profile and Flight Path` for additional details.

	Returns
	-------
	time: float
		Travel time from the start location to the end location.  Units are determined by `outputTimeUnits`, which default to be in seconds.
	groundDistance: float
		Ground travel distance from the start location to the end location.  Units are determined by `outputDistUnits`, which default to be in meters.
	flightDistance: float
		Total travel distance (i.e., including both the horizontal and vertical components of flight) from the start location to the end location.  Units are determined by `outputDistUnits`, which default to be in meters.


	Note
	----
	`getTimeDistScalar3D()` is similar to `getTimeDist3D()`, but instead of returning matrices and vectors, `getTimeDistScalar3D()` returns just scalar values for the travel time and distances between start and end locations.

	Example
	-------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Example 1 
		>>> [timeSec, grndDistMeters, totalDistMeters] = vrv.getTimeDistScalar3D(
		...     startLoc           = [42.80, -78.90],
		...     endLoc             = [42.85, -78.95],
		...     cruiseAltMetersAGL = 120,
		...     takeoffSpeedMPS    = 15,
		...     cruiseSpeedMPS     = 20,
		...     landSpeedMPS       = 10,
		...     routeType          = 'square')
		>>> [timeSec, grndDistMeters, totalDistMeters]
		[364.85047765232866, 6897.009553046573, 7137.009553046573]

	The result means the total flight time is 364.85 seconds, ground distance is 6897 meters, and total flight distance is 7137 meters.

	Example 2 - This example includes all functional arguments:
		>>> [timeMin, grndDistMiles, totalDistMiles] = vrv.getTimeDistScalar3D(
		...     startLoc           = [42.80, -78.90],
		...     endLoc             = [42.85, -78.95],
		...     routeType          = 'trapezoidal',
		...     cruiseAltMetersAGL = 120,
		...     takeoffSpeedMPS    = 25,
		...     climbRateMPS       = 6,
		...     cruiseSpeedMPS     = 25,
		...     landSpeedMPS       = 25,
		...     descentRateMPS     = 6,
		...     outputTimeUnits    = 'minutes',
		...     outputDistUnits    = 'miles')
		>>> [timeMin, grndDistMiles, totalDistMiles]		
		[4.617491177183978, 4.28561370067641, 4.303774693834719]
	"""

	# validataion
	[valFlag, errorMsg, warningMsg] = valGetTimeDistScalar3D(startLoc, endLoc, outputDistUnits, outputTimeUnits, takeoffSpeedMPS, cruiseSpeedMPS, landSpeedMPS, cruiseAltMetersAGL, routeType, climbRateMPS, descentRateMPS)
	if (not valFlag):
		print (errorMsg)
		return [None, None, None]
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	flight = buildNoLoiteringFlight(routeType, startLoc, cruiseAltMetersAGL, endLoc, takeoffSpeedMPS, climbRateMPS, cruiseSpeedMPS, landSpeedMPS, descentRateMPS)
	[timeSec, gDistMeters, fDistMeters] = getTimeDistFromFlight(flight.copy())

	time = timeSec * privConvertTime(1.0, "s", outputTimeUnits)
	groundDistance = gDistMeters * privConvertDistance(1.0, "m", outputDistUnits)
	flightDistance = fDistMeters * privConvertDistance(1.0, "m", outputDistUnits)

	return [time, groundDistance, flightDistance]