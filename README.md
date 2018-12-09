# BarBeerDrinker
### Class Project

This repository contains the code which generates renadom data as well as the SQL queries, triggers, and constraints used.

* datagen
	* datagen/data - contains all the source data for generation
	* datagen/table - contains the randomly generated csv tables
	* datagen/csv.py - parses and loads csv files
	* datagen/source.py - parses and loads non-csv files
	* datagen/op.py - Main entry point, controls the generation of data
* triggers - contains the SQL triggers which enforce constraints