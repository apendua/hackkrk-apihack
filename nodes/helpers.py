from django.http import HttpResponse
import json

def success(response, status=200):
	return HttpResponse(
		content_type = 'application/json',
		content      = json.dumps(response),
		status       = status,
	)

def error(message="", status=400):
	return HttpResponse(
		content_type = 'application/json',
		content      = json.dumps({"error":message}),
		status       = status,
	)
