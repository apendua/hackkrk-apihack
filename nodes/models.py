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
