from veroviz._common import *
from veroviz._internal import locs2Dict
from veroviz._internal import loc2Dict
from veroviz._geometry import geoDistance2D

def pgrGetSnapToRoadLatLon(gid, loc, databaseName):
	"""
	A function to get snapped latlng for one coordinate using pgRouting

	Parameters
	----------
	gid: int
		The gid of the street in pgRouting database
	loc: list
		The location to be snapped to road
	databaseName: string, Require
		If you are hosting a data provider on your local machine (e.g., pgRouting), you'll need to specify the name of the local database.

	Returns
	-------
	list
		A snapped locations in the format of [lat, lon], notice that this function will lost the info of altitude of the location.
	"""

	conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (
		databaseName, 
		config['VRV_SETTING_PGROUTING_USERNAME'], 
		config['VRV_SETTING_PGROUTING_HOST'], 
		config['VRV_SETTING_PGROUTING_PASSWORD']))
	cur = conn.cursor()

	# For maintainability
	dicLoc = loc2Dict(loc)

	sqlCommand  = " select ST_X(point), ST_Y(point)"
	sqlCommand += " from ("
	sqlCommand += " 	select ST_ClosestPoint("
	sqlCommand += " 		ST_GeomFromEWKT(CONCAT('SRID=4326; LINESTRING(',x1,' ',y1,', ',x2,' ',y2,')')),"
	sqlCommand += " 		ST_GeomFromEWKT('SRID=4326;POINT(%s %s)')) as point" % (dicLoc['lon'], dicLoc['lat']) # Be very careful about lon and lat
	sqlCommand += " 	from ways"
	sqlCommand += " 	where gid=%s" % (gid)
	sqlCommand += " ) a;"
	cur.execute(sqlCommand)
	row = cur.fetchone()
	snapLoc = [row[1], row[0]]

	conn.close()

	return snapLoc

def pgrGetNearestStreet(loc, databaseName):
	"""
	A function to return the details of the nearest street given a known coordinate

	Parameters
	----------
	loc: list
		The locationi that trying to find the nearest street of
	databaseName: string, Require
		If you are hosting a data provider on your local machine (e.g., pgRouting), you'll need to specify the name of the local database.

	Returns
	-------
	gid: int
		gid from Ways table, identifier for street
	sourceVid: int
		sourceVid from Ways table, identifier for source vertice
	targetVid: int
		targetVid from Ways table, identifier for target vertice
	sourceLat: int
		sourceLat from Ways table, latitude for source vertice
	sourceLon: int
		sourceLon from Ways table, longitude for source vertice
	targetLat: int
		targetLat from Ways table, latitude for target vertice
	targetLon: int
		targetLon from Ways table, longitude for target vertice
	cost_s: int
		cost_s from Ways table, time needs from source to target
	reverse_cost_s: int
		reverse_cost_s from Ways table, time needs from target to source
	one_way: int
		one_way from Ways table, indicate if it is one way street
	"""
	conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (
		databaseName, 
		config['VRV_SETTING_PGROUTING_USERNAME'], 
		config['VRV_SETTING_PGROUTING_HOST'], 
		config['VRV_SETTING_PGROUTING_PASSWORD']))
	cur = conn.cursor()

	# For maintainability
	dicLoc = loc2Dict(loc)

	try:
		sqlCommand  = " select gid, source, target, y1, x1, y2, x2, cost_s, reverse_cost_s, one_way"
		sqlCommand += " from "
		sqlCommand += " 	ways"
		sqlCommand += "	where"
		sqlCommand += "		x1 >= %s - 0.01 and x1 <= %s + 0.01" % (dicLoc['lon'], dicLoc['lon']) # Eliminate most of the ways there
		sqlCommand += " order by"
		sqlCommand += " 	ST_Distance("
		sqlCommand += "			ST_GeogFromText('SRID=4326; POINT(%s %s)')," % (dicLoc['lon'], dicLoc['lat'])  # Be very careful about lon and lat
		sqlCommand += "			ST_GeogFromText(CONCAT('SRID=4326; LINESTRING(',x1,' ',y1,', ',x2,' ',y2,')')))"
		sqlCommand += "	limit 1;"
		cur.execute(sqlCommand)
		row = cur.fetchone()
		street = {
			"gid" : int(row[0]),
			"source" : int(row[1]),
			"target" : int(row[2]),
			"sourceLoc" : [row[3], row[4]],
			"targetLoc" : [row[5], row[6]],
			"cost_s" : row[7],
			"reverse_cost_s" : row[8],
			"one_way" : row[9]
		}

	except:
		sqlCommand  = " select gid, source, target, y1, x1, y2, x2, length_m, cost_s, reverse_cost_s, one_way"
		sqlCommand += " from "
		sqlCommand += " 	ways"
		sqlCommand += " order by"
		sqlCommand += " 	ST_Distance("
		sqlCommand += "			ST_GeogFromText('SRID=4326; POINT(%s %s)')," % (dicLoc['lon'], dicLoc['lat'])  # Be very careful about lon and lat
		sqlCommand += "			ST_GeogFromText(CONCAT('SRID=4326; LINESTRING(',x1,' ',y1,', ',x2,' ',y2,')')))"
		sqlCommand += "	limit 1;"
		cur.execute(sqlCommand)
		row = cur.fetchone()
		street = {
			"gid" : int(row[0]),
			"source" : int(row[1]),
			"target" : int(row[2]),
			"sourceLoc" : [row[3], row[4]],
			"targetLoc" : [row[5], row[6]],
			"cost_s" : row[7],
			"reverse_cost_s" : row[8],
			"one_way" : row[9]
		}

	conn.close()

	return street

