#!/usr/bin/env python
import argparse
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
from lxml import etree
import urllib2

# INSTRUCTIONS: Set script in cgi folder for server (e.g. cgi-bin), enter Koha id to generate download buttons for all files in PRESERVATION bundle
# TODO: error handling, checksum checking?

print "Content-Type: text/html"
print
print """\

<html>
<head>
<title>Make happy with glorious DSpace order!</title>
<script language="javascript">
function add(type) {

    var input = document.createElement("input");
    input.type = "text";
    input.name = "handle";
    // input.className = "css-class-name"; // set the CSS class
    container.appendChild(input); // put it into the DOM
   
    var br = document.createElement("br");
    container.appendChild(br); 

}
</script>
</head>

<body>
	<center>
	<form name = "dspace-handles" action="dspace-order.py">
		<h2>Enter Koha catalog IDs.</h2>

		<p>Click 'Add' to enter a new Koha ID. 'Submit' when done.</p>

		<input type="button" value="Add" onclick="add(document.forms.value)"/>

		<p id="container"><input type = "text" name = "handle" /><br /> </p>
		
		<input type = "submit" value="Submit" />

	</form>
	
<p>
""" 

form = cgi.FieldStorage()
handles = form.getlist('handle')

dspace_address = 'YOUR_DSPACE_ADDRESS'
bitstreams = []

for value in handles:
 url = 'http://' + dspace_address + '/rest/search.xml?query=' + value  
  
 tree = 	etree.parse(urllib2.urlopen(url))
 
 for node in tree.xpath('/search/searchresultsinfo/resultIDs/integer'): 
  url = 'http://' + dspace_address + '/rest/items/' + node.text + '/bundles.xml'
  items_tree = etree.parse(urllib2.urlopen(url))
  for i in items_tree.xpath('bundle/name[.="RESTRICTED"]/preceding-sibling::bitstreams/bitstream/id'):
   download_url = 'http://' + dspace_address + '/rest/bitstreams/' + i.text + '/download.xml'
   print """<form action = %s> DSpace item: <input type = "submit" value = %s></form>""" % (download_url, i.text)

print """\

</center>
</body>
</html>

"""
