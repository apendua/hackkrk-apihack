import validate
import builtins
import json

from nodes.models import addNode, getNode
from nodes.evaluate import evalNode
from nodes.helpers import error, success

cache = {}

# NODES

def nodes(request, node_id=None):
	if request.method == 'POST' and node_id is None:
		node = json.loads(request.body) # parse POST data
		err = validate.validateNode(node)
		if err:
			return error(err, 422)
		node["id"] = addNode(node)
		return success(node, 201)
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
	#TODO: check if name is valid
	if request.method == 'GET':
		if not name in cache:
			cache[name] = addNode({
					'kind': 'function',
					'body': name,
				})
		return success({"id": cache[name]})
	return error()

def functions(request, node_id=None):
	if request.method == 'POST' and node_id is None:
		node = json.loads(request.body) # parse POST data
		node['kind'] = 'function'
		err = validate.validateNode(node)
		if err:
			return error(err, 422)
		return success({'id':addNode(node)}, 201)
	return error()

# EVALUATE

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
