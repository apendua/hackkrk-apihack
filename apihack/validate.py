
def validateNode(node):
	kind = node['kind']
	if kind == 'constant':
		valueType = node['type']
		if valueType == 'int':
			if type(node['value']) != int:
				return 'Could not parse integer'
		elif valueType == 'bool':
			if type(node['value']) != bool:
				return 'Could not parse boolean'
		elif valueType == 'string':
			if type(node['value']) != str:
				return 'Could not parse string'
	elif kind == 'function':
		pass
