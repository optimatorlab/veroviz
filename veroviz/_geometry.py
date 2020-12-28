from veroviz._common import *

#####################################################################
# General Naming Rules for Input Parameters
# loc  - Location.  A coordinate in the form of [lat, lon].
#        If the location is specific, name it with xxxLoc 
#        (e.g., startLoc, endLoc, etc.)
# line - Line.  Two locations in the form of [[lat1, lon1], [lat2, lon2]].
# path - Path.  A list of locs, in [[lat1, lon1], [lat2, lon2], [lat3, lon3], ...]
# poly - Polygon.  A sequence of locations, 
#        assuming solid and closed, in [[lat1, lon1], [lat2, lon2], [lat3, lon3], ...]
#####################################################################

def geoIsPointInPoly(loc, poly):
	"""
	Determine if a point is inside a polygon.  Points that are along the perimeter of the polygon (including vertices) are considered to be "inside".

	Parameters
	----------
	loc: list
		The coordinate of the point, in [lat, lon] format
	poly: list of lists
		The polygon to check if the point is inside, in [[lat, lon], [lat, lon], ..., [lat, lon]] format
	Returns
	-------
	boolean
		The point is inside the polygon or not
	"""

	if (loc in poly):
		return True

	x = loc[1]
	y = loc[0]
	inside = False
	j = len(poly) - 1
	for i in range(0,len(poly)):
		# Check if pt is in interior:
		xi = poly[i][1]
		yi = poly[i][0]
		xj = poly[j][1]
		yj = poly[j][0]
		intersect = (yi > y) != (yj > y)
		if (intersect):
			intersect = (x < (xj - xi) * (y - yi) / float(yj - yi) + xi)
		if (intersect):
			inside = not inside
		j = i
		
	return inside

def geoIsPathInPoly(path, poly):
	"""
	Determine if a given path crosses with a polygon

	Parameters
	----------
	path: list of lists
		A list of coordinates in the form of [[lat, lon], [lat, lon], ..., [lat, lon]], it will be considered as open polyline
	poly: list of lists
		A list of coordinates in the form of [[lat, lon], [lat, lon], ..., [lat, lon]], it will be considered as closed polygon
	
	Returns
	-------
	boolean
		True if the path lies entirely in the polygon, false if at least one point of path is not inside polygon

	"""

	insideFlag = True
	for i in range(len(path)):
		if (not geoIsPointInPoly(path[i], poly)):
			insideFlag = False
			break

	if (insideFlag and geoIsPathCrossPoly(path, poly)):
		insideFlag = False

	return insideFlag 

def geoIsPathCrossPoly(path, poly):
	"""
	Determine if a given path crosses with a polygon

	Parameters
	----------
	path: list of lists
		A list of coordinates in the form of [[lat, lon], [lat, lon], ..., [lat, lon]], it will be considered as open polyline
	poly: list of lists
		A list of coordinates in the form of [[lat, lon], [lat, lon], ..., [lat, lon]], it will be considered as closed polygon

	Returns
	-------
	boolean
		True if the path have intersection with the polygon, false if no intersection

	"""

	crossFlag = False
	lstLine = []

	for i in range(1, len(path)):
		lstLine.append([path[i - 1], path[i]])

	for i in range(len(lstLine)):
		if (geoIsLineCrossPoly(lstLine[i], poly)):
			crossFlag = True
			break

	return crossFlag

def geoIsLineCrossPoly(line, poly):
	"""
	Determine if a given line crosses with a polygon

	Parameters
	----------
	line: list of lists
		The line to check if it is crossing polygon, in [[startLat, startLon], [endLat, endLon]] format
	poly: list of lists
		The polygon to check if the point is inside, in [[lat, lon], [lat, lon], ..., [lat, lon]] format

	Returns
	-------
	boolean
		True if the line has intersection with the polygon, false if no intersection

	"""
	crossFlag = False
	lstLine = []

	startPt = [line[0][0], line[0][1]]
	endPt = [line[1][0], line[1][1]]

	for i in range(1, len(poly)):
		lstLine.append([poly[i - 1], poly[i]])
	lstLine.append([poly[len(poly) - 1], poly[0]])

	for i in range(len(lstLine)):
		if not (startPt == lstLine[i][0] or endPt == lstLine[i][1] or startPt == lstLine[i][1] or endPt == lstLine[i][0]):
			if (geoIsLineCrossLine([startPt, endPt], lstLine[i])):
				crossFlag = True
				break

	return crossFlag

