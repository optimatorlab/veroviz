from veroviz._common import *

def owGetWeather(location, metricUnits, APIkey):		
	if (metricUnits):
		units = 'metric'
	else:
		units = 'imperial'
	
	weatherUrl = ('https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=%s' % (location[0], location[1], APIkey, units))
	
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', weatherUrl)
		data = json.loads(response.data.decode('utf-8'))

		http_status = response.status

		if (http_status == 200):
			# OK
			print(data)
			
			#snapLoc = [data['features'][0]['geometry']['coordinates'][0][1], 
			#			data['features'][0]['geometry']['coordinates'][0][0]] 

            
			return weatherDF
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return
	except:
		print("Error: ", sys.exc_info()[1])
		raise 
		
		
		
		
