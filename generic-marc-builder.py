import csv
import sys
import os
import shutil

targetPath = '/path/to/simple/archive/format/directory/'			   ## Path to write the marc.xml files, include the trailing slash

f = open('source.csv')

data = csv.DictReader(f)

for i in data:
	marc = open(targetPath + i['COLUMN_NAME_WITH_BIB_OR_SYSID_VALUE'] + '/' + 'metadata_marc.xml', 'w')		## open marc.xml file to write
	marc.write(i['COLUMN_NAME_WITH_MARC_XML_VALUE'])	
	marc.close()
	
	print('marc.xml for ' + i['COLUMN_NAME_WITH_BIB_OR_SYSID_VALUE'] + ' written.')
