import urllib2
import urlparse
import json

from urllib2 import urlopen

prefix = "http://127.0.0.1:8000"
#prefix = "http://hackkrk-apihack.lenarcik.org:80"

def make_request(url, data=None):
	if data:
		response = urlopen( urlparse.urljoin(prefix, url), json.dumps(data).encode('utf-8') )
	else:
		response = urlopen( urlparse.urljoin(prefix, url) )

	result = json.loads(response.read().decode('utf-8'))
	
	print url
	print response.code, result

	try:
		return result['id']
	except KeyError:
		return None

id0 = make_request("/nodes", {"kind":"constant","type":"int","value":371})
id1 = make_request("/nodes", {"kind":"constant","type":"int","value":121})
id2 = make_request("/functions/builtin/add")
id3 = make_request("/nodes", {"kind":"invoke","function":id2,"arguments":[id0,id1]})
make_request("/nodes/%i/evaluate" % id3)

id0 = make_request("/nodes", {"kind":"constant","type":"int","value":406})
id1 = make_request("/functions", {"body":id0})
id2 = make_request("/nodes", {"kind":"invoke","function":id1,"arguments":[]})
id3 = make_request("/nodes/%i/evaluate" % id2)