def pgrGetShapepointsTimeDist(startLoc, endLoc, databaseName):
	"""
	A function to get a list of shapepoints from start coordinate to end coordinate.

	Parameters
	----------
	startLoc: list
		Start location, the format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt]
	endLat: float
		Required, latitude of end coordinate
	endLon: float
		Required, longitude of end coordinate
	databaseName: string, Require
		If you are hosting a data provider on your local machine (e.g., pgRouting), you'll need to specify the name of the local database.

	Returns
	-------
	path: list of lists
		A list of coordinates in sequence that shape the route from startLoc to endLoc
	timeSecs: list
		time between current shapepoint and previous shapepoint, the first element should be 0
	distMeters: list
		distance between current shapepoint and previous shapepoint, the first element should be 0
	"""

	conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (
		databaseName, 
		config['VRV_SETTING_PGROUTING_USERNAME'], 
		config['VRV_SETTING_PGROUTING_HOST'], 
		config['VRV_SETTING_PGROUTING_PASSWORD']))
	conn.autocommit = True
	cur = conn.cursor()

	# Calculate the distance between snapped location and source/target of closest street for the START coordinate
	startStreet = pgrGetNearestStreet(startLoc, databaseName)
	snapStartLoc = pgrGetSnapToRoadLatLon(startStreet['gid'], startLoc, databaseName)
	dicSnapStartLoc = loc2Dict(snapStartLoc)
	distSnapStart2Source = geoDistance2D(snapStartLoc, startStreet['sourceLoc'])
	distSnapStart2Target = geoDistance2D(snapStartLoc, startStreet['targetLoc'])

	# Calculate the distance between snapped location and source/target of closest street for the END coordinate
	endStreet = pgrGetNearestStreet(endLoc, databaseName)
	snapEndLoc = pgrGetSnapToRoadLatLon(endStreet['gid'], endLoc, databaseName)
	dicSnapEndLoc = loc2Dict(snapEndLoc)
	distSnapEnd2Source = geoDistance2D(snapEndLoc, endStreet['sourceLoc'])
	distSnapEnd2Target = geoDistance2D(snapEndLoc, endStreet['targetLoc'])

	# Find the number of vertices in the pgRouting database
	sqlCommand  = "	select count(*) from ways_vertices_pgr;"
	cur.execute(sqlCommand)
	row = cur.fetchone()
	newlyInsertVidNum = int(row[0]) + 1

	# Testify and find a dummyClassID to put temp vertices and segments
	dummyClassID = 821 # Hard-coded number, no specific meaning
	# FIXME! For database security reason, we need to testify if class_id = 821 is not used in the original database

	# insert the snapped location for START coordinate, and two segments from the coordinate to source/target of the closest street
	sqlCommand  = "	insert into ways_vertices_pgr (id, lon, lat) values (%s, %s, %s);" % (
		newlyInsertVidNum, 
		dicSnapStartLoc['lon'], 
		dicSnapStartLoc['lat'])
	sqlCommand += "	insert into ways (class_id, source, target, length_m, x1, y1, x2, y2, cost_s, reverse_cost_s) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" % (
		dummyClassID, 
		newlyInsertVidNum, 
		startStreet['target'], 
		distSnapStart2Target, 
		dicSnapStartLoc['lon'],
		dicSnapStartLoc['lat'],
		startStreet['targetLoc'][1], 
		startStreet['targetLoc'][0], 
		startStreet['cost_s'] * distSnapStart2Target / (distSnapStart2Target + distSnapStart2Source), 
		startStreet['reverse_cost_s'] * distSnapStart2Target / (distSnapStart2Target + distSnapStart2Source))
	sqlCommand += "	insert into ways (class_id, source, target, length_m, x1, y1, x2, y2, cost_s, reverse_cost_s) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" % (
		dummyClassID, 
		startStreet['source'], 
		newlyInsertVidNum, 
		distSnapStart2Source, 
		startStreet['sourceLoc'][1], 
		startStreet['sourceLoc'][0], 
		dicSnapStartLoc['lon'],
		dicSnapStartLoc['lat'],
		startStreet['cost_s'] * distSnapStart2Source / (distSnapStart2Target + distSnapStart2Source), 
		startStreet['reverse_cost_s'] * distSnapStart2Source / (distSnapStart2Target + distSnapStart2Source))

	# insert the snapped location for END coordinate, and two segments from the coordinate to source/target of the closest street
	sqlCommand += "	insert into ways_vertices_pgr (id, lon, lat) values (%s, %s, %s);" % (
		newlyInsertVidNum + 1, 
		dicSnapEndLoc['lon'], 
		dicSnapEndLoc['lat'])
	sqlCommand += "	insert into ways (class_id, source, target, length_m, x1, y1, x2, y2, cost_s, reverse_cost_s) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" % (
		dummyClassID, 
		newlyInsertVidNum + 1, 
		endStreet['target'], 
		distSnapEnd2Target, 
		dicSnapEndLoc['lon'],
		dicSnapEndLoc['lat'],
		endStreet['targetLoc'][1], 
		endStreet['targetLoc'][0], 
		endStreet['cost_s'] * distSnapEnd2Target / (distSnapEnd2Target + distSnapEnd2Source), 
		endStreet['reverse_cost_s'] * distSnapEnd2Target / (distSnapEnd2Target + distSnapEnd2Source))
	sqlCommand += "	insert into ways (class_id, source, target, length_m, x1, y1, x2, y2, cost_s, reverse_cost_s) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" % (
		dummyClassID, 
		endStreet['source'], 
		newlyInsertVidNum + 1, 
		distSnapEnd2Source, 
		endStreet['sourceLoc'][1], 
		endStreet['sourceLoc'][0], 
		dicSnapEndLoc['lon'],
		dicSnapEndLoc['lat'],
		endStreet['cost_s'] * distSnapEnd2Source / (distSnapEnd2Target + distSnapEnd2Source), 
		endStreet['reverse_cost_s'] * distSnapEnd2Source / (distSnapEnd2Target + distSnapEnd2Source))

	# Do dijstra algorithm to find shortest path
	sqlCommand += " select b.gid as gid, b.y1 as lats1, b.x1 as lons1, b.y2 as lats2, b.x2 as lons2, a.cost as secs, b.length_m as dist "
	sqlCommand += "	from "
	sqlCommand += "		pgr_dijkstra("
	sqlCommand += "			'select gid as id, source, target, cost_s as cost, reverse_cost_s as reverse_cost from ways',"
	sqlCommand += "			%s," % (newlyInsertVidNum)
	sqlCommand += "			%s," % (newlyInsertVidNum + 1)
	sqlCommand += "			directed := true"
	sqlCommand += "		) a"
	sqlCommand += "	left join"
	sqlCommand += "		ways b"
	sqlCommand += "	on a.edge = b.gid"
	sqlCommand += "	order by a.path_seq"

	# Return the shapepoint result from dijstra algorithm
	cur.execute(sqlCommand)
	row = cur.fetchall()
	summary = pd.DataFrame(row, columns=['gid', 'lats1', 'lons1', 'lats2', 'lons2', 'secs', 'dist'])
	
	# Delete the temp data
	sqlCommand  = "	delete from ways_vertices_pgr where id = (%s);" % (newlyInsertVidNum)
	sqlCommand += "	delete from ways_vertices_pgr where id = (%s);" % (newlyInsertVidNum + 1)
	sqlCommand += "	delete from ways where class_id = %s;" % (dummyClassID)
	cur.execute(sqlCommand)

	# The last row is junk info, drop it
	summary.drop(summary.index[len(summary) - 1], inplace = True)

	# Sorting the coordinates so that they can be linked to each other
	lats1 = summary['lats1'].tolist()
	lons1 = summary['lons1'].tolist()
	lats2 = summary['lats2'].tolist()
	lons2 = summary['lons2'].tolist()
	path = []
	path.append(startLoc)
	for i in range(1, len(lats1)):
		if (lats1[i] != lats1[i - 1] and lats1[i] != lats2[i - 1]):
			path.append([lats1[i], lons1[i]])
		else:
			path.append([lats2[i], lons2[i]])
	timeSecs = summary['secs'].tolist()
	distMeters = summary['dist'].tolist()

	conn.close()

	return [path, timeSecs, distMeters]

