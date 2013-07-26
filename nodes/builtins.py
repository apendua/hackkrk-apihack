
def add(*args):
	return sum(args)

def mult(*args):
	prod = 1
	for value in args:
		prod *= value
	return prod

def lt(a, b):
	return a < b
