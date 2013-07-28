import urllib2
import urlparse
import json

from urllib2 import urlopen, HTTPError

#prefix = "http://127.0.0.1:8000"
prefix = "http://hackkrk-apihack.lenarcik.org:80"

def request(url, data=None):
	try:
		if data:
			response = urlopen( urlparse.urljoin(prefix, url), json.dumps(data).encode('utf-8') )
		else:
			response = urlopen( urlparse.urljoin(prefix, url) )
	except HTTPError, err:
		print err
		return

	result = json.loads(response.read().decode('utf-8'))
	
	print url, data or ""
	print response.code, result

	try:
		return result['id']
	except KeyError:
		return None

# invoking builtin function

id0 = request("/nodes", {"kind":"constant","type":"int","value":371})
id1 = request("/nodes", {"kind":"constant","type":"int","value":121})
id2 = request("/functions/builtin/add")
id3 = request("/nodes", {"kind":"invoke","function":id2,"arguments":[id0,id1]})
request("/nodes/%i/evaluate" % id3)

# function returning constant

id0 = request("/nodes", {"kind":"constant","type":"int","value":406})
id1 = request("/functions", {"body":id0})
id2 = request("/nodes", {"kind":"invoke","function":id1,"arguments":[]})
id3 = request("/nodes/%i/evaluate" % id2)

# simple conditional with type

id0 = request("/nodes", {"kind":"constant","type":"bool","value":True})
id1 = request("/nodes", {"kind":"constant","type":"string","value":"ZCBCWOVT"})
id2 = request("/nodes", {"kind":"constant","type":"int","value":682})
id3 = request("/nodes", {"kind":"if","predicate":id0,"true_branch":id1,"false_branch":id2})
id3 = request("/nodes", {"kind":"if","predicate":id1,"true_branch":id1,"false_branch":id2})

# function returning sum of arguments

id0 = request("/nodes", {"kind":"argument","argument":0})
id1 = request("/nodes", {"kind":"argument","argument":1})
id2 = request("/functions/builtin/add")
id3 = request("/nodes", {"kind":"invoke","function":id2,"arguments":[1,2]})
id4 = request("/functions", {"body":id3})
id5 = request("/nodes", {"kind":"constant","type":"int","value":129})
id6 = request("/nodes", {"kind":"constant","type":"int","value":546})
id7 = request("/nodes", {"kind":"invoke","function":id4,"arguments":[id5,id6]})
request("/nodes/%i/evaluate" % id7)
