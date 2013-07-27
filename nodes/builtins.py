
def BUILTIN_add(*args):
	return sum(args)

def BUILTIN_mult(*args):
	prod = 1
	for value in args:
		prod *= value
	return prod

def BUILTIN_lt(arg1, arg2):
	return arg1 < arg2

def BUILTIN_if(predicate, true_branch, false_branch):
	if predicate:
		return true_branch
	return false_branch

library = {
	'add' : BUILTIN_add,
	'mult': BUILTIN_mult,
	'lt'  : BUILTIN_lt,
	'if'  : BUILTIN_if,
}
