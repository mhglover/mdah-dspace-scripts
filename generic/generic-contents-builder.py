import csv
import sys
import os
import shutil

targetPath = '/path/to/target/folders/'					   ## Path to write files, include the trailing slash

f = open('source.csv')

data = csv.DictReader(f)

		contents = open(targetPath + i['CSV_BIB_SYSID_HEADER'] + '/' + 'contents', 'w')	## open contents file
	
		contents.write('dublin_core.xml' + '\t' + 'bundle:ORIGINAL\n')
		
		contents.write(i['CSV_BIB_SYSID_HEADER'] + 'REST_OF_FILENAME.EXTENSTION' + '\t' + 'bundle:ORIGINAL\n')

		# Write as many content lines as necessary to enumerate all the item's files. Default bundle should be ORIGINAL.
	
		### Assign a file to a preservation bundle to keep the file inaccessible to certain users.
		# contents.write(i['itembib']      + '-01-postcard.tif' + '\t' + 'bundle:PRESERVATION\n')
		
		contents.close()
	
	

