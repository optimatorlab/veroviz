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

def getDHMS(seconds):
    '''
    Split a given number of seconds into integer
    days, hours, minutes, and seconds.
    This function is used by `fmtDHMS()`, `fmtHMS()`, ...
    which format the time labels for createGantt().
    '''
    
    seconds  = int(seconds)
    
    days     = int(seconds / (60*60*24))
    seconds -= (60*60*24) * days
    
    hours    = int(seconds / (60*60))
    seconds -= (60*60) * hours
    
    minutes  = int(seconds / 60)
    seconds -= 60 * minutes
    
    return [days, hours, minutes, seconds]
    
def fmtDHMS(seconds, pos):
    # Used by createGantt()
    [days, hours, minutes, seconds] = getDHMS(seconds)
    return "%d:%02d:%02d:%02d" % (days, hours, minutes, seconds)

def fmtHMS(seconds, pos):
    # Used by createGantt()
    [days, hours, minutes, seconds] = getDHMS(seconds)        
    return "%02d:%02d:%02d" % (hours, minutes, seconds)

def fmtMS(seconds, pos):
    # Used by createGantt()
    [days, hours, minutes, seconds] = getDHMS(seconds)
    return "%02d:%02d" % (minutes, seconds)

def fmtD(seconds, pos):
    # Used by createGantt()
    days = seconds / (60.0 * 60.0 * 24.0)
    return "%.1f" % (days)

def fmtH(seconds, pos):
    # Used by createGantt()
    hours = seconds / (60.0 * 60.0)
    return "%.1f" % (hours)

def fmtM(seconds, pos):
    # Used by createGantt()
    minutes = seconds / 60.0
    return "%.1f" % (minutes)

def fmtS(seconds, pos):
    # Used by createGantt()    
    return "%d" % (seconds)
    
def expandCesiumColor(colorString):
    '''
    Returns None or Cesium.Color.COLORNAME
    '''
    if (colorString is None):
        return None
    
    # Remove any spaces
    colorString.replace(" ", "")
    
    if ('.' in colorString):
        parts = colorString.split('.')
        # If correct, parts should have 3 elements
        if (len(parts) == 3):
            return '{}.{}.{}'.format(parts[0].capitalize(), parts[1].capitalize(), parts[2].upper())
        else:
            return(colorString)
    else:
        return 'Cesium.Color.{}'.format(colorString.upper())
        
def stripCesiumColor(colorString):
    '''
    Returns None or colorname
    '''
    if (colorString is None):
        return None
    
    # Remove any spaces
    colorString.replace(" ", "")
    
    if ('.' in colorString):
        parts = colorString.split('.')
        # If correct, parts should have 3 elements
        if (len(parts) == 3):
            return '{}'.format(parts[2].lower())
        else:
            return(colorString)
    else:
        return '{}'.format(colorString.lower())
        
def splitLeafletCustomIconType(iconType):
	'''
	If iconPrefix is 'custom', iconType is expected to be a string of the form '[marker size]-[font color]-[font size]' or '[marker size]-none'.  This function returns a list of size 3, containing the 3 elements separated by '-'.  Missing elements default to be None.
	'''	
	if (iconType is None):
		return [None, None, None]
	
	# Ensure we're working with a string
	iconType = str(iconType)

	try:
		iconType = iconType.lower()
	except:
		pass
		
	# Remove any spaces
	iconType.replace(" ", "")

	if ('-' in iconType):
		parts = iconType.split('-')

		# First element is supposed to be a number (marker radius)
		try:
			parts[0] = float(parts[0])
		except:
			pass	

		# Second element should be either a string or None
		if (len(parts) >= 2):
			if (parts[1] == 'none'):
				parts[1] = None

		# Last element should be either a number or None
		if (len(parts) >= 3):
			if (parts[2] == 'none'):
				parts[2] = None
			else:
				try:
					parts[2] = float(parts[2])
				except:
					pass
		else:
			parts.append(None)	

		return parts[0:3]	
	else:
		try:
			iconType = float(iconType)
		except:
			pass
			
		return [iconType, None, None]

def bitFieldDecomp(value, dictionary):
    '''
    This function decomposes a "bitField" to find all values from a dictionary's keys
    that sum to "value".  For example:
        orsWaycategoryDict = {0: 'No category',
                              1: 'Highway',
                              2: 'Steps',
                              4: 'Ferry',
                              8: 'Unpaved road',
                              16: 'Track',
                              32: 'Tunnel',
                              64: 'Paved road',
                              128: 'Ford'}
        bitFieldDecomp(97, orsWaycategoryDict) returns 'Paved road, Tunnel, Highway'
    '''
    
    # value must be a number
    try:
        val = float(value)
    except:
        return None

    if (float(val).is_integer() == False):
        return None

    returnArray = []

    if (val == 0):
        return dictionary[val] if val in dictionary else None 
    while val > 0:
        x = max([k for k in orsWaycategoryDict.keys() if k <= val])
        returnArray.append(dictionary[x]) 
        val -= x


    if (len(returnArray) == 0):
        return None
    else:
        return ', '.join(returnArray)
    