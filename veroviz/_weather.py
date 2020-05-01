from veroviz._common import *

from veroviz._queryOpenWeather import owGetWeather

def privGetWeather(location, id, metricUnits, dataProvider, dataProviderArgs):	

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	if (weatherDataProviderDictionary[dataProvider] == 'openweather'):
		weatherDF = owGetWeather(location, id, metricUnits, dataProviderArgs['APIkey'])
		return weatherDF



