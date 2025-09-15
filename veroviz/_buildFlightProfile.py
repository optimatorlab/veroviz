from veroviz._common import *

from veroviz._utilities import privConvertSpeed    # FIXME -- Where is this used?

from veroviz._geometry import geoMileageInPath2D
from veroviz._geometry import geoDistancePath2D
from veroviz._geometry import geoDistance2D

from veroviz._internal import loc2Dict
from veroviz._internal import locs2Dict

def buildNoLoiteringFlight(routeType='square', startLoc=None, cruiseAltMetersAGL=None, endLoc=None, takeoffSpeedMPS=None, rateOfClimbMPS=None, cruiseSpeedMPS=None, landSpeedMPS=None, rateOfDescentMPS=None):
	
	"""
	This function generates a flight profile/path given routeType, origin/destinate location and speed of all phase. The profile it generate does not include loiter (i.e. the loiter column is all zero)

	Parameters
	----------
	routeType: string, Optional, default as 'square'
		Type of flight profile/path, options are 'square', 'triangular', 'trapezoidal', 'straight'.
	startLoc: list, Required, default as 'None'
		Start location, the format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt].
	cruiseAltMetersAGL: float, Required, default as 'None'
		Cruise altitude, meters above sea level.
	endLoc: list, Required, default as 'None'
		End location, the format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt].
	rateOfClimbMPS: float, Required, default as 'None'
		Rate of climb of the aircraft, it is a vertical speed.
	climbGradientInDegree: float, Required, default as 'None'
		Climb gradient, the unit is degree, horizontal as zero, minimal value as 0, maximum value as 90 (vertical up).
	cruiseSpeedMPS: float, Required, default as 'None'
		Speed of cruise, in the unit of meters/second.
	rateOfDescentMPS: float, Required, default as 'None'
		Rate of descent, vertical speed.
	descentGradientInDegree: float, Required, default as 'None'
		Descent gradient, the unit is degree, horizontal as zero, minimal value as 0, maximum value as 90 (vertical down).

	Return
	------
	flight dataframe
		A dataframe to be interpreted into assignments dataframe
	"""

	try:
		routeType = routeType.lower()
	except:
		pass

	# Generate flight profile without loitering
	if (routeType == 'square'):
		flight = _buildFlightProfile(
			startLoc=startLoc, 
			cruiseAltMetersAGL=cruiseAltMetersAGL,
			endLoc=endLoc,
			takeoffSpeedMPS=takeoffSpeedMPS,
			rateOfClimbMPS=takeoffSpeedMPS,
			cruiseSpeedMPS=cruiseSpeedMPS,
			landSpeedMPS=landSpeedMPS,
			rateOfDescentMPS=landSpeedMPS)
		
	elif (routeType == 'triangular'):
		dicStartLoc = loc2Dict(startLoc)
		dicEndLoc = loc2Dict(endLoc)
		midLoc = [(dicStartLoc['lat'] + dicEndLoc['lat']) / 2, (dicStartLoc['lon'] + dicEndLoc['lon']) / 2, cruiseAltMetersAGL]
		flight = _buildFlightPath(
			path=[startLoc, midLoc, endLoc],
			speedMPS=cruiseSpeedMPS)
		# There will be only three locations
		flight.loc[0, 'description'] = "beforeDeparture"
		flight.loc[1, 'description'] = "takeoffAtAlt and arrivalAtAlt"
		flight.loc[2, 'description'] = "afterArrival"

	elif (routeType == 'trapezoidal'):
		flight = _buildFlightProfile(
			startLoc=startLoc, 
			cruiseAltMetersAGL=cruiseAltMetersAGL,
			endLoc=endLoc,
			takeoffSpeedMPS=takeoffSpeedMPS,
			rateOfClimbMPS=rateOfClimbMPS,
			cruiseSpeedMPS=cruiseSpeedMPS,
			landSpeedMPS=landSpeedMPS,
			rateOfDescentMPS=rateOfDescentMPS)

	elif (routeType == 'straight'):
		flight = _buildFlightPath(
			path=[startLoc, endLoc],
			speedMPS=cruiseSpeedMPS)
		# There will be only two locations
		flight.loc[0, 'description'] = "beforeDeparture"
		flight.loc[1, 'description'] = "afterArrival"

	return flight

