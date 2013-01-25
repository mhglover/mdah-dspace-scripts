#!/usr/bin/python
import argparse
import csv
import os
import re
import shutil
import sys
import urllib2

def pull_files(fileslist, output, permissions):
	for f in fileslist:
			#interpret wildcard for dc.identifier
			s = '\[dc.identifier\]'
			r = i['dc.identifier']
			f = re.sub(s, r, f)
			
			#check to see if this is a local file
			if(os.path.exists(f)):
				shutil.copy(f, path)
				local = f.split('/')[-1]
				print '%s copied' % local
				output.write('%s\tpermissions:%s\n' % (local, permissions))

			#check to see if this is a url
			h = re.search('^http://', f)
			if h:
				#try to open remote file
				try:
					webFile = urllib2.urlopen(f)
				except IOError as e:
					print 'ERROR: ' + f + ' could not be opened.'
				else:
					#if opened then write file to local machine
					local = f.split('/')[-1]
					localFile = open(path + '/' + local, 'w')
					localFile.write(webFile.read())
					webFile.close()
					localFile.close()
					print '%s downloaded' % local
					output.write('%s\tpermissions:%s\n' % (local, permissions))


parser = argparse.ArgumentParser(description='generate a Simple Archive Format directory structure from a properly formatted CSV')

parser.add_argument('infile', default='sample.csv', type=argparse.FileType('r'), help='the CSV to process')
parser.add_argument('outdir', default='test', help='the root for the directory structure to create')
parser.add_argument('-f', '--force', action='store_true', help='delete and overwrite the output directory structure')
parser.add_argument('-c', '--carryon', action='store_true', help='ignore existing output files and continue generating new ones')


args = parser.parse_args()

if args.force:
	try:
		shutil.rmtree(args.outdir)
	except StandardError as e:
		print 'ERROR: ' + args.outdir + ' is not present. Will create directory.'
	else:
		print 'deleting %s folder and contents' % args.outdir


#generate the root target directory
if not os.path.exists(args.outdir):
	os.makedirs(args.outdir)
else:
	print args.outdir + ' already exists.'
	if not args.carryon:
		sys.exit()

data = csv.DictReader(args.infile)	## Put .csv data in key-value table

for i in data:	
	path = args.outdir + '/' + i['dc.identifier']

	#create target directories
	if not os.path.exists(path):		## Check folder is not already there
		os.makedirs(path)		## Write folder from unique ID name	
		print '%s folder written.' % path
	else:
		print '%s folder already exists.' % path
		#skip the rest of the generation for this item
		continue

	#----------------------marc-xml --------------------------------------
	if 'mdah.marcxml' in i and i['mdah.marcxml'] != "":
		marc = open(path + '/metadata_marc.xml', 'w')
		marc.write(i['mdah.marcxml'])	
		marc.close()
		print 'metadata_marc.xml for %s written.' % path
	#----------------------marc-xml done--------------------------------------

	#----------------------marc-dat --------------------------------------
	if 'mdah.marcdat' in i and i['mdah.marcdat'] != "":
		marc = open(path + '/marc.dat', 'w')
		marc.write(i['mdah.marcdat'])	
		marc.close()
		print 'marc.dat for %s written.' % path
	#----------------------marc-dat done--------------------------------------

	#----------------------write dublin core --------------------------------------
	dc = open(path + '/dublin_core.xml', 'w')
	dc.write('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n')		
	dc.write('<dublin_core>\n')
	
	### Map DC elements with optional qualifiers to the .csv headers.
	### Reference: http://dublincore.org/documents/dcmi-terms/	

	for name in i.keys():
		if i[name] == "":
			continue

		#pull out the DC element name
		m =  re.search('^dc\.(.*)$', name)
		if m:
			identifier = m.group(1)

			#pull out the qualifier name
			qualifier = 'none'
			q = re.search('^dc\.(.*)\.(.*)$', name)
			if q:
				identifier = q.group(1)
				qualifier = q.group(2)

		
			value = i[name]
			
			if identifier != "" and value != "":
				dc.write('<dcvalue element=\"%s\" qualifier=\"%s\">%s</dcvalue>\n' % (identifier, qualifier, i[name]))
					
	### Set the DCMIType value to one listed here: http://dublincore.org/documents/dcmi-terms/#H7
	### Example: dc.write('<dcvalue element=\"type\" qualifier=\"DCMIType\">Image</dcvalue>\n')
	
	# dc.write('<dcvalue element=\"type\" qualifier=\"DCMIType\">DC-TYPE-VALUE</dcvalue>\n')	
	
	dc.write('</dublin_core>')
	dc.close()																			
	print(path + '/dublin_core.xml written')
	#----------------------dublin core done --------------------------------------


	#----------------------start to write contents--------------------------------------
	contents = open(path + '/contents', 'w')
		
	#----------------------copy in files --------------------------------------
	# the files field should be a plain list of the files that should be included
	# we can use:
	#	urls				http://mdah.state.ms.us/arrec_digital_archives/moncrief/images/12321-photo.tif
	#	local paths			images/12321-photo.tif
	#	absolute paths			/workspace/moncrief/images/12321-photo.tif
	#	id-related wildcards		/workspace/moncrief/images/[dc.identifier]-photo.tif
	
	if 'mdah.files' in i and i['mdah.files'] != "":
		fileslist = i['mdah.files'].split('\n')
		pull_files(fileslist, contents, " -r 'Anonymous'")

	#---------------------preservation files -------------------------------
	# Assign files under 'mdah.preservation' with restricted read permissions
	
	if 'mdah.preservation' in i and i['mdah.preservation'] != "":
			fileslist = i['mdah.preservation'].split('\n')
			pull_files(fileslist, contents, " -r 'Staff'")
	
	#----------------------finish contents--------------------------------------
	contents.close()
