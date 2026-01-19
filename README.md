The idea is to recommend games based on the pc specs entered by the user 

This directory contains:	

Data scrapers to get recommended specs for games using steam api

Reference data sheet scrapers for data from Passmark (cpu/gpu hardware data)

Yet to build:

Recommendation algorithm

Interface

Script to match specs from game database and reference sheet(Mostly complete)


Note:
game data scrappers store to a .db file(not given here, it takes around 3 days to fully scrape all data)

code from the following repos used:
for appids - https://github.com/jsnli/steamappidlist
for passmark scraper - https://github.com/x3r0s/PassMark-Scraper/tree/main