def pgrGetTimeDist(fromLocs, toLocs, databaseName):
	"""
	This function generated time and distance matrix using pgRouting

	Parameters
	----------
	fromLocs: list, Conditional
		Used in 'one2many' mode. To state the coordinate of the starting node
	locs: list of lists
		Used in 'all2all', 'one2many', 'many2one' modes. A list of coordinates, in the format of [[lat1, lon1], [lat2, lon2], ...]
	toLocs: list, Conditional
		Used in 'many2one' mode. To state the coordinate of the ending node
	databaseName: string	
		If you are hosting a data provider on your local machine (e.g., pgRouting), you'll need to specify the name of the local database. 

	Returns
	-------
	timeSecs: dictionary
		The key of each item in this dictionary is in (coordID1, coordID2) format, the travelling time from first entry to second entry, the units are seconds
	distMeters: dictionary
		The key of each item in this dictionary is in (coordID1, coordID2) format, the travelling distance from first entry to second entry, the units are meters
	"""

	conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (
		databaseName, 
		config['VRV_SETTING_PGROUTING_USERNAME'], 
		config['VRV_SETTING_PGROUTING_HOST'], 
		config['VRV_SETTING_PGROUTING_PASSWORD']))
	conn.autocommit = True
	cur = conn.cursor()

	dummyClassID = 821 # Hard-coded number, no specific meaning
	# FIXME! For database security reason, we need to testify if class_id = 821 is not used in the original database	

	sqlCommand  = " select max(id) from ways_vertices_pgr;"
	cur.execute(sqlCommand)
	row = cur.fetchone()
	newlyInsertVidNum = int(row[0]) + 1

	locs = fromLocs.copy()
	for i in range(len(toLocs)):
		try:
			locs.index(toLocs[i])
		except ValueError:
			locs.append(toLocs[i])

	startVidList = []
	endVidList = []
	for i in range(len(fromLocs)):
		startVidList.append(newlyInsertVidNum + locs.index(fromLocs[i]))
	for i in range(len(toLocs)):
		endVidList.append(newlyInsertVidNum + locs.index(toLocs[i]))

	for i in range(len(locs)):
		# Add dummy vertices
		street = pgrGetNearestStreet(locs[i], databaseName)
		snapLoc = pgrGetSnapToRoadLatLon(street['gid'], locs[i], databaseName)
		dicSnapLoc = loc2Dict(snapLoc)
		sqlCommand	= "	insert into ways_vertices_pgr (id, lon, lat) values (%s, %s, %s);" % (
			newlyInsertVidNum + locs.index(locs[i]),
			dicSnapLoc['lon'],
			dicSnapLoc['lat'])
		cur.execute(sqlCommand)

		# Add four two road segments
		distSource2Snapped = geoDistance2D(street['sourceLoc'], snapLoc)
		distSnapped2Target = geoDistance2D(snapLoc, street['targetLoc'])
		ratio = distSource2Snapped / (distSource2Snapped + distSnapped2Target)
		dicSourceLoc = loc2Dict(street['sourceLoc'])
		dicTargetLoc = loc2Dict(street['targetLoc'])
		sqlCommand  = "	insert into ways (class_id, source, target, length_m, x1, y1, x2, y2, cost_s, reverse_cost_s) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" % (
			dummyClassID, 
			street['source'],
			newlyInsertVidNum + locs.index(locs[i]),
			distSource2Snapped,
			dicSourceLoc['lon'],
			dicSourceLoc['lat'],
			dicSnapLoc['lon'],
			dicSnapLoc['lat'],
			street['cost_s'] * ratio,
			street['reverse_cost_s'] * ratio)
		cur.execute(sqlCommand)
		sqlCommand  = "	insert into ways (class_id, source, target, length_m, x1, y1, x2, y2, cost_s, reverse_cost_s) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" % (
			dummyClassID, 
			newlyInsertVidNum + locs.index(locs[i]),
			street['target'],
			distSnapped2Target,
			dicSnapLoc['lon'],
			dicSnapLoc['lat'],
			dicTargetLoc['lon'],
			dicTargetLoc['lat'],
			street['cost_s'] * (1 - ratio),
			street['reverse_cost_s'] * (1 - ratio))
		cur.execute(sqlCommand)

	sqlCommand  = "	select " 
	sqlCommand += "		start_vid as start_node, "
	sqlCommand += "		end_vid as end_node, "
	sqlCommand += "		sum(cost) as time, "
	sqlCommand += "		sum(length_m) as distance "
	sqlCommand += "	from ("
	sqlCommand += "		select "
	sqlCommand += "			a.*, "
	sqlCommand += "			b.length_m"
	sqlCommand += "		from pgr_dijkstra("
	sqlCommand += "			'select gid as id, source, target, cost_s as cost, reverse_cost_s as reverse_cost from ways', "
	sqlCommand += "			ARRAY%s, " % (startVidList)
	sqlCommand += "			ARRAY%s, " % (endVidList)
	sqlCommand += "			directed := true) a "
	sqlCommand += "		left join "
	sqlCommand += "			ways b "
	sqlCommand += "		on "
	sqlCommand += "			a.edge = b.gid "
	sqlCommand += "		order by "
	sqlCommand += "			a.path_seq"
	sqlCommand += "		) x "
	sqlCommand += "	group by "
	sqlCommand += "		start_vid, "
	sqlCommand += "		end_vid;"
	cur.execute(sqlCommand)
	row = cur.fetchall()

	for i in range(len(startVidList)):
		sqlCommand  = "	delete from ways_vertices_pgr where id = %s;" % (startVidList[i])
		cur.execute(sqlCommand)
	for i in range(len(endVidList)):
		sqlCommand  = "	delete from ways_vertices_pgr where id = %s;" % (endVidList[i])
		cur.execute(sqlCommand)
	sqlCommand  = "	delete from ways where class_id = %s;" % (dummyClassID)
	cur.execute(sqlCommand)

	conn.close()

	rawDist = {}
	rawTime = {}
	for i in range(len(row)):
		rawTime[row[i][0], row[i][1]] = row[i][2]
		rawDist[row[i][0], row[i][1]] = row[i][3]
	distMeters = {}
	timeSecs = {}

	for i in range(len(fromLocs)):
		for j in range(len(toLocs)):
			try:
				distMeters[i, j] = rawDist[startVidList[i], endVidList[j]]
			except:
				distMeters[i, j] = 0
			try:
				timeSecs[i, j] = rawTime[startVidList[i], endVidList[j]]
			except:
				timeSecs[i, j] = 0

	return [timeSecs, distMeters]
