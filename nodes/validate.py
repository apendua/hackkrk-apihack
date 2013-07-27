
def validateNode(node):
	kind = node['kind']
	if kind == 'constant':
		valueType = node['type']
		if valueType == 'int':
			if not isinstance(node['value'], ( int, long )):
				return 'Could not parse integer'
		elif valueType == 'bool':
			if not isinstance(node['value'], bool):
				return 'Could not parse boolean'
		elif valueType == 'string':
			if not isinstance(node['value'], basestring):
				return 'Could not parse string'
	elif kind == 'function':
		pass
