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

	for dest in nodes[nodes['id'] != originNodeID]['id'].tolist():
		if (originNodeID, dest) in costDict.keys():
			data.append({'id': dest, 'cost': costDict[originNodeID, dest]})
		
	dataframe = pd.DataFrame(data)

	if (k <= 0):
		k = len(dataframe)

	return dataframe.sort_values(by=['cost', 'id'], ascending=True).head(k)