def geoIsLineCrossLine(line1, line2):
	"""
	Determine if a given line crosses with another given line

	Parameters
	----------
	line1: list of lists
		The line to check if it is crossing another line, in [[startLat, startLon], [endLat, endLon]] format
	line2: list of lists
		The other line to check if it is crossing another line, in [[startLat, startLon], [endLat, endLon]] format

	Returns
	-------
	boolean
		True if the line has intersection with another line, false if no intersection

	"""

	intersect = False

	[p, q] = line1
	[u, w] = line2

	loopPQU = geoIsClockWise(p, q, u)
	loopPQW = geoIsClockWise(p, q, w)
	loopUWP = geoIsClockWise(u, w, p)
	loopUWQ = geoIsClockWise(u, w, q)

	if (loopPQU != loopPQW and loopUWP != loopUWQ):
		intersect = True

	if (loopPQU != loopPQW and loopUWP == loopUWQ):
		if (geoIsOnSegment(p, line2) or geoIsOnSegment(q, line2)):
			intersect = True

	if (loopPQU == loopPQW and loopUWP != loopUWQ):
		if (geoIsOnSegment(u, line1) or geoIsOnSegment(w, line1)):
			intersect = True

	if (loopPQU == loopPQW and loopUWP == loopUWQ):
		if (geoIsOnSegment(u, line1) or geoIsOnSegment(w, line1) or geoIsOnSegment(p, line2) or geoIsOnSegment(q, line2)):
			intersect = True

	return intersect

def geoIsClockWise(loc1, loc2, loc3):
	"""
	Determine if three locs are clockwised

	Parameters
	----------
	loc1: list
		First location, in [lat, lon] format
	loc2: list
		Second location, in [lat, lon] format
	loc3: list
		Third location, in [lat, lon] format

	Return
	------
	boolean
		True if three given locs are clockwised, false if three given locs are collinear or counter-clockwised

	"""

	[x1, y1] = [loc1[0], loc1[1]]
	[x2, y2] = [loc2[0], loc2[1]]
	[x3, y3] = [loc3[0], loc3[1]]

	val = (x2 * y3 + x3 * y1 + x1 * y2) - (x2 * y1 + x3 * y2 + x1 * y3)

	if (val >= 0):
		clockWise = True
	else:
		clockWise = False

	return clockWise

def geoIsOnSegment(loc, line):
	"""
	Determine if loc is on line segment

	Parameters
	----------
	loc: list
		First location, in [lat, lon] format
	line: list of lists
		Line segment, in [[lat,lon], [lat,lon]] format

	Return
	------
	boolean
		True if loc is on line segment, including two edge vertices

	"""

	[y1, x1] = [line[0][0], line[0][1]]
	[y2, x2] = [loc[0], loc[1]]
	[y3, x3] = [line[1][0], line[1][1]]

	val = (x2 * y3 + x3 * y1 + x1 * y2) - (x2 * y1 + x3 * y2 + x1 * y3)
	if (val == 0 and x2 >= min(x1, x3) and x2 <= max(x1, x3) and y2 >= min(y1, y3) and y2 <= max(y1, y3)):
		onSegment = True
	else:
		onSegment = False

	return onSegment

