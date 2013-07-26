from django.http import HttpResponse

import json
import builtins

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

def evalNode(node_id, args):
	node = getNode(node_id)
	if node is None:
		pass # what shoud we do?
	kind = node['kind']
	if kind == 'constant':
		return node['value']
	elif kind == 'invoke':
		args = [evalNode(i, None) for i in node['arguments']]
		return evalNode(node['function'], args)
	elif kind == 'argument':
		#TODO: check if arguments are ok
		return args['argument']
	elif kind == 'function':
		if hasattr(builtins, node['body']):
			return getattr(builtins, node['body']).__call__(*args)
		else:
			return evalNode(node['body'], args)
	elif kind == 'if':
		if evalNode(node['predicate']):
			return evalNode(node['true_branch'])
		return evalNode(node['false_branch'])
	return None

def evaluate(request, node_id):
	if request.method == 'GET':
		try:
			node_id = int(node_id)
		except ValueError:
			return error()

		result = evalNode(node_id, None) # eval with no arguments
		return success({
				'result' : result,
			})
	return error()
