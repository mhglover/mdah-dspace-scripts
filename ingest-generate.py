#!/usr/bin/python
import argparse
import csv
import cgi
import os
import re
import shutil
import subprocess
import sys
import urllib2

def pull_files(fileslist, output, bundle, permissions=''):
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
				output.write('%s\tbundle:%s\t%s\n' % (local, bundle, permissions))

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
					output.write('%s\tbundle:%s\t%s\n' % (local, bundle, permissions))
					
					#make JPEG derivative of TIFF, if user-specified
					if (local.endswith('.tif') or local.endswith('.tiff')) and args.thumb_list:
						for thumb in args.thumb_list:
							subprocess.call('convert ' + path + '/' + local  + ' -resize ' + thumb + 'x' + thumb + ' -set filename:fname "%t-' + thumb +'" +adjoin ' + path + '/"%[filename:fname].jpg"', shell=True)
							print 'thumbnail ' + thumb + ' for ' + local + ' written.'
							output.write(os.path.splitext(local)[0] + '-' + thumb + '.jpg\tbundle:ORIGINAL\n')

parser = argparse.ArgumentParser(description='generate a Simple Archive Format directory structure from a properly formatted CSV')

parser.add_argument('infile', default='sample.csv', type=argparse.FileType('r'), help='the CSV to process')
parser.add_argument('outdir', default='test', help='the root for the directory structure to create')
parser.add_argument('-f', '--force', action='store_true', help='delete and overwrite the output directory structure')
parser.add_argument('-c', '--carryon', action='store_true', help='ignore existing output files and continue generating new ones')
parser.add_argument('-t', '--thumb', action='append', dest='thumb_list', default = [], help='specify additional thumbs to make from tiffs, if present. 100px thumbs are made automatically. Value specifices longest side of image. Examples values: 1) -t 500 -t 1024 2) -t 2400 ... etc.')

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

data = csv.DictReader(args.infile)		# Put .csv data in key-value table

for i in data:	
	path = args.outdir + '/' + i['dc.identifier']

	if not os.path.exists(path):		# Check folder is not already there
		os.makedirs(path)		# Write folder from unique ID name	
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

			#cgi.escape will escape HTML characters
			value = cgi.escape(i[name]) 
			
			if identifier != "" and value != "":
				
				#multiple value entries if '%%' delimiter exists
				value_list = value.split('%%')
				for single_value in value_list:
					dc.write('<dcvalue element=\"%s\" qualifier=\"%s\">%s</dcvalue>\n' % (identifier, qualifier, single_value))
					
	# Set the DCMIType value to one listed here: http://dublincore.org/documents/dcmi-terms/#H7
	# Example: dc.write('<dcvalue element=\"type\" qualifier=\"DCMIType\">Image</dcvalue>\n')
	
	# dc.write('<dcvalue element=\"type\" qualifier=\"DCMIType\">DC-TYPE-VALUE</dcvalue>\n')	
	
	dc.write('</dublin_core>')
	dc.close()																			
	print(path + '/dublin_core.xml written')
	#----------------------dublin core done--------------------------------------


	#---------------------- start to write contents--------------------------------------
	contents = open(path + '/contents', 'w')
		
	#----------------------copy in files--------------------------------------
	# the files field should be a plain list of the files that should be included
	# we can use:
	#	urls				http://mdah.state.ms.us/arrec_digital_archives/moncrief/images/12321-photo.tif
	#	local paths			images/12321-photo.tif
	#	absolute paths			/workspace/moncrief/images/12321-photo.tif
	#	id-related wildcards		/workspace/moncrief/images/[dc.identifier]-photo.tif
	
	if 'mdah.files' in i and i['mdah.files'] != "":
		fileslist = i['mdah.files'].split('\n')
		pull_files(fileslist, contents, 'ORIGINAL')

	#---------------------restricted files-------------------------------
	# Assign files under 'mdah.restricted' with restricted read permissions
	
	if 'mdah.restricted' in i and i['mdah.restricted'] != '':
		fileslist = i['mdah.restricted'].split('\n')
		pull_files(fileslist, contents, 'RESTRICTED', "permissions: -r 'Restricted'")

	#---------------------staff files----------------------------------------
	# Assign files under 'mdah.staff' with restricted read permissions

	if 'mdah.staff' in i and i['mdah.staff'] != '':
		fileslist = i['mdah.staff'].split('\n')
		pull_files(fileslist, contents, 'STAFF', "permissions: -r 'Staff'")

	#----------------------finish contents--------------------------------------
	contents.close()
