from veroviz._common import *

def elevapiGetElevation(locs, APIkey):
	"""
	EXPERIMENTAL.  Finds the elevation, in units of meters above mean sea level (MSL), for a given location or list of locations.  See https://elevation-api.io for more info.

	Parameters
	----------
	locs: list of lists, Required, default as None
		A list of one or more GPS coordinate of the form [[lat, lon], ...] or [[lat, lon, alt], ...].  If altitude is included in locs, the function will add the elevation to the input altitude.  Otherwise, the input altitude will be assumed to be 0.
	APIkey: string
		Enables access to ORS server.
	
	Return
	------
	list of lists, of the form [[lat, lon, altMSL], [lat, lon, altMSL], ..., [lat, lon, altMSL]].
	"""
    
    
	elevUrl = ('https://elevation-api.io/api/elevation')
	points = []
	for i in range(0, len(locs)):
		points.append([locs[i][0], locs[i][1]])

	encoded_body = json.dumps({
		"points": points})
	
	headers = {
				'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
				'Authorization': APIkey,
				'Content-Type': 'application/json'}

	try:
		
		http = urllib3.PoolManager()
		response = http.request('POST', elevUrl, headers=headers, body=encoded_body)

		data = json.loads(response.data.decode('utf-8'))
		http_status = response.status

		locsWithAlt = []
		
		if (http_status == 200):
			# OK			
			for i in range(0, len(data['elevations'])):
				lat = data['elevations'][i]['lat']
				lon = data['elevations'][i]['lon']
				alt = data['elevations'][i]['elevation']
				
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

			
			