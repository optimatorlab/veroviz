from veroviz._common import *

from veroviz._queryORS import orsIsochrones
# from veroviz._queryHere import hereIsochrones

def privIsochrones(location, locationType, travelMode, rangeType, rangeSize, interval, smoothing, dataProvider, dataProviderArgs):
	"""
	FIXME
	
	"""

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	# NOTE:  Neither mapquest, pgRouting, nor OSRM are supported.

	# FIXME -- None is not allowed    

	if (isoDataProviderDictionary[dataProvider] == 'ors-online'):
		iso = orsIsochrones(location, locationType, travelMode, rangeType, rangeSize, interval, smoothing, dataProviderArgs['APIkey'])
		return iso
		