
def BUILTIN_add(*args):
	sum = 0
	for arg in args:
		sum += arg.eval()
	return sum

def BUILTIN_mult(*args):
	prod = 1
	for arg in args:
		prod *= arg.eval()
	return prod

def BUILTIN_lt(arg1, arg2):
	return arg1.eval() < arg2.eval()

def BUILTIN_if(predicate, true_branch, false_branch):
	if predicate.eval():
		return true_branch.eval()
	return false_branch.eval()

library = {
	'add' : BUILTIN_add,
	'mult': BUILTIN_mult,
	'lt'  : BUILTIN_lt,
	'if'  : BUILTIN_if,
}
