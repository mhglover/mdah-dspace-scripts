import csv
import sys
import os
import shutil

sourcePath = '/path/to/source/files/'							## Path to source files, include the trailing slash
targetPath = '/path/to/target/folders/'					   ## Path to write files, include the trailing slash

f = open('source.csv')

data = csv.DictReader(f)

for i in data:
	if(os.path.exists(sourcePath + i['CSV_BIB_SYSID_HEADER'] + 'REST_OF_FILENAME.EXTENSTION')):
		
		shutil.copy(sourcePath + i['CSV_BIB_SYSID_HEADER'] + 'REST_OF_FILENAME.EXTENSTION', targetPath + i['CSV_BIB_SYSID_HEADER'] + '/' + i['itembib'] + 'REST_OF_FILENAME.EXTENSTION')

		print i['CSV_BIB_SYSID_HEADER'] + 'REST_OF_FILENAME.EXTENSTION' + ' copied.'
