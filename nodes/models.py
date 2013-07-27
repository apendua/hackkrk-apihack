from django.db import models

class Node(models.Model):
	json = models.TextField(max_length=16)

import json

def addNode(data):
	node = Node(json=json.dumps(data))
	node.save()
	return node.id

def getNode(node_id):
	try:
		node = Node.objects.get(id=node_id)
	except Node.DoesNotExist:
		return None
	return json.loads(node.json)

def updateNode(node_id, **kwargs):
	try:
		node = Node.objects.get(id=node_id)
	except Node.DoesNotExist:
		return None
	data = json.loads(node.json)
	data.update(kwargs)
	node.json = json.dumps(data)
	node.save()
	return data

def updateType(nodeId, nodeType=None):
	if nodeType:
		print "type of node", nodeId, "is", nodeType
		updateNode(nodeId, type=nodeType) # nodeId can be none
	return nodeType
