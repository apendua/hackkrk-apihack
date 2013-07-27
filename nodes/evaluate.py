from nodes.models import getNode, updateType
from nodes.builtins import library

class lazy(object):
	def __init__(self, nodeId, args=None):
		self.nodeId = nodeId
		self.args   = args

	def eval(self):
		if not hasattr(self, 'value'):
			self.value = evalNode(self.nodeId, self.args)
		return self.value

	def evalType(self):
		if not hasattr(self, 'nodeType'):
			self.nodeType = evalType(self.nodeId, self.args)
		return self.nodeType

def evalNode(nodeId, args=None):
	node = getNode(nodeId)
	if node is None:
		pass # what shoud we do?
	kind = node['kind']
	if kind == 'constant':
		return node['value']
	elif kind == 'invoke':
		#Q: do we need to pass args here?
		return evalNode(node['function'],
			[lazy(i, args) for i in node['arguments']])
	elif kind == 'builtin':
		return library[node['name']].__call__(*args)
	elif kind == 'function':
		return evalNode(node['body'], args)
	elif kind == 'argument':
		return args[node['argument']].eval()
	elif kind == 'if':
		if evalNode(node['predicate'], args):
			return evalNode(node['true_branch'], args)
		return evalNode(node['false_branch'], args)
	return None

def evalType(node, args=None):
	# prepare node data
	if isinstance(node, (int, long)):
		nodeId = node
		node   = getNode(node)
	elif isinstance(node, dict):
		nodeId = node.get('id', None)
	else:
		raise ValueError
	print "computing type of node:", node
	# try easy solution ;)
	if 'type' in node:
		# also kind == constant goes here
		return node['type']
	# so we need to compute it :/
	kind = node['kind']
	if kind == 'invoke':
		nodeType = evalType(node['function'],
			[lazy(i, args) for i in node['arguments']])
		print "type of invoke result is", nodeType
		return updateType(nodeId, nodeType)
	elif kind == 'builtin':
		funcName = node['name']
		# move this logic to builtin module
		if funcName == 'add' or funcName == 'mult':
			return 'int'
		elif funcName == 'lt':
			return 'bool'
		#TODO: if
	elif kind == 'function':
		return evalType(node['body'], args)
	elif kind == 'argument':
		return args[node['argument']].evalType()
	elif kind == 'if':
		typeTrue  = evalType(node['true_branch'], args)
		typeFalse = evalType(node['false_branch'], args)
		if typeTrue != typeFalse:
			raise TypeError
		return updateType(nodeId, typeTrue)

	return None
