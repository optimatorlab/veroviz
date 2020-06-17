from veroviz._common import *
from veroviz._validation import valGetTimeDistScalar2D

from veroviz._getTimeDistFromLocs2D import getTimeDistFromLocs2D

def getTimeDistScalar2D(startLoc=None, endLoc=None, outputDistUnits='meters', outputTimeUnits='seconds', routeType='euclidean2D', speedMPS=None, dataProvider=None, dataProviderArgs=None):
	"""
	Returns scalar values of time and distance between 2 points in 2 dimensions.

	Parameters
	----------		
	startLoc: list, Required, default as None
		The starting location, expressed as either [lat, lon] or [lat, lon, alt].  Differences in altitude between the starting and ending locations will be ignored (this is a 2D function).
	endLoc: list, Required, default as None
		The ending location, expressed as either [lat, lon] or [lat, lon, alt].   Differences in altitude between the starting and ending locations will be ignored (this is a 2D function).
	outputDistUnits: string, Optional, default as 'meters'
		Specifies the desired distance units for the function's output.  Valid values are 'meters', 'm', 'kilometers', 'km', 'miles', 'mi', 'feet', 'ft', 'nm', and 'nmi' (nautical miles). See :ref:`Units` for options and abbreviations.
	outputTimeUnits: string, Optional, default as 'seconds'
		Specifies the desired time units for the function's output.  Valid values are 'seconds', 'hours', and 'minutes'. See :ref:`Units` for options and abbreviations.
	routeType: string, Optional, default as 'euclidean2D'
		This describes a characteristic of the travel mode.  Possible values are: 'euclidean2D', 'manhattan', 'fastest', 'shortest', 'pedestrian', 'cycling', and 'truck'.  The 'euclidean2D' and 'manhattan' options are calculated directly from GPS coordinates, without a road network.  Neither of these two options require a data provider.  However, the other options rely on road network information and require a data provider.  Furthermore, some of those other options are not supported by all data providers.  See :ref:`Data Providers` for details.
	speedMPS: float, Conditional, default as None
		Speed of the vehicle, in units of meters per second. For route types that are not road-network based (i.e., 'euclidean2D' and 'manhattan'), this field is required to calculate travel times. Otherwise, if a route type already incorporates travel speeds from road network data, (i.e., 'fastest', 'shortest', and 'pedestrain'), this input argument may be ignored.  If provided, `speedMPS` will override travel speed data used by the route type option.
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for obtaining the travel data. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.

	Returns
	-------
	time: float
		Travel time from the start location to the end location.  Units are determined by `outputTimeUnits`, which default to be in seconds.
	dist: float
		Distance from the start location to the end location.  Units are determined by `outputDistUnits`, which default to be in meters.

	Note
	----
	`getTimeDistScalar2D()` is similar to `getTimeDist2D()`, but instead of returning matrices and vectors, `getTimeDistScalar2D()` returns two scalars for the travel time and distances between start and end locations.
	
	
	Example
	-------
	Import veroviz and check if the version is up-to-date:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Example 1 
		>>> import os
		>>>
		>>> [timeSec, distMeters] = vrv.getTimeDistScalar2D(
		...     startLoc         = [42.80, -78.80],
		...     endLoc           = [42.90, -78.80],
		...     routeType        = 'fastest',
		...     dataProvider     = 'ORS-online',
		...     dataProviderArgs = {'APIkey': os.environ['ORSKEY']})
		>>> print("Travel time in seconds: %.2f" % (timeSec))
		>>> print("Distance in meters: %.2f" % (distMeters))
		Travel time in seconds: 1134.74
		Distance in meters: 13891.61

	Example 2 - This example includes all functional arguments:
		>>> [timeMin, distMiles] = vrv.getTimeDistScalar2D(
		...     startLoc         = [42.80, -78.80], 
		...     endLoc           = [42.90, -78.80],
		...     outputTimeUnits  = 'minutes',
		...     outputDistUnits  = 'miles',
		...     routeType        = 'fastest',
		...     speedMPS         = None,
		...     dataProvider     = 'ORS-online',
		...     dataProviderArgs = {'APIkey': os.environ['ORSKEY']})
		>>> [timeMin, distMiles]
		[18.912333333333333, 8.631867722171823]

	"""

	# validataion
	[valFlag, errorMsg, warningMsg] = valGetTimeDistScalar2D(startLoc, endLoc, outputDistUnits, outputTimeUnits, routeType, speedMPS, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return [None, None]
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	[dicTime, dicDist] = getTimeDistFromLocs2D(
		fromLocs=[startLoc], 
		fromRows=[0], 
		toLocs=[endLoc], 
		toCols=[0], 
		outputDistUnits=outputDistUnits, 
		outputTimeUnits=outputTimeUnits, 
		routeType=routeType, 
		speedMPS=speedMPS, 
		dataProvider=dataProvider, 
		dataProviderArgs=dataProviderArgs)

	time = dicTime[0, 0]
	dist = dicDist[0, 0]

	return [time, dist]