import pandas as pd

def privNearestNodes(nodes, originNodeID, k, costDict):
	"""
	Returns a pandas dataframe with 2 columns, 'id' and 'cost'.  The 'id' column
	represents a nodeID, the 'cost' represents either a time or a distance 
	(consistent with the data provided by costDict).
	The dataframe is sorted according to ascending values of 'cost'.  The 
	top k rows are returned (i.e., the nearest k nodes).
	"""

	data = []

	for keys in costDict.keys():
		if (keys[0] == originNodeID):
			if (keys[1] != originNodeID):
				data.append({'id': keys[1], 'cost': costDict[keys]})

	dataframe = pd.DataFrame(data) 

	return dataframe.sort_values(by=['cost', 'id'], ascending=True).head(k)