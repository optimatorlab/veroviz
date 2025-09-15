from veroviz._common import *

def elevapiGetElevation(locs):
	"""
	Finds the elevation, in units of meters above mean sea level (MSL), for a given location or list of locations.
	See https://github.com/Jorl17/open-elevation/blob/master/docs/api.md for more info.
	No API key is required.
	
	Parameters
	----------
	locs: list of lists, Required, default as None
		A list of one or more GPS coordinate of the form [[lat, lon], ...] or [[lat, lon, alt], ...].  If altitude is included in locs, the function will add the elevation to the input altitude.  Otherwise, the input altitude will be assumed to be 0.
	
	Return
	------
	list of lists, of the form [[lat, lon, altMSL], [lat, lon, altMSL], ..., [lat, lon, altMSL]].
	"""
    
    # Old:
	# elevUrl = ('https://elevation-api.io/api/elevation')

	# 2025-09-13.  See https://github.com/Jorl17/open-elevation/blob/master/docs/api.md
	elevUrl = 'https://api.open-elevation.com/api/v1/lookup'

	locations = []
	for i in range(0, len(locs)):
		locations.append({"latitude": locs[i][0], 
						  "longitude": locs[i][1]})

	encoded_body = json.dumps({
		"locations": locations})
	
	headers = {
				'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
				'Content-Type': 'application/json'}

	try:
		
		http = urllib3.PoolManager()
		response = http.request('POST', elevUrl, headers=headers, body=encoded_body)

		data = json.loads(response.data.decode('utf-8'))
		http_status = response.status

		locsWithAlt = []
		
		if (http_status == 200):
			# OK			
			for i in range(0, len(data['results'])):
				lat = data['results'][i]['latitude']
				lon = data['results'][i]['longitude']
				alt = data['results'][i]['elevation']
				
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

			
			
