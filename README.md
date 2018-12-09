# BarBeerDrinker
### Class Project

This repository contains the code which generates random data as well as the SQL queries, triggers, and constraints used.
Over 20,000 tuples of semi-realistic data is generated, making sure to fit certain constraints. Most of the seed data is
scraped from the internet.

* datagen
	* datagen/data - contains all the source data for generation
	* datagen/table - contains the randomly generated csv tables
	* datagen/csv.py - parses and loads csv files
	* datagen/source.py - parses and loads non-csv files
	* datagen/op.py - Main entry point, controls the generation of data
* triggers - contains the SQL triggers which enforce constraints