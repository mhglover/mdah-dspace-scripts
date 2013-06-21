#!/usr/bin/python
import argparse
import csv
import cgi
import os
import re
import shutil
import subprocess
import sys

def make_preservation (path, local):
	contents = open(os.path.join(path, 'contents'), 'a')	
	
	#preservation derivatives follow Archivematica's chart: https://www.archivematica.org/wiki/Format_policies
	file_name, file_extension = os.path.splitext(local)
	
	#word processing files, convert to ODT
	if (file_extension.lower() == '.wpd' or file_extension.lower() == '.wbk' or file_extension.lower() == '.rtf'):
		subprocess.call('unoconv -f odt "' + path + '/' + local + '"', shell=True)
	 	contents.write(os.path.splitext(local)[0] + '.odt\tbundle:PRESERVATION\n')
		print 'Made preservation derivative for ' + os.path.join(root, folder, local)
	
	#pdf documents
	if (file_extension.lower() == '.pdf'):
		#convert to PDF/A
		subprocess.call('unoconv -o "' + path + '/' + os.path.splitext(local)[0] + '.archive.pdf' + '" -f pdf -eSelectPdfVersion=1 "' + path + '/' + local + '"', shell=True)
		contents.write(os.path.splitext(local)[0] + '.pdfa\tbundle:PRESERVATION\n')
		print 'Made preservation derivative for ' + os.path.join(root, folder, local)	
	
	#saved emails, convert to mime/mbox
	if (file_extension.lower() == '.msg'):
		subprocess.call('(cd ' + path + '&& perl -w /usr/bin/msgconvert.pl "' + local + '")', shell=True)
                contents.write(os.path.splitext(local)[0] + '.msg.mime\tbundle:PRESERVATION\n')
		print 'Made preservation derivative for ' + os.path.join(root, folder, local)	
	contents.close()	
	
def make_access (path, local):
	contents = open(os.path.join(path, 'contents'), 'a')		
	
	#access derivatives follow Archivematica's chart: https://www.archivematica.org/wiki/Format_policies
	file_name, file_extension = os.path.splitext(local)
	
	#word processing files, convert to PDF
	if (file_extension.lower() == '.wpd' or file_extension.lower() == '.wbk' or file_extension.lower() == '.rtf'):
		subprocess.call('unoconv -f pdf "' + path + '/' + local + '"', shell=True)
	 	contents.write(os.path.splitext(local)[0] + '.pdf\tbundle:ACCESS\n')
	 	print 'Made access derivative for ' + os.path.join(root, folder, local)
	
	#saved emails, convert to mime/mbox
	if (file_extension.lower() == '.msg'):
		subprocess.call('(cd ' + path + '&& perl -w /usr/bin/msgconvert.pl "' + local + '")', shell=True)
		contents.write(os.path.splitext(local)[0] + '.msg.mime\tbundle:ACCESS\n')
		print 'Made access derivative for ' + os.path.join(root, folder, local)
	contents.close()	

def make_jpeg (path, local):
	contents = open(os.path.join(path, 'contents'), 'a')	
	
	if (local.lower().endswith('.tif') or local.lower().endswith('.tiff')):
		convert_cmd = subprocess.call('convert "' + path + '/' + local  + '" -resize 1024x1024 -set filename:fname "%t-1024" +adjoin ' + path + '/"%[filename:fname].jpg"', shell=True)
		if (convert_cmd != 0):
			print 'ERROR: ' + local + ' was not converted.'
		else:
			print 'thumbnail 1024 for ' + local + ' written.'
			contents.write(os.path.splitext(local)[0] + '-1024.jpg\tbundle:ORIGINAL\n')
	contents.close()	

parser = argparse.ArgumentParser(description='generate preservation and access derivatives for file in the Simple Archive Format')

parser.add_argument('rootdir', help='the target directory containing the original files from which to create derivatives')
parser.add_argument('-p', '--preservation', action='store_true', help='generate preservation copies')
parser.add_argument('-a', '--access', action='store_true', help='generate access copies')
parser.add_argument('-j', '--jpeg', action='store_true', help='generate 1024x1024 JPEGs for TIFFs')

args = parser.parse_args()

rootdir = sys.argv[1]

for root, subfolders, files in os.walk(rootdir):
	for folder in subfolders:
		filenames = []
		path = os.path.join(root, folder)		

		#open 'contents' file and set each file in a list		
		with open(os.path.join(root, folder, 'contents')) as f:
			for line in f.readlines():
				filenames.append(line[0:line.find('\t')])
			f.close()		
		
		#run derivatives functions for each filename in filenames
		for local in filenames:
			if args.preservation:
				make_preservation(path, local)
			if args.access:
				make_access(path, local)
			if args.jpeg:
				make_jpeg(path, local)