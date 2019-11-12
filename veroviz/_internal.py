from veroviz._common import *
from veroviz._geometry import geoDistance2D

def distributeTimeDist(path, totalTime):
	"""
	This function gives time stamps for a series of coordinates, given a start time and total time, used in shapepoint calculating. The distribution is made based on the euclidean distance between neigboring coordinates - they are very close to each other

	Parameters
	----------
	path: list of lists
		A path that consist a list of locations as shapepoints/waypoints, in the form of [[lat, lon], [lat, lon], ..., [lat, lon]], it will be considered as open polyline.
	totalTime: float
		Required, total time to be distributed

	Returns
	-------
	timeSecs: list
		A list of time stamps, those time stamps are not accumulative in seconds.
	distMeters: list
		Distance between neighboring coordinates in meters.
	"""

	timeSecs = []
	distMeters = []
	totalDistMeters = 0
	distMeters.append(0)
	timeSecs.append(0)
	for i in range(1, len(path)):
		d = geoDistance2D(path[i - 1], path[i])
		distMeters.append(d)
		totalDistMeters += d

	for i in range(1, len(path)):
		timeSecs.append(totalTime * float(distMeters[i]) / float(totalDistMeters))

	return [timeSecs, distMeters]

def randomPick(coefficients):
	"""
	Given a list of coefficients, randomly return an index according to that coefficient. e.g., [10, 20, 30, 20, 20] will have 30% chances returns '2' (the third index)

	Parameters
	----------
	coefficients: list
		A list of float indicates the relative chances to pick index

	Returns
	-------
	int
		The index that randomly chosen
	"""

	totalSum = sum(coefficients)
	tmpSum = 0
	rnd = np.random.uniform(0, totalSum)
	index = 0
	for i in range(len(coefficients)):
		tmpSum += coefficients[i]
		if rnd <= tmpSum:
			index = i
			break

	return index

def loc2Dict(loc):
	"""
	Convert a loc into a dictionary, for the consideration of maintainability.

	Parameters
	----------
	loc: list
		A location, in format of [lat, lon] or [lat, lon, alt]

	Return
	------
	dictionary
		A dictionary of location
	"""
	if (len(loc) == 2):
		locDict = {
			'lat': loc[0],
			'lon': loc[1],
			'alt': 0
		}
	elif (len(loc) == 3):
		locDict = {
			'lat': loc[0],
			'lon': loc[1],
			'alt': loc[2]
		}
	else:
		return

	return locDict

def locs2Dict(locs):
	"""
	Convert a list of locs into dictionaries, for the consideration of maintainability.

	Parameters
	----------
	locs: list of lists
		A list of location, in format of [[lat, lon], [lat, lon], ...] or [[lat, lon, alt], [lat, lon, alt], ...]

	Return
	------
	dictionary
		A dictionary of location
	"""

	locsDict = []
	for i in range(len(locs)):
		locsDict.append(loc2Dict(locs[i]))

	return locsDict

def areaOfTriangle(loc1, loc2, loc3):
	"""
	Calculates the area of triangle defined by three locations

	Parameters
	----------
	loc1: list
		First location
	loc2: list
		Second location
	loc3: list
		Third location

	Return
	------
	float
		Area of triangle
	"""

	# Using Heron's Formula
	a = geoDistance2D(loc1, loc2)
	b = geoDistance2D(loc2, loc3)
	c = geoDistance2D(loc1, loc3)

	s = (a + b + c) / 2
	area = math.sqrt(s * (s - a) * (s - b) * (s - c))

	return area

def delHeadSlash(originStr):
	if (originStr is not None):
		firstChar = originStr[:1]
		if (firstChar == "/"):
			newStr = originStr[1:]
		else:
			newStr = originStr
	else:
		newStr = originStr

	return newStr

def delTailSlash(originStr):
	if (originStr is not None):
		tailChar = originStr[-1]
		if (tailChar == "/"):
			newStr = originStr[:-1]
		else:
			newStr = originStr
	else:
		newStr = originStr

	return newStr

def addHeadSlash(originStr):
	if (originStr is not None):
		firstChar = originStr[:1]
		if (firstChar != "/"):
			originStr = '/' + originStr
		
	return originStr

def addTailSlash(originStr):
	if (originStr is not None):
		tailChar = originStr[-1]
		if (tailChar != "/"):
			newStr = originStr + "/"
		else:
			newStr = originStr
	else:
		newStr = originStr

	return newStr

def replaceBackslashToSlash(path):
	if (path is not None):
		path = path.replace("\\", "/")
	return path
