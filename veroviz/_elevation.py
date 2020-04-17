from veroviz._common import *

from veroviz._queryORS import orsGetElevation
# from veroviz._queryHere import hereGetElevation

def privGetElevation(locs, dataProvider, dataProviderArgs):
	"""
	FIXME
	
	"""

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	# NOTE:  Neither mapquest, pgRouting, nor OSRM are supported.
	# FIXME -- None is not allowed    

	if (elevDataProviderDictionary[dataProvider] == 'ors-online'):
		locsWithAlt = orsGetElevation(locs, dataProviderArgs['APIkey'])
		return locsWithAlt
		