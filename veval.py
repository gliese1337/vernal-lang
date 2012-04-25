#### veval.py
#
# Built in global procedures and the Vernal Eval function

from vtypes import *
from vparser import to_string

### lazy environments

class Env(dict):
	"An environment: a dict of {'var':val} pairs, with an outer Env."
	def __init__(self, bindings={}, outer=None):
		self.update(bindings)
		self.outer = outer

	def __getitem__(self, var):
		return super(Env,self.find(var)).__getitem__(var)
	
	def find(self, var):
		"Find the innermost Env where var appears."
		if var in self:
			return self
		elif not self.outer is None:
			return self.outer.find(var)
		else: raise ValueError("%s is not defined"%var)

#### eval

def eval(x, env):
	"Evaluate an expression in an environment."
	while True:
		if isa(x, Symbol):		  # variable reference
			return env[x]
		elif isa(x, list):		  # (proc exp*)
			proc = eval(x[0], env)
			if hasattr(proc, '__call__'):
				val = proc(env,*x[1:])
				if isa(val, Tail):
					x = val.expr
					env = val.env
				else:
					return val
			elif isa(proc, bool): #sugar for boolean branches
				x = x[1] if proc else x[2]
			else:
				raise ValueError("%s = %s is not a procedure" % (to_string(x[0]),to_string(proc)))
		else:
			return x

