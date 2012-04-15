#### vtypes.py
#
# Built in data types

Symbol = str
isa = isinstance

class Deferral():
	def __init__(self, expr, env):
		self.expr = expr
		self.env = env

