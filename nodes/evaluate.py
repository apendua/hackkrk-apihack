from nodes.models import getNode
from nodes.builtins import library

def evalNode(node_id, args=None):
	node = getNode(node_id)
	if node is None:
		pass # what shoud we do?
	kind = node['kind']
	if kind == 'constant':
		return node['value']
	elif kind == 'invoke':
		return evalNode(node['function'], [evalNode(i, args) for i in node['arguments']])
	elif kind == 'argument':
		#TODO: check if arguments are ok
		return args[node['argument']]
	elif kind == 'builtin':
		return library[node['name']].__call__(*args)
	elif kind == 'function':
		return evalNode(node['body'], args)
	elif kind == 'if':
		if evalNode(node['predicate'], args):
			return evalNode(node['true_branch'], args)
		return evalNode(node['false_branch'], args)
	return None
	