def _buildFlightProfile(startLoc, cruiseAltMetersAGL, endLoc, takeoffSpeedMPS, rateOfClimbMPS, cruiseSpeedMPS, landSpeedMPS, rateOfDescentMPS):

	"""
	Build a flight profile, by profile, it means it has take_off/cruise/loiter(mission)/landing phase, if we want to construct a customized profile, use _buildFlightPath

	Parameters
	----------
	startLoc: list
		Start location, the format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt].
	cruiseAltMetersAGL: float
		Cruise altitude, meters above sea level.
	endLoc: list
		End location, the format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt].
	rateOfClimbMPS: float
		Rate of climb of the aircraft, it is a vertical speed.
	climbGradientInDegree: float
		Climb gradient, the unit is degree, horizontal as zero, minimal value as 0, maximum value as 90 (vertical up).
	cruiseSpeedMPS: float
		Speed of cruise, in the unit of meters/second.
	rateOfDescentMPS: float
		Rate of descent, vertical speed.
	descentGradientInDegree: float
		Descent gradient, the unit is degree, horizontal as zero, minimal value as 0, maximum value as 90 (vertical down).
	
	Return
	------
	flight dataframe
		A dataframe to be interpreted into assignments dataframe
	"""

	# Interpret locations into readable dictionary
	dicStartLoc = loc2Dict(startLoc)
	dicEndLoc = loc2Dict(endLoc)

	# Calculate gradients of climbing and landing
	climbGradientInDegree = math.degrees(math.asin(rateOfClimbMPS / takeoffSpeedMPS))
	descentGradientInDegree = math.degrees(math.asin(rateOfDescentMPS / landSpeedMPS))

	# calculate the ideal takeoff/landing time/ground distance
	idealTakeoffTimeSec = (cruiseAltMetersAGL - dicStartLoc['alt']) / rateOfClimbMPS
	idealTakeoffGroundDistance = (cruiseAltMetersAGL - dicStartLoc['alt']) / math.tan(math.radians(climbGradientInDegree))
	idealLandingTimeSec = (cruiseAltMetersAGL - dicEndLoc['alt']) / rateOfDescentMPS
	idealLandingGroundDistance = (cruiseAltMetersAGL - dicEndLoc['alt']) / math.tan(math.radians(descentGradientInDegree))

	# including start and end, takeoffAt and arrivalAt are not included in here
	markPath = [startLoc, endLoc]

	# Total ground distance
	totalGroundDistance = geoDistancePath2D(markPath)

	flightList = []

	# For the first location, add one row
	flightList.append({
		'lat': dicStartLoc['lat'],
		'lon': dicStartLoc['lon'],
		'altAGL': dicStartLoc['alt'],
		'accuGroundDistance': 0.0,
		'description': "beforeTakeoff",
		'loiterTime': 0.0
		})	

	# Check if distance is enough for taking off and landing
	if (totalGroundDistance > idealTakeoffGroundDistance + idealLandingGroundDistance):
		# if can reach cruise altitude, everything is ideal
		takeoffMileage = geoMileageInPath2D(markPath, idealTakeoffGroundDistance)
		landingMileage = geoMileageInPath2D(markPath, totalGroundDistance - idealLandingGroundDistance)

		# if can cruise, it means we need two locations
		flightList.append({
			'lat': takeoffMileage['loc'][0],
			'lon': takeoffMileage['loc'][1],
			'altAGL': cruiseAltMetersAGL,
			'accuGroundDistance': idealTakeoffGroundDistance,
			'description': "takeoffAtAlt",
			'loiterTime': 0.0
			})
		flightList.append({
			'lat': landingMileage['loc'][0],
			'lon': landingMileage['loc'][1],
			'altAGL': cruiseAltMetersAGL,
			'accuGroundDistance': totalGroundDistance - idealLandingGroundDistance,
			'description': "arrivalAtAlt",
			'loiterTime': 0.0
			})
	else:
		# if can not reach cruise altitude, the profile is "triangle", i.e. the takeoffAt position are the same as arrivalAt position
		deltaAGLTakeoffLanding = dicStartLoc['alt'] - dicEndLoc['alt']
		deltaAGLCruiseTakeoff = (
			(totalGroundDistance - deltaAGLTakeoffLanding / math.tan(math.radians(descentGradientInDegree))) 
			* (math.tan(math.radians(climbGradientInDegree)) + math.tan(math.radians(descentGradientInDegree)))
		)
		deltaAGLCruiseLanding = deltaAGLCruiseTakeoff + deltaAGLTakeoffLanding
		takeoffGroundDistance = deltaAGLCruiseTakeoff / math.tan(math.radians(climbGradientInDegree))
		landingGroundDistance = deltaAGLCruiseLanding / math.tan(math.radians(descentGradientInDegree))

		takeoffMileage = geoMileageInPath2D(markPath, takeoffGroundDistance)

		flightList.append({
			'lat': takeoffMileage['loc'][0],
			'lon': takeoffMileage['loc'][1],
			'altAGL': deltaAGLCruiseTakeoff + dicStartLoc['alt'],
			'accuGroundDistance': takeoffGroundDistance,
			'description': "takeoffAtAlt and arrivalAtAlt",
			'loiterTime': 0.0
			})

	# For the last location, add one row
	flightList.append({
		'lat': dicEndLoc['lat'],
		'lon': dicEndLoc['lon'],
		'altAGL': dicEndLoc['alt'],
		'accuGroundDistance': totalGroundDistance,
		'description': "afterArrival",
		'loiterTime': 0.0
		})

	# Create dataframe
	flightDF = pd.DataFrame(flightList)
	
	# Reorder flight in order
	flightDF = flightDF.sort_values('accuGroundDistance', ascending=True)
	flightDF = flightDF.reset_index(drop=True)

	# Add the 'groundDistance' column to flight dataframe
	groundDistance = [0.0]
	for i in range(1, len(flightDF)):
		groundDistance.append(geoDistance2D((flightDF.iloc[i]['lat'], flightDF.iloc[i]['lon']), (flightDF.iloc[i - 1]['lat'], flightDF.iloc[i - 1]['lon'])))
	flightDF['groundDistance'] = groundDistance

	# Add the 'flightDistance' column to flight dataframe
	flightDistance = [0.0]
	for i in range(1, len(flightDF)):
		deltaHeight = flightDF.iloc[i]['altAGL'] - flightDF.iloc[i - 1]['altAGL']
		groundDistance = flightDF.iloc[i]['groundDistance']
		flightDistance.append(math.sqrt(deltaHeight * deltaHeight + groundDistance * groundDistance))
	flightDF['flightDistance'] = flightDistance

	# Add the 'accuFlightDistance' column to flight dataframe
	accuFlightDistance = [0.0]
	for i in range(1, len(flightDF)):
		accuFlightDistance.append(accuFlightDistance[i - 1] + flightDF.iloc[i]['flightDistance'])
	flightDF['accuFlightDistance'] = accuFlightDistance

	# Add the 'time' column to flight dataframe
	duration = [0.0]
	for i in range(1, len(flightDF)):
		if (flightDF.iloc[i]['description'] == "takeoffAtAlt" or flightDF.iloc[i]['description'] == "takeoffAtAlt and arrivalAtAlt"):
			speed = takeoffSpeedMPS
			duration.append(flightDF.iloc[i]['flightDistance'] / speed)
		elif (flightDF.iloc[i]['description'] == "arrivalAtAlt"):
			speed = cruiseSpeedMPS
			duration.append(flightDF.iloc[i]['flightDistance'] / speed)
		elif(flightDF.iloc[i]['description'] == "afterArrival"):
			speed = landSpeedMPS
			duration.append(flightDF.iloc[i]['flightDistance'] / speed)
	flightDF['timeFromPreviousPosition'] = duration

	# Add the 'accuTime' column to flight dataframe
	startTimeSec = []
	endTimeSec = []
	startTimeSec.append(0.0)
	endTimeSec.append(flightDF.iloc[0]['loiterTime'])
	for i in range(1, len(flightDF)):
		startTimeSec.append(endTimeSec[i - 1] + flightDF.iloc[i]['timeFromPreviousPosition'])
		endTimeSec.append(endTimeSec[i - 1] + flightDF.iloc[i]['timeFromPreviousPosition'] + flightDF.iloc[i]['loiterTime'])
	flightDF['pathStartTimeSec'] = startTimeSec
	flightDF['pathEndTimeSec'] = endTimeSec

	return flightDF