def geoIsPassLine(loc, line, tolerance):
	'''
	Determine if any point along a line is within tolerance meters of a stationary point.
	(did our line pass by the target?)

	Parameters
	----------
	loc: list
		The stationary point to be tested if it has been passed, in [lat, lon] format
	line: list of lists
		A line segment to be tested if it is passing a stationary point, in [[lat, lon], [lat, lon]] format
	tolerance: float
		How close the line to stationary location is considered as passed
	
	Returns
	-------
	boolean
		Whether or not the line passes the point
	'''

	d = geoMinDistLoc2Line(loc, line)
	if (d <= tolerance):
		passFlag = True
	else:
		passFlag = False
		
	return passFlag

def geoIsPassPath(loc, path, tolerance):
	'''
	Determine if any point along a path is within tolerance meters of a stationary point.
	(did our path pass by the target?)

	Parameters
	----------
	loc: list
		The stationary point to be tested if it has been passed, in [lat, lon] format
	path: list of lists
		A list of coordinates in the form of [[lat, lon], [lat, lon], ..., [lat, lon]], it will be considered as open polyline
	tolerance: float
		How close the path to stationary location is considered as passed
	
	Returns
	-------
	boolean
		Whether or not the path passes th point
	'''

	d = geoMinDistLoc2Path(loc, path)
	if (d <= tolerance):
		passFlag = True
	else:
		passFlag = False
		
	return passFlag

def geoMinDistLoc2Path(loc, path):
	"""
	Calculate the minimum distance in [meters] from a single stationary location (target) to any point along a path.

	Parameters
	----------
	loc: list
		The coordinate of stationary location, in [lat, lon] format
	path: list of lists
		The path to calculate the distance

	Returns
	-------
	float
		The minimum distance between stationary location and given line
	"""

	# THIS IS NOT THE OPTIMAL WAY! DISTANCE BETWEEN WAYPOINTS AND STATIONARY LOC HAVE BEEN CALCULATED TWICE.
	lstLine = []
	for i in range(1, len(path)):
		lstLine.append([path[i - 1], path[i]])

	distMeters = geoMinDistLoc2Line(loc, lstLine[0])
	for i in range(len(lstLine)):
		tmpDistMeters = geoMinDistLoc2Line(loc, lstLine[i])
		if (distMeters > tmpDistMeters):
			distMeters = tmpDistMeters

	return distMeters

def geoMinDistLoc2Line(loc, line):
	"""
	Calculate the minimum distance in [meters] from a single stationary location (target) to any point along a line segment.

	Note
	----
	Now only works in a flat 2D space

	Parameters
	----------
	loc: list
		The coordinate of stationary location, in [lat, lon] format
	line: list of lists
		The line segment to calculate the distance

	Returns
	-------
	float
		The minimum distance between stationary location and given line
	"""

	# The line is denoted as AB, the stationary location is denoted by S
	locA = line[0]
	locB = line[1]
	locS = loc

	# Check if the loc is on line, if so the distance is 0
	if (geoIsOnSegment(loc, line)):
		return 0.0

	# Vectors start from A
	vecAS = [float(locS[0] - locA[0]), float(locS[1] - locA[1])]
	vecAB = [float(locB[0] - locA[0]), float(locB[1] - locA[1])]

	# Vectors start from B
	vecBS = [float(locS[0] - locB[0]), float(locS[1] - locB[1])]
	vecBA = [float(locA[0] - locB[0]), float(locA[1] - locB[1])]

	# cos value for A angle and B angle
	cosSAB = geoFindCos(vecAS, vecAB)
	cosSBA = geoFindCos(vecBS, vecBA)

	# if both angles are sharp, the closest point will be in the line, otherwise the closest point is at the edge
	if (cosSAB >= 0 and cosSBA >= 0):
		areaSAB = geoAreaOfTriangle(locS, locA, locB)
		bottom = geoDistance2D(locA, locB)
		height = 2 * areaSAB / bottom
		distMeters = height
	else:
		distAS = geoDistance2D(locS, locA)
		distBS = geoDistance2D(locS, locB)
		distMeters = min(distAS, distBS)

	return distMeters

