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

typeCache = {}

def clearCache():
	typeCache = {}

def store(nodeId, nodeType):
	typeCache[nodeId] = nodeType
	return nodeType

def evalType(node, args=None):
	# prepare node data
	if isinstance(node, (int, long)):
		nodeId = node
		try:
			return typeCache[nodeId]
		except KeyError:
			pass # not yet in cache
		node = getNode(node)
	elif isinstance(node, dict):
		nodeId = node.get('id', None)
	else:
		raise ValueError
	# we need this to prevent infinite loop
	store(nodeId, None)
	#print "computing type of node:", node
	# try easy solution ;)
	if 'type' in node: # check if type is given explicitly
		return store(nodeId, node['type']) # also kind == constant goes here
	# so we need to compute it :/
	kind = node['kind']
	if kind == 'invoke':
		return store(nodeId, evalType(node['function'],
			[lazy(i, args) for i in node['arguments']]))
	elif kind == 'builtin':
		funcName = node['name']
		# move this logic to builtin module
		if funcName == 'add' or funcName == 'mult':
			return store(nodeId, 'int')
		elif funcName == 'lt':
			return store(nodeId, 'bool')
		#TODO: if
	elif kind == 'function':
		if node['body']: # this can be null
			return evalType(node['body'], args)
		return store(nodeId, None) # abstract function
	elif kind == 'argument':
		if args: #TODO: check if index is fine
			return args[node['argument']].evalType()
		return None
	elif kind == 'if':
		predicate = evalType(node['predicate'])
		if predicate == 'bool':
			typeTrue  = evalType(node['true_branch'], args)
			typeFalse = evalType(node['false_branch'], args)
			# it's ok if one of them is undefined, hmm?
			if typeTrue and typeFalse and typeTrue != typeFalse:
				raise TypeError("Type mismatch")
		else:
			raise TypeError("Type mismatch")
		return store(nodeId, typeTrue)

	return None
