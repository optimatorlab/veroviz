.. _Units:

Units
=====

*VeRoViz* uses specific strings to denote units for the output 
values from different functions (e.g., for distance, time and area). 
All abbreviation below are case insensitive.

For input values, the units are defined in the names of fields (e.g.,
units of 'speedMPS' are [meters per second]).

Distance Units
--------------

+-----------------+-----------------------------------------+
| Units           | Valid *VeRoViz* Abbreviations           |
+=================+=========================================+
| Meters (default)| 'meters', 'm'                           |
+-----------------+-----------------------------------------+
| Kilometers      | 'kilometers', 'km'                      |
+-----------------+-----------------------------------------+
| Miles           | 'miles', 'mi'                           |
+-----------------+-----------------------------------------+
| Feet            | 'feet', 'ft'                            |
+-----------------+-----------------------------------------+
| Nautical Miles  | 'nm', 'nmi'                             |
+-----------------+-----------------------------------------+


Time Units
----------

+------------------+-----------------------------------------+
| Units            | Valid *VeRoViz* Abbreviations           |
+==================+=========================================+
| Seconds (default)| 'seconds', 'sec', 's'                   |
+------------------+-----------------------------------------+
| Minutes          | 'minutes', 'min'                        |
+------------------+-----------------------------------------+
| Hours            | 'hours', 'h'                            |
+------------------+-----------------------------------------+


Area Units
----------

+-----------------------+-----------------------------------+
| Units                 | Valid *VeRoViz* Abbreviations     |
+=======================+===================================+
| Square meters         | 'sqm', 'sqmeters', 'sm'           |
+-----------------------+-----------------------------------+
| Square feet           | 'sqft', 'sqfeet', 'sf'            |
+-----------------------+-----------------------------------+
| Square miles          | 'sqmi', 'sqmiles', 'smi'          |
+-----------------------+-----------------------------------+
| Square kilometers     | 'sqkm', 'sqkilometers', 'skm'     |
+-----------------------+-----------------------------------+

*VeRoViz* provides utility functions to help the user transform units.
See :meth:`~veroviz.utilities.convertDistance`, :meth:`~veroviz.utilities.convertTime`,
:meth:`~veroviz.utilities.convertSpeed` and :meth:`~veroviz.utilities.convertArea`