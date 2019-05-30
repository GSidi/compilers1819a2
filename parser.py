
import plex



class ParseError(Exception):
	""" A user defined exception class, to describe parse errors. """
	pass



class myParser:
	
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
		self.stmt_list()
	
	def stmt_list(self):
		
       		 if self.la in ("id", "print"):
           		 self.stmt()
            		 self.stmt_list()
        	elif self.la == None:
           		 return
       		else:
           	   raise ParseError("{} wasn't an 'id', 'print' or 'None' token!".format(self.la))

	def stmt(self):
		
       		 if self.la == "id":
            		self.match("id")
            		self.match("=")
            		self.expr()
        	elif self.la == "print":
           		 self.match("print")
            		 self.expr()
        	else:
            		raise ParseError("{} wasn't an 'id' or 'print' token!".format(self.la))
	
	def expr(self):
		
        	if self.la in ("(","id", "binary_num"):
          		 self.term()
           		 self.term_tail()
       		 else:
            		raise ParseError("{} wasn't an '(', 'id' or 'binary_num' token!".format(self.la)
	
	
	def term_tail(self):
       
		if self.la == "xor": 
           		 self.match("xor")
            		 self.term()
            		 self.term_tail()
       		 elif self.la in ("id", "print", ")", None):
           		 return
        	 else:
           		 raise ParseError("{} wasn't an 'xor', 'id', 'print' or ')' token!".format(self.la))

   	 def term(self):
        	if self.la in ("(","id", "binary_num"):
           		 self.factor()
            		 self.factor_tail()
       		 else:
			raise ParseError("{} wasn't an '(', 'id' or 'binary_num' token!".format(self.la))

	 def factor_tail(self):
      		  if self.la == "or":
          		  self.match("or")
            		  self.factor()
           		  self.factor_tail()
      		  elif self.la in ("xor", "id", "print", ")", None):
            			return
       		  else:
         		   raise ParseError("{} wasn't an 'xor', 'id', 'print' or ')' token!".format(self.la))

    	def factor(self):
        	if self.la in ("(", "id", "binary_num"):
           		 self.atom()
           		 self.atom_tail()
      	        else:
           		raise ParseError("{} wasn't an '(', 'id' or 'binary_num' token!".format(self.la))
	
					 
       def atom_tail(self):
        	if self.la == "and":
           		 self.match("and")
            		 self.atom()
            		 self.atom_tail()
        	elif self.LA in ("xor", "or", "print", "id", ")", None):
           		 return
       		 else:
            		raise ParseError("{} was not what i expected!".format(self.la))

        def atom(self):
       		 if self.la == "(":
           		 self.match("(")
            		 self.expr()
            		 self.match(")")
        	 elif self.la == ("id"):
          		 self.match("id")
       		 elif self.la == ("binary_num"):
            		 self.match("binary_num")
        	 else:
            raise ParseError("{} wasn't an '(', 'id' or 'binary_num' token!".format(self.la))
		
# the main part of prog

# create the parser object
parser = myParser()

# open file for parsing
with open("test.txt") as fp:
    parser.parse(fp)

