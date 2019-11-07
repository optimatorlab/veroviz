from veroviz._common import *

from veroviz._queryORS import orsGeocode
from veroviz._queryORS import orsReverseGeocode
from veroviz._queryMapQuest import mqGeocode
from veroviz._queryMapQuest import mqReverseGeocode

def privGeocode(location=None, dataProvider=None, dataProviderArgs=None):
	"""
	Convert a street address, city, state, or zip code to GPS coordinates ([lat, lon] format).

	Parameters
	----------
	location: string, Required
		A text string indicating a street address, state, or zip code.
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for generating nodes on a road network. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.
	
	Return
	------
	list
		A GPS coordinate, of the form [lat, lon].
	"""

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	# NOTE:  Neither pgRouting nor OSRM are supported.
	#        pgRouting would require a database of the entire planet.
	#        OSRM doesn't have a geocode function.
    
	if (dataProvider == None):
		# Initialize our geocoder:
		geopy.geocoders.options.default_user_agent = 'unknown'
		geolocator = Nominatim()
	
		loc = geolocator.geocode(location, timeout=20)
		if (loc is not None):
			return ([loc.latitude, loc.longitude])
			
		else:
			print('ERROR: Could not geocode location %s.' % (location))
	# elif (dataProvider == 'OSRM-online'):
	# 	print('OSRM-online NOT SUPPORTED')
	elif (geoDataProviderDictionary[dataProvider] == 'ors-online'):
		loc = orsGeocode(location, dataProviderArgs['APIkey'])
		return (loc)
		
	elif (geoDataProviderDictionary[dataProvider] == 'mapquest'):
		loc = mqGeocode(location, dataProviderArgs['APIkey'])
		return (loc)
		

def privReverseGeocode(location=None, dataProvider=None, dataProviderArgs=None):
	"""
	Convert a GPS coordinate (of the form [lat, lon] or [lat, lon, alt]) to an address.  If altitude is provided it will be ignored.

	Parameters
	----------
	location: list, Required
		A GPS coordinate of the form [lat, lon] or [lat, lon, alt].
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for generating nodes on a road network. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.
	
	Return
	------
	list
		A GPS coordinate, of the form [lat, lon], indicating the location of the returned address.  Note that this location might not match the input coordinates.
	dictionary
		A dataProvider-specific dictionary containing address details.
	"""

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	# NOTE:  Neither pgRouting nor OSRM are supported.
	#        pgRouting would require a database of the entire planet.
	#        OSRM doesn't have a geocode function.
	
	if (dataProvider == None):  
		# Initialize our geocoder:
		# geolocator = Nominatim(user_agent="specify_your_app_name_here")
		geopy.geocoders.options.default_user_agent = 'unknown'
		geolocator = Nominatim()
		
		loc = geolocator.reverse(location, timeout=20)
		if (loc is not None):
			# print(loc.raw)            
			# print(loc.address)
			return ([loc.latitude, loc.longitude], loc.raw)
		else:
			print('ERROR: Could not geocode location %s.' % (location))
	elif (geoDataProviderDictionary[dataProvider] == 'ors-online'):
		[loc, address] = orsReverseGeocode(location, dataProviderArgs['APIkey'])
		return (loc, address)
		
	elif (geoDataProviderDictionary[dataProvider] == 'mapquest'):
		[loc, address] = mqReverseGeocode(location, dataProviderArgs['APIkey'])
		return (loc, address)
		