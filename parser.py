
import plex



class ParseError(Exception):
	""" A user defined exception class, to describe parse errors. """
	pass



class MyParser:
	
	""" A class encapsulating all parsing functionality
	for a particular grammar. """
	
	def create_scanner(self,fp):
		
		# create and store the scanner object
		self.scanner = plex.Scanner(self.LEXICON, fp)
		# get initial lookahead
       		self.la, self.text = self.next_token()
		
	def __init__(self):
		letter = plex.Range("Azaz")
		digit  = plex.Range("09")
		binary = plex.Range("01")
		id_token= letter + plex.Rep(letter|digit)
      		and_token = plex.Str('and')
        	or_token= plex.Str('or')
        	xor = plex.Str('xor')
        	equals = plex.Str('=')
        	open_parenthesis= plex.Str('(')
        	close_parenthesis= plex.Str(')')
        	print_token = plex.Str('print')
        	space = plex.Any(' \n\t')
		binary_num = Rep1(binary)
		

		# the scanner lexicon - constructor argument is a list of (pattern,action ) tuples
		self.LEXICON = plex.Lexicon([(space, plex.IGNORE),
                                    	     (and_token, 'and'),
                                             (or_token, 'or'),
                                             (xor, 'xor'),
                                             (equals, '='),
                                             (print_token, 'print'),
                                             (open_parenthesis, '('),
                                             (close_parenthesis, ')'),
                                             (binary_num, 'binary_num'),
                                             (id_token, 'id')])
				

	def next_token(self):
		""" Returns tuple (next_token,matched-text). """
		return self.scanner.read()		

	
	def position(self):
		""" Utility function that returns position in text in case of errors.
		Here it simply returns the scanner position. """
		
		return self.scanner.position()
	

	def match(self,token):
		""" Consumes (matches with current lookahead) an expected token.
		Raises ParseError if anything else is found. Acquires new lookahead. """ 
		
		if self.la==token:
			self.la,self.text = self.next_token()
		else:
			raise ParseError("found {} instead of {}".format(self.la,token))
	
	
	def parse(self,fp):
		""" Creates scanner for input file object fp and calls the parse logic code. """
		
		# create the plex scanner for fp
		self.create_scanner(fp)
		
		# call parsing logic
		self.session()
	
			
	def session(self):
		
       		 if self.la in ("id", "print"):
           		 self.statement()
            		 self.session()
        	elif self.la == None:
           		 return
       		else:
           	   raise ParseError("{} wasn't an 'id', 'print' or 'None' token!".format(self.LA))

			 	
	
	def facts(self):
		""" Facts -> Fact Facts | ε """
		
		if self.la=='!':
			self.fact()
			self.facts()
		elif self.la=='?':	# from FOLLOW set!
			return
		else:
			raise ParseError("in facts: ! or ? expected")
			
	def statement(self):
		
       		 if self.la == "id":
            		self.match("id")
            		self.match("=")
            		self.expr()
        	elif self.lA == "print":
           		 self.match("print")
            		 self.expr()
        	else:
            		raise ParseError("{} wasn't an 'id' or 'print' token!".format(self.la))
	
	def expr(self):
		
        	if self.la in ("(","id", "binary_num"):
          		 self.term()
           		 self.term_tail()
       		 else:
            		raise ParseError("{} wasn't an '(', 'id' or 'binaty_num' token!".format(self.la)
	
	
	def fact(self):
		""" Fact -> ! string """
		
		if self.la=='!':
			self.match('!')
			self.match('string')
		else:
			raise ParseError("in fact: ! expected")
			 	

	def question(self):
		""" Question -> ? string """
		
		if self.la=='?':
			self.match('?')
			self.match('string')
		else:
			raise ParseError("in question: ? expected")

		
# the main part of prog

# create the parser object
parser = MyParser()

# open file for parsing
with open("recursive-descent-parsing.txt","r") as fp:

	# parse file
	try:
		parser.parse(fp)
	except plex.errors.PlexError:
		_,lineno,charno = parser.position()	
		print("Scanner Error: at line {} char {}".format(lineno,charno+1))
	except ParseError as perr:
		_,lineno,charno = parser.position()	
		print("Parser Error: {} at line {} char {}".format(perr,lineno,charno+1))

