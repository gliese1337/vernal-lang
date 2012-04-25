#### vtypes.py
#
# Built in data types

#Symbol = str
isa = isinstance

class Symbol(str):
	pass

class VString(str):
	pass

class Tail():
	def __init__(self, expr, env):
		self.expr = expr
		self.env = env

