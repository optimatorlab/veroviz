from veroviz._common import *

from veroviz._queryORS import orsGetElevation
from veroviz._queryUSGS import usgsGetElevation
from veroviz._queryElevationapiio import elevapiGetElevation
# from veroviz._queryHere import hereGetElevation

def privGetElevationLocs(locs, dataProvider, dataProviderArgs):
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
	elif (elevDataProviderDictionary[dataProvider] == 'usgs'):
		locsWithAlt = usgsGetElevation(locs)
		return locsWithAlt
	elif (elevDataProviderDictionary[dataProvider] == 'elevapi'):
		locsWithAlt = elevapiGetElevation(locs)
		return locsWithAlt


def privGetElevationNodes(dataframe, replaceOnlyNone, dataProvider, dataProviderArgs):
	if (replaceOnlyNone):
		df = dataframe[dataframe['elevMeters'].isin([None])][['lat', 'lon']]
	else:
		df = dataframe[['lat', 'lon']]
	indices = list(df.index)
	locs = list(map(list, zip(df.lat, df.lon)))

	if (len(indices) == 0):
		print("There were no missing elevations in the input nodes dataframe.  Try setting the `replaceOnlyNone` flag to `False` if you want to update elevation data for all nodes.")
	else:
		locsWithAlt = privGetElevationLocs(locs, dataProvider, dataProviderArgs)

		if (len(locsWithAlt) != len(indices)):
			print("Error: Something went wrong with the request.  Sorry.")
		else:
			for i in range(0, len(indices)):
				dfIndex = indices[i]
				dataframe.loc[dfIndex, 'elevMeters'] = locsWithAlt[i][2]
			
	return dataframe
	
def privGetElevationArcsAsgn(dataframe, replaceOnlyNone, dataProvider, dataProviderArgs):

	# Start with starting location:
	if (replaceOnlyNone):
		df = dataframe[dataframe['startElevMeters'].isin([None])][['startLat', 'startLon']]
	else:
		df = dataframe[['startLat', 'startLon']]		
	indices = list(df.index)
	locs = list(map(list, zip(df.startLat, df.startLon)))

	nothingToUpdateStart = False
	if (len(indices) == 0):
		nothingToUpdateStart = True
		print("There were no missing START elevations.")
	else:
		locsWithAlt = privGetElevationLocs(locs, dataProvider, dataProviderArgs)

		if (len(locsWithAlt) != len(indices)):
			print("Error: Something went wrong with the request.  Sorry.")
		else:
			for i in range(0, len(indices)):
				dfIndex = indices[i]
				dataframe.loc[dfIndex, 'startElevMeters'] = locsWithAlt[i][2]

	# Repeat the process for ending location:
	if (replaceOnlyNone):
		df = dataframe[dataframe['endElevMeters'].isin([None])][['endLat', 'endLon']]
	else:	
		df = dataframe[['endLat', 'endLon']]
	indices = list(df.index)
	locs = list(map(list, zip(df.endLat, df.endLon)))

	nothingToUpdateEnd = False
	if (len(indices) == 0):
		nothingToUpdateEnd = True
		print("There were no missing END elevations.")
	else:
		locsWithAlt = privGetElevationLocs(locs, dataProvider, dataProviderArgs)

		if (len(locsWithAlt) != len(indices)):
			print("Error: Something went wrong with the request.  Sorry.")
		else:
			for i in range(0, len(indices)):
				dfIndex = indices[i]
				dataframe.loc[dfIndex, 'endElevMeters'] = locsWithAlt[i][2]

	if ((nothingToUpdateStart) and (nothingToUpdateEnd)):
		print("No elevations were updated.  Try setting the `replaceOnlyNone` flag to `False` if you want to update elevation data for all arcs.")

	return dataframe
