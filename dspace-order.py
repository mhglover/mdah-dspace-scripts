#!/usr/bin/env python
import argparse
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
from lxml import etree
import urllib2

# TODO: able to enter Koha id's, error handling, checksum checking?
# Set script in cgi folder for server (e.g. cgi-bin)

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
		<h2>Enter DSpace identifier URIs.</h2>

		<p>Click 'Add' to enter a new URI. 'Submit' when done.</p>

		<input type="button" value="Add" onclick="add(document.forms.value)"/>

		<p id="container"><input type = "text" name = "handle" /><br /> </p>
		
		<input type = "submit" value="Submit" />

	</form>
	
<p>
""" 

form = cgi.FieldStorage()
handles = form.getlist("handle")

dspace_address = '10.8.4.245:8080'
bitstreams = []

for handle in handles:
 url = 'http://' + dspace_address + '/rest/items/' + handle + '/bundles.xml'
  
 tree = 	etree.parse(urllib2.urlopen(url))
 
 # use XPath to locate bundle with name PRESERVATION and get each bitstream id in that bundle
 for node in tree.xpath('/bundles/bundle/name[.="PRESERVATION"]/../bitstreams/bitstream/id'):
  url = 'http://10.8.4.245:8080/rest/bitstreams/' + node.text + '/download.xml'
  print """<form action = %s> DSpace handle %s: <input type = "submit" value = %s></form>""" % (url, handle, node.text)

print """\

</center>
</body>
</html>

"""
