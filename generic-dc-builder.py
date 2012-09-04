import csv
import sys
import os
import shutil

targetPath      = '/path/to/target/files/'						   ## Path to write files, include the trailing slash

f = open('source.csv')														## open the data source (usually a .csv)

data = csv.DictReader(f)													## put .csv contents into key-value hash table

for i in data:
	dc = open(targetPath + i['CSV_BIB_OR_SYSID_HEADER'] + '/' + 'dublin_core.xml', 'w')			## open dublin_core.xml file
	
	dc.write('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n')		
	dc.write('<dublin_core>\n')
	
	### Map DC elements with optional qualifiers to the .csv headers. Examples:	
	### dc.write('<dcvalue element=\"identifier\" qualifier=\"none\">' + i['itembib'] + '</dcvalue>\n')
	### dc.write('<dcvalue element=\"identifier\" qualifier=\"item\">' + i['itemno']  + '</dcvalue>\n')	
	
	### Reference: http://dublincore.org/documents/dcmi-terms/	
	
	### Write as many of these lines as you need to.
	dc.write('<dcvalue element=\"DC-ELEMENT\" qualifier=\"DC-QUALIFIER\">' + i['CSV_HEADER'] + '</dcvalue>\n')
			
	### Set the DCMIType value to one listed here: http://dublincore.org/documents/dcmi-terms/#H7
	### Example: dc.write('<dcvalue element=\"type\" qualifier=\"DCMIType\">Image</dcvalue>\n')
	
	dc.write('<dcvalue element=\"type\" qualifier=\"DCMIType\">DC-TYPE-VALUE</dcvalue>\n')	
	
	dc.write('</dublin_core>')

	dc.close()																			
	
	print(i['CSV_BIB_OR_SYSID_HEADER'] + ' dublin_core.xml written')