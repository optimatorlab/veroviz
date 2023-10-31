from veroviz._common import *

from veroviz._utilities import privInitDataframe

def deconstructAssignments(assignments=None, includeStationaryFlag=False, includeVerticalFlag=False):
	"""
	Given an Assignments dataframe, according to objectID and odID, separate it into a set of routes

	Parameters
	----------
	assignments: :ref:`Assignments`, Required
		Assignments dataframe, to be converted and separated by `odID`
	includeStationaryFlag: boolean, Optional, default as False
		Decide whether we includes the "routes" that have the same origin and destination
	includeVerticalFlag: boolean, Optional, default as False
		Decide whether we includes the "routes" that is vertical to the ground
	
	Return
	------
	list
		It is a list of assignment dataframes, each dataframe is a route or a period of stationary 'movement'
	"""
	lstSubAssignments = []

	# If we need to include all stationary rows, find all stationary, each row becomes a new dataframe
	if (includeStationaryFlag):
		stationaryRows = assignments.loc[(assignments['startLat'] == assignments['endLat']) & (assignments['startLon'] == assignments['endLon']) & (assignments['startAltMeters'] == assignments['endAltMeters'])]
		stationaryRows = stationaryRows.reset_index(drop=True)
		for i in range(0, len(stationaryRows)):
			lstSubAssignments.append(stationaryRows.loc[i: i, :].copy())

	# If we need to include all vertical rows, find all vertical, each row becomes a new dataframe
	if (includeVerticalFlag):
		verticalRows = assignments.loc[(assignments['startLat'] == assignments['endLat']) & (assignments['startLon'] == assignments['endLon']) & (assignments['startAltMeters'] != assignments['endAltMeters'])]
		verticalRows = verticalRows.reset_index(drop=True)
		for i in range(0, len(verticalRows)):
			lstSubAssignments.append(verticalRows.loc[i: i, :].copy())

	collection = assignments.loc[(assignments['startLat'] != assignments['endLat']) | (assignments['startLon'] != assignments['endLon'])]
	if (len(collection) > 0):
		collection = collection.sort_values(by=['objectID', 'startTimeSec', 'modelFile', 'odID'], ascending=True)
		collection = collection.reset_index(drop=True)

		# Find consecutive routes
		tmpSubAssignment = privInitDataframe('Assignments')
		for i in range(len(collection)):
			if (len(tmpSubAssignment) == 0):
				tmpSubAssignment = pd.DataFrame(collection.loc[i: i, :].copy(), columns = tmpSubAssignment.columns)
			else:
				if (tmpSubAssignment.iloc[len(tmpSubAssignment) - 1]['endLat'] == collection.iloc[i]['startLat'] 
					and tmpSubAssignment.iloc[len(tmpSubAssignment) - 1]['endLon'] == collection.iloc[i]['startLon'] 
					and tmpSubAssignment.iloc[len(tmpSubAssignment) - 1]['endAltMeters'] == collection.iloc[i]['startAltMeters']
					and tmpSubAssignment.iloc[len(tmpSubAssignment) - 1]['endTimeSec'] == collection.iloc[i]['startTimeSec']
					and tmpSubAssignment.iloc[len(tmpSubAssignment) - 1]['odID'] == collection.iloc[i]['odID']):
					tmpSubAssignment = pd.concat([tmpSubAssignment, collection.loc[i: i, :].copy()], ignore_index= True, sort=True)
				else:
					lstSubAssignments.append(tmpSubAssignment.copy())
					tmpSubAssignment = pd.DataFrame(collection.loc[i: i, :].copy(), columns = tmpSubAssignment.columns)
		lstSubAssignments.append(tmpSubAssignment.copy())

	# Re-index odID for lstRoutes
	for i in range(0, len(lstSubAssignments)):
		lstSubAssignments[i] = lstSubAssignments[i].reset_index(drop=True)
		lstSubAssignments[i]['odID'] = i

	return lstSubAssignments