def _buildFlightPath(path, speedMPS):

	"""
	Since _buildFlightProfile is not very flexible, this function gives a more customized method to generate profile, by listing lists of lats, lons and alts.

	Parameters
	----------
	path: list of lists
		A list of locations along with the flight path, in the format of [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt].
	speedMPS: float
		A constant speed, during this path the vehicle will cruise in this speed.

	Return
	------
	flight dataframe
		A dataframe to be interpreted into assignments dataframe.
	"""

	# Flight Profile dataframe
	flightDF = pd.DataFrame(columns=['lat', 'lon', 'altAGL', 'accuGroundDistance', 'description', 'loiterTime', 'groundDistance', 'flightDistance', 'accuFlightDistance', 'timeFromPreviousPosition' ,'pathStartTimeSec', 'pathEndTimeSec'])

	flightList = []
	
	# Check and guarantee that each point in path has 3 dimension
	dicPath = locs2Dict(path)

	# Add flight path one coordinate at a time
	accuGroundDistance = 0
	accuFlightDistance = 0
	accuPathTime = 0
	for i in range(len(path)):
		# Calculate fields for flight dataframe
		if i > 0:
			groundDistance = geoDistance2D(path[i - 1], path[i])
			deltaAGL = dicPath[i]['alt'] - dicPath[i - 1]['alt']
			flightDistance = math.sqrt(groundDistance * groundDistance + deltaAGL * deltaAGL)
		else:
			groundDistance = 0
			flightDistance = 0
		accuGroundDistance += groundDistance
		accuFlightDistance += flightDistance
		timeFromPreviousPosition = accuFlightDistance / speedMPS
		accuPathTime += timeFromPreviousPosition

		# And one way point to the flight path
		flightList.append({
			'lat': dicPath[i]['lat'],
			'lon': dicPath[i]['lon'],
			'altAGL': dicPath[i]['alt'],
			'accuGroundDistance': accuGroundDistance,
			'description': "Waypoint",
			'loiterTime': 0.0,
			'groundDistance': groundDistance, 
			'flightDistance': flightDistance, 
			'accuFlightDistance': accuFlightDistance, 
			'timeFromPreviousPosition': accuFlightDistance / speedMPS,
			'pathStartTimeSec': accuPathTime, 
			'pathEndTimeSec': accuPathTime
			})

	if (len(flightDF) == 0):
		flightDF = pd.DataFrame(flightList, columns=flightDF.columns)
	else:
		flightDF = pd.concat([flightDF, pd.DataFrame(flightList)], ignore_index=True)
	
	return flightDF