def geoFindCos(vec1, vec2):
	cosAngle = (vec1[0] * vec2[0] + vec1[1] * vec2[1]) / (math.sqrt(vec1[0] * vec1[0] + vec1[1] * vec1[1]) * math.sqrt(vec2[0] * vec2[0] + vec2[1] * vec2[1]))
	return cosAngle
  
def geoPointInDistance2D(loc, direction, distMeters):
	"""
	Generate a GPS coordinate given a current coordinate, a direction and a distance

	Parameters
	----------
	loc: list
		The coordinate of the current coordinate, in [lat, lon] format
	direction: float
		The direction, range [0, 360] in degree, 0 means North, 90 means East
	distMeters: float
		The distance between current point and the point we needs

	Returns
	-------
	list
		A location in distance with given direction, in [lat, lon] form.
	"""
	newLoc = list(geopy.distance.distance(meters=distMeters).destination(point=loc, bearing=direction))

	return newLoc

def geoDistance2D(loc1, loc2):
	"""
	Distance, in meters, between two locations in 2D

	Parameters
	----------
	loc1: list
		First location, in [lat, lon]
	loc2: list
		Second location, in [lat, lon]
	
	Return
	------
	float
		Distance, in meters, between two locations.
	"""
	
	distMeters = geopy.distance.distance(loc1[0:2], loc2[0:2]).meters

	return distMeters

def geoDistance3D(loc1, loc2):
	"""
	Distance, in meters, between two locations in 3D

	Parameters
	----------
	loc1: list
		First location, in [lat, lon, alt]
	loc2: list
		Second location, in [lat, lon, alt]
	
	Return
	------
	float
		Distance, in meters, between two locations.
	"""

	# FIXME! For now we assume the earth is flat
	groundDist = geopy.distance.distance(loc1[0:2], loc2[0:2]).meters
	if (len(loc1)==3):
		alt1 = loc1[2]
	else:
		alt1 = 0
	if (len(loc2)==3):
		alt2 = loc2[2]
	else:
		alt2 = 0
	deltaAGL = alt1 - alt2

	distMeters = math.sqrt(groundDist * groundDist + deltaAGL * deltaAGL)

	return distMeters

def geoAreaOfTriangle(loc1, loc2, loc3):
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

def geoAreaOfPolygon(poly):
	"""
	Calculates the area of a polygon. Assumes a solid, but not necessarily convex, shape.

	Parameters
	----------
	poly: list of lists
		A list of lat/lon defines the boundary, in the form of [[lat, lon], [lat, lon], ... , [lat, lon]]

	Return
	------
	float
		Area of polygon
	"""

	# poly must be a list of [lat, lon] lists.  Altitude cannot be included,
	# as it will break tripy.earclip.
	cleanPoly = []
	for i in poly:
		# Just add [lat, lon]
		cleanPoly.append([i[0], i[1]])
		
	polyArea = 0
	
	# Use polygon triangulation to cut the bounding region into a list of triangles, calculate the area of each triangle
	lstTriangle = tripy.earclip(cleanPoly)
	lstArea = []
	for i in range(len(lstTriangle)):
		lstArea.append(geoAreaOfTriangle(lstTriangle[i][0], lstTriangle[i][1], lstTriangle[i][2]))

	for i in lstArea:
		polyArea = i + polyArea

	return polyArea

def geoDistancePath2D(path):
	"""
	Given a list of lats and lons, calculate the total distance along the path

	Parameters
	----------
	path: list of lists
		A list of coordinates that form a path. In format of [[lat, lon], [lat, lon], ...]

	Return
	------
	float
		Total length of the path.
	"""

	dist = 0
	for i in range(0, len(path) - 1):
		dist += geoDistance2D([path[i]], path[i + 1])

	return dist

