import setuptools
from veroviz import __version__

long_description = """
VeRoViz is a suite of tools (primarily written in Python) to easily generate, test, and visualize vehicle routing problems.

Key features of the Python tools include:
- Generation of nodes on road networks;
- Calculation of travel time/distance matrices using external data providers;
- Creation of Leaflet maps to view nodes, routes, and basic geometric shapes; and 
- Generation of dynamic CesiumJS content to view 4D "movies" of vehicle routing problems.

Source code is available at https://github.com/optimatorlab/veroviz.  Documentation and examples are maintained on the project homepage (https://veroviz.org).

"""

setuptools.setup(
	name="veroviz",
	version=__version__,
	author="Chase Murray, Lan Peng",
	author_email="cmurray3@buffalo.edu, lanpeng@buffalo.edu",
	description="VeRoViz: Vehicle Routing Visualization",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://veroviz.org",
	license='MIT', 
	packages=['veroviz'], 
	download_url = "https://github.com/optimatorlab/veroviz",
	project_urls={
		"Bug Tracker": "https://github.com/optimatorlab/veroviz/issues",
		"Documentation": "https://veroviz.org",
		"Source Code": "https://github.com/optimatorlab/veroviz",
	},
	python_requires='>=2.7',
	install_requires=[
		'numpy', 
		'pandas', 
		'geopy', 
		'psycopg2-binary', 
		'urllib3', 
		'folium',
		'tripy',
		'scipy',
		'matplotlib'
	],
	classifiers=[
		"Development Status :: 2 - Pre-Alpha",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Topic :: Scientific/Engineering :: Visualization", 
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	]
)