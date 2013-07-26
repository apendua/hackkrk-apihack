import urllib2
import urlparse
import json

from urllib2 import urlopen

prefix = "http://127.0.0.1:8000"

def make_request(url, data=None):
	if data:
		response = urlopen( urlparse.urljoin(prefix, url), json.dumps(data).encode('utf-8') )
	else:
		response = urlopen( urlparse.urljoin(prefix, url) )

	result = json.loads(response.read().decode('utf-8'))
	print response.code, result

	return result

result = make_request("/nodes", {"kind":"constant","type":"int","value":371})
result = make_request("/nodes", {"kind":"constant","type":"int","value":121})
result = make_request("/functions/builtin/add")

#result = make_request("/nodes/%i" % result["id"])
