from vtypes import *
import re
import string

class Token():
	def __init__(self,tokentype="",value=""):
		self.tokentype = tokentype
		self.value = value
	
	def __eq__(self,other):
		if isa(other,str):
			return self.tokentype == other
		elif isa(other,Token):
			return self.tokentype == other.tokentype and self.value == other.value
		else: return False
	
	def __ne__(self,other):
		return not self.__eq__(other)
	
	def __repr__(self):
		return self.value if self.value != "" else self.tokentype

def getString(s,i):
	i += 1
	n = i
	try:
		while True:
			if s[n] == '\\':
				n += 2
			elif s[n] == '"':
				break
			else:
				n += 1
	except IndexError:
			raise SyntaxError("Nonterminated string")
	return (Token(tokentype="string",value=s[i:n]),n+1)

def getSymbol(s,i):
	sym_illegal = string.whitespace+"(){}';"
	n = i+1
	try:
		while not s[n] in sym_illegal:
			n += 1
	except IndexError:
		pass
	return (Token(tokentype="symbol",value=s[i:n]),n)

def tokenize(s):
	"Convert a string into a list of tokens."
	#re.findall("\".*?\"|[(){};']|[^(){};'\s]+", s)
	i = 0
	delimiters = "(){}';"
	tokens = []
	token = None
	while i < len(s):
		if s[i] in string.whitespace:
			i += 1
			continue
		elif s[i] in delimiters:
			token = Token(tokentype=s[i])
			i += 1
		elif s[i] == '"': # get a string
			token, i = getString(s,i)
		else:
			token, i = getSymbol(s,i)
		tokens.append(token)
	return tokens

def parse(tokens):
	"Read an expression from a sequence of tokens."
	if tokens == None:
		raise SyntaxError('unexpected EOF while reading')
	token = tokens.pop(0)
	if token == '(':
		L = []
		while tokens[0] != ')':
			L.append(parse(tokens))
		tokens.pop(0) # pop off ')'
		return L
	elif token == '{':
		L = [Symbol('begin')]
		while tokens[0] != '}':
			L.append(parse(tokens))
		tokens.pop(0) # pop off '}'
		return L
	elif token == "'":
		return [Symbol('q'),parse(tokens)]
	elif token == ";":
		parse(tokens)
		return parse(tokens) if len(tokens) > 0 else None
	elif token == ')':
		raise SyntaxError('unexpected )')
	elif token == '}':
		raise SyntaxError('unexpected }')
	else:
		return atom(token)

def atom(token):
	"Numbers become numbers; every other token is a symbol."
	val = token.value
	try: return int(val)
	except ValueError:
		try: return float(val)
		except ValueError:
			return VString(val) if token == 'string' else Symbol(val) 

def to_string(exp):
	"Convert a Python object back into a Lisp-readable string."
	return '('+' '.join(map(to_string, exp))+')' if isa(exp, list) else str(exp)