def geoClosestPointLoc2Line(loc, line):
	"""
	Find the point along a given line that is closest to a given location.

	Parameters
	----------
	loc: list
		The coordinate of the current coordinate, in [lat, lon, alt] format
	line: list of locations
		A list of two coordinates in the form of [lat, lon]
	Returns
	-------
	minLoc: list specifying a location, in [lat, lon] format.
	"""
	# The line is denoted as AB, the stationary location is denoted by S
	locA = line[0]
	locB = line[1]
	locS = loc
	minLoc = None

	# Check if the loc is on line, if so return the location
	if (geoIsOnSegment(loc, line)):
		minLoc = locS
	else:
		# Vectors start from A
		vecAS = [float(locS[0] - locA[0]), float(locS[1] - locA[1])]
		vecAB = [float(locB[0] - locA[0]), float(locB[1] - locA[1])]

		area = geoAreaOfTriangle(locA, locB, locS)
		h = 2 * area / geoDistance2D(locA, locB)
		lAS = geoDistance2D(locA, locS)
		dist = math.sqrt(lAS * lAS - h * h)

		cosSAB = geoFindCos(vecAS, vecAB)

		if cosSAB >= 0:
			tmpLocDict = geoMileageInPath2D([locA, locB], dist)
			minLoc = tmpLocDict['loc']
		else:
			minLoc = locA

	return minLoc
	
def geoMileageInPath2D(path, mileageInMeters):
	"""
	Given a path in 2D, and a mileage, find the GPS coordinate and the coordinates of source/target of the segment that coordinate at.

	Parameters
	----------
	path: list of lists
		The path that traveled on. In format of [[lat, lon], [lat, lon], ...]
	mileageInMeters: float
		The mileage start from the origin location

	Returns
	-------
	dictionary with the following 5 keys
		'loc': List, of the form [lat, lon], indicating the location at that mileage.
		'inPathFlag': Boolean. If at that mileage it still stays in the path, return true, else return false.
		'bearingInDegree': float.  Heading at that mileage.
		'preLoc': List, of the form [lat, lon], indicating the previous location on the path.
		'nextLoc': List, of the form [lat, lon], indicating the next location on the path.
	"""

	inPathFlag = False
	accuDistance = 0
	preLoc = []
	nextLoc = []

	for i in range(0, len(path) - 1):
		d = geoDistance2D(path[i], path[i + 1])
		accuDistance += d
		if (accuDistance > mileageInMeters):
			preLoc = path[i]
			nextLoc = path[i + 1]
			inPathFlag = True
			break

	if (inPathFlag == False):
		loc = path[-1]
		preLoc = path[-2]
		nextLoc = path[-1]
	else:
		remainDist = accuDistance - mileageInMeters
		segDist = geoDistance2D(preLoc, nextLoc)
		lat = nextLoc[0] + (remainDist / segDist) * (preLoc[0] - nextLoc[0])
		lon = nextLoc[1] + (remainDist / segDist) * (preLoc[1] - nextLoc[1])
		loc = [lat, lon]

	bearingInDegree = geoGetHeading(preLoc, nextLoc)

	return {
		'loc': loc,
		'inPathFlag': inPathFlag,
		'bearingInDegree': bearingInDegree,
		'preLoc': preLoc,
		'nextLoc': nextLoc
	}

def geoGetHeading(currentLoc, goalLoc):
	"""
	Given current location and a goal location, calculate the heading.  North is 0-degrees, east is 90-degrees, south is 180-degrees, west is 270-degrees.

	Parameters
	----------
	currentLoc: list
		The [lat, lon] of current location
	goalLoc: list
		The [lat, lon] of goal location


	Return
	------
	float
		Heading at current location towards goal location in degrees.
	"""

	radPreLat = np.radians(currentLoc[0])
	radNextLat = np.radians(goalLoc[0])
	deltaLon = np.radians(goalLoc[1] - currentLoc[1])
	x = np.sin(deltaLon) * np.cos(radNextLat)
	y = (np.cos(radPreLat) * np.sin(radNextLat) - (np.sin(radPreLat) * np.cos(radNextLat) * np.cos(deltaLon)))
	bearingInDegree = np.degrees(np.arctan2(x, y))
	if bearingInDegree < 0:
		bearingInDegree += 360

	return bearingInDegree
	