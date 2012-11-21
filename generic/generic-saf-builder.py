import csv
import sys
import os
import shutil

targetPath = '/path/to/target/path/'													 	 	## Path to write files, include trailing slash (e.g. /mnt/freenas-repo/cooper-ingest/)

f = open('source.csv')																				## Open the source .csv

data = csv.DictReader(f)																			## Put .csv data in key-value table

for i in data:																							
	if not os.path.exists(targetPath + i['CSV_COLUMN_WITH_BIB_OR_SYSID']):			## Check folder is not already there.
		os.makedirs(targetPath + i['CSV_COLUMN_WITH_BIB_OR_SYSID'])						## Write folder from unique ID name	)	
		print i['CSV_COLUMN_WITH_BIB_OR_SYSID'] + 'folder written.'  							
	else:
		print targetPath + i['CSV_COLUMN_WITH_BIB_OR_SYSID'] + ' already exists.'
