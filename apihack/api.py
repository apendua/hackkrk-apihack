from django.http import HttpResponse

import json

nodes_db = []
cache = {}

def addNode(node):
	node_id = len(nodes_db)
	nodes_db.append(node.copy())
	return node_id

def getNode(node_id):
	try:
		return nodes_db[node_id]
	except IndexError:
		return None

def success(response, status=200):
	return HttpResponse(
		content_type = 'application/json',
		content      = json.dumps(response),
		status       = status,
	)

def error(message="", status=400):
	return HttpResponse(
		content_type = 'application/json',
		content      = json.dumps({"error":message}),
		status       = status,
	)

def nodes(request, node_id=None):

	if request.method == 'POST' and node_id is None:
		#TODO: check if node is ok
		data = json.loads(request.body) # parse POST data
		data["id"] = addNode(data)
		return success(data, 201)

	elif request.method == 'GET' and node_id:

		try:
			node_id = int(node_id)
		except ValueError:
			return error()

		node = getNode(node_id)
		if node:
			return success(node, 200)
		else:
			return error()

	else:
		return error()

	return error()

def builtin(request, name):

	if request.method == 'GET':
		if not name in cache:
			cache[name] = addNode({
					'kind': 'function',
					'body': name,
				})
		return success({"id": cache[name]})

	return error()

def functions(request, name):
	pass

def evaluate(request, node_id):
	pass
