import validate
import builtins
import json
import db

from helpers import error, success

cache = {}

# NODES

def nodes(request, node_id=None):

	if request.method == 'POST' and node_id is None:
		try:
			validate.validate(node)
		except ValueError, e:
			return error(str(e))
		
		# parse POST data
		data = json.loads(request.body)
		data["id"] = db.add(data)

		return success(data, 201)

	elif request.method == 'GET' and node_id:

		try:
			node_id = int(node_id)
		except ValueError:
			return error()

		node = db.get(node_id)
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
			cache[name] = db.add({
					'kind': 'function',
					'body': name,
				})
		return success({"id": cache[name]})

	return error()

def functions(request, name):
	pass

# EVALUATE

def evalNode(node_id, args):
	node = db.get(node_id)
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
