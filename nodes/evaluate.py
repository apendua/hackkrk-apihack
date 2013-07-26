from nodes.models import getNode
import builtins

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
	