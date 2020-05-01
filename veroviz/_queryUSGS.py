from veroviz._common import *

def usgsGetElevation(locs):
	"""
	EXPERIMENTAL.  Finds the elevation, in units of meters above mean sea level (MSL), for a given location or list of locations.  See https://nationalmap.gov/epqs/ for more info.

	Parameters
	----------
	locs: list of lists, Required, default as None
		A list of one or more GPS coordinate of the form [[lat, lon], ...] or [[lat, lon, alt], ...].  If altitude is included in locs, the function will add the elevation to the input altitude.  Otherwise, the input altitude will be assumed to be 0.
	
	Return
	------
	list of lists, of the form [[lat, lon, altMSL], [lat, lon, altMSL], ..., [lat, lon, altMSL]].
	"""
    
	locsWithAlt = []    

	try:
		for i in range(0, len(locs)):
			# USGS uses x=lon, y=lat:
			elevUrl = ('https://nationalmap.gov/epqs/pqs.php?x=%s&y=%s&units=Meters&output=json' % (locs[i][1], locs[i][0]))
	
			http = urllib3.PoolManager()
			response = http.request('GET', elevUrl)
			data = json.loads(response.data.decode('utf-8'))

			http_status = response.status
	
			if (http_status == 200):
				# OK
				abbrev = data['USGS_Elevation_Point_Query_Service']['Elevation_Query']
				alt    = abbrev['Elevation']
				lat    = abbrev['y']
				lon    = abbrev['x']

				# Returns "-1000000" (a string) if no elev data exist
				if (type(alt) is str):
					alt = -1000000
				else:
					if (len(locs[i]) > 2):
						alt += locs[i][2]

				locsWithAlt.append([ lat, lon, alt ])
		
			else:
				# Error of some kind
				http_status_description = responses[http_status]
				print("Error Code %s: %s" % (http_status, http_status_description))
				return
				
		return locsWithAlt

	except:
		print("Error: ", sys.exc_info()[1])
		raise 
			
			