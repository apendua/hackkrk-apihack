import validate
import builtins
import json

from nodes.models import addNode, getNode, updateNode
from nodes.evaluate import evalNode, evalType, clearCache
from nodes.helpers import error, success

cache = {}

# NODES

def nodes(request, node_id=None):
	if request.method == 'POST' and node_id is None:
		node = json.loads(request.body) # parse POST data
		err = validate.validateNode(node)
		if err:
			return error(err, 422)
		try:
			clearCache()
			nodeType = evalType(node)
		except TypeError, err:
			return error("Type mismatch", 422)
		node["id"] = addNode(node)
		if nodeType: # for now, we don't store node type in db
			node["type"] = nodeType
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
					'kind' : 'builtin',
					'name' : name,
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
		node['id'] = addNode(node)
		del node['kind']
		return success(node, 201)
	elif request.method == 'PUT' and node_id:
		#TODO: also update node type
		data = json.loads(request.body) # parse POST data
		node = updateNode(node_id, **data)
		if node:
			return success(data, 201)
		else:
			error("")
	return error("")

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