def getTimeDistFromFlight(flight):
	"""
	Given a flight profile, returns the total time, ground distance and flight distance of that flight profile

	Parameters
	----------
	flight: flight dataframe
		A flight profile to be calculated.

	Returns
	-------
	time: float
		Total time of this flight.
	groundDistance: float
		Total ground distance of this flight.
	flightDistance: float
		Total flight distance of this flight.
	"""

	time = flight['pathEndTimeSec'].max()
	groundDistance = flight['accuGroundDistance'].max()
	flightDistance = flight['accuFlightDistance'].max()
	return [time, groundDistance, flightDistance]

def addLoiterTimeToFlight(flight, loiterPosition, loiterTime):
	"""
	Given a flight profile, loiter position and loiter time, return a flight profile with loiter

	Parameters
	----------
	flight: flight dataframe
		The flight profile to add loiter action.
	loiterPosition: string
		A string to specify where are we going to loiter.
	loiterTime: float
		The amount of loiter time that we are going to ADD to this position.

	Return
	------
	flight dataframe
		A new flight dataframe that includes the newly added loiter time.
	"""

	flightWithLoiter = flight.copy()

	try:
		loiterPosition = loiterPosition.lower()
	except:
		pass

	if (loiterPosition == "beforeDeparture".lower()):
		flightWithLoiter.loc[flightWithLoiter['description'] == "beforeDeparture", 'loiterTime'] += loiterTime
		flightWithLoiter.loc[flightWithLoiter['description'] == "beforeTakeoff", 'loiterTime'] += loiterTime

	elif (loiterPosition == "departAtAlt".lower()):
		flightWithLoiter.loc[flightWithLoiter['description'] == "takeoffAtAlt", 'loiterTime'] += loiterTime
		flightWithLoiter.loc[flightWithLoiter['description'] == "takeoffAtAlt and arrivalAtAlt", 'loiterTime'] += loiterTime

	elif (loiterPosition == "arrivalAtAlt".lower()):
		flightWithLoiter.loc[flightWithLoiter['description'] == "arrivalAtAlt", 'loiterTime'] += loiterTime
		flightWithLoiter.loc[flightWithLoiter['description'] == "takeoffAtAlt and arrivalAtAlt", 'loiterTime'] += loiterTime

	elif (loiterPosition == "afterArrival".lower()):
		flightWithLoiter.loc[flightWithLoiter['description'] == "afterArrival", 'loiterTime'] += loiterTime
		flightWithLoiter.loc[flightWithLoiter['description'] == "afterLand", 'loiterTime'] += loiterTime

	# Recalculate 'pathStartTimeSec' and 'pathEndTimeSec' columns
	lstStartTimeSec = flightWithLoiter['pathStartTimeSec'].tolist()
	lstEndTimeSec = flightWithLoiter['pathEndTimeSec'].tolist()
	for i in range(1, len(flightWithLoiter)):
		lstStartTimeSec[i] = lstEndTimeSec[i - 1] + flightWithLoiter.iloc[i]['timeFromPreviousPosition']
		lstEndTimeSec[i] = lstEndTimeSec[i - 1] + flightWithLoiter.iloc[i]['timeFromPreviousPosition'] + flightWithLoiter.iloc[i]['loiterTime']
	flightWithLoiter['pathStartTimeSec'] = lstStartTimeSec
	flightWithLoiter['pathEndTimeSec'] = lstEndTimeSec

	return flightWithLoiter
