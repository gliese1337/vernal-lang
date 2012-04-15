#### veval.py
#
# Built in global procedures and the Vernal Eval function

from vtypes import *

### lazy environments

class Env(dict):
	"An environment: a dict of {'var':val} pairs, with an outer Env."
	def __init__(self, bindings={}, outer=None):
		self.update(bindings)
		self.outer = outer

	def __getitem__(self, var):
		loc = self.find(var)
		val = super(Env,loc).__getitem__(var)
		if isa(val, Deferral):
			val = eval(val.expr, val.env)
			loc[var] = val
		return val

	def find(self, var):
		"Find the innermost Env where var appears."
		if var in self:
			return self
		elif not self.outer is None:
			return self.outer.find(var)
		else: raise ValueError("%s is not defined"%(var,))

#### eval

def eval(x, env):
	"Evaluate an expression in an environment."
	val = x
	if isa(x, Symbol):		  # variable reference
		val = env.find(x)[x]
	elif isa(x, list):		  # (proc exp*)
		proc = eval(x[0], env)
		if hasattr(proc, '__call__'): val = proc(env,*x[1:])
		else: raise ValueError("%s = %s is not a procedure" % (to_string(x[0]),to_string(proc)))
	return val

