
nodes = []

def add(node):
	node_id = len(nodes)
	nodes.append(node.copy())
	return node_id

def get(node_id):
	try:
		return nodes[node_id]
	except IndexError:
		return None
