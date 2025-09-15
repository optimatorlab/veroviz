from veroviz._common import *

def owGetWeather(location, id, metricUnits, APIkey):		
	if (metricUnits):
		units = 'metric'
	else:
		units = 'imperial'
	
	weatherUrl = ('https://api.openweathermap.org/data/3.0/onecall?lat=%s&lon=%s&appid=%s&units=%s' % (location[0], location[1], APIkey, units))
	
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', weatherUrl)
		data = json.loads(response.data.decode('utf-8'))

		http_status = response.status

		if (http_status == 200):
			# OK
			x = []

			subDict = {}
			subDict['id']       = id
			subDict['lat']      = data['lat'] 
			subDict['lon']      = data['lon'] 
			subDict['timezone'] = data['timezone']
			subDict['class']    = 'current'
			for key in data['current']:
				if (key == 'rain'):
					for subkey in data['current']['rain']:
						subDict['rain_' + subkey] = data['current']['rain'][subkey]
				elif (key == 'snow'):
					for subkey in data['current']['snow']:
						subDict['snow_' + subkey] = data['current']['snow'][subkey]
				elif (key == 'weather'):
					for subkey in data['current']['weather'][0]:
						subDict['weather_' + subkey] = data['current']['weather'][0][subkey]
				else:
					subDict[key] = data['current'][key]
			x.append(subDict)

			for i in range(0, len(data['minutely'])):
				subDict = {}
				subDict['id']       = id
				subDict['lat']      = data['lat'] 
				subDict['lon']      = data['lon'] 
				subDict['timezone'] = data['timezone']
				subDict['class']    = 'minutely'
				for key in data['minutely'][i]:
					subDict[key] = data['minutely'][i][key]
				x.append(subDict)
			
			for i in range(0, len(data['hourly'])):
				subDict = {}
				subDict['id']       = id
				subDict['lat']      = data['lat'] 
				subDict['lon']      = data['lon'] 
				subDict['timezone'] = data['timezone']
				subDict['class']    = 'hourly'
				for key in data['hourly'][i]:				
					if (key == 'rain'):
						for subkey in data['hourly'][i]['rain']:
							subDict['rain_' + subkey] = data['hourly'][i]['rain'][subkey]
					elif (key == 'snow'):
						for subkey in data['hourly'][i]['snow']:
							subDict['snow_' + subkey] = data['hourly'][i]['snow'][subkey]
					elif (key == 'weather'):
						for subkey in data['hourly'][i]['weather'][0]:
							subDict['weather_' + subkey] = data['hourly'][i]['weather'][0][subkey]
					else:
						subDict[key] = data['hourly'][i][key]
				x.append(subDict)

			for i in range(0, len(data['daily'])):
				subDict = {}
				subDict['id']       = id
				subDict['lat']      = data['lat'] 
				subDict['lon']      = data['lon'] 
				subDict['timezone'] = data['timezone']
				subDict['class']    = 'daily'
				for key in data['daily'][i]:
					if (key == 'weather'):
						for subkey in data['daily'][i]['weather'][0]:
							subDict['weather_' + subkey] = data['daily'][i]['weather'][0][subkey]

					elif (key == 'temp'):
						for subkey in data['daily'][i]['temp']:
							subDict['temp_' + subkey] = data['daily'][i]['temp'][subkey]

					elif (key == 'feels_like'):
						for subkey in data['daily'][i]['feels_like']:
							subDict['feels_like_' + subkey] = data['daily'][i]['feels_like'][subkey]

					else:
						subDict[key] = data['daily'][i][key]
				x.append(subDict)


			df = pd.DataFrame(x)

			try:
				df['dt'] = pd.to_datetime(df['dt'], unit='s')
			except Exception:
				# Handle invalid dates, e.g., by appending NaT or the original value
				df['dt'] = pd.NaT
			
			try:
				df['sunrise'] = pd.to_datetime(df['sunrise'], unit='s')
			except Exception:
				df['sunrise'] = pd.NaT
				
			try:
				df['sunset'] = pd.to_datetime(df['sunset'], unit='s')
			except Exception:
				df['sunset'] =  pd.NaT

			return df
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return
	except:
		print("Error: ", sys.exc_info()[1])
		raise 
		
		
		
		
