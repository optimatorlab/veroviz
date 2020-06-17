from veroviz._common import *
from veroviz._validation import valGetTimeDist2D

from veroviz._getTimeDistFromLocs2D import getTimeDistFromLocs2D

def getTimeDist2D(nodes=None, matrixType='all2all', fromNodeID=None, toNodeID=None, outputDistUnits='meters', outputTimeUnits='seconds', routeType='euclidean2D', speedMPS=None, dataProvider=None, dataProviderArgs=None):
	
	"""
	Generates two dictionaries; one for distance, one for time.  This is for vehicles that travel only on the ground (2-dimensional movement).
	
	Parameters
	----------
	nodes: :ref:`Nodes`, Required, default as None
		This :ref:`Nodes` dataframe contains the locations between which the travel time and distance will be calculated.
	matrixType: string, Optional, default as 'all2all'
		Specifies the structure of the travel matrices.  Valid options include 'all2all', 'many2one', and 'one2many'.  The default 'all2all' option will return square matrices (one for time, one for distance) describing the directed travel time and travel distance between all pairs of nodes.  The 'one2many' option will return vectors describing the directed travel from one node to all other nodes.  Similarly, the 'many2one' option will return vectors describing the directed travel from all nodes to a given node.  See the table in the note below for details.
	fromNodeID: int, Optional, default as None
		Specifies the node ID (from the `id` column of the input `nodes` dataframe) of the origin node.  This parameter is required for the 'one2many' matrix type; it is ignored by all other matrix types.  See the table in the note below for details.
	toNodeID: int, Optional, default as None
		Specifies the node ID (from the `id` column of the input `nodes` dataframe) of the destination node.  This parameter is required for the 'many2one' matrix type; it is ignored for all other matrix types.  See the table in the note below for details.
	outputDistUnits: string, Optional, default as 'meters'
		Specifies the desired distance units for the function's output.  Valid values are 'meters', 'm', 'kilometers', 'km', 'miles', 'mi', 'feet', 'ft', 'nm', and 'nmi' (nautical miles). See :ref:`Units` for options and abbreviations.
	outputTimeUnits: string, Optional, default as 'seconds'
		Specifies the desired time units for the function's output.  Valid values are 'seconds', 'hours', and 'minutes'. See :ref:`Units` for options and abbreviations.
	routeType: string, Optional, default as 'euclidean2D'
		This describes a characteristic of the travel mode.  Possible values are: 'euclidean2D', 'manhattan', 'fastest', 'shortest', 'pedestrian', 'cycling', and 'truck'.  The 'euclidean2D' and 'manhattan' options are calculated directly from GPS coordinates, without a road network.  Neither of these two options require a data provider.  However, the other options rely on road network information and require a data provider.  Furthermore, some of those other options are not supported by all data providers.  See :ref:`Data Providers` for details.
	speedMPS: float, Conditional, default as None
		Speed of the vehicle, in units of meters per second. For route types that are not road-network based (i.e., 'euclidean2D' and 'manhattan'), this field is required to calculate travel times. Otherwise, if a route type already incorporates travel speeds from road network data, (i.e., 'fastest', 'shortest', and 'pedestrain'), this input argument may be ignored.  If provided, `speedMPS` will override travel speed data used by the route type option.
	dataProvider: string, Conditional, default as None
		Specifies the data source to be used for obtaining the travel data. See :ref:`Data Providers` for options and requirements.
	dataProviderArgs: dictionary, Conditional, default as None
		For some data providers, additional parameters are required (e.g., API keys or database names). See :ref:`Data Providers` for the additional arguments required for each supported data provider.


	Returns
	-------
	time: dictionary
		A Python dictionary containing travel times.  Time units are defined by `outputTimeUnits`.  The format of key values is: `(fromID, toID)`.  The travel time from ID 1 to ID 2 is provided by `time[1, 2]`. 
	dist: dictionary
		A Python dictionary containing travel distances.  Distance units are defined by `outputDistUnits`.  The format of key values is: `(fromID, toID)`.  The travel distance from ID 1 to ID 2 is provided by `dist[1, 2]`.  

	Note
	----
	For `matrixType`, the options are 'all2all', 'one2many', and 'many2one'.

	+----------------------+--------------+------------+------------------+
	| `matrixType` options | `fromNodeID` | `toNodeID` | Return type      |
	+======================+==============+============+==================+
	| 'all2all'            | ignored      | ignored    | Square matrices  |
	+----------------------+--------------+------------+------------------+
	| 'one2many'           | required     | ignored    | Row vectors      |
	+----------------------+--------------+------------+------------------+
	| 'many2one'           | ignored      | required   | Column vectors   |
	+----------------------+--------------+------------+------------------+

	In 'all2all', square matrices will be generated for all node pairs in the  
	provided `nodes` dataframe.

	In 'one2many', a node `id` will be assigned in the `fromNodeID` field, which 
	comes from the `id` column in the provided `nodes` dataframe.
	Row vectors will be returned for the time and distance from that node 
	to all the nodes in the provided `nodes` dataframe.

	In 'many2one', column vectors will be returned for the time and distance 
	from all nodes in the provided `nodes` dataframe to the node indicated 
	by `toNodeID`.
	


	Examples
	--------
	Import veroviz and check if the version is up-to-date
	    >>> import veroviz as vrv
	    >>> vrv.checkVersion()

	Generate a :ref:`Nodes` dataframe from a list of coordinates.  See :meth:`~veroviz.generateNodes.generateNodes` for other methods to generate "nodes" dataframes.
	    >>> locs = [
	    ...     [42.1538, -78.4253], 
	    ...     [42.3465, -78.6234], 
	    ...     [42.6343, -78.1146]]
	    >>> exampleNodes = vrv.createNodesFromLocs(locs=locs)
	
	Example 1 - Generate time and distance matrices that only consider Euclidean travel (default), and assume the speed is a constant at 15 m/s.  No data provider is required/used in this case.
		>>> [timeSec, distMeters] = vrv.getTimeDist2D(
		...     nodes        = exampleNodes,
		...     routeType    = 'euclidean2D',
		...     speedMPS     = 15)
		>>> print("Travel time from node 1 to 2 is %.2f seconds" % (timeSec[1, 2]))
		>>> print("Travel distance from node 1 to 2 is %.2f meters" % (distMeters[1, 2]))

	Example 2 - Use a data provider to find the time and distance matrices according to the 'fastest' travel time metric.  
		>>> import os
		>>> ORS_API_KEY = os.environ['ORSKEY']   
		>>> # If you don't have environment variables configured, 
		>>> # uncomment and try the following line:   
		>>> # ORS_API_KEY = 'YOUR_ORS_KEY_GOES_HERE'
		>>> [timeSec, distMeters] = vrv.getTimeDist2D(
		...     nodes        = exampleNodes,
		...     routeType    = 'fastest',
		...     dataProvider = 'ORS-online',
		...     dataProviderArgs = { 'APIkey' : ORS_API_KEY })
		>>> print("Travel time from node 1 to 2 is %.2f seconds" % (timeSec[1, 2]))
		>>> print("Travel distance from node 1 to 2 is %.2f meters" % (distMeters[1, 2]))		
	
	Example 3 - Sometimes you don't need the full square matrix of travel data.  Here, we find the time/distance information associated with traveling from node 3 to all other nodes:
		>>> [timeSec, distMeters] = vrv.getTimeDist2D(
		...     nodes            = exampleNodes,
		...     matrixType       = 'one2many',
		...     fromNodeID       = 3,
		...     toNodeID         = None,
		...     routeType        = 'fastest',
		...     dataProvider     = 'ORS-online',
		...     dataProviderArgs = { 'APIkey' : ORS_API_KEY })
		>>> [timeSec, distMeters]

	Example 4 - Similarly, we can find the time/distance information for travel from all nodes to node 3:
		>>> [timeSec, distMeters] = vrv.getTimeDist2D(
		...     nodes            = exampleNodes,
		...     matrixType       = 'many2one',
		...     fromNodeID       = None,
		...     toNodeID         = 3,
		...     routeType        = 'fastest',
		...     dataProvider     = 'ORS-online',
		...     dataProviderArgs = { 'APIkey' : ORS_API_KEY })
		>>> [timeSec, distMeters]

	Example 5 - As with the `getShapepoints2D()` function, you can provide the speed of the vehicle to override the speed data from a data provider.  Here, we set a constant vehicle speed of 35 MPH (and convert to meters per second).  We also specify that we want time and distance outputs to be in Hours and Miles, respectively.
		>>> # This example includes all functional arguments:
		>>> [timeHours, distMiles] = vrv.getTimeDist2D(
		...     nodes            = exampleNodes, 
		...     matrixType       = 'all2all',
		...     fromNodeID       = None, 
		...     toNodeID         = None, 
		...     outputTimeUnits  = 'hours',
		...     outputDistUnits  = 'miles',
		...     routeType        = 'fastest',
		...     speedMPS         = vrv.convertSpeed(35, 'miles', 'hour', 'meters', 'second'),   # (MPH to m/s)
		...     dataProvider     = 'ORS-online',
		...     dataProviderArgs = {
		...         'APIkey': ORS_API_KEY})
		>>> [timeHours, distMiles]

	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valGetTimeDist2D(nodes, matrixType, fromNodeID, toNodeID, outputDistUnits, outputTimeUnits, routeType, speedMPS, dataProvider, dataProviderArgs)
	if (not valFlag):
		print (errorMsg)
		return [None, None]
	elif (config['VRV_SETTING_SHOWWARNINGMESSAGE'] and warningMsg != ""):
		print (warningMsg)

	try:
		matrixType = matrixType.lower()
	except:
		pass
		
	# Specify the list of rows and columns of output dataframes
	fromRows = []
	toCols = []
	if (matrixType == "all2all"):
		fromRows = nodes['id'].tolist()
		toCols = nodes['id'].tolist()
	elif (matrixType == "one2many"):
		fromRows = [fromNodeID]
		toCols = nodes['id'].tolist()
	elif (matrixType == "many2one"):
		fromRows = nodes['id'].tolist()
		toCols = [toNodeID]
	else:
		return 

	# Specify the list of coordinations, for each coordinate, it is in [lat, lon] format
	fromLocs = []
	toLocs = []
	for i in range(0, len(fromRows)):
		fromLocs.append([nodes.loc[nodes['id'] == fromRows[i], 'lat'].values[0], nodes.loc[nodes['id'] == fromRows[i], 'lon'].values[0]])
	for i in range(0, len(toCols)):
		toLocs.append([nodes.loc[nodes['id'] == toCols[i], 'lat'].values[0], nodes.loc[nodes['id'] == toCols[i], 'lon'].values[0]])

	# get time/dist
	[time, dist] = getTimeDistFromLocs2D(fromLocs, fromRows, toLocs, toCols, outputDistUnits, outputTimeUnits, routeType, speedMPS, dataProvider, dataProviderArgs)

	return [time, dist]
