from src.constants.constants import DIGITS, LETTERS, LETTERS_DIGITS
from src.constants.keywords import *
from src.constants.tokentypes import *
from src.errors import ExpectedCharError, IllegalCharError
from src.tokens import *


class Position:
	def __init__(self, idx, ln, col, fn, ftxt):
		self.idx = idx
		self.ln = ln
		self.col = col
		self.fn = fn
		self.ftxt = ftxt
	
	def advance(self, current_char=None):
		self.idx += 1
		self.col += 1

		if current_char == '\n':
			self.ln += 1
			self.col = 0
		
		return self
	
	def copy(self):
		return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

class Lexer:
	def __init__(self, fn, text):
		self.fn = fn
		self.text = text
		self.pos = Position(-1, 0, -1, fn, text)
		self.current_char = None
		self.advance()

	def advance(self):
		self.pos.advance(self.current_char)
		self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

	def make_tokens(self):
		tokens = []

		while self.current_char != None:
			if self.current_char in ' \t':
				self.advance()
			elif self.current_char in ';\n':
				tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
				self.advance()
			elif self.current_char in DIGITS:
				tokens.append(self.make_number())
			elif self.current_char in LETTERS:
				tokens.append(self.make_identifier())
			elif self.current_char == '"':
				tokens.append(self.make_string('"'))
			elif self.current_char == "'":
				tokens.append(self.make_string("'"))
			elif self.current_char == '+':
				tokens.append(self.make_plus_increment())
			elif self.current_char == '-':
				tokens.append(self.make_minus_arrow_decrement())
			elif self.current_char == '*':
				tokens.append(self.make_mul())
			elif self.current_char == '/':
				token = self.make_div_comments()
				if token: tokens.append(token)
			elif self.current_char == '%':
				tokens.append(self.make_modul())
			elif self.current_char == '^':
				tokens.append(self.make_pow())
			elif self.current_char == '#':
				tokens.append(self.make_root())
			elif self.current_char == '(':
				tokens.append(Token(TT_LPAREN, pos_start=self.pos))
				self.advance()
			elif self.current_char == ')':
				tokens.append(Token(TT_RPAREN, pos_start=self.pos))
				self.advance()
			elif self.current_char == '[':
				tokens.append(Token(TT_LSQUARE, pos_start=self.pos))
				self.advance()
			elif self.current_char == ']':
				tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
				self.advance()
			elif self.current_char == '{':
				tokens.append(Token(TT_LCURLY, pos_start=self.pos))
				self.advance()
			elif self.current_char == '}':
				tokens.append(Token(TT_RCURLY, pos_start=self.pos))
				self.advance()
			elif self.current_char == '!':
				tokens.append(self.make_not_equals())
			elif self.current_char == '=':
				tokens.append(self.make_equals())
			elif self.current_char == '<':
				tokens.append(self.make_less_than())
			elif self.current_char == '>':
				tokens.append(self.make_greater_than())
			elif self.current_char == '&':
				token, error = self.make_and()
				if error: return [], error
				tokens.append(token)
			elif self.current_char == '|':
				token, error = self.make_or()
				if error: return [], error
				tokens.append(token)
			elif self.current_char == ',':
				tokens.append(Token(TT_COMMA, pos_start=self.pos))
				self.advance()
			elif self.current_char == '?':
				tokens.append(Token(TT_QUESTION, pos_start=self.pos))
				self.advance()
			elif self.current_char == ':':
				tokens.append(Token(TT_COLON, pos_start=self.pos))
				self.advance()
			else:
				pos_start = self.pos.copy()
				char = self.current_char
				self.advance()
				return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

		tokens.append(Token(TT_EOF, pos_start=self.pos))
		return tokens, None

	def make_number(self):
		num_str = ''
		dot_count = 0
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in DIGITS + '.':
			if self.current_char == '.':
				if dot_count == 1: break
				dot_count += 1
				num_str += '.'
			else:
				num_str += self.current_char
			self.advance()

		if dot_count == 0:
			return Token(TT_INT, int(num_str), pos_start, self.pos)
		else:
			return Token(TT_FLOAT, float(num_str), pos_start, self.pos)
	
	def make_string(self, quote_type):
		self.quote_type = quote_type
		string = ''
		pos_start = self.pos.copy()
		escape_character = False
		self.advance()

		escape_characters = {
			'n': '\n',
			't': '\t',
		}

		while self.current_char != None and (self.current_char != quote_type or escape_character):
			if escape_character:
				string += escape_characters.get(self.current_char, self.current_char)
				escape_character = False
			else:
				if self.current_char == '\\':
					escape_character = True
				else:
					string += self.current_char
			self.advance()
		self.advance()

		return Token(TT_STRING, string, pos_start, self.pos)

	def make_identifier(self):
		id_str = ''
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
			id_str += self.current_char
			self.advance()

		tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
		return Token(tok_type, id_str, pos_start, self.pos)
	
	def make_plus_increment(self):
		tok_type = TT_PLUS
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '+':
			self.advance()
			tok_type = TT_INCREMENT
		elif self.current_char == '=':
			self.advance()
			tok_type = TT_PLUSEQ

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_minus_arrow_decrement(self):
		tok_type = TT_MINUS
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '>':
			self.advance()
			tok_type = TT_ARROW
		elif self.current_char == '-':
			self.advance()
			tok_type = TT_DECREMENT
		elif self.current_char == '=':
			self.advance()
			tok_type = TT_MINUSEQ

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_mul(self):
		tok_type = TT_MUL
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_MULEQ

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_div_comments(self):
		tok_type = TT_DIV
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '/':
			while self.current_char and self.current_char != '\n':
				self.advance()
			self.advance()
			return
		elif self.current_char == '*':
			self.advance()
			while self.current_char:
				while self.current_char and self.current_char != '*':
					self.advance()
				self.advance()
				if self.current_char == '/':
					break
			self.advance()
			return
		elif self.current_char == '=':
			self.advance()
			tok_type = TT_DIVEQ

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_modul(self):
		tok_type = TT_MODUL
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_MODULEQ

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_pow(self):
		tok_type = TT_POW
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_POWEQ

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_root(self):
		tok_type = TT_ROOT
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_ROOTEQ

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_not_equals(self):
		tok_type = TT_NOT
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_NE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
	
	def make_equals(self):
		tok_type = TT_EQ
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			if self.current_char == '=':
				self.advance()
				tok_type = TT_EEE
			else: tok_type = TT_EE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_less_than(self):
		tok_type = TT_LT
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_LTE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_greater_than(self):
		tok_type = TT_GT
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_GTE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_and(self):
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '&':
			self.advance()
			return Token(TT_AND, pos_start=pos_start, pos_end=self.pos), None

		self.advance()
		return None, ExpectedCharError(pos_start, self.pos, "'&' (after '&')")

	def make_or(self):
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '|':
			self.advance()
			return Token(TT_OR, pos_start=pos_start, pos_end=self.pos), None

		self.advance()
		return None, ExpectedCharError(pos_start, self.pos, "'|' (after '|')")
