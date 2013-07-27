from nodes.models import getNode
from nodes.builtins import library

class lazy(object):
	def __init__(self, nodeId, args=None):
		self.nodeId = nodeId
		self.args   = args

	def eval(self):
		if not hasattr(self, 'value'):
			self.value = evalNode(self.nodeId, self.args)
		return self.value

def evalNode(nodeId, args=None):
	node = getNode(nodeId)
	if node is None:
		pass # what shoud we do?
	kind = node['kind']
	if kind == 'constant':
		return node['value']
	elif kind == 'invoke':
		#Q: do we need to pass args here?
		return evalNode(node['function'], [lazy(i, args) for i in node['arguments']])
	elif kind == 'argument':
		return args[node['argument']].eval()
	elif kind == 'builtin':
		return library[node['name']].__call__(*args)
	elif kind == 'function':
		return evalNode(node['body'], args)
	elif kind == 'if':
		if evalNode(node['predicate'], args):
			return evalNode(node['true_branch'], args)
		return evalNode(node['false_branch'], args)
	return None
	
