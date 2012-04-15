### built-in globals

from vtypes import *
from veval import eval, Env
from vparser import to_string

def vau(clos_env, vars, call_env_sym, body):
		vars.append(call_env_sym)
		def closure(call_env, *args):
			args.append(call_env)
			return eval(body, Env(zip(vars, args), clos_env))
		return closure

def lam(clos_env, vars, body):
		def closure(call_env, *args):
			args = [Deferral(exp, call_env) for exp in args]
			return eval(body, Env(zip(vars, args), clos_env))
		return closure

def define(v,var,e):
	val = eval(e, v)
	v[var] = val
	return val
	
def set(v,var,e):
	val = eval(e, v)
	env.find(var)[var] = val
	return val

def quote(v,exp): return exp

def cond(v,*x):
	for (p, e) in x:
		if eval(p, v):
			return eval(e, v)
	raise ValueError("No Branch Evaluates to True")

def begin(v,*x):
	val = 0
	for e in x:
		val = eval(e, v)
	return val
	
def vprint(v,e):
	val = eval(e, v)
	print to_string(val)
	return val
	
global_env = Env({
	'+':	lambda v,x,y:eval(x,v)+eval(y,v),
	'-':	lambda v,x,y:eval(x,v)-eval(y,v),
	'*':	lambda v,x,y:eval(x,v)*eval(y,v),
	'/':	lambda v,x,y:eval(x,v)/eval(y,v),
	'>':	lambda v,x,y:eval(x,v)>eval(y,v),
	'<':	lambda v,x,y:eval(x,v)<eval(y,v),
	'>=':	lambda v,x,y:eval(x,v)>=eval(y,v),
	'<=':	lambda v,x,y:eval(x,v)<=eval(y,v),
	'=':	lambda v,x,y:eval(x,v)==eval(y,v),
	'eq?':	lambda v,x,y:
				(lambda vx,vy: (not isa(vx, list)) and (vx == vy))(eval(x,v),eval(y,v)),
	'cons':	lambda v,x,y:[eval(x,v)]+eval(y,v),
	'car':	lambda v,x:eval(x,v)[0],
	'cdr':	lambda v,x:eval(x,v)[1:],
	'list':	lambda v,*x:[eval(expr, v) for exp in x],
	'append':	lambda v,x,y:eval(x,v)+eval(y,v),
	'len':	lambda v,x:len(eval(x,v)),
	'null?':	lambda v,x:eval(x,v)==[],
	'symbol?':	lambda v,x:isa(eval(x,v),Symbol),
	'list?':	lambda v,x:isa(eval(x,v),list),
	'atom?':	lambda v,x:not isa(eval(x,v), list),
	'exit':		lambda v:exit(),
	'True':		True,
	'False':	False,
	'if':		lambda v,z,t,f: eval((t if eval(z,v) else f), v),
	'cond':		cond,
	'define':	define,
	'set!':		set,
	'vau':		vau,
	'lambda':	lam,
	'q': quote,
	'quote': quote,
	'begin': begin,
	'print': vprint,
	'eval': lambda v,x,e: eval(x,e)
})
